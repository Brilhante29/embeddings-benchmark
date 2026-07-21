# Change Proposal: correct-vectorizer-baseline

Project: `embeddings-benchmark` (#8)

## Intent

Replace set-overlap heuristics and binary hit rate with numeric vectorizers, cosine ranking, and mathematically correct Recall@k.

## Scope

- In scope: word/character TF-IDF, feature hashing, fair retrieval comparison, shared-contract evidence, and truthful non-neural labeling.
- Out of scope: paid APIs, downloaded transformer weights, production-scale relevance datasets, and unrelated infrastructure.

## Portfolio Impact

Program: `ai-evaluation-retrieval`.

The result contract and Recall@k semantics can be consumed by sibling evaluation repositories without code coupling.

## Acceptance Signal

Tests demonstrate partial relevance recovery, all three vectorizers produce numeric vectors, and the committed benchmark satisfies the common top-level contract.
