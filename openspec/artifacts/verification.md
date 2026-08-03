# Verification

- Four unit tests pass for Recall@k semantics, sparse vectorizers, dense adapter substitution, and result contract.
- Docker dependency resolution passes `pip check` against the Linux lock.
- The image caches BGE-small and MiniLM during build.
- The non-root container completes with `--network none`.
- Both dense models report Recall@3 `0.875` on the same four-query fixture.
- The source run reports BGE-small at median `3.8599 ms/query` and MiniLM at `17.211 ms/query`; these timings are environment-specific.
- V2 provenance is generated from source SHA `3a6ec33`; the publication commit still requires exact-head GitHub Actions verification.
