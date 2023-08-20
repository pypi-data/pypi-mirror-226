from fugue_ml.testing.knn.local_indexer_suite import LocalKNNIndexerTests


class HnswlibKNNIndexerTests(LocalKNNIndexerTests.Tests):
    @property
    def primary_indexer(self):
        return "hnswlib"
