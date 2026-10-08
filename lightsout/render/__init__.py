"""
Render module - 可視化
"""

try:
    from .open3d import Open3DRenderer
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    Open3DRenderer = None

__all__ = []

if Open3DRenderer is not None:
    __all__.append('Open3DRenderer')
