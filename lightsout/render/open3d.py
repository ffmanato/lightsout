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

    def create_point_cloud(
        self,
        geometry: Geometry,
        state: np.ndarray | None = None,
        on_color=(1.0, 0.85, 0.2),
        off_color=(0.15, 0.15, 0.15)
    ):

        pcd = o3d.geometry.PointCloud()

        pcd.points = o3d.utility.Vector3dVector(
            geometry.positions()
        )

        if state is None:
            colors = np.tile(
                np.asarray(self.sphere_color, dtype=float),
                (len(geometry), 1)
            )
        else:
            state = np.asarray(state, dtype=np.uint8)

            colors = np.tile(
                np.asarray(off_color, dtype=float),
                (len(state), 1)
            )
            colors[state == 1] = np.asarray(
                on_color,
                dtype=float
            )

        pcd.colors = o3d.utility.Vector3dVector(
            colors
        )

        return pcd

    def play_lights_out(
        self,
        geometry: Geometry,
        game,
        initial_state: np.ndarray | None = None,
        on_color=(1.0, 0.85, 0.2),
        off_color=(0.15, 0.15, 0.15),
        point_size: float = 18.0
    ):
        """
        Open3D 上で Lights Out を対話的にプレイする。

        Controls
        --------
        - Shift + 左クリック: ノード選択
        - Q / Esc: 選択を確定して次へ（未選択なら終了）
        """

        if initial_state is None:
            state = game.random_state()
        else:
            state = np.asarray(
                initial_state,
                dtype=np.uint8
            ).copy()

        if len(state) != len(geometry):
            raise ValueError(
                "state size must match geometry size"
            )

        moves = 0

        print("\n3D Lights Out controls:")
        print("  Shift + Left Click : select a node")
        print("  Q / Esc            : apply selected move")
        print("  Q / Esc with no selection exits")

        while True:
            lights_on = int(state.sum())
            total = len(state)

            print(
                f"\nMoves: {moves} | "
                f"Lights on: {lights_on}/{total}"
            )

            if game.is_solved(state):
                print("Cleared! All lights are off.")
                return state, moves, True

            pcd = self.create_point_cloud(
                geometry=geometry,
                state=state,
                on_color=on_color,
                off_color=off_color
            )

            vis = o3d.visualization.VisualizerWithEditing()

            vis.create_window(
                window_name=(
                    f"{geometry.name} Lights Out - "
                    f"Move {moves}"
                )
            )
            vis.add_geometry(pcd)

            if self.show_coordinate_frame:
                vis.add_geometry(
                    self.create_coordinate_frame()
                )

            opt = vis.get_render_option()
            opt.background_color = np.asarray(
                self.background_color
            )
            opt.point_size = point_size

            vis.run()

            picked = vis.get_picked_points()
            vis.destroy_window()

            if len(picked) == 0:
                print("No node selected. Exiting game.")
                return state, moves, False

            if len(picked) > 1:
                print(
                    "Multiple nodes selected; "
                    "only the first one is used."
                )

            vertex = int(picked[0])

            state = game.press(state, vertex)
            moves += 1

            print(
                f"Pressed node: {vertex}"
            )
