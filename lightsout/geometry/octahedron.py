from __future__ import annotations

import math
import numpy as np

from .base import Geometry


class Octahedron(Geometry):
    """
    正八面体
    """

    def __init__(self, radius: float):
        super().__init__(
            radius=radius,
            name="Octahedron"
        )
        self.generate()

    def generate(self):
        scale = math.sqrt(2.0) * self.radius

        positions = np.asarray([
            [1.0, 0.0, 0.0],
            [-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, -1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.0, 0.0, -1.0],
        ], dtype=float) * scale

        positions -= positions.mean(axis=0)

        for i, pos in enumerate(positions):
            self.add_node((i,), pos)
