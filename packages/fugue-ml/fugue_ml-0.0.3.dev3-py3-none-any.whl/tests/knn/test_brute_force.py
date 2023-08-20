from fugue_ml.testing.knn.local_indexer_suite import LocalKNNIndexerTests


class BruteForceKNNIndexerTests(LocalKNNIndexerTests.Tests):
    @property
    def primary_indexer(self):
        return "brute_force"
