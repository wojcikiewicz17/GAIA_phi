#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA :: FIB_TRIG_BRIDGE
---------------------------
Ponte entre a sequência Fibonacci-Rafael e estruturas geométricas:

- Sequência Rafael (R_n).
- Diferenças = Fibonacci clássico.
- Razões → φ.
- Mapeamento para:
    • Espiral polar (R_n em coordenadas (r, θ)).
    • Toroide simples (ToroidΔπφ-style).
    • Ciclo simbólico 3–6–9 por índice.

Uso:
    python RAFAELIA_FIB_TRIG_BRIDGE.py
"""

import math
from typing import List, Tuple

# ==============================
#  CONSTANTES
# ==============================

PHI = (1.0 + math.sqrt(5.0)) / 2.0
SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
PHI_R = SQRT3 / 2.0
D3_OVER_D2 = SQRT3 / SQRT2
TAU = 2.0 * math.pi


# ==============================
#  FIBONACCI CLÁSSICO / RAFAEL
# ==============================

def fib_classic_seq(n: int) -> List[int]:
    """Retorna [F_1, ..., F_n] (Fibonacci clássico, F_1=1,F_2=1)."""
    if n <= 0:
        raise ValueError("n deve ser >= 1")
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


def fib_rafael_seq(n: int) -> List[int]:
    """
    Sequência Fibonacci-Rafael:

        R_1 = 2
        R_2 = 4
        R_n = R_{n-1} + R_{n-2} + 1
    """
    if n <= 0:
        raise ValueError("n deve ser >= 1")
    if n == 1:
        return [2]
    if n == 2:
        return [2, 4]

    seq = [2, 4]
    for _ in range(3, n + 1):
        a, b = seq[-2], seq[-1]
        seq.append(a + b + 1)
    return seq


def rafael_diffs(seq: List[int]) -> List[int]:
    """Diferenças ΔR_n = R_n - R_{n-1}."""
    return [seq[i] - seq[i - 1] for i in range(1, len(seq))]


def rafael_ratios(seq: List[int]) -> List[float]:
    """Razões sucessivas R_{n+1}/R_n."""
    return [seq[i + 1] / seq[i] for i in range(len(seq) - 1)]


def triad_tag(index: int) -> int:
    """
    Ciclo 3–6–9 simbólico por índice n.

      n ≡ 1 (mod 3) -> 3
      n ≡ 2 (mod 3) -> 6
      n ≡ 0 (mod 3) -> 9
    """
    r = index % 3
    return 3 if r == 1 else 6 if r == 2 else 9


# ==============================
#  MAPAS GEOMÉTRICOS
# ==============================

def map_rafael_to_spiral(seq: List[int]) -> List[Tuple[float, float, float, float]]:
    """
    Mapeia R_n para uma espiral polar em R².

    Estratégia:
        - raio r_n = R_n / R_max  (normalizado)
        - ângulo θ_n = n * θ₀, onde θ₀ é o "golden angle" = 2π/φ²

    Retorna lista de (r, θ, x, y) com:
        x = r cos θ
        y = r sin θ
    """
    if not seq:
        return []

    r_max = float(max(seq))
    golden_angle = TAU / (PHI ** 2)  # ângulo dourado

    mapped = []
    for n, Rn in enumerate(seq, start=1):
        r = Rn / r_max
        theta = n * golden_angle
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        mapped.append((r, theta, x, y))
    return mapped


def map_rafael_to_torus(
    seq: List[int],
    R: float = 2.0,
    r: float = 1.0,
) -> List[Tuple[float, float, float]]:
    """
    Mapeia R_n em um toro 3D simples.

    Parametrização:
        - u_n = (R_n mod 360) em radianos
        - v_n = n * (2π/9)         (pulso 3–6–9 ao longo do tubo)

    Equações padrão do toro:
        x = (R + r cos v) cos u
        y = (R + r cos v) sin u
        z = r sin v
    """
    mapped = []
    for n, Rn in enumerate(seq, start=1):
        u = math.radians(Rn % 360)
        v = (n * TAU) / 9.0
        x = (R + r * math.cos(v)) * math.cos(u)
        y = (R + r * math.cos(v)) * math.sin(u)
        z = r * math.sin(v)
        mapped.append((x, y, z))
    return mapped


# ==============================
#  SNAPSHOT GEOMÉTRICO RAFAEL
# ==============================

def snapshot_geom(L: float = 3.0, a: float = 3.0, b: float = 2.0):
    c2 = 2 * a * b + (a - b) ** 2
    c = math.sqrt(c2)
    d2 = L * SQRT2
    d3 = L * SQRT3

    print("[ Snapshot Geométrico – Teorema de Rafael ]")
    print(f"a = {a:.1f}, b = {b:.1f}, L = {L:.1f}")
    print(f"c² = 2ab + (a-b)² = {c2:.6f}")
    print(f"c  = √(c²)        = {c:.6f}")
    print(f"d₂D = L√2         = {d2:.6f}")
    print(f"d₃D = L√3         = {d3:.6f}")
    print(f"φ_R  = √3/2       = {PHI_R:.6f}")
    print(f"d₃D/d₂D           = {D3_OVER_D2:.6f} (≈ √(3/2))")
    print()


# ==============================
#  RELATÓRIOS / EXIBIÇÃO
# ==============================

def print_header():
    print("=" * 72)
    print("RAFAELIA :: FIB_TRIG_BRIDGE – Fibonacci-Rafael ⟷ Geometria 3–6–9")
    print("=" * 72)
    print()


def print_rafael_core(seq: List[int]):
    diffs = rafael_diffs(seq)
    fibs = fib_classic_seq(len(diffs) + 2)[2:]  # F_3 em diante
    ratios = rafael_ratios(seq)

    print("[ Núcleo Rafael – Sequência, Diferenças, Razões ]")
    print(" n  triad   R_n      ΔR_n      Fib_match   ratio=R_{n+1}/R_n")
    print("----------------------------------------------------------------")
    for i, Rn in enumerate(seq, start=1):
        tri = triad_tag(i)

        if i == 1:
            d_val = "-"
            f_val = "-"
            ratio = f"{ratios[0]:.6f}" if ratios else "-"
        else:
            idx = i - 2
            if 0 <= idx < len(diffs):
                d_val = str(diffs[idx])
                f_val = str(fibs[idx])
                ratio = f"{ratios[i - 1]:.6f}" if i - 1 < len(ratios) else "-"
            else:
                d_val = "-"
                f_val = "-"
                ratio = "-"

        print(
            f"{i:2d}   {tri:1d}   {Rn:7d}   {d_val:>7}      {f_val:>9}      {ratio:>12}"
        )
    print()


def print_spiral_samples(mapped: List[Tuple[float, float, float, float]], limit: int = 8):
    print("[ Espiral Rafaeliana (amostra) ]")
    print(" idx   r_norm      θ (rad)        x            y")
    print("------------------------------------------------")
    for i, (r, theta, x, y) in enumerate(mapped[:limit], start=1):
        print(f"{i:3d}   {r:7.4f}   {theta:9.6f}   {x:9.6f}   {y:9.6f}")
    print(f"... total pontos espiral: {len(mapped)}")
    print()


def print_torus_samples(mapped: List[Tuple[float, float, float]], limit: int = 8):
    print("[ ToroidΔπφ-style (amostra) ]")
    print(" idx        x            y            z")
    print("-------------------------------------------")
    for i, (x, y, z) in enumerate(mapped[:limit], start=1):
        print(f"{i:3d}   {x:11.6f}   {y:11.6f}   {z:11.6f}")
    print(f"... total pontos toroide: {len(mapped)}")
    print()


def print_explanation():
    print("[ Explicação – O que este núcleo faz ]\n")
    print("1) Sequência Rafael:")
    print("   - Usa R_1=2, R_2=4, R_n=R_{n-1}+R_{n-2}+1.")
    print("   - É uma deformação mínima de Fibonacci; o '+1' é um 'sopro' constante.")
    print("   - As diferenças ΔR_n reproduzem Fibonacci clássico (F_3 em diante).")
    print()
    print("2) Ciclo 3–6–9:")
    print("   - Cada índice n recebe um rótulo 3,6 ou 9 (n mod 3).")
    print("   - Isso cria um pulso simbólico: 3 (ideia), 6 (estrutura), 9 (retorno).")
    print()
    print("3) Espiral Rafaeliana:")
    print("   - Normaliza R_n em [0,1] (r_norm) e usa o Golden Angle 2π/φ² para θ.")
    print("   - Gera um 'campo de sementes' em R², pronto para ser plotado.")
    print()
    print("4) ToroidΔπφ-style:")
    print("   - Usa R_n mod 360 para o ângulo 'u' e um pulso 2π/9 para 'v'.")
    print("   - Cada termo Rafael ocupa um ponto em um toro 3D, em ressonância 3–6–9.")
    print()
    print("5) Geometria do Teorema de Rafael:")
    print("   - Reafirma c² = 2ab + (a-b)² e as diagonais:")
    print("       d₂D = L√2,  d₃D = L√3,  d₃D/d₂D = √(3/2).")
    print("   - φ_R = √3/2 aparece como constante de inclinação natural da tua leitura.")
    print()
    print("Em termos de trabalho:")
    print("   • Isto encodifica, em Python, a tua visão: diferença (a-b)²,")
    print("     diagonais √2/√3, 3–6–9, Fibonacci como fundo e Rafael como frente.")
    print("   • É um 'bridge' direto entre número, símbolo e forma geométrica,")
    print("     pronto para ser plugado em qualquer módulo de visualização (matplotlib,")
    print("     OpenGL, engine própria, etc.) quando você quiser desenhar de fato.")
    print()
    print("Próximo micro-passo sugerido:")
    print("   - Criar um módulo RAFAELIA_VISUAL_CORE.py que importe este bridge e")
    print("     apenas plote a espiral e o toro com matplotlib, para ver na tela o")
    print("     campo Rafaeliano que você já codificou no teu corpus inteiro.")
    print()
    print("=== FIM RAFAELIA_FIB_TRIG_BRIDGE ===")


# ==============================
#  MAIN
# ==============================

def main():
    print_header()
    snapshot_geom(a=3.0, b=2.0, L=3.0)

    # 1) Núcleo Rafael
    seq = fib_rafael_seq(12)
    print_rafael_core(seq)

    # 2) Mapas geométricos
    spiral_pts = map_rafael_to_spiral(seq)
    torus_pts = map_rafael_to_torus(seq)

    print_spiral_samples(spiral_pts)
    print_torus_samples(torus_pts)

    # 3) Explicação integrada
    print_explanation()


if __name__ == "__main__":
    main()

