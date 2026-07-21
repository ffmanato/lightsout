from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .field.base import Field
from .matrix import (
    find_inconsistent_rows,
)
from .rref import (
    RREFResult,
    rref_augmented,
)


# ==========================================================
# Result
# ==========================================================

@dataclass(slots=True)
class SolveResult:
    """
    Result of solving Ax = b over a finite field.
    """

    #
    # Existence
    #
    is_solvable: bool

    #
    # Uniqueness
    #
    has_unique_solution: bool

    #
    # Particular solution
    #
    particular_solution: np.ndarray | None

    #
    # RREF result
    #
    rref: RREFResult

    # ======================================================
    # Properties
    # ======================================================

    @property
    def field(self) -> Field:
        return self.rref.field

    @property
    def rank(self) -> int:
        return self.rref.rank

    @property
    def nullity(self) -> int:
        return self.rref.nullity

    @property
    def rows(self) -> int:
        return self.rref.rows

    @property
    def cols(self) -> int:
        return self.rref.cols

    @property
    def pivot_columns(self) -> list[int]:
        return self.rref.pivot_columns

    @property
    def free_columns(self) -> list[int]:
        return self.rref.free_columns


# ==========================================================
# Internal helpers
# ==========================================================

def _check_solvable(
    rref: RREFResult,
) -> bool:
    """
    Check whether Ax = b is solvable.
    """

    if rref.rhs is None:
        return True

    inconsistent = find_inconsistent_rows(
        rref.augmented,
        rref.cols,
        rref.field,
    )

    return len(inconsistent) == 0


def _build_particular_solution(
    rref: RREFResult,
) -> np.ndarray:
    """
    Construct one particular solution from an RREF matrix.

    Free variables are set to zero.
    """

    field = rref.field

    x = np.full(
        rref.cols,
        field.zero,
        dtype=np.uint8,
    )

    if rref.rhs is None:
        return x

    rhs = rref.rhs[:, 0]

    #
    # Pivot variables
    #

    for row, col in zip(
        rref.pivot_rows,
        rref.pivot_columns,
    ):

        x[col] = rhs[row]

    return x


# ==========================================================
# Public
# ==========================================================

def solve_from_rref(
    result: RREFResult,
) -> SolveResult:
    """
    Solve Ax = b from an already computed RREF.
    """

    #
    # Check consistency
    #

    solvable = _check_solvable(result)

    if not solvable:

        return SolveResult(
            is_solvable=False,
            has_unique_solution=False,
            particular_solution=None,
            rref=result,
        )

    #
    # Construct one particular solution
    #

    field = result.field

    x = np.full(
        result.cols,
        field.zero,
        dtype=np.uint8,
    )

    if result.rhs is not None:

        rhs = result.rhs[:, 0]

        #
        # Free variables are fixed to zero.
        #
        # Therefore each pivot variable is simply
        # the corresponding RHS entry.
        #

        for row, col in zip(
            result.pivot_rows,
            result.pivot_columns,
        ):

            x[col] = rhs[row]

    #
    # Unique solution ?
    #

    unique = (
        result.rank
        ==
        result.cols
    )

    return SolveResult(
        is_solvable=True,
        has_unique_solution=unique,
        particular_solution=x,
        rref=result,
    )

# ==========================================================
# Public API
# ==========================================================

def solve(
    A: np.ndarray,
    b: np.ndarray,
    field: Field,
) -> SolveResult:
    """
    Solve the linear system

        Ax = b

    over a finite field.

    Parameters
    ----------
    A
        Coefficient matrix.

    b
        Right-hand side vector or matrix.

    field
        Finite field.

    Returns
    -------
    SolveResult
    """

    result = rref_augmented(
        A,
        b,
        field,
    )

    return solve_from_rref(result)


def solve_homogeneous(
    A: np.ndarray,
    field: Field,
) -> SolveResult:
    """
    Solve the homogeneous system

        Ax = 0

    over a finite field.

    This simply computes one particular solution,
    which is always the zero vector.
    """

    b = np.full(
        A.shape[0],
        field.zero,
        dtype=np.uint8,
    )

    return solve(
        A,
        b,
        field,
    )