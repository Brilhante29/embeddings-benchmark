# Architecture Decision

Decision: ports-and-adapters, CLI-first benchmark with one vectorizer port.

Rationale: retrieval metrics and ranking policy must remain independent from model construction. FastEmbed is isolated in a lazy adapter; BGE-small, MiniLM, and deterministic sparse controls satisfy the same protocol. CLI and Docker select profiles but depend inward on the benchmark use case.

SOLID and simplicity:

- SRP: fixture validation, vector generation, ranking, metrics, and presentation are separate concerns.
- OCP/DIP: adding a local or hosted model requires a new adapter, not metric changes.
- LSP/ISP: every adapter supplies only corpus and batched-query vectorization plus metadata.
- KISS/YAGNI: no vector database, HTTP API, queue, cloud service, or agent graph runs in the measured path.

Rejected:

- Sparse-only publication: honest as a control, but insufficient for a repository named embeddings benchmark.
- Sentence Transformers/PyTorch: materially larger runtime for this CPU-focused comparison.
- Hosted embeddings: credentials, network variance, and mutable pricing would weaken the local baseline.
- Qdrant server: six documents do not justify introducing storage/network overhead into the encoder comparison.
