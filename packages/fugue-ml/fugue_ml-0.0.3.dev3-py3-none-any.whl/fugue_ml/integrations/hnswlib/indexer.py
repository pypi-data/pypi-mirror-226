from typing import Any, Dict, Optional, Tuple

import hnswlib
import numpy as np

from fugue_ml.knn.indexer import LocalKNNIndexer, register_knn_indexer

_DEFAULT_BUILD_PARAMS: Dict[str, Any] = {
    "M": 16,
    "ef_construction": 200,
    "random_seed": 100,
}


@register_knn_indexer("hnswlib")
class HnswlibKNNIndexer(LocalKNNIndexer):
    def build_local(
        self, arr: np.ndarray, worker_nthreads: Optional[int], **kwargs: Any
    ) -> None:
        params = _DEFAULT_BUILD_PARAMS.copy()
        params.update(kwargs)
        index = hnswlib.Index(space="l2", dim=arr.shape[1])
        index.init_index(max_elements=arr.shape[0], **params)
        if self.metric == "cos":
            arr = _normalize(arr)
        index.add_items(
            arr, np.arange(arr.shape[0]), num_threads=_to_num_threads(worker_nthreads)
        )
        self._index = index
        self._min_size = arr.nbytes

    def can_broadcast(self, size_limit: int) -> bool:
        return self._min_size < size_limit

    def search_local(
        self,
        query: np.ndarray,
        k: int,
        sort_output: bool,
        worker_nthreads: Optional[int],
        **kwargs: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        if k > self._index.element_count:
            k = self._index.element_count
        ef = kwargs.pop("ef", k * 2)
        if ef > 0:
            self._index.set_ef(ef)
        if self.metric == "cos":
            query = _normalize(query)
        idx, dist = self._index.knn_query(
            query, k=k, num_threads=_to_num_threads(worker_nthreads), **kwargs
        )
        if self.metric == "cos":
            dist /= 2.0
        if self.metric == "l2":
            dist = np.sqrt(dist)
        return idx, dist


def _normalize(df: np.ndarray) -> np.ndarray:
    return df / np.linalg.norm(df, axis=1, keepdims=True)


def _to_num_threads(worker_nthreads: Optional[int]) -> int:
    return (
        worker_nthreads if worker_nthreads is not None and worker_nthreads > 0 else -1
    )
