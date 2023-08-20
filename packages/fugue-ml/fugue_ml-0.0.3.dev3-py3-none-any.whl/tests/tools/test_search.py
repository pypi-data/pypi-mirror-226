import pandas as pd

from fugue_ml.tools.text_search import (
    TextSearchIndex,
    _build_input_df,
    _build_query_df,
    _melt_df,
)
import fugue.api as fa
import pytest


@pytest.mark.parametrize(
    "backend", [None, "spark_session", "fugue_dask_client", "fugue_ray_session"]
)
def test_text_search_index(backend, request, tmpdir):
    with fa.engine_context(
        None if backend is None else request.getfixturevalue(backend)
    ):
        idx = TextSearchIndex(embedding_model="openai")
        idx = idx.build(
            [
                "this is schema",
                "this is partition",
                "this is schema and partition",
                "this is schema and partition",
            ]
        )
        res = idx.search("schema", 2)
        assert fa.as_pandas(res).text.sort_values().tolist() == [
            "this is schema",
            "this is schema and partition",
        ]

        idx = TextSearchIndex(
            embedding_model="openai",
            embedding_cache="file:" + str(tmpdir.join("t.parquet")),
        )
        idx = idx.build(
            pd.DataFrame(
                [
                    [1, "what is schema", "what is partition"],
                    [2, "what is partition", "what is partition"],
                ],
                columns=["id", "question", "answer"],
            ),
            cols=["question", "answer"],
        )
        res = idx.search("partition", 1)
        assert fa.as_pandas(res)["id"].sort_values().tolist() == [1, 2]
        res = idx.search("schema", 1)
        assert fa.as_pandas(res)["id"].sort_values().tolist() == [1]
        res = idx.search(
            pd.DataFrame(dict(qid=[1, 2, 3], q=["schema", "partition", "schema"])),
            1,
            query_col="q",
            dist_col="dist",
        )
        assert fa.count(res) == 4
        assert ["qid", "dist"] in fa.get_schema(res)


def test_build_input_df():
    df, cols = _build_input_df(["ab", "cd", "ab"])
    assert df.as_pandas().text.sort_values().tolist() == ["ab", "cd"]
    assert df.as_pandas().unique_id.sort_values().tolist() == [0, 1]
    assert cols == ["text"]
    sdf = pd.DataFrame(dict(unique_id=[1, 0], text1=["ab", "cd"], text2=["xy", "ab"]))
    df, cols = _build_input_df(sdf, cols=["text1", "text2"])
    pd.testing.assert_frame_equal(fa.as_pandas(df), sdf)
    assert cols == ["text1", "text2"]
    sdf = pd.DataFrame(dict(text1=["ab", "cd"], text2=["xy", "ab"]))
    df, cols = _build_input_df(sdf, cols=["text1", "text2"])
    assert "unique_id" in df.schema
    assert cols == ["text1", "text2"]


def test_melt_df():
    df = fa.as_fugue_df(
        pd.DataFrame(dict(unique_id=[1, 2], a=["ab", "cd"], b=["xy", "ab"]))
    )
    mdf = _melt_df(df, ["a", "b"], use_cache=False)
    assert mdf[["text", "unique_ids", "cache_id"]].as_pandas().sort_values(
        "text"
    ).values.tolist() == [["ab", [1, 2], ""], ["cd", [2], ""], ["xy", [1], ""]]
    mdf = _melt_df(df, ["a", "b"], use_cache=True)
    assert mdf.as_pandas()["cache_id"].nunique() == 3


def test_build_query_df():
    df, col = _build_query_df("ab", query_col=None, use_cache=False)
    assert fa.as_array(df) == [["ab"]]
    assert col == "input_query"

    df, col = _build_query_df(["ab", "cd", "ab"], query_col=None, use_cache=False)
    assert fa.as_pandas(df)[col].sort_values().tolist() == ["ab", "cd"]
    assert col == "input_query"

    idx = _melt_df(
        fa.as_fugue_df(pd.DataFrame(dict(unique_id=[1, 2], a=["ab", "cd"]))),
        ["a"],
        use_cache=True,
    )
    df, col = _build_query_df(["ab", "cd", "ab"], query_col=None, use_cache=True)
    assert set(idx.as_pandas()["cache_id"].unique()) == set(
        df.as_pandas()["cache_id"].unique()
    )

    df, col = _build_query_df(
        pd.DataFrame(dict(t=["ab", "cd", "ab"], q=[1, 2, 3])),
        query_col="t",
        use_cache=True,
    )
    assert fa.count(df) == 2
    assert fa.as_pandas(df)[col].sort_values().tolist() == ["ab", "cd"]
    assert col == "t"
    assert set(idx.as_pandas()["cache_id"].unique()) == set(
        df.as_pandas()["cache_id"].unique()
    )
