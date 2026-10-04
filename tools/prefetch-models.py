import json
import os
from pathlib import Path

from fastembed import TextEmbedding
from fastembed.common.utils import define_cache_dir
from huggingface_hub import snapshot_download

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "benchmarks" / "config" / "embeddings-baseline-v2.json"
LOCK = ROOT / "benchmarks" / "config" / "model-artifacts.lock.json"


def pin_locked_revisions(cache_dir: Path, lock_path: Path = LOCK, download=snapshot_download) -> None:
    """Download each locked snapshot and point the cache's ``main`` ref at it.

    FastEmbed resolves models through the cached ``main`` ref before it touches the
    network, so pinning the ref keeps every later load on the locked commit even after
    the upstream repository publishes a new revision.
    """
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    for entry in lock["models"]:
        repository = entry["cache_repository"]
        revision = entry["revision"]
        download(repo_id=repository, revision=revision, cache_dir=str(cache_dir))
        ref = cache_dir / f"models--{repository.replace('/', '--')}" / "refs" / "main"
        ref.parent.mkdir(parents=True, exist_ok=True)
        ref.write_text(revision, encoding="utf-8")


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    cache_dir = define_cache_dir(os.environ.get("FASTEMBED_CACHE_PATH"))
    pin_locked_revisions(cache_dir)
    for model_name in config["models"]:
        model = TextEmbedding(
            model_name=model_name, cache_dir=str(cache_dir), local_files_only=True
        )
        vectors = list(model.passage_embed(["portfolio embedding cache warmup"]))
        if not vectors or len(vectors[0]) <= 0:
            raise RuntimeError(f"failed to cache {model_name}")
        print(f"cached={model_name} dimensions={len(vectors[0])}")


if __name__ == "__main__":
    main()
