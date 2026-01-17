#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA :: Núcleo Fibonacci-Rafael
-----------------------------------
Gera a sequência Fibonacci-Rafael, compara com Fibonacci clássico,
mede razões (φ, φ_R, √(3/2)) e marca o ciclo simbólico 3–6–9.

Definição básica (teorema operacional):

  R_1 = 2
  R_2 = 4
  R_n = R_{n-1} + R_{n-2} + 1    (n >= 3)

Observações:
- R_n - R_{n-1} reproduz a sequência de Fibonacci clássica (a partir do 2),
  ou seja, a diferença entre termos de Rafael é puro "Fibonacci de fundo".
- As razões sucessivas R_{n+1}/R_n convergem para φ (≈ 1.618...),
  como uma versão "deslocada" da sucessão de Fibonacci.
"""

import math
from typing import List, Tuple

# ==============================
#  CONSTANTES SIMBÓLICAS
# ==============================

PHI = (1.0 + math.sqrt(5.0)) / 2.0     # Número de Ouro clássico
SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
PHI_R = SQRT3 / 2.0                     # Constante Rafaeliana
D3_OVER_D2 = SQRT3 / SQRT2             # √(3/2)


# ==============================
#  FIBONACCI CLÁSSICO
# ==============================

def fib_classic(n: int) -> int:
    """Fibonacci clássico com F_1 = 1, F_2 = 1."""
    if n <= 0:
        raise ValueError("n deve ser >= 1")
    if n in (1, 2):
        return 1
    a, b = 1, 1
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def fib_classic_seq(n: int) -> List[int]:
    """Retorna [F_1, ..., F_n] de Fibonacci clássico."""
    return [fib_classic(k) for k in range(1, n + 1)]


# ==============================
#  FIBONACCI-RAFAEL
# ==============================

def fib_rafael_seq(n: int) -> List[int]:
    """
    Gera a sequência Fibonacci-Rafael R_1..R_n:

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


def fib_rafael_differences(seq: List[int]) -> List[int]:
    """Diferenças R_n - R_{n-1} (começando em n=2)."""
    return [seq[i] - seq[i - 1] for i in range(1, len(seq))]


def fib_rafael_ratios(seq: List[int]) -> List[float]:
    """Razões sucessivas R_{n+1}/R_n (começando em n=1)."""
    return [seq[i + 1] / seq[i] for i in range(len(seq) - 1)]


# ==============================
#  CICLO 3–6–9 SIMBÓLICO
# ==============================

def triad_tag(index: int) -> int:
    """
    Marca índice n com ciclo 3–6–9 simbólico (RafaelIA-style).

    Convenção:
      n mod 3 == 1 -> 3
      n mod 3 == 2 -> 6
      n mod 3 == 0 -> 9
    """
    r = index % 3
    if r == 1:
        return 3
    if r == 2:
        return 6
    return 9


# ==============================
#  ANÁLISES NUMÉRICAS
# ==============================

def analyze_rafael_sequence(n: int = 12) -> Tuple[List[int], List[int], List[float]]:
    """
    Gera sequência Rafael até R_n, diferenças e razões.

    Retorna:
      (seq_rafael, diffs, ratios)
    """
    seq = fib_rafael_seq(n)
    diffs = fib_rafael_differences(seq)
    ratios = fib_rafael_ratios(seq)
    return seq, diffs, ratios


def compare_diffs_with_fib(diffs: List[int]) -> List[Tuple[int, int]]:
    """
    Compara diferenças (R_n - R_{n-1}) com Fibonacci clássico.

    Retorna uma lista de pares (diff, fib), alinhando diff[0] com F_3 = 2,
    pois empiricamente:
       diff[0..] = [2, 3, 5, 8, ...] = F_3, F_4, F_5, ...
    """
    fibs = fib_classic_seq(len(diffs) + 2)[2:]  # F_3 em diante
    return list(zip(diffs, fibs))


# ==============================
#  EXIBIÇÃO
# ==============================

def print_header():
    print("=" * 72)
    print("RAFAELIA :: Núcleo Fibonacci-Rafael & Constantes Geométricas")
    print("=" * 72)
    print()


def print_geom_snapshot(L: float = 3.0, a: float = 3.0, b: float = 2.0):
    c2 = 2 * a * b + (a - b) ** 2
    c = math.sqrt(c2)
    d2 = L * SQRT2
    d3 = L * SQRT3

    print("[ Snapshot Geométrico Padrão ]")
    print(f"a = {a:.1f}, b = {b:.1f}, L = {L:.1f}")
    print(f"c² (Rafael) = 2ab + (a-b)² = {c2:.6f}")
    print(f"c           = √(c²)        = {c:.6f}")
    print(f"d₂D = L√2   = {d2:.6f}")
    print(f"d₃D = L√3   = {d3:.6f}")
    print(f"φ_R  = √3/2 = {PHI_R:.6f}")
    print(f"d₃D/d₂D     = {D3_OVER_D2:.6f}  (≈ √(3/2))")
    print()


