from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def verify(cache: Path, lock_path: Path) -> None:
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    if lock.get("schema_version") != 1 or not isinstance(lock.get("models"), list):
        raise ValueError("invalid model artifact lock")
    for model in lock["models"]:
        repository = model["cache_repository"]
        revision = model["revision"]
        if not isinstance(repository, str) or not isinstance(revision, str):
            raise ValueError("invalid model lock entry")
        reference = cache / f"models--{repository.replace('/', '--')}" / "refs" / "main"
        observed = reference.read_text(encoding="utf-8").strip()
        if observed != revision:
            raise ValueError(
                f"model revision drift for {model['model']}: expected {revision}, got {observed}"
            )
        tree = reference.parent.parent / "trees" / f"{revision}.json"
        if not tree.is_file():
            raise ValueError(f"missing snapshot tree for {model['model']}")
        print(f"model_revision={model['model']}@{revision}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cache",
        default=os.environ.get("FASTEMBED_CACHE_PATH", "/opt/fastembed-cache"),
    )
    parser.add_argument(
        "--lock", default="benchmarks/config/model-artifacts.lock.json"
    )
    args = parser.parse_args()
    verify(Path(args.cache), Path(args.lock))


if __name__ == "__main__":
    main()
