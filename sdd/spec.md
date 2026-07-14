# Spec: 8 - embeddings-benchmark

## Claim

Embedding comparison benchmark that ranks deterministic retrieval models by Recall@k, indexing time, and query time.

## Acceptance Criteria

- Runs locally with `python -m embeddings_benchmark benchmark --output benchmarks/results/embeddings-baseline.json`.
- Runs in Docker with no paid secret.
- Writes benchmark JSON under `benchmarks/results/`.
- Keeps domain/evaluation logic independent from CLI and future providers.
