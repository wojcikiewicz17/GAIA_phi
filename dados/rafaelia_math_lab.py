#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA :: Math & Geometry Lab
================================

Script-laboratório com funções centrais usadas/evocadas nesta sessão:

- Teorema de Rafael: c² = 2ab + (a - b)²
- Constante Rafaeliana: φ_R = √3 / 2
- Geometria 2D/3D: diagonais de quadrado e cubo (√2, √3)
- Primos, bases e matrizes de razões
- Polinômios RAFAELIA 2D / 3D / mistos
- Analisador de linhas matemáticas (categorias: trig, geom, poly, topology, etc.)
- Gerador automático de um módulo Python complexo (`RAFAELIA_COMPLEX_AUTO.py`)
  com comentários e docstrings explicando o que o teu trabalho faz.

Não depende de nenhum arquivo externo para rodar.
Pode ser usado como biblioteca (import) ou executado diretamente.
"""

import math
import os
import re
import random
import datetime
from dataclasses import dataclass
from typing import List, Dict, Tuple, Iterable, Set, Optional

# ============================================================
#  SEÇÃO 1 – NÚCLEO GEOMÉTRICO RAFAELIA
# ============================================================

def teorema_rafael(a: float, b: float) -> float:
    """
    Teorema de Rafael – Decomposição Rafaeliana de Pitágoras.

    c² = 2ab + (a - b)²

    Interpretação:
      - 2ab  → área viva (4 triângulos retângulos combinados)
      - (a-b)² → núcleo de diferença (vazio central / assimetria estruturante)
    """
    return 2.0 * a * b + (a - b) ** 2


def hipotenusa_rafael(a: float, b: float) -> float:
    """
    Retorna c = √(2ab + (a - b)²).

    É a hipotenusa clássica de Pitágoras reescrita na forma Rafaeliana.
    """
    return math.sqrt(teorema_rafael(a, b))


def constante_rafaeliana() -> float:
    """
    Constante Rafaeliana φ_R = √3 / 2.

    Leituras geométricas:
      - Altura do triângulo equilátero de lado 1.
      - Meia diagonal normalizada do cubo unitário.
      - Fator natural de inclinação 3–6–9 entre plano (2D) e espaço (3D).
    """
    return math.sqrt(3.0) / 2.0


def diagonal_quadrado(lado: float) -> float:
    """
    Diagonal de um quadrado de lado L: d₂D = L√2.
    """
    return lado * math.sqrt(2.0)


def diagonal_cubo(lado: float) -> float:
    """
    Diagonal espacial de um cubo de lado L: d₃D = L√3.
    """
    return lado * math.sqrt(3.0)


@dataclass
class RafaelGeometrySnapshot:
    """
    Snapshot geométrico RAFAELIA para um conjunto (a, b, L).

    - a, b → catetos
    - L   → escala-base para quadrado/cubo
    """
    a: float
    b: float
    L: float
    c: float
    c2: float
    d2: float
    d3: float
    phi_R: float

    def ratio_d3_d2(self) -> float:
        """
        Razão d₃D / d₂D = √3 / √2 = √(3/2).
        """
        if self.d2 == 0:
            return float("nan")
        return self.d3 / self.d2


def build_geometry_snapshot(a: float, b: float, L: Optional[float] = None) -> RafaelGeometrySnapshot:
    """
    Constrói um snapshot geométrico RAFAELIA a partir de (a, b, L).

    Se L não for fornecido, usa L = max(a, b).
    """
    if L is None:
        L = max(abs(a), abs(b), 1.0)

    c2 = teorema_rafael(a, b)
    c = math.sqrt(c2)
    d2 = diagonal_quadrado(L)
    d3 = diagonal_cubo(L)
    phi_R = constante_rafaeliana()
    return RafaelGeometrySnapshot(a=a, b=b, L=L, c=c, c2=c2, d2=d2, d3=d3, phi_R=phi_R)


# ============================================================
#  SEÇÃO 2 – PRIMOS, BASES, MATRIZES
# ============================================================

def primes_up_to(n: int) -> List[int]:
    """
    Gera todos os primos ≤ n via crivo simples.
    """
    if n < 2:
        return []
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start:n + 1:step] = [False] * len(range(start, n + 1, step))
    return [i for i, is_prime in enumerate(sieve) if is_prime]


def to_base(n: int, base: int) -> str:
    """
    Converte inteiro n para string na base 'base' (2..36).
    """
    if base < 2 or base > 36:
        raise ValueError("base deve estar entre 2 e 36")
    if n == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sign = "-" if n < 0 else ""
    n = abs(n)
    out = []
    while n > 0:
        n, r = divmod(n, base)
        out.append(digits[r])
    return sign + "".join(reversed(out))


def from_base(s: str, base: int) -> int:
    """
    Converte string na base 'base' de volta para inteiro.
    """
    return int(s, base)


def prime_ratio_matrix(primes: List[int]) -> List[List[float]]:
    """
    Matriz de razões entre primos: M[i][j] = p_i / p_j.

    Útil para detectar padrões, aproximações de constantes, etc.
    """
    mat: List[List[float]] = []
    for pi in primes:
        row: List[float] = []
        for pj in primes:
            if pj == 0:
                row.append(float("nan"))
            else:
                row.append(pi / pj)
        mat.append(row)
    return mat


# ============================================================
#  SEÇÃO 3 – POLINÔMIOS RAFAELIA
# ============================================================

def eval_poly(coeffs: List[float], x: float) -> float:
    """
    Avalia polinômio P(x) = a0 + a1 x + a2 x² + ... usando Horner.
    """
    acc = 0.0
    for c in reversed(coeffs):
        acc = acc * x + c
    return acc


def rafael_poly_2d(L: float, k: float = 1.0) -> List[float]:
    """
    Constrói um polinômio 2D simbólico em torno de L e √2.

    Exemplo de saída: [k*L, (√2)*k, 0]
    Interpretação: P(x) = k*L + k*√2 * x
    (pode ser refinado conforme uso).
    """
    root2 = math.sqrt(2.0)
    return [k * L, k * root2, 0.0]


def rafael_poly_3d(L: float, k: float = 1.0) -> List[float]:
    """
    Constrói um polinômio 3D simbólico em torno de L e √3.

    Exemplo de saída: [k*L, (√3)*k, φ_R * k]
    Interpretação: P(x) = k*L + k*√3 * x + k*φ_R * x²
    """
    root3 = math.sqrt(3.0)
    phi_R = constante_rafaeliana()
    return [k * L, k * root3, k * phi_R]


def rafael_poly_mixed(a: float, b: float, L: Optional[float] = None) -> List[float]:
    """
    Polinômio misto integrando:

    - Teorema de Rafael (c² = 2ab + (a-b)²)
    - diagonais d₂D, d₃D
    - Constante Rafaeliana φ_R

    Retorna coeficientes [c0, c1, c2, c3] para:
      P(x) = c0 + c1 x + c2 x² + c3 x³
    """
    snap = build_geometry_snapshot(a, b, L)
    # c0: núcleo de diferença normalizado
    diff2 = (a - b) ** 2
    c0 = diff2
    # c1: componente 2ab (área viva)
    c1 = 2.0 * a * b
    # c2: relação entre diagonais e φ_R
    c2 = snap.d3 - snap.d2 * snap.phi_R
    # c3: termo de “overdrive” 3–6–9 simbólico
    c3 = snap.phi_R * (snap.d3 / max(snap.d2, 1e-9))

    return [c0, c1, c2, c3]


# ============================================================
#  SEÇÃO 4 – ANÁLISE DE LINHAS MATEMÁTICAS
# ============================================================

NUM_REGEX = re.compile(r"[-+]?\d+(?:[.,]\d+)?")


def normalize_number(token: str) -> float:
    """
    Normaliza string numérica para float (vírgula → ponto).
    """
    token = token.replace(",", ".")
    return float(token)


def approx_equal(x: float, y: float, rel_tol: float = 1e-3) -> bool:
    """
    Compara floats com tolerância relativa.
    """
    if y == 0:
        return False
    return abs(x - y) / abs(y) <= rel_tol


TRIG_KEYS = [
    r"\bsin\b", r"\bcos\b", r"\btan\b",
    "seno", "cosseno", "tangente",
    "radiano", "grau", "graus", "°",
]

GEOM_KEYS = [
    "triângulo", "triangulo", "cateto", "hipotenusa",
    "quadrado", "cubo", "toro", "toroide", "toroidal",
    "esfera", "círculo", "circulo", "diagonal",
]

GROWTH_KEYS = [
    "fibonacci", "fibonnaci", "fibonnacci", "lucas",
    "exponencial", "log", "log10", "ln", "polinômio", "polinomio",
]

RAFAELIA_KEYS = [
    "RAFAELIA", "Teorema de Rafael", "Constante Rafaeliana",
    "φ_R", "phi_R", "ToroidΔπφ", "toro_rafael",
    "ψχρΔΣΩ", "ΣΩΔΦBITRAF",
]


def categorize_line(text: str) -> Set[str]:
    """
    Atribui categorias a uma linha de texto matemático/geométrico.

    Possíveis rótulos:
      - trig, geom, growth, rafaelia, poly, matrix,
        complex, logical, prob, calculus, prime, topology
    """
    t = text.lower()
    cats: Set[str] = set()

    # trig
    if any(re.search(k, t) for k in TRIG_KEYS):
        cats.add("trig")

    # geom
    if any(k in t for k in GEOM_KEYS):
        cats.add("geom")

    # growth
    if any(k in t for k in GROWTH_KEYS):
        cats.add("growth")

    # rafaelia
    if any(k.lower() in t for k in (k.lower() for k in RAFAELIA_KEYS)):
        cats.add("rafaelia")

    # poly
    if re.search(r"[xyz]\s*\^\s*\d", t) or "polinômio" in t or "polinomio" in t:
        cats.add("poly")

    # matrix
    if any(k in t for k in ["matriz", "matrix", "vetor", "tensor", "det(", "determinante"]):
        cats.add("matrix")

    # complex
    if "i^2" in t or "imaginário" in t or "imaginario" in t or "complex" in t:
        cats.add("complex")

    # logical
    if any(k in t for k in ["∀", "∃", "⇒", "⇔", "conjunto", "∈", "∩", "∪"]):
        cats.add("logical")

    # prob
    if any(k in t for k in ["probabilidade", "distribuição", "gauss", "normal(", "σ", "desvio padrão"]):
        cats.add("prob")

    # calculus
    if any(k in t for k in ["d/dx", "∫", "derivada", "integral", "grad", "∇"]):
        cats.add("calculus")

    # primes explícitos menores
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if f"{p} " in text or f"{p}," in text or f"{p}." in text:
            cats.add("prime")
            break

    # topology
    if "toro" in t or "toroid" in t or "toroidal" in t:
        cats.add("topology")

    return cats


def extract_numbers(text: str) -> List[float]:
    """
    Extrai todos os números reais encontrados na linha (vírgula ou ponto).
    """
    vals: List[float] = []
    for m in NUM_REGEX.findall(text):
        try:
            vals.append(normalize_number(m))
        except ValueError:
            continue
    return vals


# ============================================================
#  SEÇÃO 5 – GERADOR DE CÓDIGO PY COMPLEXO
# ============================================================

AUTO_HEADER = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
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
\"\"\"

import math
from dataclasses import dataclass
from typing import List

"""


