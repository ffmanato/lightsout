"""
Lights Out ソルバー - 統合デモスクリプト

このスクリプトは、ライツアウト問題を解くための統合的な例を示します。
以下の手順で実行されます：

1. 正四面体格子の盤面を作成
2. 距離ベースの隣接行列を生成
3. ゲームグラフを構築
4. ランダムな盤面を生成
5. 線形方程式 Ax = b を GF(2) で求解
6. 3D可視化で結果を表示
"""

from lightsout import (
    Tetrahedron,
    DistanceAdjacency,
    LightsOutGraph,
    GF2,
    solve,
    Open3DRenderer
)


def main():
    """メイン処理"""
    
    print("=" * 60)
    print("Lights Out Solver - 統合デモ")
    print("=" * 60)
    
    # ========================================================
    # 1. 盤面の作成
    # ========================================================
    print("\n[Step 1] 盤面の作成")
    print("-" * 60)
    
    levels = 3
    radius = 1.0
    geo = Tetrahedron(levels=levels, radius=radius)
    
    print(f"✓ 正四面体格子を作成しました")
    print(f"  - レベル数: {levels}")
    print(f"  - 半径: {radius}")
    print(f"  - ノード数: {len(geo)}")
    print(f"  - {geo}")
    
    # ========================================================
    # 2. 隣接行列の生成
    # ========================================================
    print("\n[Step 2] 隣接行列の生成")
    print("-" * 60)
    
    adj_builder = DistanceAdjacency(radius=radius, tolerance=1e-6)
    adjacency = adj_builder.build(geo)
    
    print(f"✓ 隣接行列を生成しました")
    print(f"  - 行列サイズ: {adjacency.shape[0]}×{adjacency.shape[1]}")
    print(f"  - 非ゼロ要素数: {adjacency.sum()}")
    print(f"  - 密度: {adjacency.sum() / (adjacency.shape[0] * adjacency.shape[1]) * 100:.2f}%")
    
    # ========================================================
    # 3. ゲームグラフの構築
    # ========================================================
    print("\n[Step 3] ゲームグラフの構築")
    print("-" * 60)
    
    game = LightsOutGraph(adjacency, include_self=True)
    
    print(f"✓ ゲームグラフを構築しました")
    print(f"  - {game}")
    print(f"  - 遷移行列サイズ: {game.get_matrix().shape}")
    
    # ========================================================
    # 4. ランダムな盤面の生成
    # ========================================================
    print("\n[Step 4] ランダムな盤面の生成")
    print("-" * 60)
    
    state = game.random_state()
    
    print(f"✓ ランダムな盤面を生成しました")
    print(f"  - 初期状態: {state}")
    print(f"  - 点灯数: {state.sum()}")
    print(f"  - 消灯数: {len(state) - state.sum()}")
    
    # ========================================================
    # 5. 線形方程式の求解
    # ========================================================
    print("\n[Step 5] 線形方程式 Ax = b の求解")
    print("-" * 60)
    
    matrix = game.transition_matrix()
    field = GF2()
    
    print(f"求解中...")
    print(f"  - 係数行列: {matrix.shape}")
    print(f"  - 体: GF(2)")
    
    result = solve(matrix, state, field)
    
    print(f"\n✓ 方程式を求解しました")
    print(f"  - 可解性: {'可解' if result.is_solvable else '不可解'}")
    
    if result.is_solvable:
        print(f"  - 一意解: {'あり' if result.has_unique_solution else 'なし'}")
        print(f"  - ランク: {result.rank}")
        print(f"  - 零化度: {result.nullity}")
        
        if result.particular_solution is not None:
            sol = result.particular_solution
            print(f"  - 特解: {sol}")
            print(f"    - スイッチを押す数: {sol.sum()}")
            
            # 検証
            result_state = game.press_sequence(state, [i for i, v in enumerate(sol) if v == 1])
            is_solved = game.is_solved(result_state)
            print(f"    - 検証: {'成功 ✓' if is_solved else '失敗 ✗'}")
    else:
        print(f"  - この盤面は解くことができません")
    
    # ========================================================
    # 6. 3D可視化
    # ========================================================
    print("\n[Step 6] 3D可視化")
    print("-" * 60)
    
    print("Open3Dビューアを起動します...")
    print("（マウスで回転、スクロールでズーム、右クリックでパン）")
    
    renderer = Open3DRenderer(
        sphere_resolution=20,
        sphere_color=(0.2, 0.6, 1.0),
        show_coordinate_frame=True
    )
    renderer.draw(geo)
    
    print("\nビューアを閉じました")
    
    # ========================================================
    # 完了
    # ========================================================
    print("\n" + "=" * 60)
    print("デモンストレーション完了！")
    print("=" * 60)


if __name__ == '__main__':
    main()
