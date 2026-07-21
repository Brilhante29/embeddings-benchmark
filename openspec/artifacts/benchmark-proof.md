# Benchmark Proof: embeddings-benchmark

## Primary Metric

- Metric: `best_recall_at_3`
- Unit: `ratio`
- Result: `1.0`
- Best encoder: `character-tfidf`
- Result path: `benchmarks/results/embeddings-baseline.json`

## Command

    python -m embeddings_benchmark benchmark --k 3 --output benchmarks/results/embeddings-baseline.json

## Interpretation

All four query-level recall samples were `1.0` for character TF-IDF. Word TF-IDF and feature hashing each scored `0.875` because the two-relevant-document query recovered only one relevant item. The fixture is a regression set, not a production-quality claim.
