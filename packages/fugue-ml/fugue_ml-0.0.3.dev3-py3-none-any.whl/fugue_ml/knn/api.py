from typing import Any, Dict, List, Optional, Union

import fugue.api as fa
from fugue import AnyDataFrame
from triad import assert_or_throw

from fugue_ml.utils.schema import is_vec_col

from .indexer import DistributedKNNIndexer, knn_indexer, KNNIndexer
from .brute_force import BruteForceKNNIndexer


def build_knn_index(
    index: AnyDataFrame,
    vec_col: str = "vector",
    metric: str = "cos",
    partition: Union[str, List[str], None] = None,
    indexer: Any = BruteForceKNNIndexer,
    index_shards: Optional[int] = None,
    index_broadcast_threshold: Any = "100m",
    temp_path: Optional[str] = None,
    worker_nthreads: Optional[int] = None,
    init_kwargs: Optional[Dict[str, Any]] = None,
    build_kwargs: Optional[Dict[str, Any]] = None,
) -> KNNIndexer:
    """Build a KNN indexer.

    :param index: the index dataframe
    :param vec_col: the column name of the vector column
    :param metric: distance metric, default to cos
    :param partition: partition keys, default to None (no hard partitioning)
    :param indexer: indexer name, default to brute_force
    :param index_shards: number of index shards, default to None. For example, if
        index_shards=2, the index will be partitioned into 2 shards. This is to
        improve parallelism for large index.
    :param index_broadcast_threshold: the memory constraint when broadcasting the index,
        default to 100m
    :param temp_path: the temp directory to store intermediate data, default to None
    :param worker_nthreads: number of threads for a worker to use,
        default to None (use all)
    :return: the indexer that is ready to use
    """
    index_schema = fa.get_schema(index)
    assert_or_throw(
        is_vec_col(index_schema, vec_col),
        ValueError(f"{vec_col} is not a vector column in index"),
    )
    if partition is None and index_shards is None:
        idx = knn_indexer(indexer, metric=metric, **(init_kwargs or {}))
    else:
        by = [partition] if isinstance(partition, str) else partition
        idx = DistributedKNNIndexer(
            metric=metric,
            indexer=indexer,
            group_cols=by,
            index_shards=index_shards,
            index_broadcast_threshold=index_broadcast_threshold,
            save_dir=temp_path,
            indexer_init_kwargs=init_kwargs,
        )
    return idx.build(
        index, vec_col=vec_col, worker_nthreads=worker_nthreads, **(build_kwargs or {})
    )


def compute_knn(
    index: AnyDataFrame,
    query: AnyDataFrame,
    k: int = 1,
    vec_col: str = "vector",
    partition: Union[str, List[str], None] = None,
    metric: str = "cos",
    dist_col: Optional[str] = None,
    rank_col: Optional[str] = None,
    drop_vec_col: bool = True,
    indexer: Any = BruteForceKNNIndexer,
    index_shards: Optional[int] = None,
    index_cache_mem_limit: Any = "1g",
    index_broadcast_threshold: Any = "100m",
    build_worker_nthreads: Optional[int] = None,
    query_shards: Optional[int] = None,
    query_preprocess_mode: str = "direct",
    query_chunk_mem_limit: Any = "100m",
    query_chunk_row_limit: int = 0,
    search_worker_nthreads: Optional[int] = None,
    temp_path: Optional[str] = None,
    init_kwargs: Optional[Dict[str, Any]] = None,
    build_kwargs: Optional[Dict[str, Any]] = None,
    search_kwargs: Optional[Dict[str, Any]] = None,
) -> AnyDataFrame:
    """Compute the k nearest neighbors of query in index

    :param index: the index dataframe
    :param query: the query dataframe
    :param k: number of nearest neighbors
    :param vec_col: the column name of the vector column
    :param partition: partition keys, default to None (no hard partitioning)
    :param metric: distance metric, default to cos
    :param dist_col: the column name of the distance column, default to None
        (no distance column)
    :param rank_col: the column name of the rank column, default to None
        (no rank column)
    :param drop_vec_col: whether to drop the vector column in the output,
        default to True
    :param indexer: indexer name, default to brute_force
    :param index_shards: number of index shards, default to None. For example, if
        index_shards=2, the index will be partitioned into 2 shards. This is to
        improve parallelism for large index.
    :param index_cache_mem_limit: the memory constraint on index cache
        in worker memory, default to 1g
    :param index_broadcast_threshold: the memory constraint when broadcasting the index,
        default to 100m
    :param build_worker_nthreads: number of threads for a worker to index a shard,
        default to None (use all)
    :param query_shards: number of query shards, default to None. For example,
        if query_shards=2, there will be 2 identical indexers processing different
        shards of the data. This is to increase parallelism for large query.
    :param query_preprocess_mode: the mode to preprocess query, default to
        ``direct``. If choosing ``file``, partitions of the query will be saved to
        files and ```temp_path`` will be required.
    :param query_chunk_mem_limit: the memory constraint on query chunks,
        default to 100m
    :param query_chunk_row_limit: the row constraint on query chunks,
        default to 0 (no row constraint)
    :param search_worker_nthreads: number of threads for a worker to process a chunk
        of query, default to None (use all)
    :param temp_path: the temp directory to store intermediate data, default to None
    :return: the index dataframe with search results from index
    """
    query_schema = fa.get_schema(query)
    assert_or_throw(
        is_vec_col(query_schema, vec_col),
        ValueError(f"{vec_col} is not a vector column in query"),
    )

    idx = build_knn_index(
        index=index,
        vec_col=vec_col,
        metric=metric,
        partition=partition,
        indexer=indexer,
        index_shards=index_shards,
        index_broadcast_threshold=index_broadcast_threshold,
        temp_path=temp_path,
        worker_nthreads=build_worker_nthreads,
        init_kwargs=init_kwargs,
        build_kwargs=build_kwargs,
    )

    return idx.search(
        query,
        k=k,
        vec_col=vec_col,
        dist_col=dist_col,
        rank_col=rank_col,
        query_shards=query_shards,
        index_cache_mem_limit=index_cache_mem_limit,
        index_broadcast_threshold=index_broadcast_threshold,
        query_preprocess_mode=query_preprocess_mode,
        query_chunk_mem_limit=query_chunk_mem_limit,
        query_chunk_row_limit=query_chunk_row_limit,
        drop_vec_col=drop_vec_col,
        temp_path=temp_path,
        worker_nthreads=search_worker_nthreads,
        **(search_kwargs or {}),
    )
