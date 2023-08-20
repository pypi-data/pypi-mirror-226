from typing import Any, Iterable, List, Optional, Tuple, Union

import fugue.api as fa
import pandas as pd
import pyarrow as pa
from fugue import AnyDataFrame, DataFrame
from triad import assert_or_throw, to_uuid

from fugue_ml.embedding.api import compute_embeddings
from fugue_ml.knn import build_knn_index
from fugue_ml.knn.brute_force import BruteForceKNNIndexer

_EMBEDDING_VALUE_COL = "text"
_EMBEDDING_VEC_COL = "vector"
_EMBEDDING_CACHE_ID_COL = "cache_id"
_INDEX_UNIQUE_IDS_COL = "unique_ids"
_INDEX_UNIQUE_ID_COL = "unique_id"
_DEFAULT_QUERY_COL = "input_query"


class TextSearchIndex:
    def __init__(
        self,
        embedding_model: Any,
        embedding_cache: Any = None,
        indexer: Any = BruteForceKNNIndexer,
        metric: str = "cos",
        **embedding_kwargs: Any,
    ):
        self.embedding_model = embedding_model
        self.embedding_cache = embedding_cache
        self.indexer = indexer
        self.metric = metric
        self.embedding_kwargs = embedding_kwargs

    def build(
        self,
        index_df: Union[AnyDataFrame, List[str]],
        cols: Union[str, List[str], None] = None,
        **indexer_kwargs: Any,
    ) -> "TextSearchIndex":
        self.src_df, idx_cols = _build_input_df(index_df, cols)
        mdf = _melt_df(
            self.src_df, idx_cols, use_cache=self.embedding_cache is not None
        )
        embeddings = compute_embeddings(
            mdf,
            col=_EMBEDDING_VALUE_COL,
            vec_col=_EMBEDDING_VEC_COL + ":[float32]",
            model=self.embedding_model,
            cache=self.embedding_cache,
            cache_uid_col=_EMBEDDING_CACHE_ID_COL,
            **(self.embedding_kwargs or {}),
        )
        if _EMBEDDING_CACHE_ID_COL in embeddings.schema:
            embeddings = embeddings.drop([_EMBEDDING_CACHE_ID_COL])
        self.index = build_knn_index(
            embeddings,
            indexer=self.indexer,
            vec_col=_EMBEDDING_VEC_COL,
            metric=self.metric,
            **indexer_kwargs,
        )
        return self

    def search(
        self,
        query: Union[AnyDataFrame, List[str], str],
        k: int,
        query_col: Optional[str] = None,
        **search_kwargs: Any,
    ) -> AnyDataFrame:
        df, col = _build_query_df(
            query, query_col, use_cache=self.embedding_cache is not None
        )
        embeddings = compute_embeddings(
            df,
            col=col,
            vec_col=_EMBEDDING_VEC_COL + ":[float32]",
            model=self.embedding_model,
            cache=self.embedding_cache,
            cache_uid_col=_EMBEDDING_CACHE_ID_COL,
            **self.embedding_kwargs,
        )
        if _EMBEDDING_CACHE_ID_COL in embeddings.schema:
            embeddings = embeddings.drop([_EMBEDDING_CACHE_ID_COL])
        res = self.index.search(
            embeddings, k, vec_col=_EMBEDDING_VEC_COL, **search_kwargs
        )
        res = _postprocess(
            res, self.src_df, query=None if isinstance(query, (str, list)) else query
        )
        return fa.get_native_as_df(res) if not isinstance(query, DataFrame) else res


def _build_input_df(
    index_df: Union[AnyDataFrame, List[str]], cols: Union[str, List[str], None] = None
) -> Tuple[DataFrame, List[str]]:
    if isinstance(index_df, list):
        assert_or_throw(
            cols is None, ValueError("cols must be None if index_df is list")
        )
        _df: Any = pd.DataFrame(dict(text=list(set(index_df))))
        _df = _df.assign(**{_INDEX_UNIQUE_ID_COL: range(len(_df))})
        _cols = ["text"]
        return fa.as_fugue_df(_df), _cols
    assert_or_throw(
        cols is not None and len(cols) > 0, ValueError("cols must be specified")
    )
    _cols = [cols] if isinstance(cols, str) else list(cols)  # type: ignore
    _df = fa.as_fugue_df(index_df)
    schema = fa.get_schema(_df)
    for col in _cols:
        assert_or_throw(
            pa.types.is_string(schema[col].type),
            ValueError(f"column {col} is not string in index_df"),
        )
    if _INDEX_UNIQUE_ID_COL not in schema:

        def _add_unique(df: Iterable[List[Any]]) -> Iterable[List[Any]]:
            for row in df:
                yield row + [to_uuid(row)]

        _df = fa.transform(_df, _add_unique, schema=f"*,{_INDEX_UNIQUE_ID_COL}:str")
    return _df, _cols


