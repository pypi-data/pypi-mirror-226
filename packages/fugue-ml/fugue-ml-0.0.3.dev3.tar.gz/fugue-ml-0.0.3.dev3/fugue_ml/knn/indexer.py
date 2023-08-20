import os
import pickle
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type, Union
from uuid import uuid4

import fsspec
import fugue.api as fa
import numpy as np
import pandas as pd
import threadpoolctl
from fugue import AnyDataFrame, DataFrame
from triad import Schema, assert_or_throw
from triad.utils.batch_reslicers import PandasBatchReslicer
from triad.utils.convert import to_size
from triad.utils.threading import SerializableRLock

from fugue_ml.utils.fugue_ext import deterministic_shard
from fugue_ml.utils.io import unzip_to_temp, zip_temp
from fugue_ml.utils.registry import fugue_ml_plugin
from fugue_ml.utils.schema import is_vec_col

_COLUMN_PREFIX = "_fugue_ml_knn"
_INDEXERS: Dict[str, Type["KNNIndexer"]] = {}
_INDEXER_ATTR = "_indexer_name"
_INDEXER_BLOB_COLUMN_NAME = _COLUMN_PREFIX + "_indexer_blob"
_INDEXER_METADATA_BLOB_COLUMN_NAME = _COLUMN_PREFIX + "_indexer_metadata_blob"
_INDEXER_SHARD_COLUMN_NAME = _COLUMN_PREFIX + "_indexer_shard"
_QUERY_SHARDS_COLUMN_NAME = _COLUMN_PREFIX + "_query_shard"
_QUERY_BLOB_COLUMN_NAME = _COLUMN_PREFIX + "_query_blob"
_QUERY_DEDUP_COLUMN_NAME = _COLUMN_PREFIX + "_query_dedup"
_TEMP_DIST_COL = _COLUMN_PREFIX + "_temp_dist"


def register_knn_indexer(name: str) -> Callable:
    def deco(cls: Type) -> Type:
        assert_or_throw(
            issubclass(cls, KNNIndexer),
            TypeError(f"{cls} is not a subtype of KNNIndexer"),
        )
        assert_or_throw(
            name not in _INDEXERS,
            ValueError(
                f"{name}:{_INDEXERS.get(name, None)} "
                "is already registered as a KNNIndexer"
            ),
        )
        setattr(cls, _INDEXER_ATTR, name)
        _INDEXERS[name] = cls
        return cls

    return deco


@fugue_ml_plugin
def knn_indexer(indexer: Any, **kwargs: Any) -> "KNNIndexer":
    if isinstance(indexer, str):
        # knn_indexer as plugin has loaded all entry points
        return _INDEXERS[indexer](**kwargs)
    elif isinstance(indexer, KNNIndexer):
        return indexer
    elif isinstance(indexer, type) and issubclass(indexer, KNNIndexer):
        return indexer(**kwargs)
    else:
        raise ValueError(f"{indexer} is not a valid KNNIndexer")


