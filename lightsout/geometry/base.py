from __future__ import annotations

from dataclasses import dataclass
from abc import ABC, abstractmethod
import numpy as np


@dataclass
class Node:
    """
    ライツアウトを構成する1つの格子点
    """

    # 頂点番号
    id: int

    # 格子座標
    lattice: tuple[int, ...]

    # 描画用座標
    position: np.ndarray


class Geometry(ABC):
    """
    全ての形状の基底クラス
    """

    def __init__(
        self,
        radius: float,
        name: str = "Geometry"
    ):

        self.radius = radius
        self.name = name

        self.nodes: list[Node] = []

        # 格子座標 -> Node
        self.node_map: dict[tuple[int, ...], Node] = {}

    @abstractmethod
    def generate(self):
        """
        格子を生成する
        """
        pass

    def add_node(
        self,
        lattice: tuple[int, ...],
        position
    ):

        position = np.asarray(position, dtype=float)

        node = Node(
            id=len(self.nodes),
            lattice=lattice,
            position=position
        )

        self.nodes.append(node)
        self.node_map[lattice] = node

    def center(self):
        """
        全体の重心を原点へ移動
        """

        if len(self.nodes) == 0:
            return

        center = np.mean(
            [node.position for node in self.nodes],
            axis=0
        )

        for node in self.nodes:
            node.position -= center

    def positions(self) -> np.ndarray:
        """
        全頂点の座標を NumPy 配列で返す
        """

        return np.array(
            [node.position for node in self.nodes]
        )

    def lattices(self):
        """
        格子座標一覧
        """

        return [
            node.lattice
            for node in self.nodes
        ]

    def get_node(self, lattice):

        return self.node_map.get(lattice)

    def __len__(self):

        return len(self.nodes)

    def __iter__(self):

        return iter(self.nodes)

    def __getitem__(self, index):

        return self.nodes[index]

    def __repr__(self):

        return (
            f"{self.name}"
            f"(nodes={len(self)}, "
            f"radius={self.radius})"
        )