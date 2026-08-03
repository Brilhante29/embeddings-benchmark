# Verification

- Four unit tests pass for Recall@k semantics, sparse vectorizers, dense adapter substitution, and result contract.
- Docker dependency resolution passes `pip check` against the Linux lock.
- The image caches BGE-small and MiniLM during build.
- The non-root container completes with `--network none`.
- Both dense models report Recall@3 `0.875` on the same four-query fixture.
- The source run reports BGE-small at median `3.9213 ms/query` and MiniLM at `18.8207 ms/query`; these timings are environment-specific.
- Publication remains pending until generated V2 provenance and exact-head GitHub Actions pass.