class KNNIndexer(ABC):
    def __init__(self, metric: str):
        self.metric = metric

    @abstractmethod  # pragma: no cover
    def build(
        self,
        index: AnyDataFrame,
        vec_col: str,
        worker_nthreads: Optional[int] = None,
        **kwargs: Any,
    ) -> "KNNIndexer":
        raise NotImplementedError

    @abstractmethod  # pragma: no cover
    def search_local(
        self,
        query: np.ndarray,
        k: int,
        sort_output: bool,
        worker_nthreads: Optional[int],
        **kwargs: Any,
    ) -> Tuple[np.ndarray, np.ndarray]:
        raise NotImplementedError

    @abstractmethod  # pragma: no cover
    def can_broadcast(self, size_limit: int) -> bool:
        raise NotImplementedError

    @abstractmethod  # pragma: no cover
    def get_metadata_df(self) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod  # pragma: no cover
    def get_metadata_schema(self) -> Schema:
        raise NotImplementedError

    @abstractmethod  # pragma: no cover
    def get_dim(self) -> int:
        raise NotImplementedError

    def save(self, path: str) -> None:
        with zip_temp(path) as tmpdir:
            fs, path = fsspec.core.url_to_fs(tmpdir)
            fs.write_bytes(
                os.path.join(path, "indexer_type.bin"), pickle.dumps(self.__class__)
            )
            params = dict(self.__dict__)
            self.save_special_params(params, tmpdir)
            fs.write_bytes(os.path.join(path, "params.bin"), pickle.dumps(params))

    @staticmethod
    def load(path: str, cache_size: Any = None) -> "KNNIndexer":
        return _INDEXER_LOADER.load(path, cache_size=cache_size)

    def save_special_params(self, data: Dict[str, Any], folder: str) -> None:
        return

    def load_special_params(self, folder: str) -> Dict[str, Any]:
        return {}

    def search(
        self,
        query: AnyDataFrame,
        k: int,
        vec_col: str,
        dist_col: Optional[str] = None,
        rank_col: Optional[str] = None,
        drop_vec_col: bool = True,
        index_cache_mem_limit: Any = "1g",
        index_broadcast_threshold: Any = "500m",
        query_shards: Optional[int] = None,
        query_preprocess_mode: str = "direct",
        query_chunk_mem_limit: Any = "100m",
        query_chunk_row_limit: int = 0,
        temp_path: Optional[str] = None,
        worker_nthreads: Optional[int] = None,
        **kwargs: Any,
    ) -> AnyDataFrame:
        output_schema = self._construct_schema(
            fa.get_schema(query),
            vec_col=vec_col,
            dist_col=dist_col,
            rank_col=rank_col,
            drop_vec_col=drop_vec_col,
        )
        indexer_ser = _KNNIndexerSerializer(
            self, to_size(index_broadcast_threshold), temp_path
        )

        def _wrapper(dfs: Iterable[pd.DataFrame]) -> Iterable[pd.DataFrame]:
            indexer = indexer_ser.get_instance(cache_size=index_cache_mem_limit)
            reslicer = PandasBatchReslicer(
                row_limit=query_chunk_row_limit, size_limit=query_chunk_mem_limit
            )
            for df in reslicer.reslice(dfs):
                for res in _search_pd_df(
                    indexer=indexer,
                    df=df,
                    k=k,
                    vec_col=vec_col,
                    dist_col=dist_col,
                    rank_col=rank_col,
                    drop_vec_col=drop_vec_col,
                    sort_output=rank_col is not None,
                    worker_nthreads=worker_nthreads,
                    **kwargs,
                ):
                    yield res[output_schema.names]

        return fa.transform(
            query, _wrapper, schema=output_schema, partition=query_shards
        )

    def get_np_arr(self, df: pd.DataFrame, vec_col: str) -> np.array:
        return np.array(list(df[vec_col]))

    def _construct_schema(
        self,
        schema: Schema,
        vec_col: str,
        dist_col: Optional[str],
        rank_col: Optional[str],
        drop_vec_col: bool,
    ) -> Schema:
        schema = schema + self.get_metadata_schema()
        assert_or_throw(
            is_vec_col(schema, vec_col), ValueError(f"{vec_col} is not a vector column")
        )
        if dist_col is not None:
            schema = schema + (dist_col, float)
        if rank_col is not None:
            schema = schema + (rank_col, int)
        if drop_vec_col:
            schema = schema.exclude(vec_col)
        return schema


class LocalKNNIndexer(KNNIndexer):
    def build(
        self,
        index: AnyDataFrame,
        vec_col: str,
        worker_nthreads: Optional[int] = None,
        **kwargs: Any,
    ) -> "KNNIndexer":
        with threadpoolctl.threadpool_limits(limits=worker_nthreads):
            pdf = fa.as_pandas(index).reset_index(drop=True)
            self._metadata_df = pdf.drop(columns=[vec_col])
            self._metadata_schema = fa.get_schema(index) - vec_col
            arr = self.get_np_arr(pdf, vec_col=vec_col)
            self._dim = arr.shape[1]
            self.build_local(arr, worker_nthreads=worker_nthreads, **kwargs)
            return self

    def get_metadata_df(self) -> pd.DataFrame:
        return self._metadata_df

    def get_metadata_schema(self) -> Schema:
        return self._metadata_schema

    def get_dim(self) -> int:
        return self._dim

    @abstractmethod  # pragma: no cover
    def build_local(
        self, arr: np.ndarray, worker_nthreads: Optional[int], **kwargs: Any
    ) -> None:
        raise NotImplementedError


