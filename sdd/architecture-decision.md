# Architecture Decision

Decision: ports-and-adapters, CLI-first benchmark with a sparse-vectorizer port.

Rationale: ranking and Recall@k are independent from encoder construction. The baseline implements word TF-IDF, character TF-IDF, and deterministic feature hashing with numeric sparse vectors and cosine similarity. CLI, Docker, and future neural/provider adapters depend inward.

Rejected:

- Token-set Jaccard: it is a lexical overlap heuristic rather than a vectorizer benchmark.
- Downloaded transformer model as the default: useful as a later adapter, but too heavy for the credential-free baseline.
- External managed service: it would make the baseline dependent on credentials and mutable provider behavior.
- Web UI or messaging: neither contributes to the measured claim.
