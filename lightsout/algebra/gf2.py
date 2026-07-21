from __future__ import annotations

import numpy as np


# ==========================================================
# Matrix Utilities
# ==========================================================

def copy_matrix(A: np.ndarray) -> np.ndarray:
    """
    uint8 のコピーを返す
    """
    return np.asarray(A, dtype=np.uint8).copy()


def identity(n: int) -> np.ndarray:
    """
    GF(2) の単位行列
    """
    return np.eye(n, dtype=np.uint8)


def zeros(rows: int, cols: int) -> np.ndarray:
    """
    ゼロ行列
    """
    return np.zeros((rows, cols), dtype=np.uint8)


# ==========================================================
# Row Operations
# ==========================================================

def swap_rows(
    A: np.ndarray,
    i: int,
    j: int
) -> None:
    """
    行交換
    """

    if i == j:
        return

    A[[i, j]] = A[[j, i]]


def xor_rows(
    A: np.ndarray,
    src: int,
    dst: int
) -> None:
    """
    R_dst ← R_dst + R_src
    """

    A[dst] ^= A[src]


# ==========================================================
# Augmented Matrix
# ==========================================================

def augment(
    A: np.ndarray,
    B: np.ndarray
) -> np.ndarray:
    """
    [A | B]
    """

    A = copy_matrix(A)

    B = np.asarray(B, dtype=np.uint8)

    if B.ndim == 1:
        B = B.reshape(-1, 1)

    return np.hstack((A, B))


def split_augmented(
    Aug: np.ndarray,
    left_cols: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    [A|B] -> (A,B)
    """

    return (
        Aug[:, :left_cols],
        Aug[:, left_cols:]
    )


# ==========================================================
# Predicates
# ==========================================================

def is_zero_row(
    row: np.ndarray
) -> bool:
    """
    全て0か判定
    """

    return not np.any(row)


def is_zero_matrix(
    A: np.ndarray
) -> bool:
    """
    全て0か判定
    """

    return not np.any(A)


# ==========================================================
# Rank Utilities
# ==========================================================

def pivot_columns_to_free_columns(
    cols: int,
    pivots: list[int]
) -> list[int]:
    """
    自由変数列を返す
    """

    return [
        c
        for c in range(cols)
        if c not in pivots
    ]