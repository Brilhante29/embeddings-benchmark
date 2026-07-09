# #8 embeddings-benchmark

**Status:** scaffold

**Proves:** comparacao de modelos de embedding.

**Benchmark target:** recall_at_k, indexing_time_ms, query_time_ms.

**Stack:** python, sentence-transformers, faiss, qdrant, docker.

## Next milestone

Implement the smallest Docker-runnable version and produce the first JSON benchmark under enchmarks/results/.

## Run

`ash
docker build -t embeddings-benchmark .
docker run --rm embeddings-benchmark
`

## Benchmark

`ash
docker run --rm embeddings-benchmark benchmark
`

| Metric | Value | Unit |
|---|---:|---|
| recall_at_k, indexing_time_ms, query_time_ms | pending | pending |

## Architecture

Defined in sdd/spec.md before implementation.

## References

See REFERENCES.md.