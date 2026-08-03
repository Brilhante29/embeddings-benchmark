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
| Benchmark publication needs source/image/fixture/config/lock/artifact provenance. | `patch_now` | `contracts`, `validation` | Reuse the V2 schema, evidence producer, and exact-head gate. | implemented |
| Model downloads made repeated Docker builds unnecessarily slow. | `patch_now` | `container patterns` | Separate dependency, model-cache, package, and fixture layers. | implemented locally |
| Retrieval adapters need batched query/passages semantics without leaking provider APIs into metrics. | `backlog` | `AI evaluation harness` | Promote the proven vectorizer-port pattern after the macro closes. | recorded |
| Model choices and relevance fixtures are project-specific. | `reject` | `templates` | Keep their content local; reuse only contracts and adapter rules. | done |

## Final Gate

- [x] Reusable improvements were patched or recorded.
- [x] Project-specific implementation was not moved into the kit.
- [x] Validation reflects dependency locks, publication provenance, tests, and Docker execution.
