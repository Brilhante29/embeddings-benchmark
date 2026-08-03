# embeddings-benchmark Specification

## Requirement: reproducible local neural proof

The system SHALL expose local and Docker paths that compare two versioned dense embedding models without paid credentials. The built container SHALL complete with networking disabled.

## Requirement: correct and comparable retrieval metrics

The system SHALL compute Recall@k as the fraction of all relevant documents returned in the first `k` positions and SHALL compare models on identical fixtures, ranking, warmup, and repetition rules.

### Scenario: partially recovered relevance set

- GIVEN a query has two relevant documents
- WHEN one relevant document appears in the top `k`
- THEN the query Recall@k is `0.5`

## Requirement: replaceable encoders

The system SHALL access dense, sparse, local, or future hosted encoders through one batched vectorizer protocol.

### Scenario: provider substitution

- GIVEN an adapter implements passage and query vectorization
- WHEN the benchmark selects it
- THEN metric, ranking, timing, and output code remain unchanged

## Requirement: honest timing and scope

The system SHALL exclude model download from measured execution, include embedding plus ranking in query latency, publish warmup/repeat policy, and identify the fixture as a regression baseline rather than production-quality evidence.
