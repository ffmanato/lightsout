from __future__ import annotations

import numpy as np

from ..geometry.base import Geometry
from .base import AdjacencyBuilder


class DistanceAdjacency(AdjacencyBuilder):
    """
    距離に基づいて隣接行列を生成する。

    中心間距離が
        distance <= threshold
    の頂点同士を隣接とする。
    """

    def __init__(self,
                 radius: float,
                 tolerance: float = 1e-6,
                 include_self: bool = True):

        self.radius = radius
        self.threshold = 2.0 * radius
        self.tolerance = tolerance
        self.include_self = include_self

    def build(self,
              geometry: Geometry) -> np.ndarray:

        n = len(geometry)

        A = np.zeros((n, n), dtype=np.uint8)

        if self.include_self:
            np.fill_diagonal(A, 1)

        positions = np.array(
            [node.position for node in geometry]
        )

        for i in range(n):

            for j in range(i + 1, n):

                d = np.linalg.norm(
                    positions[i] - positions[j]
                )

                if abs(d - self.threshold) <= self.tolerance:

                    A[i, j] = 1
                    A[j, i] = 1

        return A
