# Intent: embeddings-benchmark

## Measurable Claim

Compare two versioned local dense embedding models by Recall@3, median end-to-end query latency, throughput, and cold indexing time.

## Problem

Select a retrieval encoder from measured quality/runtime tradeoffs before the AI Evaluation and Retrieval Systems platform adopts one.

## In Scope

- BGE-small and MiniLM through FastEmbed 0.8.0/ONNX Runtime.
- Identical committed corpus, queries, relevance judgments, cosine ranking, and `k`.
- One warmup and five measured repetitions.
- Provider-neutral vectorizer port plus deterministic sparse controls.
- Offline non-root Docker execution and V2 publication provenance.

## Out Of Scope

- Paid embedding APIs, vector databases, queues, web APIs, or cloud infrastructure.
- Production-scale or MTEB quality claims from the four-query fixture.
- Silent replacement of local portfolio skills or publication contracts.

## Default Demo Path

- Status: published
- Runtime: Python 3.12.13 / FastEmbed 0.8.0 / ONNX CPU
- Benchmark command: `python -m embeddings_benchmark benchmark --profile dense --k 3 --repeat 5 --warmup 1 --output benchmarks/results/embeddings-baseline.json`

## Public Proof

- Benchmark: both models reached `Recall@3 = 0.875`; BGE-small was `4.93x` faster on median query latency in the source run.
- Result path: `benchmarks/publication/embeddings-baseline-v2.json`
