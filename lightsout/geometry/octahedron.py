from __future__ import annotations

import numpy as np

from .base import Geometry


class Octahedron(Geometry):
    """
    正八面体（6頂点）
    """

    def __init__(self, radius: float):

        super().__init__(
            radius=radius,
            name="Octahedron"
        )

        self.generate()

    def generate(self):

        scale = np.sqrt(2.0) * self.radius

        for axis in range(3):
            for sign in (-1, 1):
                position = np.zeros(3, dtype=float)
                position[axis] = sign * scale

                self.add_node(
                    lattice=(axis, sign),
                    position=position
                )
