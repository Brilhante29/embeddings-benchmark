# References

| Source | Reuse Type | Notes |
|---|---|---|
| [FastEmbed 0.8.0 on PyPI](https://pypi.org/project/fastembed/0.8.0/) | runtime dependency | Versioned CPU-local embedding runtime backed by ONNX Runtime. |
| [FastEmbed supported models](https://qdrant.github.io/fastembed/examples/Supported_Models/) | model selection | Records dimensions, licenses, and published sizes for BGE-small and MiniLM. |
| [FastEmbed retrieval guide](https://qdrant.github.io/fastembed/qdrant/Retrieval_with_FastEmbed/) | API semantics | Supports separate `passage_embed` and `query_embed` paths used by the adapter. |
| `portfolio-reuse-kit` | architecture, validation, skills, SDD | Supplies the V2 publication contract and reusable evidence producer. |
| Committed local fixtures | benchmark workload | Keeps relevance judgments reviewable and identical for every model. |

No paid API response or proprietary dataset is required. Model bytes are downloaded only while building the Docker image or warming a new local cache; the container benchmark is verified with networking disabled.
