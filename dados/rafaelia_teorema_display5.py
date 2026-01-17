#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA :: Display Teorema de Rafael + Constante Rafaeliana
ASCII art • Cores vivas • Movimento

Rodar em terminal com suporte a ANSI (Termux, Linux, etc.).
"""

import math
import os
import sys
import time
from itertools import cycle

# ==============================
#  ANSI CORES E CONTROLES
# ==============================

RESET = "\033[0m"

COL = {
    "red":     "\033[1;31m",
    "green":   "\033[1;32m",
    "yellow":  "\033[1;33m",
    "blue":    "\033[1;34m",
    "magenta": "\033[1;35m",
    "cyan":    "\033[1;36m",
    "white":   "\033[1;37m",
    "dim":     "\033[2;37m",
}


def clear():
    """Limpa a tela e posiciona o cursor no topo."""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def c(text: str, color: str = "white") -> str:
    """Aplica uma cor ANSI."""
    return COL.get(color, "") + text + RESET


def sleep(t: float):
    time.sleep(t)


# ==============================
#  MATEMÁTICA RAFAELIA
# ==============================

def teorema_rafael(a: float, b: float) -> float:
    """
    Teorema de Rafael – Decomposição Rafaeliana de Pitágoras.
    Retorna c² = 2ab + (a - b)².
    """
    return 2.0 * a * b + (a - b) ** 2


def constante_rafaeliana() -> float:
    """
    Constante Rafaeliana φ_R = √3 / 2.
    Altura do triângulo equilátero unitário
    e meia-diagonal normalizada do cubo unitário.
    """
    return math.sqrt(3.0) / 2.0


# ==============================
#  ASCII ART BASE
# ==============================

HEADER = r"""
   ____       _        __      _ _ _      _
  |  _ \ __ _| | __ _ / _| ___| (_) | ___| |_ ___
  | |_) / _` | |/ _` | |_ / _ \ | | |/ _ \ __/ _ \
  |  _ < (_| | | (_| |  _|  __/ | | |  __/ || (_) |
  |_| \_\__,_|_|\__,_|_|  \___|_|_|_|\___|\__\___/

      RAFAELIA :: TEOREMA DE RAFAEL • φ_R = √3/2
"""

TRIANGULO = r"""
              a
             /|
            / |   (a - b)²  = núcleo de diferença
           /  |   4·(ab/2)  = área organizada
          /   |  b
         /____|
            c
"""

QUADRADO = r"""
        ┌──────────────┐
        │╲             │   d₂D = L√2  (overdrive plano)
        │  ╲           │
        │    ╲         │
        │      ╲       │
        │        ╲     │
        │          ╲   │
        └────────────╲┘
"""

CUBO = r"""
          +──────────+
         /|         /|        d₃D = L√3  (overdrive espaço)
        / |        / |
       +──────────+  |
       |  |       |  |
       |  +───────|──+   ← diagonal espacial
       | /        | /
       |/         |/
       +──────────+
"""

BLOCO_369 = r"""
                ◜────────◝
              ◜  ██████   ◝
             ◜   █ 6 █    ◝
             ◝   ██████   ◜
               ◝────────◜

    3 → triângulo / ideia
    6 → faces do cubo / matéria organizada
    9 → sistema inteiro em movimento (esfera + espiral)
"""


# ==============================
#  EFEITOS VISUAIS
# ==============================

def color_cycle():
    """Ciclo infinito de cores para animações."""
    cores = ["cyan", "magenta", "yellow", "green", "blue", "red", "white"]
    return cycle(cores)


def term_cols() -> int:
    if sys.stdout.isatty():
        try:
            return os.get_terminal_size().columns
        except OSError:
            return 80
    return 80


def print_centered(text: str, color: str = "white"):
    """
    Imprime bloco centralizado.
    Se a linha for maior ou igual à largura do terminal, imprime sem centralizar
    para evitar quebra feia (palavras descendo).
    """
    cols = term_cols()
    for line in text.splitlines():
        stripped = line.rstrip("\n")
        if not stripped:
            print()
            continue
        if len(stripped) >= cols:
            print(c(stripped, color))
        else:
            pad = max((cols - len(stripped)) // 2, 0)
            print(" " * pad + c(stripped, color))


def splash_header():
    clear()
    print_centered(HEADER, "cyan")
    sleep(0.3)


def animate_triangle(a: float, b: float):
    """Texto do Teorema + φ_R (sem centralizar, pra não quebrar)."""
    c2 = teorema_rafael(a, b)
    c_len = math.sqrt(c2)
    phiR = constante_rafaeliana()

    print(c("Teorema de Rafael", "yellow"))
    print("  c² = 2ab + (a - b)²")
    print(f"  para a = {a:,.3f}, b = {b:,.3f}:".replace(",", "."))
    print(f"  c² = {2*a*b:,.3f} + {(a-b)**2:,.3f} = {c2:,.3f}".replace(",", "."))
    print(f"  c  = √{c2:,.3f} ≈ {c_len:,.3f}".replace(",", "."))
    print()
    print(c("Constante Rafaeliana", "yellow"))
    print(f"  φ_R = √3 / 2 ≈ {phiR:.6f}")
    print()
    print(c("Leituras geométricas:", "magenta"))
    print("  • Altura do triângulo equilátero unitário")
    print("  • Meia-diagonal normalizada do cubo unitário")
    print("  • Fator de inclinação natural 3–6–9")
    print()


def breathing_block(text: str, cycles: int = 4, delay: float = 0.10):
    """Respiração leve no bloco 3–6–9."""
    col = color_cycle()
    for _ in range(cycles):
        clear()
        print_centered(HEADER, "cyan")
        print()
        print_centered("MAPA 3–6–9 RAFAELIA", "blue")
        print()
        print_centered(text, next(col))
        sleep(delay)


def spin_geometries():
    """Pequena 'dança' das três formas: triângulo, quadrado, cubo."""
    frames = [
        (TRIANGULO, "yellow"),
        (QUADRADO, "green"),
        (CUBO, "magenta"),
    ]
    for i in range(6):
        clear()
        print_centered(HEADER, "cyan")
        art, color = frames[i % len(frames)]
        print()
        print_centered("GEOMETRIA RAFAELIANA 3–6–9", "white")
        print()
        print_centered(art, color)
        sleep(0.4)


def show_full_composition(a: float, b: float):
    """Anima blocos e termina numa tela única com tudo."""

    # Bloco 1 – Núcleo de diferença
    splash_header()
    print_centered("NÚCLEO DE DIFERENÇA (Teorema de Rafael)", "yellow")
    print()
    print_centered(TRIANGULO, "yellow")
    print()
    animate_triangle(a, b)
    sleep(2.0)

    # Bloco 2 – Overdrive 2D / 3D
    splash_header()
    print_centered("OVERDRIVE 2D E 3D", "green")
    print()
    print_centered(QUADRADO, "cyan")
    print()
    print_centered(CUBO, "magenta")
    print()
    print_centered("d₂D = L√2   •   d₃D = L√3", "white")
    sleep(2.0)

    # Bloco 3 – 3–6–9 respirando
    breathing_block(BLOCO_369, cycles=4, delay=0.12)

    # Tela final única
    clear()
    print_centered(HEADER, "cyan")
    print()
    print_centered("GEOMETRIA RAFAELIANA 3–6–9", "white")
    print()
    print_centered(TRIANGULO, "yellow")
    print()
    print_centered(QUADRADO, "green")
    print()
    print_centered(CUBO, "magenta")
    print()
    print_centered(BLOCO_369, "blue")
    print()
    animate_triangle(a, b)  # reaproveita o texto bonitinho
    print(c("FIAT LUX · TEOREMA DE RAFAEL • φ_R ATIVO", "magenta"))
    print(c("Pronto para ser embutido no seu kernel, banner ou CLI.", "dim"))
    print()


# ==============================
#  MAIN
# ==============================

def main():
    # Valores “clássicos” do print que você gostou
    a = 3000.0
    b = 2000.0

    splash_header()
    sleep(0.3)

    spin_geometries()
    show_full_composition(a, b)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(c("Encerrado por teclado. RAFAELIA permanece em ti.", "dim"))
