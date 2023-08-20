import pickle

import cloudpickle
import fugue.api as fa
import numpy as np
import pandas as pd
from pytest import fixture, raises

from fugue_ml.knn import (
    BruteForceKNNIndexer,
    DistributedKNNIndexer,
    KNNIndexer,
    knn_indexer,
)
from fugue_ml.knn.indexer import (
    _INDEXER_SHARD_COLUMN_NAME,
    _QUERY_BLOB_COLUMN_NAME,
    _QUERY_SHARDS_COLUMN_NAME,
    _cache_query_to_file,
    _KNNIndexerLoader,
    _process_query_directly,
)


@fixture
def index_df():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = arr1 + 0.001
    arr = np.concatenate([arr1, arr2], axis=0)
    return pd.DataFrame(dict(idx=range(len(arr)), dummy=10, vec_x=list(arr)))


@fixture
def index_gp_df(index_df):
    return index_df.assign(gp=[0, 0, 1, 1])


@fixture
def indexer(index_df, tmpdir):
    bi = BruteForceKNNIndexer(metric="cos").build(index_df, vec_col="vec_x")
    path = str(tmpdir.join("index.bin"))
    bi.save(path)
    return KNNIndexer.load(path)


@fixture
def sharded_indexer(index_df, tmpdir):
    bi = DistributedKNNIndexer(
        metric="cos",
        indexer="brute_force",
        index_shards=2,
        save_dir=str(tmpdir),
    ).build(index_df, vec_col="vec_x")
    path = str(tmpdir.join("s_index.bin"))
    bi.save(path)
    return KNNIndexer.load(path)


@fixture
def gp_indexer(index_gp_df, tmpdir):
    bi = DistributedKNNIndexer(
        metric="cos",
        indexer="brute_force",
        group_cols=["gp"],
        index_shards=2,
        save_dir=str(tmpdir),
    ).build(index_gp_df, vec_col="vec_x")
    path = str(tmpdir.join("gp_index.bin"))
    bi.save(path)
    return KNNIndexer.load(path)


@fixture
def query():
    arr1 = np.array([[1, 2], [3, 4]])
    arr3 = arr1 - 0.001
    arr = np.concatenate([arr1, arr3], axis=0)
    return pd.DataFrame(dict(q=range(len(arr)), vec=list(arr)))


@fixture
def gp_query(query):
    return query.assign(gp=[0, 0, 1, 1])


def test_init_indexer():
    assert isinstance(knn_indexer("brute_force", metric="l2"), BruteForceKNNIndexer)
    bi = knn_indexer(BruteForceKNNIndexer, metric="cos")
    assert isinstance(bi, BruteForceKNNIndexer)
    assert knn_indexer(bi, metric="l2") is bi
    assert bi.metric == "cos"

    with raises(ValueError):
        knn_indexer(1)


def test_indexer(indexer, query):
    with raises(KeyError):
        indexer.search(query, 1, vec_col="vec1")

    with raises(ValueError):
        indexer.search(query, 1, vec_col="idx")

    res = fa.as_pandas(indexer.search(query, 1, vec_col="vec"))
    actual = set(tuple(x) for x in res[["q", "idx", "dummy"]].values.tolist())
    assert actual == {(0, 0, 10), (1, 1, 10), (2, 0, 10), (3, 1, 10)}

    res = fa.as_pandas(indexer.search(query, 1, vec_col="vec", dist_col="dist"))
    actual = set(
        tuple(int(xx) for xx in x)
        for x in res[["q", "idx", "dummy", "dist"]].values.tolist()
    )
    assert actual == {(0, 0, 10, 0), (1, 1, 10, 0), (2, 0, 10, 0), (3, 1, 10, 0)}

    res = fa.as_pandas(indexer.search(query, 2, vec_col="vec", rank_col="rank"))
    actual = set(tuple(x) for x in res[["q", "idx", "dummy", "rank"]].values.tolist())
    assert actual == {
        (0, 0, 10, 0),
        (1, 1, 10, 0),
        (2, 0, 10, 0),
        (3, 1, 10, 0),
        (0, 2, 10, 1),
        (1, 3, 10, 1),
        (2, 2, 10, 1),
        (3, 3, 10, 1),
    }


def test_sharded_indexer(sharded_indexer, query):
    res = fa.as_pandas(sharded_indexer.search(query, 1, vec_col="vec"))
    actual = set(tuple(x) for x in res[["q", "idx", "dummy"]].values.tolist())
    assert actual == {(0, 0, 10), (1, 1, 10), (2, 0, 10), (3, 1, 10)}

    res = fa.as_pandas(
        sharded_indexer.search(
            query, 1, vec_col="vec", dist_col="dist", query_shards=3
        )
    )
    actual = set(
        tuple(int(xx) for xx in x)
        for x in res[["q", "idx", "dummy", "dist"]].values.tolist()
    )
    assert actual == {(0, 0, 10, 0), (1, 1, 10, 0), (2, 0, 10, 0), (3, 1, 10, 0)}


