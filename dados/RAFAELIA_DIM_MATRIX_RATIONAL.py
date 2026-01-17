#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA_DIM_MATRIX_RATIONAL
Racionaliza:
 - razões D_n / D_(n-1)
 - razões Volume_esfera / Volume_cubo
e tenta achar padrões inteiros/frações simples.
"""

import math
from fractions import Fraction

def vol_hyper_sphere_inscribed(n: int, L: float = 1.0) -> float:
    """Volume da hiperesfera inscrita num hipercubo de lado L."""
    r = L / 2.0
    return (math.pi ** (n / 2.0)) * (r ** n) / math.gamma(n / 2.0 + 1.0)

def racionalizar(x: float, max_den: int = 1_000_000) -> Fraction:
    """Aproxima x por uma fração p/q com denominador <= max_den."""
    return Fraction(x).limit_denominator(max_den)

def main():
    print("=" * 72)
    print("RAFAELIA_DIM_MATRIX_RATIONAL – Núcleo de Racionalização")
    print("=" * 72)
    L = 1.0

    prev_D = None
    for n in range(2, 8):
        D_n = math.sqrt(n) * L
        V_cube = L ** n
        V_sphere = vol_hyper_sphere_inscribed(n, L)
        ratio_sphere_cube = V_sphere / V_cube

        print("\n--- Dimensão n =", n, "---")
        print(f"D_n = sqrt({n}) ≈ {D_n:.12f}")

        if prev_D is not None:
            raw_ratio = D_n / prev_D  # D_n / D_{n-1}
            frac_ratio = racionalizar(raw_ratio)
            print(f"Razão diagonais D_n/D_(n-1) ≈ {raw_ratio:.12f} ≈ {frac_ratio.numerator}/{frac_ratio.denominator}")
        prev_D = D_n

        # volume esfera/cubo
        frac_vol = racionalizar(ratio_sphere_cube)
        # também testar multiplicado por π para ver se simplifica
        frac_vol_pi = racionalizar(ratio_sphere_cube / math.pi)

        print(f"Volume esfera/cubo ≈ {ratio_sphere_cube:.12f}")
        print(f"  ≈ {frac_vol.numerator}/{frac_vol.denominator}")
        print(f"  (dividido por π) ≈ {frac_vol_pi.numerator}/{frac_vol_pi.denominator}")

    print("\n=== FIM RAFAELIA_DIM_MATRIX_RATIONAL ===")

if __name__ == '__main__':
    main()