def generate_complex_python_module(path: str = "RAFAELIA_COMPLEX_AUTO.py") -> str:
    """
    Gera um módulo Python complexo com base nas funções e conceitos
    deste laboratório e grava em `path`.

    Retorna o caminho final gravado.
    """
    now = datetime.datetime.now().isoformat(timespec="seconds")
    phi_R = constante_rafaeliana()
    # escolhemos alguns parâmetros simbólicos
    a = 3.0
    b = 2.0
    L = 3.0
    snap = build_geometry_snapshot(a, b, L)
    poly = rafael_poly_mixed(a, b, L)

    # escolhe alguns primos para exemplo
    primes = primes_up_to(31)

    body_lines: List[str] = []

    body_lines.append(f"# Gerado em: {now}\n")
    body_lines.append(f"PHI_R = {phi_R!r}  # Constante Rafaeliana √3/2\n")
    body_lines.append(f"A_DEFAULT = {a!r}\n")
    body_lines.append(f"B_DEFAULT = {b!r}\n")
    body_lines.append(f"L_DEFAULT = {L!r}\n\n")

    body_lines.append(
        "def teorema_rafael(a: float, b: float) -> float:\n"
        "    \"\"\"Teorema de Rafael – c² = 2ab + (a - b)².\"\"\"\n"
        "    return 2.0 * a * b + (a - b) ** 2\n\n"
    )

    body_lines.append(
        "def hipotenusa_rafael(a: float, b: float) -> float:\n"
        "    \"\"\"Retorna c = √(2ab + (a - b)²).\"\"\"\n"
        "    return math.sqrt(teorema_rafael(a, b))\n\n"
    )

    body_lines.append(
        "def diagonal_quadrado(lado: float) -> float:\n"
        "    \"\"\"Diagonal de um quadrado: d₂D = L√2.\"\"\"\n"
        "    return lado * math.sqrt(2.0)\n\n"
    )

    body_lines.append(
        "def diagonal_cubo(lado: float) -> float:\n"
        "    \"\"\"Diagonal espacial de um cubo: d₃D = L√3.\"\"\"\n"
        "    return lado * math.sqrt(3.0)\n\n"
    )

    body_lines.append(
        "@dataclass\n"
        "class RafaelSnapshot:\n"
        "    \"\"\"Snapshot geométrico RAFAELIA (a, b, L, c, d₂D, d₃D, φ_R).\"\"\"\n"
        "    a: float\n"
        "    b: float\n"
        "    L: float\n"
        "    c: float\n"
        "    c2: float\n"
        "    d2: float\n"
        "    d3: float\n"
        "    phi_R: float\n\n"
        "    def ratio_d3_d2(self) -> float:\n"
        "        if self.d2 == 0:\n"
        "            return float('nan')\n"
        "        return self.d3 / self.d2\n\n"
    )

    body_lines.append(
        "def build_snapshot(a: float = A_DEFAULT, b: float = B_DEFAULT, L: float = L_DEFAULT) -> RafaelSnapshot:\n"
        "    \"\"\"Constroi um RafaelSnapshot com base no Teorema de Rafael.\"\"\"\n"
        "    c2 = teorema_rafael(a, b)\n"
        "    c = math.sqrt(c2)\n"
        "    d2 = diagonal_quadrado(L)\n"
        "    d3 = diagonal_cubo(L)\n"
        "    return RafaelSnapshot(a=a, b=b, L=L, c=c, c2=c2, d2=d2, d3=d3, phi_R=PHI_R)\n\n"
    )

    body_lines.append(
        "def rafael_poly_mixed(a: float, b: float, L: float) -> List[float]:\n"
        "    \"\"\"Polinômio RAFAELIA misto 2D/3D/φ_R: P(x) = c0 + c1 x + c2 x² + c3 x³.\"\"\"\n"
        "    snap = build_snapshot(a, b, L)\n"
        "    diff2 = (a - b) ** 2\n"
        "    c0 = diff2\n"
        "    c1 = 2.0 * a * b\n"
        "    c2 = snap.d3 - snap.d2 * snap.phi_R\n"
        "    c3 = snap.phi_R * (snap.d3 / max(snap.d2, 1e-9))\n"
        "    return [c0, c1, c2, c3]\n\n"
    )

    body_lines.append(
        "def eval_poly(coeffs: List[float], x: float) -> float:\n"
        "    \"\"\"Avalia P(x) pelo esquema de Horner.\"\"\"\n"
        "    acc = 0.0\n"
        "    for c in reversed(coeffs):\n"
        "        acc = acc * x + c\n"
        "    return acc\n\n"
    )

    # Exemplo específico baseado nos parâmetros desta sessão
    body_lines.append(
        f"SNAP_DEFAULT = build_snapshot(A_DEFAULT, B_DEFAULT, L_DEFAULT)\n"
        f"POLY_DEFAULT = rafael_poly_mixed(A_DEFAULT, B_DEFAULT, L_DEFAULT)\n\n"
    )

    # Primos e bases – exemplo simples incluído
    body_lines.append(
        f"PRIMOS_EXEMPLO = {primes!r}\n\n"
    )

    body_lines.append(
        "def demo_rafaelia() -> None:\n"
        "    \"\"\"Demonstra, em runtime, a visão geométrica RAFAELIA desta sessão.\n\n"
        "    - Imprime snapshot (a, b, L, c, d₂D, d₃D, φ_R, d₃D/d₂D)\n"
        "    - Avalia o polinômio misto em alguns pontos\n"
        "    \"\"\"\n"
        "    snap = SNAP_DEFAULT\n"
        "    print('=== DEMO RAFAELIA COMPLEX AUTO ===')\n"
        "    print(f'a = {snap.a}, b = {snap.b}, L = {snap.L}')\n"
        "    print(f'c² = 2ab + (a - b)² = {snap.c2:.6f}')\n"
        "    print(f'c  = √(c²) = {snap.c:.6f}')\n"
        "    print(f'd₂D = L√2 = {snap.d2:.6f}')\n"
        "    print(f'd₃D = L√3 = {snap.d3:.6f}')\n"
        "    print(f'φ_R = √3/2 = {snap.phi_R:.6f}')\n"
        "    print(f'd₃D/d₂D = {snap.ratio_d3_d2():.6f}  (≈ √(3/2))')\n"
        "    print('\\nPolinômio misto P(x) = c0 + c1 x + c2 x² + c3 x³:')\n"
        "    print('  coeficientes =', POLY_DEFAULT)\n"
        "    for x in [0.0, 1.0, 2.0, 3.0]:\n"
        "        y = eval_poly(POLY_DEFAULT, x)\n"
        "        print(f'  P({{x}}) = {{y:.6f}}')\n"
        "    print('\\nPrimos usados como base simbólica:', PRIMOS_EXEMPLO)\n"
        "    print('=== FIM DEMO RAFAELIA ===')\n\n"
    )

    body_lines.append(
        "if __name__ == '__main__':\n"
        "    demo_rafaelia()\n"
    )

    full_source = AUTO_HEADER + "".join(body_lines)

    with open(path, "w", encoding="utf-8") as f:
        f.write(full_source)

    return path


