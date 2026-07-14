import unittest
from embeddings_benchmark.cli import evaluate

class EmbeddingBenchmarkTests(unittest.TestCase):
    def test_benchmark_reaches_expected_recall(self):
        result = evaluate()
        self.assertGreaterEqual(result["best_recall_at_3"], 1.0)
        self.assertEqual(len(result["models"]), 3)

if __name__ == "__main__":
    unittest.main()
