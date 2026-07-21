import unittest

from embeddings_benchmark.benchmark import evaluate, recall_at_k
from embeddings_benchmark.vectorizers import default_vectorizers


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
        result = evaluate()
        self.assertGreaterEqual(result["best_recall_at_3"], 0.75)
        self.assertEqual(len(result["models"]), 3)
        self.assertEqual(result["metric"], "best_recall_at_3")
        self.assertEqual(result["value"], result["best_recall_at_3"])
        self.assertEqual(result["unit"], "ratio")
        self.assertEqual(len(result["samples"]), 4)
        self.assertIn("timestamp", result)
        self.assertIn("command", result)
        self.assertFalse(result["scope"]["neural_models_included"])


if __name__ == "__main__":
    unittest.main()
