#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA :: MATH UNIVERSE LAB
--------------------------------
Núcleo matemático consolidando:
- Teorema de Rafael (c² = 2ab + (a-b)²)
- Geometria 2D/3D (d₂D = L√2, d₃D = L√3, razão √(3/2))
- Constante Rafaeliana φ_R = √3/2
- Modos de operação: subtração, oposição, mistura
- Bases e primos, polinômios, busca de constantes por razões/combinações.

Uso:
    python rafaelia_math_universe.py

Este módulo foi pensado para ser expandido: você pode importar em outros
scripts RAFAELIA e usar as funções como blocos de construção.
"""

import math
import random
from itertools import product, combinations

# ============================================================
#  SEÇÃO 1 — CONSTANTES FUNDAMENTAIS
# ============================================================

PI = math.pi
TAU = 2 * math.pi
SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
SQRT_3_OVER_2 = math.sqrt(3.0 / 2.0)

def constante_rafaeliana() -> float:
    """
    Constante Rafaeliana φ_R.

    Interpretações geométricas:
    - Altura do triângulo equilátero de lado 1 (projetado em 2D).
    - Meia-diagonal normalizada do cubo unitário em algumas leituras RAFAELIA.
    """
    return math.sqrt(3.0) / 2.0


# ============================================================
#  SEÇÃO 2 — GEOMETRIA: TRIÂNGULO, QUADRADO, CUBO
# ============================================================

def pitagoras(a: float, b: float) -> float:
    """Hipotenusa clássica: c = √(a² + b²)."""
    return math.sqrt(a * a + b * b)

def teorema_rafael(a: float, b: float) -> float:
    """
    Teorema de Rafael — decomposição de Pitágoras:

        c² = 2ab + (a - b)²

    Observação: algébricamente, é equivalente a a² + b².
    Serve como 'prova visual / estrutural' destacando:
    - Núcleo de diferença: (a-b)²
    - Área organizada em 4 triângulos: 4 * (ab/2) = 2ab
    """
    return 2.0 * a * b + (a - b) ** 2

def diagonais_2d_3d(L: float):
    """
    Retorna (d₂D, d₃D, razão d₃D/d₂D).

    d₂D = L√2   (diagonal de um quadrado)
    d₃D = L√3   (diagonal espacial de um cubo)
    """
    d2 = L * SQRT2
    d3 = L * SQRT3
    ratio = d3 / d2 if d2 != 0 else float("inf")
    return d2, d3, ratio


# ============================================================
#  SEÇÃO 3 — MODOS DE OPERAÇÃO: SUBTRAÇÃO, OPOSIÇÃO, MISTURA
# ============================================================

def modo_subtracao(a: float, b: float) -> dict:
    """
    Modo SUBTRAÇÃO: trata (a,b) como tensões opostas no mesmo eixo.

    Foca em:
    - diferença |a-b|
    - quadrado da diferença (a-b)²
    - diferença cúbica a³ - b³
    """
    diff = a - b
    return {
        "a": a,
        "b": b,
        "abs_diff": abs(diff),
        "diff_sq": diff ** 2,
        "diff_cube": a ** 3 - b ** 3,
    }

def modo_oposicao(a: float, b: float) -> dict:
    """
    Modo OPOSIÇÃO: trata (a,b) como vetores opostos em um plano.

    Usa:
    - norma de (a, -b)
    - soma vetorial (a + (-b)) como 'resultante'
    - produto interno com (b, a) para ver alinhamento / desalinhamento.
    """
    vx = a
    vy = -b
    norm = math.sqrt(vx * vx + vy * vy)
    dot = vx * b + vy * a
    return {
        "a": a,
        "b": b,
        "vec": (vx, vy),
        "norm": norm,
        "dot_with_rotated": dot,
    }

def modo_mistura(a: float, b: float) -> dict:
    """
    Modo MISTURA: combina SUBTRAÇÃO + OPOSIÇÃO + PITÁGORAS + RAFAEL.

    A ideia é observar:
    - c_pit = √(a² + b²)
    - c_raf² = 2ab + (a-b)²
    - razão c_raf² / c_pit²  (deve ser 1, mas aqui serve como check)
    - diagonal 2D/3D em função de L = max(|a|,|b|)
    """
    c_pit = pitagoras(a, b)
    c2_raf = teorema_rafael(a, b)
    c2_pit = a * a + b * b
    ratio = c2_raf / c2_pit if c2_pit != 0 else float("inf")
    L = max(abs(a), abs(b))
    d2, d3, r = diagonais_2d_3d(L)
    return {
        "a": a,
        "b": b,
        "c_pit": c_pit,
        "c2_rafael": c2_raf,
        "check_ratio": ratio,
        "L": L,
        "d2": d2,
        "d3": d3,
        "d3_over_d2": r,
    }


# ============================================================
#  SEÇÃO 4 — BASES, PRIMOS E COMBINAÇÕES
# ============================================================

PRIMOS_BASE = [2, 3, 5, 7, 11, 13, 17]

BASES_RAFAELIA = [1, 2, 3, 5, 7]  # 1 como 'contagem', 2/3/5/7 como bases estruturais

def to_base(n: int, base: int) -> str:
    """
    Converte n para uma string em base arbitrária (2–36).
    Base 1 (unária) é tratada como sequência de '1's.
    """
    if base < 1 or base > 36:
        raise ValueError("base deve estar entre 1 e 36")
    if n == 0:
        return "0"
    if base == 1:
        return "1" * n

    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    neg = n < 0
    n = abs(n)
    out = []
    while n > 0:
        n, r = divmod(n, base)
        out.append(digits[r])
    if neg:
        out.append("-")
    return "".join(reversed(out))

def combinacoes_primos_bases(limit: int = 100) -> list:
    """
    Gera algumas combinações p ⊗ q em múltiplas bases, coletando razões
    e produtos para procurar padrões.
    """
    resultados = []
    for p, q in combinations(PRIMOS_BASE, 2):
        for base in BASES_RAFAELIA:
            n1 = p * q
            if n1 > limit:
                continue
            rep = to_base(n1, base)
            ratio = p / q
            resultados.append({
                "p": p,
                "q": q,
                "base": base,
                "produto": n1,
                "repr": rep,
                "ratio": ratio,
            })
    return resultados


# ============================================================
#  SEÇÃO 5 — POLINÔMIOS (OPERAR E SCANNEAR)
# ============================================================

def avalia_polinomio(coefs, x: float) -> float:
    """
    Avalia P(x) = c0 + c1 x + c2 x² + ... usando Horner.
    coefs = [c0, c1, c2, ...]
    """
    acc = 0.0
    for c in reversed(coefs):
        acc = acc * x + c
    return acc

def derivada_polinomio(coefs):
    """
    Derivada de P(x) de forma simbólica simples:
    P(x) = c0 + c1 x + c2 x² + ...
    P'(x) = c1 + 2c2 x + 3c3 x² + ...
    """
    return [i * c for i, c in enumerate(coefs)][1:]

def gera_polinomios_experimentais():
    """
    Gera um pequeno conjunto de polinômios 'RAFAELIA' com
    assinaturas típicas: misturando π, φ_R, √2, √3.
    """
    phi_R = constante_rafaeliana()
    polys = {
        "P1": [0.0, 1.0, 0.0, -1.0],          # x - x³  (dobras, torção)
        "P2": [phi_R, -SQRT2, 1.0],          # φ_R - √2 x + x²
        "P3": [0.0, SQRT_3_OVER_2, -PI],     # (√3/2) x - π x²
        "P4": [1.0, -phi_R, SQRT3, -TAU],    # 1 - φ_R x + √3 x² - τ x³
    }
    return polys


# ============================================================
#  SEÇÃO 6 — LABORATÓRIO DE CONSTANTES
# ============================================================

def gera_candidatos_constantes(
    a_vals=(2.0, 3.0, 5.0),
    b_vals=(1.0, 2.0, 3.0),
    amostras_random: int = 0,
):
    """
    Varre alguns pares (a,b) em três modos:
    - subtração
    - oposição
    - mistura

    E gera razões/combinações para procurar 'constantes estáveis':
    valores que aparecem repetidamente próximos.
    """
    dados = []

    # amostras determinísticas
    for a, b in product(a_vals, b_vals):
        if b == 0:
            continue
        ms = modo_subtracao(a, b)
        mo = modo_oposicao(a, b)
        mm = modo_mistura(a, b)

        # Razões e combinações básicas
        combos = {
            "a/b": a / b,
            "b/a": b / a,
            "abs_diff/a": ms["abs_diff"] / a,
            "abs_diff/b": ms["abs_diff"] / b,
            "c_pit/L": mm["c_pit"] / mm["L"] if mm["L"] else float("inf"),
            "d3/d2": mm["d3_over_d2"],
            "phi_R": constante_rafaeliana(),
        }
        dados.append({
            "a": a,
            "b": b,
            "combos": combos,
        })

    # amostras randômicas opcionais
    for _ in range(amostras_random):
        a = random.uniform(1.0, 10.0)
        b = random.uniform(1.0, 10.0)
        if b == 0:
            continue
        mm = modo_mistura(a, b)
        combos = {
            "a/b": a / b,
            "b/a": b / a,
            "c_pit/L": mm["c_pit"] / mm["L"] if mm["L"] else float("inf"),
            "d3/d2": mm["d3_over_d2"],
            "phi_R": constante_rafaeliana(),
        }
        dados.append({
            "a": a,
            "b": b,
            "combos": combos,
        })

    return dados


# ============================================================
#  SEÇÃO 7 — DEMOS E IMPRESSÃO
# ============================================================

def demo_snapshot_geometrico(a=3.0, b=2.0, L=3.0):
    """Imprime um snapshot geométrico padrão estilo LAB."""
    c2 = teorema_rafael(a, b)
    c = math.sqrt(c2)
    d2, d3, ratio = diagonais_2d_3d(L)
    phi_R = constante_rafaeliana()

    print("[ Snapshot Geométrico Padrão ]")
    print(f"a = {a}, b = {b}, L = {L}")
    print(f"c² (Rafael) = 2ab + (a-b)² = {c2:.6f}")
    print(f"c  = √(c²) = {c:.6f}")
    print(f"d₂D = L√2 = {d2:.6f}")
    print(f"d₃D = L√3 = {d3:.6f}")
    print(f"φ_R = √3/2 = {phi_R:.6f}")
    print(f"d₃D/d₂D = {ratio:.6f}  (≈ √(3/2))")
    print()

def demo_primos_bases():
    """Mostra algumas linhas do scanner de primos em bases."""
    print("[ Primos × Bases RAFAELIA ]")
    combos = combinacoes_primos_bases(limit=150)
    for linha in combos[:10]:
        p = linha["p"]
        q = linha["q"]
        base = linha["base"]
        prod = linha["produto"]
        rep = linha["repr"]
        ratio = linha["ratio"]
        print(
            f"p={p:2d}, q={q:2d}, base={base:2d} -> "
            f"p*q={prod:3d} (repr='{rep}'), p/q={ratio:.6f}"
        )
    print(f"... total combinações calculadas: {len(combos)}")
    print()

def demo_polinomios():
    """Demonstra alguns polinômios experimentais."""
    print("[ Polinômios RAFAELIA ]")
    polys = gera_polinomios_experimentais()
    xs = [0.0, 0.5, 1.0, 2.0]
    for nome, coefs in polys.items():
        dcoefs = derivada_polinomio(coefs)
        print(f"{nome}(x) com coefs={coefs}, derivada={dcoefs}")
        for x in xs:
            y = avalia_polinomio(coefs, x)
            print(f"  x={x:4.1f} -> {nome}(x)={y: .6f}")
        print()
    print()

def demo_constantes():
    """Imprime algumas combinações numéricas para caça de constantes."""
    print("[ Candidatos a Constantes – Varredura RAFAELIA ]")
    dados = gera_candidatos_constantes(amostras_random=5)
    # Vamos apenas mostrar algumas linhas agregando média de alguns termos.
    termos = ["a/b", "b/a", "c_pit/L", "d3/d2", "phi_R"]
    acumuladores = {t: [] for t in termos}
    for row in dados:
        for t in termos:
            v = row["combos"][t]
            if math.isfinite(v):
                acumuladores[t].append(v)

    for t in termos:
        vals = acumuladores[t]
        if not vals:
            continue
        media = sum(vals) / len(vals)
        minimo = min(vals)
        maximo = max(vals)
        print(f"{t:8s} -> média={media:.6f}, min={minimo:.6f}, max={maximo:.6f}")
    print()


# ============================================================
#  MAIN
# ============================================================

def main():
    print("=== RAFAELIA :: Math Universe Lab ===\n")
    demo_snapshot_geometrico()
    demo_primos_bases()
    demo_polinomios()
    demo_constantes()
    print("=== FIM RAFAELIA MATH UNIVERSE ===")

if __name__ == "__main__":
    main()
