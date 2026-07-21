from __future__ import annotations

import open3d as o3d
import numpy as np

from ..geometry.base import Geometry


class Open3DRenderer:
    """
    Geometry を Open3D で描画するクラス
    """

    def __init__(
        self,
        sphere_resolution: int = 20,
        sphere_color=(0.2, 0.6, 1.0),
        show_coordinate_frame: bool = True,
        coordinate_size: float = 2.0,
        background_color=(1.0, 1.0, 1.0)
    ):

        self.sphere_resolution = sphere_resolution
        self.sphere_color = sphere_color
        self.show_coordinate_frame = show_coordinate_frame
        self.coordinate_size = coordinate_size
        self.background_color = background_color

    def create_mesh(self, geometry: Geometry):

        mesh = o3d.geometry.TriangleMesh()

        for node in geometry:

            sphere = o3d.geometry.TriangleMesh.create_sphere(
                radius=geometry.radius,
                resolution=self.sphere_resolution
            )

            sphere.paint_uniform_color(self.sphere_color)

            sphere.translate(node.position)

            mesh += sphere

        mesh.compute_vertex_normals()

        return mesh

    def create_coordinate_frame(self):

        return o3d.geometry.TriangleMesh.create_coordinate_frame(
            size=self.coordinate_size,
            origin=[0, 0, 0]
        )

    def draw(self, geometry: Geometry):

        mesh = self.create_mesh(geometry)

        geometries = [mesh]

        if self.show_coordinate_frame:
            geometries.append(
                self.create_coordinate_frame()
            )

        vis = o3d.visualization.Visualizer()

        vis.create_window(
            window_name=geometry.name
        )

        vis.add_geometry(mesh)

        if self.show_coordinate_frame:
            vis.add_geometry(
                geometries[1]
            )

        opt = vis.get_render_option()

        opt.background_color = np.asarray(
            self.background_color
        )

        vis.run()

        vis.destroy_window()
