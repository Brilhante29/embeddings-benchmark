# Release Checklist

- [x] README opens with project number, claim, and measured numbers.
- [x] Two real dense models run behind the vectorizer port.
- [x] Linux dependencies, Docker base, and model set are pinned.
- [x] Unit tests cover Recall@k, sparse controls, dense adapter substitution, and result contract.
- [x] Docker image executes the dense benchmark offline as a non-root user.
- [x] Raw benchmark JSON is tracked and contract-compatible.
- [x] V2 publication artifact generated from source commit `3a6ec33ec9e2468c2f9b29f2e015d4c98b91a437`.
- [x] Source gate verified by GitHub Actions run `30791776789`; the publication commit must pass again on its exact SHA.
- [x] Reuse improvement review is complete.

Status is `published` with committed V2 evidence; exact-head publication CI is recorded centrally after the push.
