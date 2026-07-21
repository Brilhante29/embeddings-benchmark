# #8 embeddings-benchmark: best_recall_at_3 = 1.00

Embedding comparison benchmark that ranks deterministic retrieval models by Recall@k, indexing time, and query time.

This repository belongs to the AI Evaluation and Retrieval Systems program. Its job is narrow: prove the measurable claim through the selected component pack before adding unrelated infrastructure or features.

The benchmark is the proof. best_recall_at_3 = 1.00.  The result is stored in `benchmarks/results/embeddings-baseline.json` and can be reproduced from the Docker/local path.

The important architecture decision is clean-architecture. The metric and benchmark use cases must stay independent from CLI, fixtures, and future providers.

The default path stays local-first. The project uses python, exposes cli-first, uses messaging mode `none`, and stores data with `fixture-files`. The dependency rule is explicit: Domain metrics and application benchmark orchestration do not import interface code.

The rejected work matters as much as the implemented work. Anything that does not improve the benchmark stays out of the first version.

Post angle: start with the number, show the architecture boundary, then explain which future adapter can be added without changing the core use cases.
