from __future__ import annotations

import json
import platform
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from .vectorizers import Vectorizer, cosine_similarity, default_vectorizers

DEFAULT_CORPUS = Path("data/fixtures/corpus.jsonl")
DEFAULT_QUERIES = Path("data/fixtures/queries.jsonl")
DEFAULT_COMMAND = (
    "python -m embeddings_benchmark benchmark --profile dense --k 3 --repeat 5 "
    "--warmup 1 --output benchmarks/results/embeddings-baseline.json"
)


def load_jsonl(path: Path) -> list[dict]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not rows:
        raise ValueError(f"fixture is empty: {path}")
    return rows


def recall_at_k(relevant: list[str], returned: list[str], k: int) -> float:
    expected = set(relevant)
    if not expected:
        raise ValueError("each query must declare at least one relevant document")
    return len(expected.intersection(returned[:k])) / len(expected)


def _validate_fixtures(corpus: list[dict], queries: list[dict], k: int) -> None:
    if k <= 0:
        raise ValueError("k must be positive")
    document_ids = [row.get("id") for row in corpus]
    if any(not isinstance(doc_id, str) or not doc_id for doc_id in document_ids):
        raise ValueError("every corpus row must have a non-empty string id")
    if len(document_ids) != len(set(document_ids)):
        raise ValueError("corpus contains duplicate ids")
    if any(not isinstance(row.get("text"), str) or not row["text"] for row in corpus):
        raise ValueError("every corpus row must have non-empty text")

    known_ids = set(document_ids)
    query_ids: set[str] = set()
    for row in queries:
        query_id = row.get("id")
        if not isinstance(query_id, str) or not query_id:
            raise ValueError("every query must have a non-empty string id")
        if query_id in query_ids:
            raise ValueError(f"duplicate query id: {query_id}")
        query_ids.add(query_id)
        if not isinstance(row.get("query"), str) or not row["query"]:
            raise ValueError(f"query {query_id} has no text")
        relevant = row.get("relevant")
        if not isinstance(relevant, list) or not relevant:
            raise ValueError(f"query {query_id} has no relevant ids")
        unknown = set(relevant) - known_ids
        if unknown:
            raise ValueError(f"query {query_id} references unknown ids: {sorted(unknown)}")


def evaluate(
    k: int = 3,
    corpus_path: Path = DEFAULT_CORPUS,
    queries_path: Path = DEFAULT_QUERIES,
    vectorizers: list[Vectorizer] | None = None,
    command: str = DEFAULT_COMMAND,
    timing_repeat: int = 5,
    warmup_iterations: int = 1,
    profile: str = "sparse",
) -> dict:
    corpus = load_jsonl(corpus_path)
    queries = load_jsonl(queries_path)
    _validate_fixtures(corpus, queries, k)
    if timing_repeat <= 0:
        raise ValueError("timing_repeat must be positive")
    if warmup_iterations < 0:
        raise ValueError("warmup_iterations cannot be negative")

    encoders = default_vectorizers() if vectorizers is None else vectorizers
    if not encoders:
        raise ValueError("at least one vectorizer is required")
    model_results = []
    query_texts = [row["query"] for row in queries]

    for encoder in encoders:
        indexing_started = time.perf_counter()
        vectors = encoder.fit_transform([row["text"] for row in corpus])
        if len(vectors) != len(corpus):
            raise ValueError(f"{encoder.info.name} returned the wrong corpus count")
        indexed = list(zip((row["id"] for row in corpus), vectors))
        indexing_ms = (time.perf_counter() - indexing_started) * 1000

        for _ in range(warmup_iterations):
            encoder.transform_many(query_texts)

        recall_samples: list[float] | None = None
        query_time_samples_ms = []
        for _ in range(timing_repeat):
            query_started = time.perf_counter()
            query_vectors = encoder.transform_many(query_texts)
            if len(query_vectors) != len(queries):
                raise ValueError(f"{encoder.info.name} returned the wrong query count")

            current_recall = []
            for query, query_vector in zip(queries, query_vectors):
                ranked = sorted(
                    indexed,
                    key=lambda row: (-cosine_similarity(query_vector, row[1]), row[0]),
                )
                returned = [document_id for document_id, _ in ranked]
                current_recall.append(recall_at_k(query["relevant"], returned, k))
            query_time_samples_ms.append(
                (time.perf_counter() - query_started) * 1000 / len(queries)
            )
            if recall_samples is None:
                recall_samples = current_recall
            elif current_recall != recall_samples:
                raise ValueError(f"{encoder.info.name} returned unstable rankings")

        if recall_samples is None:
            raise RuntimeError("timing loop produced no recall samples")
        query_ms = statistics.median(query_time_samples_ms)
        mean_recall = sum(recall_samples) / len(recall_samples)
        model_results.append(
            {
                "model": encoder.info.name,
                "family": encoder.info.family,
                "scope": encoder.info.scope,
                "description": encoder.info.description,
                "model_ref": encoder.info.model_ref,
                "license": encoder.info.license,
                "model_size_mb": encoder.info.model_size_mb,
                "feature_count": encoder.feature_count,
                f"recall_at_{k}": round(mean_recall, 4),
                "recall_samples": [round(value, 4) for value in recall_samples],
                "indexing_time_ms": round(indexing_ms, 4),
                "query_time_ms": round(query_ms, 4),
                "query_time_samples_ms": [
                    round(value, 4) for value in query_time_samples_ms
                ],
                "query_throughput_per_second": round(1000 / query_ms, 2),
            }
        )

    metric = f"best_recall_at_{k}"
    best = min(
        model_results,
        key=lambda row: (
            -row[f"recall_at_{k}"],
            row["query_time_ms"],
            row["model"],
        ),
    )
    fastest = min(model_results, key=lambda row: (row["query_time_ms"], row["model"]))
    value = best[f"recall_at_{k}"]
    return {
        "project": "embeddings-benchmark",
        "metric": metric,
        "value": value,
        "unit": "ratio",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "command": command,
        "repeat": timing_repeat,
        "samples": best["recall_samples"],
        "summary": {
            "corpus_size": len(corpus),
            "query_count": len(queries),
            "model_count": len(model_results),
            "k": k,
            "best_recall": value,
            "best_model": best["model"],
            "fastest_model": fastest["model"],
            "fastest_query_time_ms": fastest["query_time_ms"],
            "warmup_iterations": warmup_iterations,
            "timing_repeat": timing_repeat,
            "profile": profile,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "implementation": sys.implementation.name,
            "encoder_scope": sorted({encoder.info.scope for encoder in encoders}),
        },
        "scope": {
            "neural_models_included": any(
                encoder.info.scope == "neural-local" for encoder in encoders
            ),
            "statement": (
                "The dense profile compares versioned local ONNX models; the sparse "
                "profile remains a deterministic control."
            ),
        },
        "primary_metric": metric,
        metric: value,
        "best_model": best["model"],
        "models": model_results,
    }