def test_gp_indexer(gp_indexer: KNNIndexer, gp_query, tmpdir):
    res = fa.as_pandas(gp_indexer.search(gp_query, 1, vec_col="vec"))
    actual = sorted(res[["gp", "q", "idx", "dummy"]].values.tolist())
    assert actual == [[0, 0, 0, 10], [0, 1, 1, 10], [1, 2, 2, 10], [1, 3, 3, 10]]

    res = fa.as_pandas(
        gp_indexer.search(gp_query, 1, vec_col="vec", query_shards=3)
    )
    actual = sorted(res[["gp", "q", "idx", "dummy"]].values.tolist())
    assert actual == [[0, 0, 0, 10], [0, 1, 1, 10], [1, 2, 2, 10], [1, 3, 3, 10]]

    res = fa.as_pandas(
        gp_indexer.search(
            gp_query,
            1,
            vec_col="vec",
            query_shards=3,
            query_preprocess_mode="file",
            temp_path=str(tmpdir),
        )
    )
    actual = sorted(res[["gp", "q", "idx", "dummy"]].values.tolist())
    assert actual == [[0, 0, 0, 10], [0, 1, 1, 10], [1, 2, 2, 10], [1, 3, 3, 10]]


def test_sharding_indexer(index_df, query, tmpdir):
    idf = index_df.assign(g=[0, 0, 1, 1])
    gp = DistributedKNNIndexer(
        metric="cos", indexer=BruteForceKNNIndexer, index_shards=5
    )

    gp = pickle.loads(pickle.dumps(gp))

    gp.build(idf, vec_col="vec_x")

    path = str(tmpdir.join("index.bin"))
    gp.save(path)
    gp = KNNIndexer.load(path)

    res = fa.as_pandas(gp.search(query, 1, vec_col="vec"))
    actual = set(tuple(x) for x in res[["q", "idx", "dummy", "g"]].values.tolist())
    assert actual == {
        (0, 0, 10, 0),
        (1, 1, 10, 0),
        (2, 0, 10, 0),
        (3, 1, 10, 0),
    }

    res = fa.as_pandas(gp.search(query, 1, vec_col="vec", query_shards=5))
    actual = set(tuple(x) for x in res[["q", "idx", "dummy", "g"]].values.tolist())
    assert actual == {
        (0, 0, 10, 0),
        (1, 1, 10, 0),
        (2, 0, 10, 0),
        (3, 1, 10, 0),
    }


def test_key_grouped_indexer(index_df, query, tmpdir):
    idf = index_df.assign(g=[0, 0, 1, 1])
    qdf = pd.concat([query] * 2).assign(g=[1, 1, 1, 2, 0, 2, 2, 2], q=range(8))
    gp = DistributedKNNIndexer(
        metric="cos", indexer=BruteForceKNNIndexer, group_cols=["g"]
    )

    gp = pickle.loads(pickle.dumps(gp))

    gp.build(idf, vec_col="vec_x")

    path = str(tmpdir.join("index.bin"))
    gp.save(path)
    gp = KNNIndexer.load(path)
    res = fa.as_pandas(gp.search(qdf, 2, vec_col="vec", rank_col="rank"))
    actual = set(
        tuple(x) for x in res[["q", "g", "idx", "dummy", "rank"]].values.tolist()
    )
    assert actual == {
        (4, 0, 0, 10, 0),
        (4, 0, 1, 10, 1),
        (0, 1, 2, 10, 0),
        (1, 1, 3, 10, 0),
        (2, 1, 2, 10, 0),
        (0, 1, 3, 10, 1),
        (1, 1, 2, 10, 1),
        (2, 1, 3, 10, 1),
    }

    res = fa.as_pandas(
        gp.search(qdf, 2, vec_col="vec", rank_col="rank", query_shards=5)
    )
    actual = set(
        tuple(x) for x in res[["q", "g", "idx", "dummy", "rank"]].values.tolist()
    )
    assert actual == {
        (4, 0, 0, 10, 0),
        (4, 0, 1, 10, 1),
        (0, 1, 2, 10, 0),
        (1, 1, 3, 10, 0),
        (2, 1, 2, 10, 0),
        (0, 1, 3, 10, 1),
        (1, 1, 2, 10, 1),
        (2, 1, 3, 10, 1),
    }


