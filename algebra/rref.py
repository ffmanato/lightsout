from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .field.base import Field
from .matrix import (
    augment,
    copy_matrix,
)


# ==========================================================
# Result
# ==========================================================

@dataclass(slots=True)
class RREFResult:
    """
    Result of Reduced Row Echelon Form over a finite field.
    """

    # 掃き出し後の拡大行列全体
    augmented: np.ndarray

    # 係数行列部分
    matrix: np.ndarray

    # 右辺部分（存在しない場合は None）
    rhs: np.ndarray | None

    # 使用した有限体
    field: "Field"

    # Rank
    rank: int

    # Pivot information
    pivot_rows: list[int]
    pivot_columns: list[int]

    # Free variables
    free_columns: list[int]

    # ======================================================
    # Properties
    # ======================================================

    @property
    def rows(self) -> int:
        """行数"""
        return self.matrix.shape[0]

    @property
    def cols(self) -> int:
        """列数"""
        return self.matrix.shape[1]

    @property
    def nullity(self) -> int:
        """Nullity = 列数 - Rank"""
        return self.cols - self.rank

    @property
    def pivot_count(self) -> int:
        """ピボット数"""
        return len(self.pivot_columns)

    @property
    def is_full_rank(self) -> bool:
        """フルランクか"""
        return self.rank == self.cols

    @property
    def has_rhs(self) -> bool:
        """右辺を持つか"""
        return self.rhs is not None

    @property
    def is_square(self) -> bool:
        """正方行列か"""
        return self.rows == self.cols

    def copy(self) -> "RREFResult":
        """
        RREFResult のディープコピーを返す。
        """
        return RREFResult(
            augmented=self.augmented.copy(),
            matrix=self.matrix.copy(),
            rhs=None if self.rhs is None else self.rhs.copy(),
            field=self.field,
            rank=self.rank,
            pivot_rows=self.pivot_rows.copy(),
            pivot_columns=self.pivot_columns.copy(),
            free_columns=self.free_columns.copy(),
        )

# ==========================================================
# Internal
# ==========================================================

def _rref_inplace(
    R: np.ndarray,
    coefficient_columns: int,
    field: Field,
) -> RREFResult:
    """
    Perform Gauss-Jordan elimination in-place.

    Parameters
    ----------
    R
        Matrix to transform.

    coefficient_columns
        Number of columns in the coefficient matrix.

    field
        Finite field.
    """

    rows = R.shape[0]

    pivot_rows: list[int] = []
    pivot_columns: list[int] = []

    row = 0

    for col in range(coefficient_columns):

        # --------------------------------------------------
        # Pivot search
        # --------------------------------------------------

        pivot = None

        for r in range(row, rows):

            if not field.is_zero(R[r, col]):
                pivot = r
                break

        if pivot is None:
            continue

        # --------------------------------------------------
        # Swap
        # --------------------------------------------------

        if pivot != row:
            swap_rows(R, row, pivot)

        # --------------------------------------------------
        # Normalize pivot
        # --------------------------------------------------

        pivot_value = R[row, col]

        if not field.is_one(pivot_value):

            scale = field.inv(pivot_value)

            scale_row(
                R,
                row,
                scale,
                field,
            )

        # --------------------------------------------------
        # Eliminate
        # --------------------------------------------------

        for r in range(rows):

            if r == row:
                continue

            value = R[r, col]

            if field.is_zero(value):
                continue

            scalar = field.neg(value)

            add_row_multiple(
                R,
                row,
                r,
                scalar,
                field,
            )

        pivot_rows.append(row)
        pivot_columns.append(col)

        row += 1

        if row == rows:
            break

    free_columns = pivot_columns_to_free_columns(
        coefficient_columns,
        pivot_columns,
    )

    matrix, rhs = split_augmented(
        R,
        coefficient_columns,
    )

    matrix = matrix.copy()

    if rhs.shape[1] == 0:
        rhs = None
    else:
        rhs = rhs.copy()

    return RREFResult(
        augmented=R.copy(),
        matrix=matrix,
        rhs=rhs,
        field=field,
        rank=len(pivot_columns),
        pivot_rows=pivot_rows,
        pivot_columns=pivot_columns,
        free_columns=free_columns,
    )


# ==========================================================
# Public API
# ==========================================================

def rref(
    A: np.ndarray,
    field: Field,
) -> RREFResult:
    """
    Compute the Reduced Row Echelon Form (RREF) of a coefficient matrix.

    Parameters
    ----------
    A
        Coefficient matrix.

    field
        Finite field.

    Returns
    -------
    RREFResult
    """

    return _rref_inplace(
        R=copy_matrix(A),
        coefficient_columns=A.shape[1],
        field=field,
    )


def rref_augmented(
    A: np.ndarray,
    B: np.ndarray,
    field: Field,
) -> RREFResult:
    """
    Compute the RREF of an augmented matrix [A | B].

    Parameters
    ----------
    A
        Coefficient matrix.

    B
        Right-hand side vector or matrix.

    field
        Finite field.

    Returns
    -------
    RREFResult
    """

    return _rref_inplace(
        R=augment(A, B),
        coefficient_columns=A.shape[1],
        field=field,
    )