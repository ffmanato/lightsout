from __future__ import annotations

from itertools import product
import numpy as np

from .base import Geometry


class Cube(Geometry):
    """
    立方体（8頂点）
    """

    def __init__(self, radius: float):

        super().__init__(
            radius=radius,
            name="Cube"
        )

        self.generate()

    def generate(self):

        for sx, sy, sz in product((-1, 1), repeat=3):
            self.add_node(
                lattice=(sx, sy, sz),
                position=np.array([
                    sx * self.radius,
                    sy * self.radius,
                    sz * self.radius
                ], dtype=float)
            )
