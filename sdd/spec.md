# Spec: 8 - embeddings-benchmark

## Claim

Compare deterministic non-neural retrieval vectorizers with correct Recall@k and timing metrics.

## Acceptance Criteria

- Runs with `python -m embeddings_benchmark benchmark --k 3 --output benchmarks/results/embeddings-baseline.json`.
- Runs in Docker without credentials or model downloads.
- Compares word TF-IDF, character TF-IDF, and feature hashing through one vectorizer protocol.
- Computes per-query recall as recovered relevant documents divided by all relevant documents.
- Uses the same corpus, queries, cosine ranking, and `k` for every encoder.
- Emits the shared benchmark contract and labels the baseline as non-neural.
