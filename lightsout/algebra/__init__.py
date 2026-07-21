"""
Algebra module - 有限体上の線形方程式求解
"""

from .field import Field, GF2
from .rref import rref, rref_augmented, RREFResult
from .solve import solve, solve_homogeneous, SolveResult
from .kernel import kernel, KernelResult

__all__ = [
    # Field
    'Field',
    'GF2',
    
    # RREF
    'rref',
    'rref_augmented',
    'RREFResult',
    
    # Solve
    'solve',
    'solve_homogeneous',
    'SolveResult',
    
    # Kernel
    'kernel',
    'KernelResult',
]
