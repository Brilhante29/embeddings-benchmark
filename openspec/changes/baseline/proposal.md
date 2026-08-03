# Proposal: Real Local Embedding Comparison

## Why

A sparse-only benchmark did not satisfy the repository name or original portfolio promise to compare embedding models. The project must retain honest local reproducibility while exercising real neural inference.

## Scope

- In scope: BGE-small, MiniLM, FastEmbed/ONNX CPU inference, sparse controls, correct Recall@3, full query timing, locked dependencies, offline Docker, and V2 evidence.
- Out of scope: paid APIs, vector databases, production-scale relevance datasets, GPU tuning, and unrelated infrastructure.

## Architecture

Dense and sparse encoders implement one batched vectorizer port. The benchmark owns fixtures, ranking, metrics, warmup/repetition policy, and output contracts. FastEmbed remains an outer adapter loaded lazily.

## Verification

Four unit tests prove Recall semantics, sparse controls, adapter substitutability, and result contracts. Docker must preload both model artifacts, execute with `--network none`, and produce the dense benchmark JSON.
