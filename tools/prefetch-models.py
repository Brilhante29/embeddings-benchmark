import json
import os
from pathlib import Path

from fastembed import TextEmbedding

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "benchmarks" / "config" / "embeddings-baseline-v2.json"


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    cache_dir = os.environ.get("FASTEMBED_CACHE_PATH")
    for model_name in config["models"]:
        options = {"model_name": model_name}
        if cache_dir:
            options["cache_dir"] = cache_dir
        model = TextEmbedding(**options)
        vectors = list(model.passage_embed(["portfolio embedding cache warmup"]))
        if not vectors or len(vectors[0]) <= 0:
            raise RuntimeError(f"failed to cache {model_name}")
        print(f"cached={model_name} dimensions={len(vectors[0])}")


if __name__ == "__main__":
    main()
