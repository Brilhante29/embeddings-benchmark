import unittest

from embeddings_benchmark.benchmark import evaluate, recall_at_k
from embeddings_benchmark.vectorizers import (
    FastEmbedVectorizer,
    default_dense_vectorizers,
    default_vectorizers,
)


class FakeDenseModel:
    def passage_embed(self, texts):
        return ([1.0, 0.0] if "semantic" in text else [0.0, 1.0] for text in texts)

    def query_embed(self, texts):
        return ([1.0, 0.0] if "semantic" in text else [0.0, 1.0] for text in texts)


class BrokenDenseModel(FakeDenseModel):
    def passage_embed(self, texts):
        return [[1.0, 0.0]]


class EmbeddingBenchmarkTests(unittest.TestCase):
    def test_recall_counts_every_relevant_document(self):
        self.assertEqual(recall_at_k(["a", "b"], ["a", "c", "d"], 3), 0.5)
        self.assertEqual(recall_at_k(["a", "b"], ["a", "b", "d"], 3), 1.0)

    def test_vectorizers_emit_numeric_vectors_with_distinct_families(self):
        encoders = default_vectorizers()
        self.assertEqual(
            [encoder.info.name for encoder in encoders],
            ["word-tfidf", "character-tfidf", "feature-hashing"],
        )
        for encoder in encoders:
            vector = encoder.fit_transform(["semantic vector retrieval"])[0]
            self.assertTrue(vector)
            self.assertTrue(all(isinstance(value, float) for value in vector.values()))
            self.assertEqual(encoder.info.scope, "non-neural")

    def test_benchmark_uses_shared_result_contract(self):
        result = evaluate(
            vectorizers=default_vectorizers(),
            timing_repeat=2,
            warmup_iterations=0,
        )
        self.assertEqual(result["best_recall_at_3"], 1.0)
        self.assertEqual(len(result["models"]), 3)
        self.assertEqual(result["metric"], "best_recall_at_3")
        self.assertEqual(result["value"], result["best_recall_at_3"])
        self.assertEqual(result["unit"], "ratio")
        self.assertEqual(len(result["samples"]), 4)
        self.assertIn("timestamp", result)
        self.assertIn("command", result)
        self.assertFalse(result["scope"]["neural_models_included"])
        self.assertEqual(result["repeat"], 2)
        self.assertEqual(len(result["models"][0]["query_time_samples_ms"]), 2)
        with self.assertRaisesRegex(ValueError, "at least one vectorizer"):
            evaluate(vectorizers=[])

    def test_fastembed_adapter_keeps_provider_outside_metric_core(self):
        adapter = FastEmbedVectorizer(
            "fake/model",
            license_name="test-only",
            model_size_mb=1,
            model_factory=lambda _: FakeDenseModel(),
        )
        corpus = adapter.fit_transform(["semantic retrieval", "other"])
        queries = adapter.transform_many(["semantic query"])
        self.assertEqual(adapter.feature_count, 2)
        self.assertEqual(corpus[0], queries[0])
        self.assertEqual(adapter.info.scope, "neural-local")
        broken = FastEmbedVectorizer(
            "fake/broken",
            license_name="test-only",
            model_size_mb=1,
            model_factory=lambda _: BrokenDenseModel(),
        )
        with self.assertRaisesRegex(ValueError, "wrong corpus count"):
            evaluate(vectorizers=[broken], timing_repeat=1, warmup_iterations=0)
        self.assertEqual(
            [encoder.info.name for encoder in default_dense_vectorizers()],
            [
                "BAAI/bge-small-en-v1.5",
                "sentence-transformers/all-MiniLM-L6-v2",
            ],
        )


if __name__ == "__main__":
    unittest.main()
