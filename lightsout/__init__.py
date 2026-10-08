"""
lightsout パッケージ
ライツアウト問題のソルバー
"""

from .geometry.base import Geometry, Node
from .geometry.tetrahedron import Tetrahedron
from .geometry.octahedron import Octahedron
from .geometry.dodecahedron import Dodecahedron

from .graph.base import AdjacencyBuilder
from .graph.distance import DistanceAdjacency
from .graph.lightsout import LightsOutGraph

from .algebra.field.base import Field
from .algebra.field.gf2 import GF2
from .algebra.rref import rref, rref_augmented, RREFResult
from .algebra.solve import solve, solve_homogeneous, SolveResult
from .algebra.kernel import kernel, KernelResult

try:
    from .render.open3d import Open3DRenderer
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    Open3DRenderer = None

__all__ = [
    # Geometry
    'Geometry',
    'Node',
    'Tetrahedron',
    'Octahedron',
    'Dodecahedron',
    
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
    
]

if Open3DRenderer is not None:
    __all__.append('Open3DRenderer')

__version__ = '0.1.0'
__author__ = 'ffmanato'
