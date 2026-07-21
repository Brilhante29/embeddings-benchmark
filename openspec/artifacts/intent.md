# Intent: embeddings-benchmark

## Measurable Claim

Embedding comparison benchmark that ranks deterministic retrieval models by Recall@k, indexing time, and query time.

## Problem

Compares retrieval encoders before the platform chooses a production embedding provider.

## In Scope

- Use the selected component pack: `ai-evaluation-retrieval`.
- Keep the project under the AI Evaluation and Retrieval Systems program.
- Preserve the benchmark contract: `best_recall_at_3` in `benchmarks/results/embeddings-baseline.json`.
- Keep the default path local-first and reproducible.

## Out Of Scope

- Paid credentials for the default demo.
- External infrastructure that is not required by the benchmark.
- Replacing local portfolio skills with external components silently.

## Default Demo Path

- Status: benchmarked
- Runtime: python-cli
- Benchmark command: `python -m embeddings_benchmark benchmark --output benchmarks/results/embeddings-baseline.json`

## Public Proof

- Benchmark: best_recall_at_3 = 1.00
- Result path: `benchmarks/results/embeddings-baseline.json`