def test_key_grouped_sharding_indexer(index_df, query, tmpdir):
    idf = index_df.assign(g=[0, 0, 1, 1])
    qdf = pd.concat([query] * 2).assign(g=[1, 1, 1, 2, 0, 2, 2, 2], q=range(8))
    gp = DistributedKNNIndexer(
        metric="cos", indexer=BruteForceKNNIndexer, group_cols=["g"], index_shards=5
    )

    gp = pickle.loads(pickle.dumps(gp))

    gp.build(idf, vec_col="vec_x")

    path = str(tmpdir.join("index.bin"))
    gp.save(path)
    gp = KNNIndexer.load(path)

    res = fa.as_pandas(gp.search(qdf, 1, vec_col="vec", query_shards=5))
    actual = set(tuple(x) for x in res[["q", "g", "idx", "dummy"]].values.tolist())
    assert actual == {
        (4, 0, 0, 10),
        (0, 1, 2, 10),
        (1, 1, 3, 10),
        (2, 1, 2, 10),
    }

    res = fa.as_pandas(
        gp.search(qdf, 1, vec_col="vec", dist_col="dist", query_shards=5)
    )
    assert "dist" in res.columns
    actual = set(tuple(x) for x in res[["q", "g", "idx", "dummy"]].values.tolist())
    assert actual == {
        (4, 0, 0, 10),
        (0, 1, 2, 10),
        (1, 1, 3, 10),
        (2, 1, 2, 10),
    }


def test_indexer_loader():
    class _Loader(_KNNIndexerLoader):
        def _load(self, path):
            return path.split("-")[0], int(path.split("-")[1])

    def assert_eq(seq, cache_size, remain):
        loader = _Loader()
        for s in seq:
            assert s.split("-")[0] == loader.load(s, cache_size=cache_size)
        assert loader.get_cache_items() == remain
        nl = cloudpickle.loads(cloudpickle.dumps(loader))
        assert nl.get_cache_items() == []

    assert_eq(["a-1", "b-2", "c-3", "d-4"], 0, [])
    assert_eq(["a-1", "b-1", "c-1", "d-1"], 2, ["d", "c"])
    assert_eq(["a-1", "b-1", "c-1", "d-1"], 4, ["d", "c", "b", "a"])

    assert_eq(["a-1", "b-1"], 1, ["b"])
    assert_eq(["a-1", "b-2"], 2, ["b"])
    assert_eq(["a-2", "b-1"], 2, ["b"])
    assert_eq(["a-1", "b-3"], 2, ["a"])  # if too large will not check cache

    assert_eq(["a-1", "b-1", "a-1", "a-1"], 2, ["a", "b"])
    assert_eq(["a-1", "b-1", "a-1", "a-1", "c-2"], 2, ["a"])


def test_process_query_directly(tmpdir):
    q = pd.DataFrame(dict(qid=[1, 2, 3], qs=["q1", "q2", "q3"], gp=["g1", "g2", "g1"]))
    res = _process_query_directly(
        q, index_shards=np.array([2, 5]), query_shards=3, vec_col="qs"
    )
    assert sorted(res[_INDEXER_SHARD_COLUMN_NAME].unique().tolist()) == [2, 5]
    # one index shard should access the whole query
    df = res[res[_INDEXER_SHARD_COLUMN_NAME] == 2][q.columns]
    assert sorted(df.values.tolist()) == sorted(q.values.tolist())


def test_cache_query_to_file(tmpdir):
    q = pd.DataFrame(dict(qid=[1, 2, 3], qs=["q1", "q2", "q3"], gp=["g1", "g2", "g1"]))
    res = _cache_query_to_file(
        q,
        index_shards=np.array([2, 5]),
        query_shards=3,
        group_cols=[],
        temp_path=str(tmpdir),
    )
    assert sorted(
        res[[_QUERY_SHARDS_COLUMN_NAME, _INDEXER_SHARD_COLUMN_NAME]].values.tolist()
    ) == [[0, 2], [0, 5], [1, 2], [1, 5], [2, 2], [2, 5]]
    # one index shard should access the whole query
    df = pd.concat(
        pd.read_parquet(f)
        for f in res[res[_INDEXER_SHARD_COLUMN_NAME] == 2][_QUERY_BLOB_COLUMN_NAME]
    )
    assert sorted(df.values.tolist()) == sorted(q.values.tolist())

    res = _cache_query_to_file(
        q,
        index_shards=np.array([2, 5]),
        query_shards=3,
        group_cols=["gp"],
        temp_path=str(tmpdir),
    )
    assert sorted(
        res[
            [_QUERY_SHARDS_COLUMN_NAME, _INDEXER_SHARD_COLUMN_NAME, "gp"]
        ].values.tolist()
    ) == [
        [0, 2, "g1"],
        [0, 2, "g2"],
        [0, 5, "g1"],
        [0, 5, "g2"],
        [1, 2, "g1"],
        [1, 5, "g1"],
    ]
    # one index shard should access the whole query
    df = pd.concat(
        pd.read_parquet(f)
        for f in res[res[_INDEXER_SHARD_COLUMN_NAME] == 2][_QUERY_BLOB_COLUMN_NAME]
    )
    assert sorted(df.values.tolist()) == sorted(q.values.tolist())
