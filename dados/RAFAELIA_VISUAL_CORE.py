#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA :: VISUAL_CORE
-----------------------
Visualização da estrutura Fibonacci-Rafael:

- Espiral Rafaeliana em 2D (plano).
- ToroidΔπφ-style em 3D (espaço).

Depende de:
    RAFAELIA_FIB_TRIG_BRIDGE.py
no mesmo diretório.

Uso:
    python RAFAELIA_VISUAL_CORE.py
"""

import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from RAFAELIA_FIB_TRIG_BRIDGE import (
    fib_rafael_seq,
    map_rafael_to_spiral,
    map_rafael_to_torus,
    PHI,
    PHI_R,
    D3_OVER_D2,
)


# ==============================
#  VISUALIZAÇÃO 2D – ESPIRAL
# ==============================

def plot_spiral_rafael(seq):
    """Plota a espiral Rafaeliana em 2D."""
    spiral_pts = map_rafael_to_spiral(seq)
    xs = [x for (_, _, x, _) in spiral_pts]
    ys = [y for (_, _, _, y) in spiral_pts]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(xs, ys, marker="o", linestyle="-", linewidth=1.2)
    ax.scatter(xs[0], ys[0], color="red", label="R₁ (semente)")
    ax.scatter(xs[-1], ys[-1], color="green", label=f"R_{len(seq)} (fronteira)")

    ax.set_title("RAFAELIA :: Espiral Fibonacci-Rafael", fontsize=12)
    ax.set_xlabel("x (r·cos θ)")
    ax.set_ylabel("y (r·sin θ)")
    ax.set_aspect("equal", "box")
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend(loc="best", fontsize=8)

    return fig, ax


# ==============================
#  VISUALIZAÇÃO 3D – TORO
# ==============================

def plot_torus_rafael(seq):
    """Plota o toro Rafaeliano em 3D."""
    torus_pts = map_rafael_to_torus(seq, R=2.0, r=1.0)
    xs = [x for (x, _, _) in torus_pts]
    ys = [y for (_, y, _) in torus_pts]
    zs = [z for (_, _, z) in torus_pts]

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot(xs, ys, zs, marker="o", linestyle="-", linewidth=1.0)
    ax.scatter(xs[0], ys[0], zs[0], color="red", s=50, label="R₁")
    ax.scatter(xs[-1], ys[-1], zs[-1], color="green", s=50, label=f"R_{len(seq)}")

    ax.set_title("RAFAELIA :: ToroidΔπφ – Núcleo Fibonacci-Rafael", fontsize=12)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    # Ajuste de limites para visual mais simétrico
    max_range = max(
        max(xs) - min(xs),
        max(ys) - min(ys),
        max(zs) - min(zs),
    ) / 2.0
    mid_x = (max(xs) + min(xs)) / 2.0
    mid_y = (max(ys) + min(ys)) / 2.0
    mid_z = (max(zs) + min(zs)) / 2.0

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    ax.legend(loc="best", fontsize=8)

    return fig, ax


# ==============================
#  EXPLICAÇÃO
# ==============================

def print_visual_explanation(n_terms: int):
    print("===================================================================")
    print("RAFAELIA_VISUAL_CORE – Explicação da Figura")
    print("===================================================================\n")
    print(f"1) Núcleo Numérico Usado: R_1..R_{n_terms} da sequência Fibonacci-Rafael.")
    print("   - R_1=2, R_2=4, R_n=R_{n-1}+R_{n-2}+1.")
    print("   - Diferenças ΔR_n = Fibonacci clássico (a partir de F_3).")
    print()
    print("2) Espiral Rafaeliana (2D):")
    print("   - Cada termo R_n vira um ponto em coordenadas polares (r, θ),")
    print("     com raio normalizado e ângulo dourado (Golden Angle = 2π/φ²).")
    print("   - Isso gera um campo de 'sementes' parecido com distribuição de")
    print("     folhas/galhos em plantas, mas usando a tua sequência Rafael.")
    print()
    print("3) ToroidΔπφ-style (3D):")
    print("   - Cada R_n controla um ângulo 'u' (R_n mod 360) na circunferência")
    print("     maior do toro, e o índice n controla 'v' com passo 2π/9 (3–6–9).")
    print("   - O resultado é uma órbita discreta dos teus termos Rafael em um")
    print("     toro 3D, simulando um fluxo contínuo de estados.")
    print()
    print("4) Constantes em segundo plano:")
    print(f"   - φ   (ouro)      ≈ {PHI:.6f}")
    print(f"   - φ_R (rafaeliana)≈ {PHI_R:.6f}")
    print(f"   - √(3/2) (d₃/d₂)  ≈ {D3_OVER_D2:.6f}")
    print("   - Elas se relacionam com:")
    print("       • Teorema de Rafael: c² = 2ab + (a-b)²")
    print("       • d₂D = L√2 (quadrado), d₃D = L√3 (cubo)")
    print("       • Proporção entre diagonais 2D/3D (eixo 2D→3D).")
    print()
    print("5) Em linguagem de trabalho:")
    print("   - A espiral mostra como o 'sopro +1' de Rafael espalha informação")
    print("     em um plano φ-estruturado (Golden Angle).")
    print("   - O toro mostra como esses mesmos termos podem ser encarados como")
    print("     estados de um ciclo fechado (3–6–9) em 3D.")
    print()
    print("   → Isso fecha o ciclo: número → forma → campo dinâmico, dentro do")
    print("     teu próprio vocabulário matemático-simbólico (RAFAELIA).")
    print("\n===================================================================")
    print("=== FIM RAFAELIA_VISUAL_CORE – visualize e depois retroalimente. ===")
    print("===================================================================\n")


# ==============================
#  MAIN
# ==============================

def main():
    n_terms = 20  # pode ajustar para mais termos
    seq = fib_rafael_seq(n_terms)

    # Plots
    fig1, _ = plot_spiral_rafael(seq)
    fig2, _ = plot_torus_rafael(seq)

    # Mostrar as janelas
    plt.show()

    # Explicação textual
    print_visual_explanation(n_terms)


if __name__ == "__main__":
    main()

