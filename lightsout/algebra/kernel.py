from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .field.base import Field
from .rref import (
    RREFResult,
    rref,
)


# ==========================================================
# Result
# ==========================================================

@dataclass(slots=True)
class KernelResult:
    """
    Result of computing the null space of a matrix
    over a finite field.

    The basis vectors are stored as columns.
    """

    #
    # Basis matrix
    #
    basis: np.ndarray

    #
    # RREF
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
    def dimension(self) -> int:
        """
        Dimension of the null space.
        """
        return self.nullity

    @property
    def rows(self) -> int:
        """
        Number of variables.
        """
        return self.rref.cols

    @property
    def cols(self) -> int:
        """
        Number of basis vectors.
        """
        return self.basis.shape[1]

    @property
    def is_trivial(self) -> bool:
        """
        True iff the null space is {0}.
        """
        return self.dimension == 0

# ==========================================================
# Public
# ==========================================================

def kernel_from_rref(
    result: RREFResult,
) -> KernelResult:
    """
    Compute a basis of the null space from an RREF result.
    """

    field = result.field

    #
    # Trivial kernel
    #

    if result.nullity == 0:

        basis = np.zeros(
            (result.cols, 0),
            dtype=result.matrix.dtype,
        )

        return KernelResult(
            basis=basis,
            rref=result,
        )

    #
    # Allocate basis matrix
    #

    basis = np.zeros(
        (
            result.cols,
            result.nullity,
        ),
        dtype=result.matrix.dtype,
    )

    #
    # Construct basis vectors
    #

    for k, free_col in enumerate(result.free_columns):

        #
        # Free variable = 1
        #

        basis[free_col, k] = field.one

        #
        # Pivot variables
        #

        for row, pivot_col in zip(
            result.pivot_rows,
            result.pivot_columns,
        ):

            coefficient = result.matrix[
                row,
                free_col,
            ]

            basis[pivot_col, k] = field.neg(
                coefficient
            )

    return KernelResult(
        basis=basis,
        rref=result,
    )

# ==========================================================
# Public API
# ==========================================================

def kernel(
    A: np.ndarray,
    field: Field,
) -> KernelResult:
    """
    Compute a basis of the null space of A.

    Parameters
    ----------
    A
        Coefficient matrix.

    field
        Finite field.

    Returns
    -------
    KernelResult
    """

    result = rref(
        A,
        field,
    )

    return kernel_from_rref(result)
