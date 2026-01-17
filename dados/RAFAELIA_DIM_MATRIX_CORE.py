#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA_DIM_MATRIX_CORE
----------------------------------------------------------------------
Scanner de padrões entre dimensões 2D..7D usando:
- diagonais de hipercubos (D_n = L*sqrt(n))
- potências 2..7 e normalizações D_n^k / n^(k/2)
- volumes de hipercubos e hiperesferas inscritas
- aproximações a π, φ, φ_R, √2, √3, √(3/2)

Rodar:  python RAFAELIA_DIM_MATRIX_CORE.py
"""

import math
from typing import Dict, List, Tuple

# ==============================
#  CONSTANTES RAFAELIA
# ==============================

PHI = (1 + math.sqrt(5)) / 2.0          # número de ouro
SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
PHI_R = SQRT3 / 2.0                     # φ_R = √3/2
SQRT_3_OVER_2 = math.sqrt(3.0 / 2.0)    # d3/d2 para L=1

CONSTS = {
    "π": math.pi,
    "φ": PHI,
    "φ_R": PHI_R,
    "√2": SQRT2,
    "√3": SQRT3,
    "√(3/2)": SQRT_3_OVER_2,
}


# ==============================
#  FUNÇÕES AUXILIARES
# ==============================

def volume_hypercube(L: float, n: int) -> float:
    """Volume do hipercubo n-dimensional de lado L."""
    return L ** n


def volume_hypersphere_inscribed(L: float, n: int) -> float:
    """
    Volume da hiperesfera n-dimensional inscrita no hipercubo de lado L.
    Raio = L/2.
    Fórmula: V_n = (π^{n/2} r^n) / Γ(n/2 + 1)
    """
    r = L / 2.0
    return (math.pi ** (n / 2.0)) * (r ** n) / math.gamma(n / 2.0 + 1.0)


def nearest_constant(x: float, tol: float = 0.01) -> Tuple[str, float]:
    """
    Retorna (nome_constante, diferença) se x estiver a menos de 'tol'
    de alguma constante conhecida. Caso contrário, ("", 0.0).
    """
    best_name = ""
    best_diff = float("inf")
    for name, val in CONSTS.items():
        diff = abs(x - val)
        if diff < best_diff:
            best_diff = diff
            best_name = name
    if best_diff <= tol:
        return best_name, best_diff
    return "", 0.0


# ==============================
#  SCANNER PRINCIPAL
# ==============================

def scan_dimensions(max_dim: int = 7, L: float = 1.0) -> None:
    """
    Percorre dimensões de 2 até max_dim, calcula:
      - D_n = L*sqrt(n)
      - D_n^k para k=2..7
      - normalizações D_n^k / n^(k/2)
      - volumes hipercubo / hiperesfera
      - aproximações a constantes
    E imprime em formato legível.
    """
    print("=" * 72)
    print("RAFAELIA_DIM_MATRIX_CORE – Scanner 2D..7D")
    print("=" * 72)
    print(f"L (lado base) = {L:.6f}")
    print()

    for n in range(2, max_dim + 1):
        print("-" * 72)
        print(f"Dimensão n = {n}")
        D_n = L * math.sqrt(n)
        print(f"D_n (diagonal hipercubo) = L*sqrt(n) = {D_n:.12f}")

        # Razão entre diagonais consecutivas, quando n>2
        if n > 2:
            D_prev = L * math.sqrt(n - 1)
            ratio_diag = D_n / D_prev
            print(f"Razão D_n / D_(n-1) = {ratio_diag:.12f}")

        # Potências e normalizações
        print("\n[ Potências da Diagonal & Normalizações ]")
        print(" k   D_n^k                D_n^k / n^(k/2)        near_const")
        print("----------------------------------------------------------------")
        for k in range(2, 8):  # 2..7
            D_pow = D_n ** k
            norm = D_pow / (n ** (k / 2.0))
            cname, cdiff = nearest_constant(norm)
            if cname:
                tag = f"≈ {cname} (Δ={cdiff:.2e})"
            else:
                tag = ""
            print(f"{k:2d}  {D_pow:18.12f}   {norm:18.12f}   {tag}")

        # Volumes / Áreas
        V_cube = volume_hypercube(L, n)
        V_sphere = volume_hypersphere_inscribed(L, n)
        ratio_vs = V_sphere / V_cube

        print("\n[ Volumetria n-D ]")
        print(f"Volume hipercubo (L^n)          = {V_cube:.12f}")
        print(f"Volume hiperesfera inscrita     = {V_sphere:.12f}")
        print(f"Razão esfera/cubo (inscrita)    = {ratio_vs:.12f}")
        cname, cdiff = nearest_constant(ratio_vs)
        if cname:
            print(f"  ↳ esfera/cubo ≈ {cname} (Δ={cdiff:.2e})")

        print()

    print("=" * 72)
    print("Resumo conceitual:")
    print(" - Para qualquer n, D_n^2 / n = L^2 (invariante de área).")
    print(" - Em geral, D_n^k / n^(k/2) = L^k (invariante de ordem k).")
    print(" - As diferenças entre dimensões aparecem nas razões brutas")
    print("   D_n^k e nos volumes esfera/cubo; os invariantes revelam")
    print("   o 'núcleo comum' entre todas as dimensões (L^k).")
    print("=" * 72)


# ==============================
#  MAIN
# ==============================

if __name__ == "__main__":
    scan_dimensions(max_dim=7, L=1.0)
