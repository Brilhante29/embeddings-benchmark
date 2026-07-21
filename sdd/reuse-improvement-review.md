# Reuse Improvement Review

Project: `8 - embeddings-benchmark`

## Review Points

- [x] after scaffold
- [x] after architecture decision
- [x] after first working slice
- [x] after benchmark result
- [x] before publication
- [ ] after CI failure, if applicable

## Findings

| Finding | Classification | Kit Area | Action | Status |
|---|---|---|---|---|
| AI evaluation repositories need one enforced top-level benchmark-result contract. | `backlog` | `contracts`, `validation` | Validate required fields and tracked evidence in the kit publication gate. | pending |
| Retrieval projects need a reusable Recall@k definition that counts every relevant item. | `backlog` | `harness` | Promote the tested metric semantics after RAG adopts the same definition. | pending |
| Encoder implementations and fixtures are project-specific. | `reject` | `templates` | Keep them in this repository behind the shared port. | done |

## Final Gate

- [x] Reusable improvements were patched or recorded.
- [x] Project-specific implementation was not moved into the kit.
- [x] Validation reflects the required reuse-improvement review gate.
