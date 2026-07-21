# Verification: embeddings-benchmark

Date: `2026-07-21`

## Evidence

- Three unit tests passed, including the two-relevant/one-recovered case with Recall@k `0.5`.
- `tools/validate-project.ps1 -SkipDocker` passed.
- Docker image `embeddings-benchmark:audit` built and executed successfully.
- The container reported character TF-IDF as the best encoder with Recall@3 `1.0`.
- Word TF-IDF and feature hashing each reported `0.875` on the same fixture.
- The result contains every required top-level benchmark contract field.

## Remaining Risk

The fixture has six documents and four queries. It is a deterministic regression proof, not production retrieval evidence. Remote CI is not yet verified.
