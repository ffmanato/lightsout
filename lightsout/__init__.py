"""
lightsout パッケージ
ライツアウト問題のソルバー
"""

from .geometry.base import Geometry, Node
from .geometry.tetrahedron import Tetrahedron

from .graph.base import AdjacencyBuilder
from .graph.distance import DistanceAdjacency
from .graph.lightsout import LightsOutGraph

from .algebra.field.base import Field
from .algebra.field.gf2 import GF2
from .algebra.rref import rref, rref_augmented, RREFResult
from .algebra.solve import solve, solve_homogeneous, SolveResult
from .algebra.kernel import kernel, KernelResult

from .render.open3d import Open3DRenderer

__all__ = [
    # Geometry
    'Geometry',
    'Node',
    'Tetrahedron',
    
    # Graph
    'AdjacencyBuilder',
    'DistanceAdjacency',
    'LightsOutGraph',
    
    # Algebra - Field
    'Field',
    'GF2',
    
    # Algebra - RREF
    'rref',
    'rref_augmented',
    'RREFResult',
    
    # Algebra - Solve
    'solve',
    'solve_homogeneous',
    'SolveResult',
    
    # Algebra - Kernel
    'kernel',
    'KernelResult',
    
    # Render
    'Open3DRenderer',
]

__version__ = '0.1.0'
__author__ = 'ffmanato'
