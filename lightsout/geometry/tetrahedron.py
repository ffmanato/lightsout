from __future__ import annotations

import math
import numpy as np

from .base import Geometry


class Tetrahedron(Geometry):
    """
    正四面体格子（三角錐）
    """

    def __init__(self,
                 levels: int,
                 radius: float):

        super().__init__(
            radius=radius,
            name="Tetrahedron"
        )

        self.levels = levels

        self.generate()

    def generate(self):

        dx = 2 * self.radius
        dy = math.sqrt(3) * self.radius
        dz = math.sqrt(8 / 3) * self.radius

        positions = []

        lattice_list = []

        for k in range(self.levels):

            n = self.levels - k

            layer = []

            for i in range(n):
                for j in range(n - i):

                    x = (j + i / 2) * dx
                    y = i * dy

                    layer.append([x, y])
                    lattice_list.append((k, i, j))

            layer = np.asarray(layer)

            center = layer.mean(axis=0)

            z = k * dz

            for p in layer:
                positions.append([
                    p[0] - center[0],
                    p[1] - center[1],
                    z
                ])

        positions = np.asarray(positions)

        positions -= positions.mean(axis=0)

        for lattice, pos in zip(lattice_list, positions):
            self.add_node(lattice, pos)