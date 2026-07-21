from __future__ import annotations

from .base import Field


class GF2(Field):
    """
    Galois Field GF(2)

    Elements
    --------
    {0, 1}
    """

    # ======================================================
    # Basic information
    # ======================================================

    @property
    def order(self) -> int:
        return 2

    @property
    def zero(self) -> int:
        return 0

    @property
    def one(self) -> int:
        return 1

    # ======================================================
    # Scalar arithmetic
    # ======================================================

    def add(
        self,
        a: int,
        b: int,
    ) -> int:
        """
        a + b (mod 2)
        """
        return (a ^ b) & 1

    def sub(
        self,
        a: int,
        b: int,
    ) -> int:
        """
        a - b (mod 2)
        """
        return (a ^ b) & 1

    def mul(
        self,
        a: int,
        b: int,
    ) -> int:
        """
        a * b (mod 2)
        """
        return (a & b) & 1

    def inv(
        self,
        a: int,
    ) -> int:
        """
        Multiplicative inverse
        """

        if a == 0:
            raise ZeroDivisionError(
                "0 has no multiplicative inverse in GF(2)."
            )

        return 1

    # ======================================================
    # Helpers
    # ======================================================

    def normalize(
        self,
        value: int,
    ) -> int:
        """
        Normalize pivot to 1.

        In GF(2), every non-zero element is already 1.
        """
        return self.inv(value)