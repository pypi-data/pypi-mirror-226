from typing import Any, List
from unittest import TestCase

import fugue.api as fa
import numpy as np
import pandas as pd
import pytest

from fugue_ml.knn import KNNIndexer, build_knn_index


def l2(a: np.array, b: np.array) -> float:
    return np.linalg.norm(np.subtract(a, b), 2)


def cos_sim(a: np.array, b: np.array) -> float:
    return 1 - np.dot(a, b) / (np.linalg.norm(a, 2) * np.linalg.norm(b, 2))


class LocalKNNIndexerTests(object):
    class Tests(TestCase):
        @classmethod
        def setUpClass(cls):
            pass

        @classmethod
        def tearDownClass(cls):
            pass

        @pytest.fixture(autouse=True)
        def init_fixtures(self, tmpdir, spark_session):
            self.tmpdir = tmpdir
            self.spark_session = spark_session
            self.index_df = self.create_index_df()

        @property
        def supported_metrics(self) -> List[str]:
            return ["cos", "l2", "dot"]

        @property
        def primary_indexer(self) -> Any:
            raise NotImplementedError  # pragma: no cover

        def create_index_df(self) -> pd.DataFrame:
            arr1 = np.array([[1, 2], [3, 4]])
            arr2 = arr1 + 0.1
            arr = np.concatenate([arr1, arr2], axis=0)
            return pd.DataFrame(
                dict(idx=range(len(arr)), gp=[10, 10, 12, 10], vec_x=list(arr))
            )

        def create_indexer(self, metric: str, **kwargs: Any) -> KNNIndexer:
            idx = build_knn_index(
                index=self.index_df,
                indexer=self.primary_indexer,
                metric=metric,
                vec_col="vec_x",
                **kwargs
            )
            idx.save(self.tmpdir.join("idx1.bin"))
            idx = KNNIndexer.load(str(self.tmpdir.join("idx1.bin")))
            assert idx.get_dim() == 2
            return idx

        def test_simple_search(self):

            query = pd.DataFrame(dict(q=[1], vec=[[1.1, 2.1]]))

            if "cos" in self.supported_metrics:
                idx_cos = self.create_indexer("cos")

                with pytest.raises(KeyError):
                    idx_cos.search(query, 1, vec_col="vec1")

                with pytest.raises(ValueError):
                    idx_cos.search(query, 1, vec_col="idx")

                result = fa.as_pandas(
                    idx_cos.search(
                        query, 1, vec_col="vec", dist_col="dist", rank_col="rank"
                    )
                )
                assert np.allclose(result.values.tolist(), [[1, 2, 12, 0, 0]])

                result = fa.as_pandas(
                    idx_cos.search(
                        query, 2, vec_col="vec", dist_col="dist", rank_col="rank"
                    )
                )
                assert np.allclose(
                    result.values.tolist(),
                    [
                        [1, 2, 12, 0, 0],
                        [1, 0, 10, cos_sim([1, 2], [1.1, 2.1]), 1],
                    ],
                )

            if "l2" in self.supported_metrics:
                idx_l2 = self.create_indexer("l2")
                result = fa.as_pandas(
                    idx_l2.search(
                        query, 2, vec_col="vec", dist_col="dist", rank_col="rank"
                    )
                )
                assert np.allclose(
                    result.values.tolist(),
                    [
                        [1, 2, 12, 0, 0],
                        [1, 0, 10, l2([1, 2], [1.1, 2.1]), 1],
                    ],
                )

                result = fa.as_pandas(
                    idx_l2.search(
                        query, 4, vec_col="vec", dist_col="dist", rank_col="rank"
                    )
                )
                assert np.allclose(
                    result.values.tolist(),
                    [
                        [1, 2, 12, 0, 0],
                        [1, 0, 10, l2([1, 2], [1.1, 2.1]), 1],
                        [1, 1, 10, l2([3, 4], [1.1, 2.1]), 2],
                        [1, 3, 10, l2([3.1, 4.1], [1.1, 2.1]), 3],
                    ],
                )

        def test_sharded_search(self):
            query = pd.DataFrame(dict(q=[1, 2, 3], vec=[[1.1, 2.1], [3, 4], [10, 10]]))

            for engine in ["pandas", self.spark_session]:
                with fa.engine_context(engine):
                    idx_cos = self.create_indexer("cos", index_shards=3)
                    result = fa.as_pandas(
                        idx_cos.search(
                            query, 1, vec_col="vec", dist_col="dist", rank_col="rank"
                        )
                    ).sort_values("q")
                    assert np.allclose(
                        result.values.tolist(),
                        [
                            [1, 2, 12, 0, 0],
                            [2, 1, 10, 0, 0],
                            [3, 3, 10, cos_sim([10, 10], [3.1, 4.1]), 0],
                        ],
                    )

                    for query_shards in [None, 7]:
                        result = fa.as_pandas(
                            idx_cos.search(
                                query,
                                2,
                                vec_col="vec",
                                dist_col="dist",
                                rank_col="rank",
                                query_shards=query_shards,
                            )
                        ).sort_values(["rank", "q"])
                        assert np.allclose(
                            result.values.tolist(),
                            [
                                [1, 2, 12, 0, 0],
                                [2, 1, 10, 0, 0],
                                [3, 3, 10, cos_sim([10, 10], [3.1, 4.1]), 0],
                                [1, 0, 10, cos_sim([1.1, 2.1], [1, 2]), 1],
                                [2, 3, 10, cos_sim([3, 4], [3.1, 4.1]), 1],
                                [3, 1, 10, cos_sim([10, 10], [3, 4]), 1],
                            ],
                        )

        def test_partitioned_search(self):
            query = pd.DataFrame(
                dict(gp=[10, 10, 12], q=[1, 2, 3], vec=[[1.1, 2.1], [3, 4], [10, 10]])
            )

            for engine in ["pandas", self.spark_session]:
                with fa.engine_context(engine):
                    idx_cos = self.create_indexer("cos", index_shards=3, partition="gp")
                    result = fa.as_pandas(
                        idx_cos.search(
                            query, 1, vec_col="vec", dist_col="dist", rank_col="rank"
                        )
                    ).sort_values("q")
                    assert np.allclose(
                        result.values.tolist(),
                        [
                            [10, 1, 0, cos_sim([1.1, 2.1], [1, 2]), 0],
                            [10, 2, 1, 0, 0],
                            [12, 3, 2, cos_sim([10, 10], [1.1, 2.1]), 0],
                        ],
                    )

                    for query_shards in [None, 7]:
                        result = fa.as_pandas(
                            idx_cos.search(
                                query,
                                2,
                                vec_col="vec",
                                dist_col="dist",
                                rank_col="rank",
                                query_shards=query_shards,
                            )
                        ).sort_values(["rank", "q"])
                        assert np.allclose(
                            result.values.tolist(),
                            [
                                [10, 1, 0, cos_sim([1.1, 2.1], [1, 2]), 0],
                                [10, 2, 1, 0, 0],
                                [12, 3, 2, cos_sim([10, 10], [1.1, 2.1]), 0],
                                [10, 1, 1, cos_sim([1.1, 2.1], [3, 4]), 1],
                                [10, 2, 3, cos_sim([3, 4], [3.1, 4.1]), 1],
                            ],
                        )