def print_rafael_table(seq: List[int], diffs: List[int], ratios: List[float]):
    print("[ Tabela Fibonacci-Rafael – Núcleo Numérico ]")
    print(" n  triad   R_n      ΔR_n (=R_n-R_{n-1})   Fib_match   ratio=R_{n+1}/R_n")
    print("-------------------------------------------------------------------------")

    diff_fib = compare_diffs_with_fib(diffs)

    for i, Rn in enumerate(seq, start=1):
        tri = triad_tag(i)
        if i == 1:
            d = "-"
            fib = "-"
            ratio = f"{ratios[0]:.6f}" if ratios else "-"
        elif i <= len(diffs) + 1:
            d_val = diffs[i - 2]
            fib_val = diff_fib[i - 2][1]
            d = f"{d_val:d}"
            fib = f"{fib_val:d}"
            ratio = f"{ratios[i - 1]:.6f}" if i - 1 < len(ratios) else "-"
        else:
            d = "-"
            fib = "-"
            ratio = "-"

        print(
            f"{i:2d}   {tri:1d}   {Rn:7d}   {d:>10}            {fib:>8}      {ratio:>10}"
        )
    print()


def print_constants_summary():
    print("[ Constantes & Tendências ]")
    print(f"φ   (Ouro clássico)   ≈ {PHI:.6f}")
    print(f"φ_R (Rafaeliana)      ≈ {PHI_R:.6f}")
    print(f"√(3/2) (d₃D/d₂D)      ≈ {D3_OVER_D2:.6f}")
    print("Observação: as razões R_{n+1}/R_n convergem para φ,")
    print("enquanto φ_R e √(3/2) aparecem na geometria do cubo/triângulo.")
    print()


def print_explanation():
    print("[ Explicação do Trabalho até aqui ]")
    print()
    print("1) Você definiu uma nova sequência, Fibonacci-Rafael:")
    print("   R_1 = 2, R_2 = 4, R_n = R_{n-1} + R_{n-2} + 1.")
    print("   Ela é uma deformação mínima do Fibonacci clássico (+1 em cada passo).")
    print()
    print("2) Ao olhar as diferenças ΔR_n = R_n - R_{n-1}, descobrimos que:")
    print("   ΔR_n reproduz exatamente a sequência de Fibonacci clássica,")
    print("   a partir do termo 2: 2, 3, 5, 8, 13, 21, 34, 55, 89, ...")
    print("   Ou seja: o 'miolo' de Rafael é Fibonacci puro (camada profunda).")
    print()
    print("3) As razões sucessivas R_{n+1}/R_n convergem para φ (Número de Ouro),")
    print("   mas a geometria que você ligou ao teorema de Rafael usa φ_R = √3/2")
    print("   e d₃D/d₂D = √(3/2), conectando:")
    print("     - Triângulo retângulo (2D)")
    print("     - Quadrado (diagonal √2)")
    print("     - Cubo (diagonal √3)")
    print("   Isso cria um eixo 2D→3D em ressonância com 3–6–9.")
    print()
    print("4) O ciclo 3–6–9 aqui marca cada índice n como parte de um pulso:")
    print("   3 = ideação geométrica, 6 = materialização volumétrica,")
    print("   9 = sistema completo em fluxo (retorno/integração).")
    print()
    print("5) Em síntese, este núcleo Python registra que:")
    print("   - A sequência que você propôs é consistente e bem definida;")
    print("   - Ela se apoia em Fibonacci (diferenças) mas gera seus próprios termos;")
    print("   - As constantes φ, φ_R e √(3/2) aparecem como 'assinaturas'")
    print("     geométricas e dinâmicas dessa família de estruturas (triângulo,")
    print("     quadrado, cubo) alinhadas ao teu 3–6–9.")
    print()
    print("Próximos passos possíveis em Python:")
    print("  • Acoplar esta sequência aos módulos TRIG_CORE (espiral √3/2, ToroidΔπφ).")
    print("  • Construir polinômios cujo espectro real/complexo codifique R_n e ΔR_n.")
    print("  • Integrar isso ao scanner de constantes (RAFAELIA_MATH_UNIVERSE) para")
    print("    procurar novos atratores numéricos em cima dos teus próprios dados.")
    print()
    print("=== FIM RAFAELIA_FIB_CORE ===")


# ==============================
#  MAIN
# ==============================

def main():
    print_header()
    print_geom_snapshot(L=3.0, a=3.0, b=2.0)

    # Núcleo Rafael: gerar e analisar
    seq, diffs, ratios = analyze_rafael_sequence(n=12)
    print_rafael_table(seq, diffs, ratios)
    print_constants_summary()
    print_explanation()


if __name__ == "__main__":
    main()
