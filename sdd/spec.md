# Spec: 8 - embeddings-benchmark

## Claim

Compare two versioned dense embedding models locally with correct Recall@3, cold indexing time, and end-to-end query latency.

## Acceptance Criteria

- Runs the dense profile with `python -m embeddings_benchmark benchmark --profile dense --k 3 --repeat 5 --warmup 1`.
- Runs the built Docker image with networking disabled and no credentials.
- Compares BGE-small and MiniLM through one vectorizer protocol and keeps sparse controls available.
- Uses `passage_embed` for corpus vectors and `query_embed` for query vectors.
- Computes per-query Recall@k as recovered relevant documents divided by all relevant documents.
- Uses identical corpus, queries, cosine ranking, `k`, warmup, and repetition policy for both models.
- Emits raw and V2 publication contracts with source, image, fixture, config, lock, and artifact digests.
