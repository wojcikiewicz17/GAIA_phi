#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA_COMPLEX_AUTO
======================

Módulo gerado automaticamente pelo RAFAELIA Math & Geometry Lab.

Este arquivo demonstra, em código, várias das ideias desta sessão:

- Teorema de Rafael: c² = 2ab + (a - b)²
- Constante Rafaeliana: φ_R = √3 / 2
- Relação triângulo / quadrado / cubo (√2, √3)
- Padrão 3–6–9 como estados geométrico-dinâmicos
- Primos, bases e polinômios mistos RAFAELIA

Pode ser usado como base para outros experimentos,
importado como biblioteca ou adaptado em kernels / CLIs.
"""

import math
from dataclasses import dataclass
from typing import List

# Gerado em: 2025-11-30T15:14:42
PHI_R = 0.8660254037844386  # Constante Rafaeliana √3/2
A_DEFAULT = 3.0
B_DEFAULT = 2.0
L_DEFAULT = 3.0

def teorema_rafael(a: float, b: float) -> float:
    """Teorema de Rafael – c² = 2ab + (a - b)²."""
    return 2.0 * a * b + (a - b) ** 2

def hipotenusa_rafael(a: float, b: float) -> float:
    """Retorna c = √(2ab + (a - b)²)."""
    return math.sqrt(teorema_rafael(a, b))

def diagonal_quadrado(lado: float) -> float:
    """Diagonal de um quadrado: d₂D = L√2."""
    return lado * math.sqrt(2.0)

def diagonal_cubo(lado: float) -> float:
    """Diagonal espacial de um cubo: d₃D = L√3."""
    return lado * math.sqrt(3.0)

@dataclass
class RafaelSnapshot:
    """Snapshot geométrico RAFAELIA (a, b, L, c, d₂D, d₃D, φ_R)."""
    a: float
    b: float
    L: float
    c: float
    c2: float
    d2: float
    d3: float
    phi_R: float

    def ratio_d3_d2(self) -> float:
        if self.d2 == 0:
            return float('nan')
        return self.d3 / self.d2

def build_snapshot(a: float = A_DEFAULT, b: float = B_DEFAULT, L: float = L_DEFAULT) -> RafaelSnapshot:
    """Constroi um RafaelSnapshot com base no Teorema de Rafael."""
    c2 = teorema_rafael(a, b)
    c = math.sqrt(c2)
    d2 = diagonal_quadrado(L)
    d3 = diagonal_cubo(L)
    return RafaelSnapshot(a=a, b=b, L=L, c=c, c2=c2, d2=d2, d3=d3, phi_R=PHI_R)

def rafael_poly_mixed(a: float, b: float, L: float) -> List[float]:
    """Polinômio RAFAELIA misto 2D/3D/φ_R: P(x) = c0 + c1 x + c2 x² + c3 x³."""
    snap = build_snapshot(a, b, L)
    diff2 = (a - b) ** 2
    c0 = diff2
    c1 = 2.0 * a * b
    c2 = snap.d3 - snap.d2 * snap.phi_R
    c3 = snap.phi_R * (snap.d3 / max(snap.d2, 1e-9))
    return [c0, c1, c2, c3]

def eval_poly(coeffs: List[float], x: float) -> float:
    """Avalia P(x) pelo esquema de Horner."""
    acc = 0.0
    for c in reversed(coeffs):
        acc = acc * x + c
    return acc

SNAP_DEFAULT = build_snapshot(A_DEFAULT, B_DEFAULT, L_DEFAULT)
POLY_DEFAULT = rafael_poly_mixed(A_DEFAULT, B_DEFAULT, L_DEFAULT)

PRIMOS_EXEMPLO = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

def demo_rafaelia() -> None:
    """Demonstra, em runtime, a visão geométrica RAFAELIA desta sessão.

    - Imprime snapshot (a, b, L, c, d₂D, d₃D, φ_R, d₃D/d₂D)
    - Avalia o polinômio misto em alguns pontos
    """
    snap = SNAP_DEFAULT
    print('=== DEMO RAFAELIA COMPLEX AUTO ===')
    print(f'a = {snap.a}, b = {snap.b}, L = {snap.L}')
    print(f'c² = 2ab + (a - b)² = {snap.c2:.6f}')
    print(f'c  = √(c²) = {snap.c:.6f}')
    print(f'd₂D = L√2 = {snap.d2:.6f}')
    print(f'd₃D = L√3 = {snap.d3:.6f}')
    print(f'φ_R = √3/2 = {snap.phi_R:.6f}')
    print(f'd₃D/d₂D = {snap.ratio_d3_d2():.6f}  (≈ √(3/2))')
    print('\nPolinômio misto P(x) = c0 + c1 x + c2 x² + c3 x³:')
    print('  coeficientes =', POLY_DEFAULT)
    for x in [0.0, 1.0, 2.0, 3.0]:
        y = eval_poly(POLY_DEFAULT, x)
        print(f'  P({{x}}) = {{y:.6f}}')
    print('\nPrimos usados como base simbólica:', PRIMOS_EXEMPLO)
    print('=== FIM DEMO RAFAELIA ===')

if __name__ == '__main__':
    demo_rafaelia()
