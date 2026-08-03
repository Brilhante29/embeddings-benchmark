import argparse
import json
from pathlib import Path

from .benchmark import DEFAULT_CORPUS, DEFAULT_QUERIES, evaluate
from .vectorizers import default_dense_vectorizers, default_vectorizers


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["benchmark"], nargs="?", default="benchmark")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--profile", choices=["dense", "sparse", "all"], default="dense")
    parser.add_argument("--repeat", type=int, default=5)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument(
        "--output", default=Path("benchmarks/results/embeddings-baseline.json"), type=Path
    )
    args = parser.parse_args()
    command = (
        "python -m embeddings_benchmark benchmark "
        f"--corpus {args.corpus.as_posix()} --queries {args.queries.as_posix()} "
        f"--k {args.k} --profile {args.profile} --repeat {args.repeat} "
        f"--warmup {args.warmup} --output {args.output.as_posix()}"
    )
    sparse = default_vectorizers()
    dense = default_dense_vectorizers()
    selected = dense if args.profile == "dense" else sparse
    if args.profile == "all":
        selected = dense + sparse
    result = evaluate(
        args.k,
        args.corpus,
        args.queries,
        vectorizers=selected,
        command=command,
        timing_repeat=args.repeat,
        warmup_iterations=args.warmup,
        profile=args.profile,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
