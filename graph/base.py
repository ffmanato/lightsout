from __future__ import annotations

from abc import ABC, abstractmethod
import numpy as np

from geometry.base import Geometry


class AdjacencyBuilder(ABC):
    """
    隣接行列生成クラスの基底クラス
    """

    @abstractmethod
    def build(self, geometry: Geometry) -> np.ndarray:
        """
        Parameters
        ----------
        geometry : Geometry

        Returns
        -------
        np.ndarray
            NxN の隣接行列
        """
        pass