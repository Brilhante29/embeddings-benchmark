# Benchmark Plan

Primary metric: `best_recall_at_3`.

Command:

```powershell
python -m embeddings_benchmark benchmark --output benchmarks/results/embeddings-baseline.json
```

The benchmark uses local fixtures so the result is reproducible and does not require external credentials.
