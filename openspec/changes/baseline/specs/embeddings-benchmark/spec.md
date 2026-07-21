# embeddings-benchmark Specification

## Requirement: reproducible portfolio proof

The system SHALL expose local and Docker paths that write a benchmark JSON under `benchmarks/results/` without paid credentials or model downloads.

## Requirement: correct and comparable retrieval metrics

The system SHALL compute Recall@k as the fraction of all relevant documents returned in the first `k` positions and SHALL compare encoders on identical fixtures and ranking rules.

### Scenario: partially recovered relevance set

- GIVEN a query has two relevant documents
- WHEN one relevant document appears in the top `k`
- THEN the query Recall@k is `0.5`

## Requirement: replaceable encoders

The system SHALL access encoder implementations through one vectorizer protocol.

### Scenario: future neural adapter

- GIVEN a local or neural adapter implements the protocol
- WHEN the benchmark selects it
- THEN ranking and metric code remain unchanged

## Requirement: honest scope

The committed baseline SHALL identify every included encoder as non-neural and SHALL NOT claim transformer semantic quality.
