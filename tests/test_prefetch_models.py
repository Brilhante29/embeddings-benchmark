import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_prefetch_module():
    spec = importlib.util.spec_from_file_location(
        "prefetch_models", ROOT / "tools" / "prefetch-models.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PinLockedRevisionsTests(unittest.TestCase):
    def test_downloads_locked_commits_and_pins_main_refs(self):
        prefetch = load_prefetch_module()
        calls = []
        with tempfile.TemporaryDirectory() as directory:
            cache = Path(directory)
            lock = cache / "lock.json"
            lock.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "models": [
                            {
                                "model": "example/model",
                                "cache_repository": "org/model-onnx",
                                "revision": "a" * 40,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            prefetch.pin_locked_revisions(
                cache, lock_path=lock, download=lambda **kwargs: calls.append(kwargs)
            )

            self.assertEqual(
                calls,
                [{"repo_id": "org/model-onnx", "revision": "a" * 40, "cache_dir": str(cache)}],
            )
            ref = cache / "models--org--model-onnx" / "refs" / "main"
            self.assertEqual(ref.read_text(encoding="utf-8"), "a" * 40)

    def test_repository_lock_pins_both_benchmark_models(self):
        lock = json.loads(
            (ROOT / "benchmarks" / "config" / "model-artifacts.lock.json").read_text(
                encoding="utf-8"
            )
        )
        config = json.loads(
            (ROOT / "benchmarks" / "config" / "embeddings-baseline-v2.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual({entry["model"] for entry in lock["models"]}, set(config["models"]))
        for entry in lock["models"]:
            self.assertRegex(entry["revision"], r"^[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
