from typing import Any, Optional, Tuple

import numpy as np
import threadpoolctl

from fugue_ml.utils.numpy.distance import knn as compute_knn

from .indexer import LocalKNNIndexer, register_knn_indexer


@register_knn_indexer("brute_force")
class BruteForceKNNIndexer(LocalKNNIndexer):
    """Brute force KNN indexer. It is implemented using Numoy and
    It produces exact (perfect) k nearest neighbors.
    """

    def build_local(
        self, arr: np.ndarray, worker_nthreads: Optional[int], **kwargs: Any
    ) -> None:
        self._index = arr

    def can_broadcast(self, size_limit: int) -> bool:
        return (
            self._index.nbytes + self._metadata_df.memory_usage(deep=True).sum()
            < size_limit
        )

    def search_local(
        self,
        query: np.ndarray,
        k: int,
        sort_output: bool,
        worker_nthreads: Optional[int],
        **kwargs: Any
    ) -> Tuple[np.ndarray, np.ndarray]:
        self._dim = query.shape[1]
        with threadpoolctl.threadpool_limits(limits=worker_nthreads):
            return compute_knn(
                index=self._index,
                query=query,
                metric=self.metric,
                k=k,
                sort_output=sort_output,
            )
