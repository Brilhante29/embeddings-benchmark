# Benchmark Plan

Primary metric: `best_recall_at_3`.

Secondary metrics: median end-to-end query latency, query throughput, and cold indexing time per model.

Command:

```powershell
python -m embeddings_benchmark benchmark --profile dense --k 3 --repeat 5 --warmup 1 --output benchmarks/results/embeddings-baseline.json
```

Both 384-dimensional models receive the same six-document corpus and four queries. Corpus vectors use passage encoding; query vectors use query encoding. Each measured iteration includes query embedding, cosine scoring, ranking, and Recall@3 calculation. One warmup is excluded; five per-query timings are summarized by the median.

Publication comparability key: `embeddings:recall-at-3:dense-onnx-v1:4-queries`. Changes to model set, fixture, `k`, warmup, repeat count, or timing boundary require a new workload version/key.

The fixture is a deterministic regression set. Production model selection additionally requires a larger reviewed dataset, confidence intervals across process restarts, multilingual coverage, and representative document lengths.
