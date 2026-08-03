# Release Checklist

- [x] README opens with project number, claim, and measured numbers.
- [x] Two real dense models run behind the vectorizer port.
- [x] Linux dependencies, Docker base, and model set are pinned.
- [x] Unit tests cover Recall@k, sparse controls, dense adapter substitution, and result contract.
- [x] Docker image executes the dense benchmark offline as a non-root user.
- [x] Raw benchmark JSON is tracked and contract-compatible.
- [ ] V2 publication artifact generated from a clean source commit.
- [ ] Remote CI verified on the exact publication SHA.
- [x] Reuse improvement review is complete.

Status remains `benchmarked` until V2 evidence and exact-head remote CI both pass.
