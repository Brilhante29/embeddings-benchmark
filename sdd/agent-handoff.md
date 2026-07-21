# Agent Handoff

Project: `8 - embeddings-benchmark`

## Current State

- Word TF-IDF, character TF-IDF, and feature hashing produce numeric sparse vectors.
- Recall@k counts every relevant document and is macro-averaged across queries.
- The baseline result satisfies the shared benchmark-result contract.
- Scope is explicitly non-neural and local-first.

## Continuation Rules

- Add neural encoders only through `Vectorizer` in `src/embeddings_benchmark/vectorizers.py`.
- Do not describe these baselines as transformer models or semantic production evidence.
- Preserve per-query Recall@k samples and the shared top-level result fields.
- Calibrate larger benchmarks before full runs; avoid heavyweight downloads in the default path.

## Remaining Gates

- Local tests, benchmark, and project validator must pass after each change.
- Docker must execute the committed command.
- Publication remains blocked until the branch is pushed and remote CI is verified.
