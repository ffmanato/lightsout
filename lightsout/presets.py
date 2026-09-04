"""
lightsout.presets

盤面プリセット（ジオメトリ作成ヘルパ）
"""

from __future__ import annotations

from typing import Any, Dict

from .geometry.tetrahedron import Tetrahedron


def get_preset(name: str) -> Dict[str, Any]:
    """
    プリセット辞書を返す。存在しない場合は 'tetra_3' を返す。
    名前の例: 'tetra_2', 'tetra_3', 'tetra_4'
    """
    presets: dict[str, Dict[str, Any]] = {
        'tetra_2': {'type': 'tetrahedron', 'levels': 2, 'radius': 1.0},
        'tetra_3': {'type': 'tetrahedron', 'levels': 3, 'radius': 1.0},
        'tetra_4': {'type': 'tetrahedron', 'levels': 4, 'radius': 1.0},
    }
    return presets.get(name, presets['tetra_3'])


def build_geometry(preset: Dict[str, Any]):
    """
    プリセットから Geometry オブジェクトを構築して返す。
    今は Tetrahedron のみ対応。
    """
    t = preset
    if t.get('type') == 'tetrahedron':
        return Tetrahedron(levels=int(t.get('levels', 3)), radius=float(t.get('radius', 1.0)))
    raise ValueError(f"Unknown preset type: {t.get('type')}")
