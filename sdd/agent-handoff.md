# Agent Handoff

Project: `8 - embeddings-benchmark`

## Current Slice

- Dense FastEmbed/ONNX profile compares BGE-small and MiniLM on CPU.
- Sparse profile remains the no-download regression control.
- Raw benchmark: Recall@3 `0.875` for both models; BGE is the faster measured query path in the source run.
- Docker preloads model artifacts and runs successfully with `--network none` as UID 10001.

## Invariants

- Metrics and ranking never import FastEmbed or provider SDKs.
- Every model sees identical fixtures, `k`, warmup, repeat count, and timing boundary.
- Query latency includes embedding, cosine scoring, and ranking; model download is excluded.
- Publication requires a clean source commit, generated V2 evidence, and exact-head GitHub Actions success.

## Next Action

Validate V2 provenance against Git blobs, commit publication evidence, push, and verify every GitHub Actions step on the exact final SHA.
