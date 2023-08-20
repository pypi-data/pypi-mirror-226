import fugue.api as fa
import numpy as np
import pandas as pd
from pytest import fixture
from distributed import Client
from fugue_ml.api import compute_knn
from fugue_ml.utils.numpy.distance import knn as np_knn
import ray
import pytest


@fixture
def big_index_df():
    np.random.seed(0)
    arr = np.random.rand(1000, 16)
    return pd.DataFrame(
        dict(
            aid=range(len(arr)),
            gp=np.random.randint(0, 8, size=len(arr)),
            vec=list(arr),
        )
    )


@fixture
def big_query():
    np.random.seed(1)
    arr = np.random.rand(800, 16)
    return pd.DataFrame(
        dict(
            qid=range(len(arr)),
            gp=np.random.randint(0, 8, size=len(arr)),
            vec=list(arr),
        )
    )


@fixture
def big_search_result(big_index_df, big_query):
    test_k = 3
    idx, dist = np_knn(
        index=np.array(list(big_index_df.vec)),
        query=np.array(list(big_query.vec)),
        k=test_k,
        metric="cos",
        sort_output=True,
    )
    dfs = []
    for i in range(test_k):
        dfs.append(
            pd.DataFrame(
                dict(qid=range(idx.shape[0]), aid=idx[:, i], dist=dist[:, i], rank=i)
            )
        )
    return pd.concat(dfs).sort_values(["qid", "dist"]).reset_index(drop=True)


@fixture
def big_grouped_search_result(big_index_df, big_query):
    test_k = 3
    dfs = []
    for gp in range(8):
        idx_df = big_index_df[big_index_df.gp == gp].reset_index(drop=True)
        q_df = big_query[big_query.gp == gp].reset_index(drop=True)
        idx, dist = np_knn(
            index=np.array(list(idx_df.vec)),
            query=np.array(list(q_df.vec)),
            k=test_k,
            metric="cos",
            sort_output=True,
        )
        for i in range(test_k):
            dfs.append(
                pd.DataFrame(
                    dict(
                        qid=q_df.qid,
                        gp=gp,
                        aid=idx_df.aid.iloc[idx[:, i]].reset_index(drop=True),
                        dist=dist[:, i],
                        rank=i,
                    )
                )
            )
    return pd.concat(dfs).sort_values(["qid", "dist"]).reset_index(drop=True)


def test_knn_local(
    big_index_df, big_query, big_search_result, big_grouped_search_result, tmpdir
):
    with fa.engine_context("pandas"):
        _run_tests(
            big_index_df,
            big_query,
            big_search_result,
            big_grouped_search_result,
            tmpdir=tmpdir,
        )


def _test_knn_spark(
    big_index_df,
    big_query,
    big_search_result,
    big_grouped_search_result,
    spark_session,
    tmpdir,
):
    with fa.engine_context(spark_session):
        _run_tests(
            big_index_df,
            big_query,
            big_search_result,
            big_grouped_search_result,
            tmpdir=tmpdir,
        )


def _test_knn_dask(
    big_index_df, big_query, big_search_result, big_grouped_search_result, tmpdir
):
    with Client(processes=True) as client:
        with fa.engine_context(client):
            _run_tests(
                big_index_df,
                big_query,
                big_search_result,
                big_grouped_search_result,
                tmpdir=tmpdir,
            )


def _test_knn_ray(
    big_index_df, big_query, big_search_result, big_grouped_search_result, tmpdir
):
    with ray.init():
        with fa.engine_context("ray"):
            _run_tests(
                big_index_df,
                big_query,
                big_search_result,
                big_grouped_search_result,
                tmpdir=tmpdir,
            )


@pytest.mark.parametrize(
    "backend", ["spark_session", "fugue_dask_client", "fugue_ray_session"]
)
def test_knn(
    backend,
    request,
    big_index_df,
    big_query,
    big_search_result,
    big_grouped_search_result,
    tmpdir,
):
    with fa.engine_context(request.getfixturevalue(backend)):
        _run_tests(
            big_index_df,
            big_query,
            big_search_result,
            big_grouped_search_result,
            tmpdir=tmpdir,
        )


def _run_tests(
    big_index_df, big_query, big_search_result, big_grouped_search_result, tmpdir
):
    # no shard, no partition
    assert_eq(
        big_search_result,
        index=big_index_df.drop(columns=["gp"]),
        query=big_query.drop(columns=["gp"]),
        k=3,
        vec_col="vec",
        metric="cos",
        dist_col="dist",
        rank_col="rank",
        build_worker_nthreads=1,
        search_worker_nthreads=1,
    )

    # no partition, with shard
    assert_eq(
        big_search_result,
        index=big_index_df.drop(columns=["gp"]),
        query=big_query.drop(columns=["gp"]),
        k=3,
        vec_col="vec",
        metric="cos",
        dist_col="dist",
        rank_col="rank",
        index_shards=5,
        build_worker_nthreads=1,
        search_worker_nthreads=1,
    )

    assert_eq(
        big_search_result,
        index=big_index_df.drop(columns=["gp"]),
        query=big_query.drop(columns=["gp"]),
        k=3,
        vec_col="vec",
        metric="cos",
        dist_col="dist",
        rank_col="rank",
        index_shards=5,
        query_preprocess_mode="file",
        temp_path=str(tmpdir),
        build_worker_nthreads=1,
        search_worker_nthreads=1,
    )

    # partition, no shard
    assert_eq(
        big_grouped_search_result,
        index=big_index_df,
        query=big_query,
        partition="gp",
        k=3,
        vec_col="vec",
        metric="cos",
        dist_col="dist",
        rank_col="rank",
        build_worker_nthreads=1,
        search_worker_nthreads=1,
    )

    assert_eq(
        big_grouped_search_result,
        index=big_index_df,
        query=big_query,
        partition="gp",
        k=3,
        vec_col="vec",
        metric="cos",
        dist_col="dist",
        rank_col="rank",
        query_preprocess_mode="file",
        temp_path=str(tmpdir),
        build_worker_nthreads=1,
        search_worker_nthreads=1,
    )

    # shard and partition
    assert_eq(
        big_grouped_search_result,
        index=big_index_df,
        query=big_query,
        partition="gp",
        k=3,
        vec_col="vec",
        metric="cos",
        dist_col="dist",
        rank_col="rank",
        index_shards=5,
        query_shards=7,
        build_worker_nthreads=1,
        search_worker_nthreads=1,
    )

    assert_eq(
        big_grouped_search_result,
        index=big_index_df,
        query=big_query,
        partition="gp",
        k=3,
        vec_col="vec",
        metric="cos",
        dist_col="dist",
        rank_col="rank",
        index_shards=5,
        query_shards=7,
        query_preprocess_mode="file",
        temp_path=str(tmpdir),
        build_worker_nthreads=1,
        search_worker_nthreads=1,
    )


def assert_eq(df, **kwargs):
    res = (
        fa.as_pandas(compute_knn(**kwargs))
        .sort_values(["qid", "dist"])
        .reset_index(drop=True)
    )
    pd.testing.assert_frame_equal(res, df, check_dtype=False)
