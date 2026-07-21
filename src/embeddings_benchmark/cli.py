import argparse
import json
from pathlib import Path

from .benchmark import DEFAULT_CORPUS, DEFAULT_QUERIES, evaluate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["benchmark"], nargs="?", default="benchmark")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--queries", type=Path, default=DEFAULT_QUERIES)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument(
        "--output", default=Path("benchmarks/results/embeddings-baseline.json"), type=Path
    )
    args = parser.parse_args()
    command = (
        "python -m embeddings_benchmark benchmark "
        f"--corpus {args.corpus.as_posix()} --queries {args.queries.as_posix()} "
        f"--k {args.k} --output {args.output.as_posix()}"
    )
    result = evaluate(args.k, args.corpus, args.queries, command=command)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