# ============================================================
#  SEÇÃO 6 – CLI BÁSICO
# ============================================================

def main() -> None:
    """
    CLI simples:

    - Gera RAFAELIA_COMPLEX_AUTO.py na pasta atual.
    - Mostra um pequeno resumo geométrico da sessão.
    """
    print("=== RAFAELIA :: Math & Geometry Lab ===")

    a, b, L = 3.0, 2.0, 3.0
    snap = build_geometry_snapshot(a, b, L)

    print("\n[ Snapshot Geométrico Padrão ]")
    print(f"a = {snap.a}, b = {snap.b}, L = {snap.L}")
    print(f"c² (Rafael) = 2ab + (a-b)² = {snap.c2:.6f}")
    print(f"c  = √(c²) = {snap.c:.6f}")
    print(f"d₂D = L√2 = {snap.d2:.6f}")
    print(f"d₃D = L√3 = {snap.d3:.6f}")
    print(f"φ_R = √3/2 = {snap.phi_R:.6f}")
    print(f"d₃D/d₂D = {snap.ratio_d3_d2():.6f}  (≈ √(3/2))")

    out_path = generate_complex_python_module()
    print(f"\n[OK] Módulo Python complexo gerado em: {out_path}")
    print("Use:  python RAFAELIA_COMPLEX_AUTO.py  para ver a demo interna.")
    print("=== FIM LAB ===")


if __name__ == "__main__":
    main()
