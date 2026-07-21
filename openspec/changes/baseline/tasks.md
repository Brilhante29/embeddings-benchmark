# Change Tasks: correct-vectorizer-baseline

## Planning

- [x] Record non-neural scope and rejected alternatives.
- [x] Define correct Recall@k semantics and fair comparison rules.
- [x] Preserve a provider-neutral vectorizer boundary.

## Implementation

- [x] Implement word TF-IDF, character TF-IDF, and feature hashing.
- [x] Add per-query Recall@k samples and shared result fields.
- [x] Add tests for partial relevance recovery and encoder output.
- [x] Commit-ready benchmark JSON and matching README number.

## Verification

- [x] Run compile and unit tests.
- [x] Run `tools/validate-project.ps1 -SkipDocker`.
- [x] Build and execute `embeddings-benchmark:audit`.
- [ ] Run `openspec validate --strict` when the CLI is installed.
- [ ] Verify remote CI after publication.
