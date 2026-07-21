from __future__ import annotations

import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from .vectorizers import Vectorizer, cosine_similarity, default_vectorizers

DEFAULT_CORPUS = Path("data/fixtures/corpus.jsonl")
DEFAULT_QUERIES = Path("data/fixtures/queries.jsonl")
DEFAULT_COMMAND = (
    "python -m embeddings_benchmark benchmark --k 3 "
    "--output benchmarks/results/embeddings-baseline.json"
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
) -> dict:
    corpus = load_jsonl(corpus_path)
    queries = load_jsonl(queries_path)
    _validate_fixtures(corpus, queries, k)
    encoders = vectorizers or default_vectorizers()
    model_results = []

    for encoder in encoders:
        indexing_started = time.perf_counter()
        vectors = encoder.fit_transform([row["text"] for row in corpus])
        indexed = list(zip((row["id"] for row in corpus), vectors))
        indexing_ms = (time.perf_counter() - indexing_started) * 1000

        query_started = time.perf_counter()
        recall_samples = []
        for query in queries:
            query_vector = encoder.transform(query["query"])
            ranked = sorted(
                indexed,
                key=lambda row: (-cosine_similarity(query_vector, row[1]), row[0]),
            )
            returned = [document_id for document_id, _ in ranked]
            recall_samples.append(recall_at_k(query["relevant"], returned, k))
        query_ms = (time.perf_counter() - query_started) * 1000 / len(queries)
        mean_recall = sum(recall_samples) / len(recall_samples)
        model_results.append(
            {
                "model": encoder.info.name,
                "family": encoder.info.family,
                "scope": encoder.info.scope,
                "description": encoder.info.description,
                "feature_count": encoder.feature_count,
                f"recall_at_{k}": round(mean_recall, 4),
                "recall_samples": [round(value, 4) for value in recall_samples],
                "indexing_time_ms": round(indexing_ms, 4),
                "query_time_ms": round(query_ms, 4),
            }
        )

    metric = f"best_recall_at_{k}"
    best = min(
        model_results,
        key=lambda row: (-row[f"recall_at_{k}"], row["model"]),
    )
    value = best[f"recall_at_{k}"]
    return {
        "project": "embeddings-benchmark",
        "metric": metric,
        "value": value,
        "unit": "ratio",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "command": command,
        "repeat": 1,
        "samples": best["recall_samples"],
        "summary": {
            "corpus_size": len(corpus),
            "query_count": len(queries),
            "model_count": len(model_results),
            "k": k,
            "best_recall": value,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "implementation": sys.implementation.name,
            "encoder_scope": "non-neural-local-vectorizers",
        },
        "scope": {
            "neural_models_included": False,
            "statement": (
                "This baseline compares deterministic non-neural vectorizers; "
                "it does not claim neural semantic embedding quality."
            ),
        },
        "primary_metric": metric,
        metric: value,
        "best_model": best["model"],
        "models": model_results,
    }
