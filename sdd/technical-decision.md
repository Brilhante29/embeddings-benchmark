# Technical Decision

- Runtime: Python 3.12.13 CLI packaged through `pyproject.toml`.
- Dense runtime: FastEmbed 0.8.0 with ONNX Runtime, fully locked for Linux.
- Models: `BAAI/bge-small-en-v1.5` (MIT, 384 dimensions) and `sentence-transformers/all-MiniLM-L6-v2` (Apache-2.0, 384 dimensions).
- Model semantics: corpus uses `passage_embed`; queries use batched `query_embed`.
- Controls: word TF-IDF, character TF-IDF, and signed BLAKE2 feature hashing remain dependency-free test adapters.
- Similarity: L2-normalized vectors with cosine similarity and document-ID tie-breaking.
- Timing: one warmup, five measured repetitions, median full query path; cold indexing includes lazy model initialization.
- Reproducibility: pinned base image, Linux dependency lock, baked model cache, offline non-root container execution.
- Evidence: raw JSON plus schema-version 2 publication artifact produced from a clean Git commit.
