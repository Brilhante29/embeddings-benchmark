# Change Proposal: baseline

Project: `embeddings-benchmark` (#8)

## Intent

Embedding comparison benchmark that ranks deterministic retrieval models by Recall@k, indexing time, and query time.

## Why This Change Exists

Describe the smallest change that improves the measurable claim or removes a
known portfolio risk.

## Scope

- In scope: <scope>
- Out of scope: paid credentials, unrelated infrastructure, and unmeasured features.

## Portfolio Impact

Program: `ai-evaluation-retrieval`

This change should produce evidence, fixtures, decisions, or components that
can be reused by sibling repositories without moving project-specific behavior
into the kit.

## Acceptance Signal

The benchmark in `project.yaml` remains reproducible and its result is recorded
in `benchmarks/results/`.
