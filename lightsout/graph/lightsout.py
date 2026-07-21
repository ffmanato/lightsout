from __future__ import annotations

import numpy as np


class LightsOutGraph:
    """
    ライツアウト用グラフ

    Parameters
    ----------
    adjacency : np.ndarray
        隣接行列
    include_self : bool
        自分自身も反転するか
    """

    def __init__(
        self,
        adjacency: np.ndarray,
        include_self: bool = True
    ):

        self.adjacency = adjacency.astype(np.uint8)

        self.n = adjacency.shape[0]

        self.matrix = self.adjacency.copy()

        if include_self:
            np.fill_diagonal(self.matrix, 1)

    def size(self):

        return self.n

    def get_matrix(self):

        return self.matrix.copy()

    def empty_state(self):

        """
        全消灯状態
        """

        return np.zeros(self.n, dtype=np.uint8)

    def random_state(self):

        """
        ランダム盤面
        """

        return np.random.randint(
            0,
            2,
            size=self.n,
            dtype=np.uint8
        )

    def press(
        self,
        state: np.ndarray,
        vertex: int
    ) -> np.ndarray:

        """
        vertex を押した結果を返す
        """

        next_state = state.copy()

        next_state ^= self.matrix[:, vertex]

        return next_state

    def press_sequence(
        self,
        state: np.ndarray,
        sequence
    ) -> np.ndarray:

        """
        複数回押す
        """

        state = state.copy()

        for v in sequence:
            state ^= self.matrix[:, v]

        return state

    def is_solved(
        self,
        state: np.ndarray
    ) -> bool:

        return np.all(state == 0)

    def transition_matrix(self):

        """
        ライツアウト行列
        """

        return self.matrix.copy()

    def __repr__(self):

        return (
            f"LightsOutGraph("
            f"vertices={self.n})"
        )