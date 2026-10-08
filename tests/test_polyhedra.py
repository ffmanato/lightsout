from __future__ import annotations

import unittest

import numpy as np

from lightsout.geometry import Tetrahedron, Octahedron, Dodecahedron
from lightsout.graph import DistanceAdjacency, LightsOutGraph
from lightsout.presets import get_preset, build_geometry


class PolyhedraGeometryTests(unittest.TestCase):
    def test_octahedron_node_count(self):
        geo = Octahedron(radius=1.0)
        self.assertEqual(len(geo), 6)

    def test_dodecahedron_node_count(self):
        geo = Dodecahedron(radius=1.0)
        self.assertEqual(len(geo), 20)

    def test_octahedron_adjacency_degree(self):
        geo = Octahedron(radius=1.0)
        adjacency = DistanceAdjacency(radius=1.0, tolerance=1e-6).build(geo)
        self.assertTrue(np.all(adjacency.sum(axis=1) == 5))
        self.assertEqual(int(np.triu(adjacency, k=1).sum()), 12)

    def test_dodecahedron_adjacency_degree(self):
        geo = Dodecahedron(radius=1.0)
        adjacency = DistanceAdjacency(radius=1.0, tolerance=1e-6).build(geo)
        self.assertTrue(np.all(adjacency.sum(axis=1) == 4))
        self.assertEqual(int(np.triu(adjacency, k=1).sum()), 30)

    def test_octahedron_press_operation(self):
        geo = Octahedron(radius=1.0)
        adjacency = DistanceAdjacency(radius=1.0, tolerance=1e-6).build(geo)
        game = LightsOutGraph(adjacency, include_self=True)
        state = game.press(game.empty_state(), 0)
        self.assertEqual(int(state.sum()), 5)

    def test_dodecahedron_press_operation(self):
        geo = Dodecahedron(radius=1.0)
        adjacency = DistanceAdjacency(radius=1.0, tolerance=1e-6).build(geo)
        game = LightsOutGraph(adjacency, include_self=True)
        state = game.press(game.empty_state(), 0)
        self.assertEqual(int(state.sum()), 4)

    def test_presets_build_new_polyhedra(self):
        octa = build_geometry(get_preset('octa'))
        dodeca = build_geometry(get_preset('dodeca'))
        self.assertIsInstance(octa, Octahedron)
        self.assertIsInstance(dodeca, Dodecahedron)

    def test_existing_tetrahedron_preset_still_works(self):
        tetra = build_geometry(get_preset('tetra_3'))
        self.assertIsInstance(tetra, Tetrahedron)


if __name__ == '__main__':
    unittest.main()
