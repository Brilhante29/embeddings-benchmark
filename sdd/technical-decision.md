# Technical Decision

- Runtime: Python 3.10+ CLI packaged through `pyproject.toml`.
- Dependencies: standard library only; no provider SDK and no model download.
- Encoders: word unigram/bigram TF-IDF, character 3-5 gram TF-IDF, and signed BLAKE2 feature hashing.
- Similarity: L2-normalized sparse vectors with cosine similarity.
- Fairness: identical corpus, queries, `k`, relevance judgments, and deterministic tie-breaking.
- Benchmark: shared contract JSON at `benchmarks/results/embeddings-baseline.json`.
- Docker: installs the local package and runs the benchmark command by default.