def _melt_df(df: DataFrame, cols: List[str], use_cache: bool) -> DataFrame:
    def _melt(dfs: Iterable[pd.DataFrame]) -> Iterable[pd.DataFrame]:
        for df in dfs:
            yield df.melt(
                id_vars=[_INDEX_UNIQUE_ID_COL],
                value_vars=cols,
                value_name=_EMBEDDING_VALUE_COL + "__temp__",
            ).rename(columns={_EMBEDDING_VALUE_COL + "__temp__": _EMBEDDING_VALUE_COL})[
                [_INDEX_UNIQUE_ID_COL, _EMBEDDING_VALUE_COL]
            ]

    def _agg(df: pd.DataFrame) -> pd.DataFrame:
        df = (
            df.groupby(_EMBEDDING_VALUE_COL)
            .agg(lambda x: list(set(x)))
            .reset_index(drop=False)
        ).rename(columns={_INDEX_UNIQUE_ID_COL: _INDEX_UNIQUE_IDS_COL})
        return df.assign(
            **{
                _EMBEDDING_CACHE_ID_COL: ""
                if not use_cache
                else df[_EMBEDDING_VALUE_COL].transform(to_uuid)
            }
        )

    melt = fa.transform(
        df, _melt, schema=[df.schema[_INDEX_UNIQUE_ID_COL], (_EMBEDDING_VALUE_COL, str)]
    )
    agg = fa.transform(
        melt,
        _agg,
        schema=[
            (_EMBEDDING_VALUE_COL, str),
            (_INDEX_UNIQUE_IDS_COL, pa.list_(df.schema[_INDEX_UNIQUE_ID_COL].type)),
            (_EMBEDDING_CACHE_ID_COL, str),
        ],
        partition=dict(by=_EMBEDDING_VALUE_COL, algo="coarse"),
    )
    return agg


def _build_query_df(
    query: Union[AnyDataFrame, List[str], str],
    query_col: Optional[str],
    use_cache: bool,
) -> Tuple[DataFrame, str]:
    qcol = query_col or _DEFAULT_QUERY_COL

    def _add_cache_id(df: pd.DataFrame) -> pd.DataFrame:
        return df.assign(**{_EMBEDDING_CACHE_ID_COL: df[qcol].transform(to_uuid)})

    if isinstance(query, str):
        query = [query]
    if isinstance(query, list):
        pdf = pd.DataFrame({qcol: list(set(query))})
        if use_cache:
            pdf = _add_cache_id(pdf)
        _df = fa.as_fugue_df(pdf)
    else:
        _df = fa.distinct(fa.as_fugue_df(fa.select_columns(query, [qcol])))
        if use_cache:
            _df = fa.transform(
                _df, _add_cache_id, schema=f"*,{_EMBEDDING_CACHE_ID_COL}:str"
            )
    return _df, qcol


def _postprocess(
    result: DataFrame,
    index: DataFrame,
    query: Optional[AnyDataFrame],
) -> DataFrame:
    def _explode(dfs: Iterable[pd.DataFrame]) -> Iterable[pd.DataFrame]:
        for df in dfs:
            # pandas explode does not work with arrow list
            df = df.assign(
                **{_INDEX_UNIQUE_IDS_COL: df[_INDEX_UNIQUE_IDS_COL].astype(object)}
            )
            yield df.explode(_INDEX_UNIQUE_IDS_COL).reset_index(drop=True).rename(
                columns={_INDEX_UNIQUE_IDS_COL: _INDEX_UNIQUE_ID_COL}
            )

    result = result.drop([_EMBEDDING_VALUE_COL])
    fields: List[pa.Field] = []
    for f in result.schema.fields:
        if f.name == _INDEX_UNIQUE_IDS_COL:
            fields.append(pa.field(_INDEX_UNIQUE_ID_COL, f.type.value_type))
        elif f.name != _EMBEDDING_CACHE_ID_COL:
            fields.append(f)
    result = fa.transform(result, _explode, fields)
    joined = fa.inner_join(result, index).drop([_INDEX_UNIQUE_ID_COL])
    if query is not None:
        joined = fa.inner_join(query, joined)
    return joined
