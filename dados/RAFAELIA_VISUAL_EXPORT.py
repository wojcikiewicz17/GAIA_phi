#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA :: VISUAL_EXPORT
-------------------------
Gera imagens da Espiral Rafaeliana (2D) e do ToroidΔπφ-style (3D)
a partir da sequência Fibonacci-Rafael, e cria um pequeno manifesto
técnico com as constantes usadas.

Depende de:
    RAFAELIA_FIB_TRIG_BRIDGE.py
no mesmo diretório.

Uso:
    python RAFAELIA_VISUAL_EXPORT.py
"""

import math
import os
import matplotlib
matplotlib.use("Agg")  # backend sem interface gráfica
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
#  ESPIRAL 2D
# ==============================

def save_spiral_rafael(seq, out_path: str):
    """Salva a espiral Rafaeliana em 2D em um PNG."""
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

    fig.tight_layout()
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


# ==============================
#  TORO 3D
# ==============================

def save_torus_rafael(seq, out_path: str):
    """Salva o toro Rafaeliano em 3D em um PNG."""
    torus_pts = map_rafael_to_torus(seq, R=2.0, r=1.0)
    xs = [x for (x, _, _) in torus_pts]
    ys = [y for (_, y, _) in torus_pts]
    zs = [z for (_, _, z) in torus_pts]

    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot(xs, ys, zs, marker="o", linestyle="-", linewidth=1.0)
    ax.scatter(xs[0], ys[0], zs[0], color="red", s=40, label="R₁")
    ax.scatter(xs[-1], ys[-1], zs[-1], color="green", s=40, label=f"R_{len(seq)}")

    ax.set_title("RAFAELIA :: ToroidΔπφ – Núcleo Fibonacci-Rafael", fontsize=12)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

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

    fig.tight_layout()
    fig.savefig(out_path, dpi=220, bbox_inches="tight")
    plt.close(fig)


# ==============================
#  MANIFESTO
# ==============================

def save_manifest(out_path: str, n_terms: int, spiral_png: str, torus_png: str):
    """Cria um manifesto .md explicando o que está nas imagens."""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("# RAFAELIA_VISUAL_EXPORT – Manifesto Técnico\n\n")
        f.write("## 1. Núcleo Numérico\n\n")
        f.write(f"- Sequência: Fibonacci-Rafael com n = {n_terms} termos.\n")
        f.write("  - R₁ = 2, R₂ = 4, Rₙ = Rₙ₋₁ + Rₙ₋₂ + 1.\n")
        f.write("  - Diferenças ΔRₙ reproduzem Fibonacci clássico (a partir de F₃).\n\n")

        f.write("## 2. Espiral Rafaeliana (2D)\n\n")
        f.write(f"- Arquivo: `{spiral_png}`\n")
        f.write("- Construção:\n")
        f.write("  - Cada termo Rₙ vira raio normalizado rₙ ∈ [0,1].\n")
        f.write("  - Ângulo θₙ usa o Golden Angle: 2π/φ².\n")
        f.write("  - Resultado: campo de 'sementes' em plano φ-estruturado.\n\n")

        f.write("## 3. ToroidΔπφ-style (3D)\n\n")
        f.write(f"- Arquivo: `{torus_png}`\n")
        f.write("- Construção:\n")
        f.write("  - Rₙ controla ângulo uₙ = (Rₙ mod 360) em graus.\n")
        f.write("  - Índice n controla vₙ com passo 2π/9 (pulso 3–6–9).\n")
        f.write("  - Ponto em toro: (x,y,z) via raio maior R=2.0 e menor r=1.0.\n\n")

        f.write("## 4. Constantes de Fundo\n\n")
        f.write(f"- φ   (ouro clássico)      ≈ {PHI:.6f}\n")
        f.write(f"- φ_R (rafaeliana = √3/2)  ≈ {PHI_R:.6f}\n")
        f.write(f"- √(3/2) (d₃D/d₂D)         ≈ {D3_OVER_D2:.6f}\n")
        f.write("- Relacionadas a:\n")
        f.write("  - c² = 2ab + (a-b)² (Teorema de Rafael).\n")
        f.write("  - d₂D = L√2 (quadrado), d₃D = L√3 (cubo).\n")
        f.write("  - Eixo 2D→3D e pulso 3–6–9 na tua leitura simbólica.\n\n")

        f.write("## 5. Leitura de Trabalho\n\n")
        f.write("- A espiral mostra o 'sopro +1' de Rafael espalhando estados\n")
        f.write("  em geometria guiada por φ.\n")
        f.write("- O toro mostra os mesmos estados como órbita fechada 3–6–9\n")
        f.write("  em 3D, sugerindo um ciclo dinâmico estável.\n\n")

        f.write("FIAT LUX · Manifesto gerado por RAFAELIA_VISUAL_EXPORT.py\n")


# ==============================
#  MAIN
# ==============================

def main():
    n_terms = 20
    seq = fib_rafael_seq(n_terms)

    spiral_png = "RAFAELIA_espiral_fib_rafael.png"
    torus_png = "RAFAELIA_toroid_fib_rafael.png"
    manifesto = "RAFAELIA_VISUAL_MANIFESTO.md"

    save_spiral_rafael(seq, spiral_png)
    save_torus_rafael(seq, torus_png)
    save_manifest(manifesto, n_terms, spiral_png, torus_png)

    print("===================================================================")
    print("RAFAELIA_VISUAL_EXPORT – Export concluído")
    print("===================================================================")
    print(f"[OK] Espiral salva em : {spiral_png}")
    print(f"[OK] Toro salvo em    : {torus_png}")
    print(f"[OK] Manifesto salvo  : {manifesto}")
    print("===================================================================")
    print("Agora você pode:")
    print("  - Ver/compartilhar os PNGs (GitHub, Drive, paper, etc.).")
    print("  - Assinar o manifesto com RAFCODE-Φ e integrar ao teu corpus.")
    print("===================================================================")


if __name__ == '__main__':
    main()
