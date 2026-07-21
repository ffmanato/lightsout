from __future__ import annotations

import numpy as np

from .field.base import Field


# ==========================================================
# Matrix creation
# ==========================================================

def copy_matrix(A: np.ndarray) -> np.ndarray:
    """
    Return a deep copy of a matrix.
    """
    return np.asarray(A, dtype=np.uint8).copy()


def zeros(
    rows: int,
    cols: int,
) -> np.ndarray:
    """
    Create a zero matrix.
    """
    return np.zeros((rows, cols), dtype=np.uint8)


def identity(
    n: int,
    field: Field,
) -> np.ndarray:
    """
    Create an identity matrix.
    """
    I = np.zeros((n, n), dtype=np.uint8)

    for i in range(n):
        I[i, i] = field.one

    return I


# ==========================================================
# Augmented matrix
# ==========================================================

def augment(
    A: np.ndarray,
    B: np.ndarray,
) -> np.ndarray:
    """
    Construct [A | B].
    """

    A = np.asarray(A, dtype=np.uint8)
    B = np.asarray(B, dtype=np.uint8)

    if B.ndim == 1:
        B = B.reshape(-1, 1)

    if A.shape[0] != B.shape[0]:
        raise ValueError("Row sizes do not match.")

    return np.hstack((A, B))


def split_augmented(
    Aug: np.ndarray,
    coefficient_columns: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Split [A | B].
    """

    return (
        Aug[:, :coefficient_columns],
        Aug[:, coefficient_columns:],
    )


# ==========================================================
# Row operations
# ==========================================================

def swap_rows(
    A: np.ndarray,
    i: int,
    j: int,
) -> None:
    """
    Swap two rows.
    """

    if i == j:
        return

    A[[i, j]] = A[[j, i]]


def scale_row(
    A: np.ndarray,
    row: int,
    scalar: int,
    field: Field,
) -> None:
    """
    Multiply a row by a scalar.
    """

    for c in range(A.shape[1]):
        A[row, c] = field.mul(A[row, c], scalar)


def add_row_multiple(
    A: np.ndarray,
    src: int,
    dst: int,
    scalar: int,
    field: Field,
) -> None:
    """
    Row(dst) ← Row(dst) + scalar × Row(src)
    """

    for c in range(A.shape[1]):

        value = field.mul(
            A[src, c],
            scalar,
        )

        A[dst, c] = field.add(
            A[dst, c],
            value,
        )


# ==========================================================
# Row predicates
# ==========================================================

def is_zero_row(
    row: np.ndarray,
    field: Field,
) -> bool:
    """
    Return True if every element is zero.
    """

    return all(
        field.is_zero(v)
        for v in row
    )


def is_inconsistent_row(
    row: np.ndarray,
    coefficient_columns: int,
    field: Field,
) -> bool:
    """
    Check whether a row represents

        0 ... 0 | b

    where b ≠ 0.
    """

    left = row[:coefficient_columns]
    right = row[coefficient_columns:]

    return (
        is_zero_row(left, field)
        and any(
            not field.is_zero(v)
            for v in right
        )
    )


def find_inconsistent_rows(
    Aug: np.ndarray,
    coefficient_columns: int,
    field: Field,
) -> list[int]:
    """
    Return the indices of inconsistent rows.
    """

    rows = []

    for i in range(Aug.shape[0]):

        if is_inconsistent_row(
            Aug[i],
            coefficient_columns,
            field,
        ):
            rows.append(i)

    return rows


# ==========================================================
# Utilities
# ==========================================================

def pivot_columns_to_free_columns(
    cols: int,
    pivot_columns: list[int],
) -> list[int]:
    """
    Compute free columns from pivot columns.
    """

    pivots = set(pivot_columns)

    return [
        c
        for c in range(cols)
        if c not in pivots
    ]


def rank_from_rref(
    A: np.ndarray,
    field: Field,
) -> int:
    """
    Compute the rank of an RREF matrix.
    """

    rank = 0

    for row in A:

        if not is_zero_row(row, field):
            rank += 1

    return rank


def is_square(
    A: np.ndarray,
) -> bool:
    """
    Return True if the matrix is square.
    """

    return A.shape[0] == A.shape[1]