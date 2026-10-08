from __future__ import annotations

import math
import numpy as np

from .base import Geometry


class Dodecahedron(Geometry):
    """
    正十二面体
    """

    def __init__(self, radius: float):
        super().__init__(
            radius=radius,
            name="Dodecahedron"
        )
        self.generate()

    def generate(self):
        phi = (1.0 + math.sqrt(5.0)) / 2.0
        inv_phi = 1.0 / phi
        scale = phi * self.radius

        positions = []

        for x in (-1.0, 1.0):
            for y in (-1.0, 1.0):
                for z in (-1.0, 1.0):
                    positions.append([x, y, z])

        for y in (-inv_phi, inv_phi):
            for z in (-phi, phi):
                positions.append([0.0, y, z])

        for x in (-inv_phi, inv_phi):
            for y in (-phi, phi):
                positions.append([x, y, 0.0])

        for x in (-phi, phi):
            for z in (-inv_phi, inv_phi):
                positions.append([x, 0.0, z])

        positions = np.asarray(positions, dtype=float) * scale
        positions -= positions.mean(axis=0)

        for i, pos in enumerate(positions):
            self.add_node((i,), pos)
