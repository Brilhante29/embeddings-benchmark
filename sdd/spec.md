# Spec: embeddings-benchmark

## Number

#8

## Claim

Este projeto prova que: comparacao de modelos de embedding.

## Stack

python, sentence-transformers, faiss, qdrant, docker

## User-visible output

- Docker command: pending
- README opens with: # #8 embeddings-benchmark
- Benchmark table: recall_at_k, indexing_time_ms, query_time_ms

## Scope

In:

- Implementar o menor produto funcional que prove o claim.
- Rodar por Docker.
- Gerar benchmark JSON reproduzivel.

Out:

- Publicar repo antes do primeiro resultado numerico.
- Depender de segredo pago para o caminho default.

## Architecture

`	xt
client -> app -> domain -> adapters -> benchmark output
`

## Benchmark

Primary metric:

- name: recall_at_k, indexing_time_ms, query_time_ms
- target: first reproducible baseline
- command: pending
- result file: enchmarks/results/*.json

## Dataset or fixture

- source: pending
- size: pending
- license: pending
- deterministic seed: 42

## Definition of done

- [ ] Docker command works from clean clone.
- [ ] README starts with project number and benchmark result.
- [ ] Benchmark command writes JSON result.
- [ ] Tests cover core behavior.
- [ ] REFERENCES.md explains reuse.
- [ ] No secret or paid credential required for default demo.