class DistributedKNNIndexer(KNNIndexer):
    def __init__(
        self,
        metric: str,
        indexer: Any,
        group_cols: Optional[List[str]] = None,
        index_shards: Optional[int] = None,
        index_broadcast_threshold: Any = "10m",
        save_dir: Optional[str] = None,
        indexer_init_kwargs: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(metric)

        self._internal_group_cols: List[str] = []
        if group_cols is not None:
            self._internal_group_cols += group_cols
            self._group_cols = group_cols
        else:
            self._group_cols = []
        if index_shards is not None and index_shards > 1:
            self._internal_group_cols += [_INDEXER_SHARD_COLUMN_NAME]
            self._index_shards = index_shards
        else:
            self._index_shards = 1
        assert_or_throw(
            len(self._internal_group_cols) > 0,
            ValueError("neither group_cols contains columns nor index_shards>1)"),
        )

        self._indexer = indexer
        self._index_broadcast_threshold = to_size(index_broadcast_threshold)
        self._save_dir = save_dir
        self._indexer_init_kwargs = indexer_init_kwargs or {}

    def build(
        self,
        index: AnyDataFrame,
        vec_col: str,
        worker_nthreads: Optional[int] = None,
        **kwargs: Any,
    ) -> "KNNIndexer":
        index = fa.as_fugue_df(index)
        if self._index_shards > 1 and len(self._group_cols) > 0:
            # only when both index_shards>1 and group_cols is not empty
            index = deterministic_shard(
                index,
                self._index_shards,
                _INDEXER_SHARD_COLUMN_NAME,
                from_cols=[x for x in fa.get_column_names(index) if x != vec_col],
            )

        input_schema = fa.get_schema(index)
        assert_or_throw(
            is_vec_col(input_schema, vec_col),
            ValueError(f"{vec_col} is not a vector column"),
        )
        indexer_schema = Schema(
            [
                (_INDEXER_BLOB_COLUMN_NAME, bytes),
                (_INDEXER_METADATA_BLOB_COLUMN_NAME, bytes),
            ]
        )
        if len(self._group_cols) > 0:
            output_schema = (
                input_schema.intersect(self._internal_group_cols) + indexer_schema
            )
            group_cols = self._internal_group_cols
        else:
            output_schema = indexer_schema
            group_cols = []

        def _build_group(df: pd.DataFrame) -> pd.DataFrame:
            indexer = knn_indexer(
                self._indexer, metric=self.metric, **self._indexer_init_kwargs
            )
            subdf = df.drop(columns=group_cols)
            indexer.build(
                subdf, vec_col=vec_col, worker_nthreads=worker_nthreads, **kwargs
            )
            ser = _KNNIndexerSerializer(
                indexer, self._index_broadcast_threshold, self._save_dir
            )
            metablob = (indexer.get_metadata_schema(), indexer.get_dim())
            return df.head(1)[group_cols].assign(
                **{
                    _INDEXER_BLOB_COLUMN_NAME: pickle.dumps(ser),
                    _INDEXER_METADATA_BLOB_COLUMN_NAME: pickle.dumps(metablob),
                }
            )[output_schema.names]

        if len(group_cols) > 0:
            self._index = fa.as_pandas(
                fa.transform(
                    index,
                    _build_group,
                    schema=output_schema,
                    partition=dict(by=group_cols, algo="even"),
                ),
            )
            if _INDEXER_SHARD_COLUMN_NAME not in self._index.columns:
                self._index.insert(0, _INDEXER_SHARD_COLUMN_NAME, 0)
        else:  # must be self._index_shards>1
            self._index = fa.as_pandas(
                fa.transform(
                    index,
                    _build_group,
                    schema=output_schema.exclude(_INDEXER_SHARD_COLUMN_NAME),
                    partition=dict(num=self._index_shards, algo="default"),
                ),
            )
            self._index.insert(0, _INDEXER_SHARD_COLUMN_NAME, range(len(self._index)))

        self._mem_size = int(self._index.memory_usage(deep=True).sum())
        self._metadata_schema, self._dim = pickle.loads(
            self._index[_INDEXER_METADATA_BLOB_COLUMN_NAME].iloc[0]
        )
        return self

    def search_local(
        self,
        query: np.ndarray,
        k: int,
        sort_output: bool,
        worker_nthreads: Optional[int],
        **kwargs: Any,
    ) -> Tuple[np.ndarray, np.ndarray]:  # pragma: no cover
        raise NotImplementedError(
            "search_local is not supported for DistributedKNNIndexer"
        )

    def can_broadcast(self, size_limit: int) -> bool:
        return self._mem_size < size_limit

    def get_metadata_df(self) -> pd.DataFrame:  # pragma: no cover
        raise NotImplementedError(
            "get_metadata_df is not supported for DistributedKNNIndexer"
        )

    def get_metadata_schema(self) -> Schema:
        return self._metadata_schema

    def get_dim(self) -> int:
        return self._dim

    def search(  # noqa: C901
        self,
        query: AnyDataFrame,
        k: int,
        vec_col: str,
        dist_col: Optional[str] = None,
        rank_col: Optional[str] = None,
        drop_vec_col: bool = True,
        index_cache_mem_limit: Any = "1g",
        index_broadcast_threshold: Any = "500m",
        query_shards: Optional[int] = None,
        query_preprocess_mode: str = "direct",
        query_chunk_mem_limit: Any = "100m",
        query_chunk_row_limit: int = 0,
        temp_path: Optional[str] = None,
        worker_nthreads: Optional[int] = None,
        **kwargs: Any,
    ) -> AnyDataFrame:

        is_dist_temp = False
        if self._index_shards > 1 and dist_col is None:
            # when index is sharded, we must keep a dist_col
            # so that we can merge the results from different shards
            dist_col = _TEMP_DIST_COL
            is_dist_temp = True

        input_is_native = not isinstance(query, DataFrame)
        query = fa.as_fugue_df(query)
        query_schema = fa.get_schema(query)
        group_cols = self._internal_group_cols
        query_sharded = query_shards is not None and query_shards > 1
        query_shards = max(1, query_shards or 1)
        index_shards = self._index[_INDEXER_SHARD_COLUMN_NAME].unique()

        if query_preprocess_mode == "direct":
            query = _process_query_directly(
                query,
                index_shards=index_shards,
                query_shards=query_shards,
                vec_col=vec_col,
            )
        elif query_preprocess_mode == "file":
            assert_or_throw(
                temp_path is not None,
                ValueError("temp_path is required when query_preprocess_mode==`file`"),
            )
            query = _cache_query_to_file(
                query,
                index_shards=index_shards,
                query_shards=query_shards,
                group_cols=self._group_cols,
                temp_path=temp_path,  # type: ignore
            )

        output_schema = self._construct_schema(
            query_schema,
            vec_col=vec_col,
            dist_col=dist_col,
            rank_col=rank_col,
            drop_vec_col=drop_vec_col,
        )
        indexer_ser = _KNNIndexerSerializer(
            self, to_size(index_broadcast_threshold), temp_path
        )

        def _extract_df(
            df: pd.DataFrame, indexer: KNNIndexer
        ) -> Iterable[Tuple[KNNIndexer, Iterable[pd.DataFrame]]]:
            if query_preprocess_mode == "direct":
                idx = indexer._index.merge(df.head(1)[group_cols])  # type: ignore
                if len(idx) > 0:
                    indexer = pickle.loads(
                        idx[_INDEXER_BLOB_COLUMN_NAME].iloc[0]
                    ).get_instance(cache_size=index_cache_mem_limit)
                    yield indexer, [df]
            else:  # query_preprocess_mode == "file"
                # a bit complex logic to dedup indexer loading
                for _, gpdf in df.groupby(group_cols, dropna=False):
                    idx = indexer._index.merge(gpdf.head(1)[group_cols])  # type: ignore
                    if len(idx) > 0:
                        indexer = pickle.loads(
                            idx[_INDEXER_BLOB_COLUMN_NAME].iloc[0]
                        ).get_instance(cache_size=index_cache_mem_limit)

                        def _get_dfs() -> Iterable[pd.DataFrame]:
                            for file in gpdf[_QUERY_BLOB_COLUMN_NAME]:
                                yield pd.read_parquet(file)

                        yield indexer, _get_dfs()

        def _wrapper(df: pd.DataFrame) -> Iterable[pd.DataFrame]:
            reslicer = PandasBatchReslicer(
                row_limit=query_chunk_row_limit,
                size_limit=query_chunk_mem_limit,
            )
            g_indexer = indexer_ser.get_instance(cache_size=index_cache_mem_limit)
            for indexer, dfs in _extract_df(df, g_indexer):
                for subdf in reslicer.reslice(dfs):
                    for res in _search_pd_df(
                        indexer=indexer,
                        df=subdf,
                        k=k,
                        vec_col=vec_col,
                        dist_col=dist_col,
                        rank_col=rank_col,
                        drop_vec_col=drop_vec_col,
                        # with shards>1, we will merge resort in the end
                        sort_output=rank_col is not None and len(index_shards) == 1,
                        worker_nthreads=worker_nthreads,
                        **kwargs,
                    ):
                        if len(res) > 0:
                            yield res[output_schema.names]

        res = fa.transform(
            query,
            _wrapper,
            schema=output_schema,
            partition=dict(
                by=group_cols
                if not query_sharded
                else group_cols + [_QUERY_SHARDS_COLUMN_NAME],
                algo="even",
            ),
        )

        if len(index_shards) > 1:
            qid_group_cols = query_schema.exclude(vec_col).names

            def _get_n(df: pd.DataFrame) -> int:
                df = df.head(k)
                if rank_col is not None:
                    df = df.assign(**{rank_col: range(len(df))})
                return df

            def _take(df: pd.DataFrame) -> pd.DataFrame:
                return (
                    df.groupby(qid_group_cols, dropna=False, group_keys=False)
                    .apply(_get_n)
                    .reset_index(drop=True)
                )

            res = fa.transform(
                res,
                _take,
                schema=output_schema,
                partition=dict(
                    by=qid_group_cols, algo="coarse", presort=[(dist_col, True)]
                ),
            )

        if is_dist_temp:
            res = fa.drop_columns(res, [dist_col])

        return fa.get_native_as_df(res) if input_is_native else res


class _KNNIndexerSerializer:
    def __init__(
        self,
        indexer: KNNIndexer,
        broadcast_size_limit: int,
        temp_path: Optional[str] = None,
    ):
        self._indexer_obj: Union[KNNIndexer, str] = indexer
        self._broadcast_size_limit = broadcast_size_limit
        self._temp_file = (
            None
            if temp_path is None
            else os.path.join(temp_path, str(uuid4()) + ".index")
        )

    def __getstate__(self) -> Any:
        params = dict(self.__dict__)
        if isinstance(
            self._indexer_obj, KNNIndexer
        ) and not self._indexer_obj.can_broadcast(self._broadcast_size_limit):
            assert_or_throw(
                self._temp_file is not None, ValueError("temp_file is required")
            )
            self._indexer_obj.save(self._temp_file)  # type: ignore
            params["_indexer_obj"] = self._temp_file  # type: ignore
        return params

    def get_instance(self, cache_size: Any) -> KNNIndexer:
        if isinstance(self._indexer_obj, str):
            return KNNIndexer.load(self._indexer_obj, cache_size=cache_size)
        else:
            return self._indexer_obj


class _KNNIndexerLoader:
    def __init__(self):
        self._reset()

    def __setstate__(self, state: Any) -> None:
        self._reset()

    def __getstate__(self) -> Any:
        return {}

    def get_cache_items(self) -> List[KNNIndexer]:
        return [self._indexers[tp[2]] for tp in self._hits]

    def load(self, path: str, cache_size: Any) -> KNNIndexer:
        limit = to_size(cache_size) if cache_size is not None else 0
        with self._lock:
            if path not in self._indexers:
                indexer, size = self._load(path)
                if size > limit:
                    return indexer
                self._indexers[path] = indexer
                self._n += 1
                self._hits.append((1, self._n, path, size))
                self._update_cache(limit)
                return indexer
            else:
                indexer = self._indexers[path]
                for i in range(len(self._hits)):
                    if self._hits[i][2] == path:
                        self._n += 1
                        self._hits[i] = (
                            self._hits[i][0] + 1,
                            self._n,
                            self._hits[i][2],
                            self._hits[i][3],
                        )
                        self._update_cache(limit)
                        break
                return indexer

    def _reset(self):
        self._lock = SerializableRLock()
        self._indexers: Dict[str, KNNIndexer] = {}
        self._hits: List[Tuple[int, int, str, int]] = []
        self._n = 0

    def _update_cache(self, limit: int) -> None:
        total = sum(x[-1] for x in self._hits)
        self._hits.sort(reverse=True)
        while total > limit:
            tp = self._hits.pop()
            del self._indexers[tp[2]]
            total -= tp[-1]

    def _load(self, path: str) -> Tuple[KNNIndexer, int]:
        with unzip_to_temp(path) as tmpdir:
            fs, path = fsspec.core.url_to_fs(tmpdir)
            blob = fs.read_bytes(os.path.join(path, "indexer_type.bin"))
            tp = pickle.loads(blob)
            params_blob = fs.read_bytes(os.path.join(path, "params.bin"))
            params = pickle.loads(params_blob)
            indexer = tp.__new__(tp)
            indexer.__dict__.update(params)
            indexer.__dict__.update(indexer.load_special_params(tmpdir))
            return indexer, len(blob) + len(params_blob)


_INDEXER_LOADER = _KNNIndexerLoader()


def _search_pd_df(
    indexer: KNNIndexer,
    df: pd.DataFrame,
    k: int,
    vec_col: str,
    dist_col: Optional[str],
    rank_col: Optional[str],
    drop_vec_col: bool,
    sort_output: bool,
    worker_nthreads: Optional[int],
    **kwargs: Any,
) -> Iterable[pd.DataFrame]:
    with threadpoolctl.threadpool_limits(limits=worker_nthreads):
        qarr = indexer.get_np_arr(df, vec_col=vec_col)
        idx, dist = indexer.search_local(
            qarr,
            k=k,
            sort_output=sort_output,
            worker_nthreads=worker_nthreads,
            **kwargs,
        )
        del qarr
        df = df.reset_index(drop=True)
        if drop_vec_col:
            df = df.drop(columns=[vec_col])
        for j in range(min(k, idx.shape[1])):
            meta = indexer.get_metadata_df().iloc[idx[:, j]].reset_index(drop=True)
            more_cols: Dict[str, Any] = {}
            if dist_col is not None:
                more_cols[dist_col] = dist[:, j]
            if rank_col is not None:
                more_cols[rank_col] = j
            if len(more_cols) > 0:
                df = df.assign(**more_cols)
            yield pd.concat([df, meta], axis=1)


def _process_query_directly(
    query: AnyDataFrame,
    index_shards: np.ndarray,
    query_shards: int,
    vec_col: str,
) -> AnyDataFrame:
    hash_cols = [x for x in fa.get_column_names(query) if x != vec_col]

    def _wrapper(dfs: Iterable[pd.DataFrame]) -> Iterable[pd.DataFrame]:
        for df in dfs:
            sdf = _shard(df, query_shards, hash_cols)
            for shard in index_shards:
                yield sdf.assign(**{_INDEXER_SHARD_COLUMN_NAME: shard})

    return fa.transform(
        query,
        _wrapper,
        schema=fa.get_schema(query)
        + Schema(
            [
                (_INDEXER_SHARD_COLUMN_NAME, int),
                (_QUERY_SHARDS_COLUMN_NAME, int),
            ]
        ),
    )


def _cache_query_to_file(
    query: AnyDataFrame,
    index_shards: np.ndarray,
    query_shards: int,
    group_cols: List[str],
    temp_path: str,
) -> pd.DataFrame:
    has_gp_cols = len(group_cols) > 0
    input_schema = fa.get_schema(query)

    def _wrapper(df: pd.DataFrame, query_shards: int) -> Iterable[pd.DataFrame]:
        for rep, subdf in enumerate(np.array_split(df, query_shards)):
            if len(subdf) > 0:
                path = os.path.join(temp_path, str(uuid4()) + ".parquet")
                subdf.to_parquet(path, index=False)
                res = (
                    subdf.head(1)
                    .assign(**{_QUERY_BLOB_COLUMN_NAME: path})
                    .reset_index(drop=True)
                )
                yield res.assign(**{_QUERY_SHARDS_COLUMN_NAME: rep})

    if has_gp_cols:
        res = fa.as_pandas(
            fa.transform(
                query,
                _wrapper,
                partition=dict(by=group_cols, algo="default"),
                schema=input_schema.extract(group_cols)
                + Schema(
                    [
                        (_QUERY_SHARDS_COLUMN_NAME, int),
                        (_QUERY_BLOB_COLUMN_NAME, str),
                    ]
                ),
                params={"query_shards": query_shards},
            )
        )
    else:
        res = fa.as_pandas(
            fa.transform(
                query,
                _wrapper,
                partition=dict(num=query_shards, algo="default"),
                schema=Schema(
                    [
                        (_QUERY_SHARDS_COLUMN_NAME, int),
                        (_QUERY_BLOB_COLUMN_NAME, str),
                    ]
                ),
                params={"query_shards": 1},
            )
        )
        res[_QUERY_SHARDS_COLUMN_NAME] = range(len(res))
    return pd.concat(
        [res.assign(**{_INDEXER_SHARD_COLUMN_NAME: shard}) for shard in index_shards]
    )


def _shard(df: pd.DataFrame, query_shards: int, hash_cols: List[str]) -> pd.DataFrame:
    if query_shards <= 1:
        return df.assign(**{_QUERY_SHARDS_COLUMN_NAME: 0})
    return df.assign(
        **{
            _QUERY_SHARDS_COLUMN_NAME: pd.util.hash_pandas_object(
                df[hash_cols], index=False
            ).mod(query_shards)
        }
    )
