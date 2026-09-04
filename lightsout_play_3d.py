"""
Lights Out 3D playable demo.

Controls
--------
- Shift + Left Click: select a node
- Q / Esc: apply selected move
- Q / Esc with no selection: quit
"""

from __future__ import annotations

import numpy as np

from lightsout import (
    Tetrahedron,
    DistanceAdjacency,
    LightsOutGraph,
    Open3DRenderer
)


def create_playable_state(
    game: LightsOutGraph,
    press_count: int
) -> np.ndarray:
    """
    空盤面からランダムに押して、解ける初期盤面を作る。
    """

    while True:
        sequence = np.random.randint(
            0,
            game.size(),
            size=press_count
        )

        state = game.press_sequence(
            game.empty_state(),
            sequence
        )

        if not game.is_solved(state):
            return state


def main():
    print("=" * 60)
    print("Lights Out 3D Playable Demo")
    print("=" * 60)

    levels = 3
    radius = 1.0

    geo = Tetrahedron(
        levels=levels,
        radius=radius
    )

    adjacency = DistanceAdjacency(
        radius=radius,
        tolerance=1e-6
    ).build(geo)

    game = LightsOutGraph(
        adjacency=adjacency,
        include_self=True
    )

    initial_state = create_playable_state(
        game=game,
        press_count=max(1, game.size())
    )

    renderer = Open3DRenderer(
        show_coordinate_frame=True
    )

    _, moves, cleared = renderer.play_lights_out(
        geometry=geo,
        game=game,
        initial_state=initial_state
    )

    print("\n" + "=" * 60)
    print(f"Result: {'CLEARED' if cleared else 'QUIT'}")
    print(f"Moves: {moves}")
    print("=" * 60)


if __name__ == "__main__":
    main()
