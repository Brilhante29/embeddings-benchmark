# #8 embeddings-benchmark: same Recall@3, 4.80x latency gap

Two real 384-dimensional embedding models reached the same `Recall@3 = 0.875` on an identical local fixture. In the source Docker run, BGE-small completed the end-to-end query path at a median `3.9213 ms/query`; MiniLM required `18.8207 ms/query`.

The useful result is not that one model won quality on four queries. It is that a model decision can be made with explicit quality, latency, cold-start, license, size, fixture, and runtime evidence instead of brand preference.

FastEmbed 0.8.0 and ONNX Runtime keep CPU inference local. Model construction lives behind a vectorizer port; Recall@k, cosine ranking, timing policy, CLI, and evidence generation do not import provider code. The same core can evaluate a future local or hosted adapter without rewriting metric semantics.

The Docker build preloads both model artifacts. The benchmark then runs as an unprivileged user with networking disabled. V2 evidence binds the source commit, image digest, fixtures, benchmark config, Linux dependency lock, and raw JSON.

Limit: six documents and four queries make this a regression baseline, not production model selection. The next scale step is a reviewed multilingual dataset with process-level repetitions and confidence intervals, not more infrastructure.
