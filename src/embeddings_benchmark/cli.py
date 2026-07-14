import argparse
import json
import re
import time
from pathlib import Path

def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))

def chargrams(text: str) -> set[str]:
    compact = re.sub(r"[^a-z0-9]+", "", text.lower())
    return {compact[i:i+3] for i in range(max(len(compact) - 2, 0))}

MODELS = {
    "keyword-overlap": tokens,
    "char-trigram": chargrams,
    "hybrid-token-char": lambda text: tokens(text) | chargrams(text),
}

def load_jsonl(path: str) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]

def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / max(len(left | right), 1)

def evaluate(k: int = 3) -> dict:
    corpus = load_jsonl("data/fixtures/corpus.jsonl")
    queries = load_jsonl("data/fixtures/queries.jsonl")
    model_results = []
    for name, encoder in MODELS.items():
        start_index = time.perf_counter()
        indexed = [(doc["id"], encoder(doc["text"])) for doc in corpus]
        indexing_ms = (time.perf_counter() - start_index) * 1000
        start_query = time.perf_counter()
        hits = 0
        for query in queries:
            qvec = encoder(query["query"])
            ranked = sorted(indexed, key=lambda row: jaccard(qvec, row[1]), reverse=True)[:k]
            returned = {doc_id for doc_id, _ in ranked}
            if returned & set(query["relevant"]):
                hits += 1
        query_ms = (time.perf_counter() - start_query) * 1000 / len(queries)
        model_results.append({
            "model": name,
            "recall_at_3": round(hits / len(queries), 4),
            "indexing_time_ms": round(indexing_ms, 4),
            "query_time_ms": round(query_ms, 4),
        })
    best = max(model_results, key=lambda row: row["recall_at_3"])
    return {"project": "embeddings-benchmark", "primary_metric": "best_recall_at_3", "best_recall_at_3": best["recall_at_3"], "best_model": best["model"], "models": model_results}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["benchmark"], nargs="?", default="benchmark")
    parser.add_argument("--output", default="benchmarks/results/embeddings-baseline.json")
    args = parser.parse_args()
    result = evaluate()
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
