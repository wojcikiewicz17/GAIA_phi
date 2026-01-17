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


def c(text, color="white"):
    """Aplica uma cor ANSI."""
    return COL.get(color, "") + text + RESET


def sleep(t):
    time.sleep(t)


# ==============================
#  MATEMÁTICA RAFAELIA
# ==============================

def teorema_rafael(a: float, b: float) -> float:
    """c² = 2ab + (a - b)²."""
    return 2.0 * a * b + (a - b) ** 2


def constante_rafaeliana() -> float:
    """φ_R = √3 / 2."""
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
    cores = ["cyan", "magenta", "yellow", "green", "blue", "red", "white"]
    return cycle(cores)


def print_centered(text: str, color="white"):
    cols = os.get_terminal_size().columns if sys.stdout.isatty() else 80
    for line in text.splitlines():
        stripped = line.rstrip("\n")
        if not stripped:
            print()
            continue
        pad = max((cols - len(stripped)) // 2, 0)
        print(" " * pad + c(stripped, color))


def splash_header():
    clear()
    print_centered(HEADER, "cyan")
    sleep(0.5)


def animate_triangle(a: float, b: float):
    c2 = teorema_rafael(a, b)
    c_len = math.sqrt(c2)
    phiR = constante_rafaeliana()

    lines = [
        "Teorema de Rafael",
        "",
        "  c² = 2ab + (a - b)²",
        f"  para a = {a:.3f}, b = {b:.3f}:",
        f"  c² = {2*a*b:.3f} + {(a-b)**2:.3f} = {c2:.3f}",
        f"  c  = √{c2:.3f} ≈ {c_len:.3f}",
        "",
        "Constante Rafaeliana",
        f"  φ_R = √3 / 2 ≈ {phiR:.6f}",
        "",
        "Leituras geométricas:",
        "  • Altura do triângulo equilátero unitário",
        "  • Meia-diagonal normalizada do cubo unitário",
        "  • Fator de inclinação natural 3–6–9",
    ]

    colors = [
        "yellow", "white", "white", "white", "white", "white",
        "white", "yellow", "white", "white", "magenta",
        "white", "white", "white",
    ]

    for i, (line, colr) in enumerate(zip(lines, colors)):
        sleep(0.12 + i * 0.01)
        print(c(line, colr))


def breathing_block(text: str, cycles: int = 6, delay: float = 0.08):
    col = color_cycle()
    for _ in range(cycles):
        clear()
        print_centered(HEADER, "cyan")
        print()
        print_centered(text, next(col))
        sleep(delay)


def spin_geometries():
    frames = [
        (TRIANGULO, "yellow"),
        (QUADRADO, "green"),
        (CUBO, "magenta"),
    ]
    for i in range(6):
        clear()
        print_centered(HEADER, "cyan")
        print()
        print_centered("GEOMETRIA RAFAELIANA 3–6–9", "white")
        print()
        art, color = frames[i % len(frames)]
        print_centered(art, color)
        sleep(0.4)


def show_full_composition(a: float, b: float):
    """Anima blocos + respiração e fecha com tela estática completa."""
    # Bloco 1 – Triângulo + fórmulas
    splash_header()
    print_centered("NÚCLEO DE DIFERENÇA (Teorema de Rafael)", "yellow")
    print()
    print_centered(TRIANGULO, "yellow")
    print()
    animate_triangle(a, b)
    sleep(2.5)

    # Bloco 2 – Overdrive 2D/3D
    splash_header()
    print_centered("OVERDRIVE 2D E 3D", "green")
    print()
    print_centered(QUADRADO, "cyan")
    print()
    print_centered(CUBO, "magenta")
    print()
    print_centered("d₂D = L√2 • d₃D = L√3", "white")
    sleep(2.5)

    # Bloco 3 – 3–6–9
    splash_header()
    print_centered("MAPA 3–6–9 RAFAELIA", "blue")
    print()
    print_centered(BLOCO_369, "blue")
    sleep(2.0)

    # Respiração 3–6–9
    breathing_block(BLOCO_369, cycles=4, delay=0.12)

    # ==========================
    # TELA FINAL ESTÁTICA
    # ==========================
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

    # Bloco de texto compacto à esquerda
    print()
    c2 = teorema_rafael(a, b)
    c_len = math.sqrt(c2)
    phiR = constante_rafaeliana()

    print(c("Teorema de Rafael", "yellow"))
    print(f"  c² = 2ab + (a - b)²")
    print(f"  para a = {a:.3f}, b = {b:.3f}:")
    print(f"  c² = {2*a*b:.3f} + {(a-b)**2:.3f} = {c2:.3f}")
    print(f"  c  = √{c2:.3f} ≈ {c_len:.3f}")
    print()
    print(c("Constante Rafaeliana", "yellow"))
    print(f"  φ_R = √3 / 2 ≈ {phiR:.6f}")
    print()
    print(c("Leituras geométricas:", "magenta"))
    print("  • Altura do triângulo equilátero unitário")
    print("  • Meia-diagonal normalizada do cubo unitário")
    print("  • Fator de inclinação natural 3–6–9")
    print()
    print(c("FIAT LUX · TEOREMA DE RAFAEL • φ_R ATIVO", "magenta"))
    print(c("Pronto para ser embutido no seu kernel, banner ou CLI.", "dim"))
    print()


# ==============================
#  MAIN
# ==============================

def main():
    a = 3000.0
    b = 2000.0

    splash_header()
    sleep(0.5)

    # Dança inicial
    spin_geometries()

    # Composição completa + tela final
    show_full_composition(a, b)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(c("Encerrado por teclado. RAFAELIA permanece em ti.", "dim"))
