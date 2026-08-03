# Benchmark Proof: embeddings-benchmark

## Primary Metric

- Metric: `best_recall_at_3`
- Unit: `ratio`
- Result: `0.875`
- Models: `BAAI/bge-small-en-v1.5`, `sentence-transformers/all-MiniLM-L6-v2`
- Quality outcome: tie at `0.875`
- Fastest source run: BGE-small at median `3.8599 ms/query`
- Publication result: `benchmarks/publication/embeddings-baseline-v2.json`
- Raw result: `benchmarks/results/embeddings-baseline.json`

## Command

    python -m embeddings_benchmark benchmark --profile dense --k 3 --repeat 5 --warmup 1 --output benchmarks/results/embeddings-baseline.json

## Interpretation

Both dense models recovered the same relevant documents. BGE-small was `4.46x` faster on the measured end-to-end query path, while MiniLM had lower cold indexing time in this run. Timing is hardware-specific; comparisons require the same workload key and Docker runtime.
