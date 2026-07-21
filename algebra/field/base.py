from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class Field(ABC):
    """
    有限体の抽象基底クラス

    GF(2), GF(3), GF(p) はこのクラスを継承して実装する。
    """

    # ======================================================
    # 基本情報
    # ======================================================

    @property
    @abstractmethod
    def order(self) -> int:
        """
        有限体の位数
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def zero(self) -> int:
        """
        加法単位元
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def one(self) -> int:
        """
        乗法単位元
        """
        raise NotImplementedError

    # ======================================================
    # スカラー演算
    # ======================================================

    @abstractmethod
    def add(self, a: int, b: int) -> int:
        """加算"""
        raise NotImplementedError

    @abstractmethod
    def sub(self, a: int, b: int) -> int:
        """減算"""
        raise NotImplementedError

    @abstractmethod
    def mul(self, a: int, b: int) -> int:
        """乗算"""
        raise NotImplementedError

    @abstractmethod
    def inv(self, a: int) -> int:
        """逆元"""
        raise NotImplementedError

    def div(self, a: int, b: int) -> int:
        """
        除算
        """
        return self.mul(a, self.inv(b))

    def neg(self, a: int) -> int:
        """
        加法逆元
        """
        return self.sub(self.zero, a)

    # ======================================================
    # 行列生成
    # ======================================================

    def zeros(
        self,
        rows: int,
        cols: int,
    ) -> np.ndarray:
        return np.zeros(
            (rows, cols),
            dtype=np.uint8,
        )

    def identity(
        self,
        n: int,
    ) -> np.ndarray:
        return np.eye(
            n,
            dtype=np.uint8,
        )

    def copy(
        self,
        A: np.ndarray,
    ) -> np.ndarray:
        return np.asarray(
            A,
            dtype=np.uint8,
        ).copy()

    # ======================================================
    # 判定
    # ======================================================

    def is_zero(
        self,
        value: int,
    ) -> bool:
        return value == self.zero

    def is_one(
        self,
        value: int,
    ) -> bool:
        return value == self.one

    def equal(
        self,
        a: int,
        b: int,
    ) -> bool:
        return a == b

    def normalize(self, value: int) -> int:
    """
    ピボットを1に正規化する係数を返す。
    GF(2)では常に1、GF(3)以上では inv(value) を返す。
    """
    return self.inv(value)