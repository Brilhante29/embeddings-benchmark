# Benchmark Plan

Primary metric: `best_recall_at_3`.

Command:

```powershell
python -m embeddings_benchmark benchmark --k 3 --output benchmarks/results/embeddings-baseline.json
```

Every encoder is fitted or initialized against the same corpus. Each query is transformed by that encoder, ranked by cosine similarity, and scored with `|relevant returned in top k| / |all relevant|`. The benchmark macro-averages query samples.

The committed fixture is a deterministic regression set. A future production claim requires a larger dataset, repeated timing runs, confidence intervals, and at least one neural adapter.
