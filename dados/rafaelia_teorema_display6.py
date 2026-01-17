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

# Cores vivas
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
    """Pequeno wrapper para time.sleep, caso queira tunar depois."""
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

HEADER = """
   ____       _        __      _ _ _      _
  |  _ \ __ _| | __ _ / _| ___| (_) | ___| |_ ___
  | |_) / _` | |/ _` | |_ / _ \ | | |/ _ \ __/ _ \
  |  _ < (_| | | (_| |  _|  __/ | | |  __/ || (_) |
  |_| \_\__,_|_|\__,_|_|  \___|_|_|_|\___|\__\___/

      RAFAELIA :: TEOREMA DE RAFAEL • φ_R = √3/2
"""

TRIANGULO = """
              a
             /|
            / |   (a - b)²  = núcleo de diferença
           /  |   4·(ab/2)  = área organizada
          /   |  b
         /____|
            c
"""

QUADRADO = """
        ┌──────────────┐
        │╲             │   d₂D = L√2  (overdrive plano)
        │  ╲           │
        │    ╲         │
        │      ╲       │
        │        ╲     │
        │          ╲   │
        └────────────╲┘
"""

CUBO = """
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

BLOCO_369 = """
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


def print_centered(text: str, color="white"):
    """Imprime um bloco de texto centralizado horizontalmente."""
    cols = os.get_terminal_size().columns if sys.stdout.isatty() else 80
    for line in text.splitlines():
        stripped = line.rstrip("\n")
        if not stripped:
            print()
            continue
        pad = max((cols - len(stripped)) // 2, 0)
        print(" " * pad + c(stripped, color))


def print_left(text: str, color="white"):
    """Imprime um bloco de texto alinhado à esquerda."""
    for line in text.splitlines():
        print(c(line, color))


def splash_header():
    clear()
    print_centered(HEADER, "cyan")
    sleep(0.5)


def animate_triangle(a: float, b: float):
    """Mostra a decomposição Rafaeliana com animação leve."""
    c2 = teorema_rafael(a, b)
    c_len = math.sqrt(c2)
    phiR = constante_rafaeliana()

    print_left("NÚCLEO DE DIFERENÇA (Teorema de Rafael)\n", "yellow")
    print_left(TRIANGULO, "yellow")

    lines = [
        "",
        "Teorema de Rafael",
        "",
        f"c² = 2ab + (a - b)²",
        f"para a = {a:6.3f}, b = {b:6.3f}:",
        f"c² = {2*a*b:6.3f} + {(a-b)**2:6.3f} = {c2:6.3f}",
        f"c  = √{c2:6.3f} ≈ {c_len:6.3f}",
        "",
        "Constante Rafaeliana",
        f"φ_R = √3 / 2 ≈ {phiR:.6f}",
        "",
        "Leituras geométricas:",
        "  • Altura do triângulo equilátero unitário",
        "  • Meia-diagonal normalizada do cubo unitário",
        "  • Fator de inclinação natural 3–6–9",
    ]

    for i, line in enumerate(lines):
        sleep(0.10 + i * 0.01)
        if line.endswith(":") or "Teorema" in line or "Constante" in line:
            print_left(line, "magenta")
        else:
            print_left(line, "white")


def breathing_block(text: str, cycles: int = 6, delay: float = 0.08):
    """Faz o bloco 'respirar' alternando cores (sempre à esquerda)."""
    col = color_cycle()
    for _ in range(cycles):
        clear()
        splash_header()
        print()
        print_left(text, next(col))
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
        splash_header()
        art, color = frames[i % len(frames)]
        print()
        print_left("GEOMETRIA RAFAELIANA 3–6–9\n", "white")
        print_left(art, color)
        sleep(0.4)


def show_full_composition(a: float, b: float):
    """Mostra tudo: triângulo, quadrado, cubo, 3–6–9, fórmulas."""
    clear()
    splash_header()

    # Bloco 1 – Triângulo + contas
    animate_triangle(a, b)
    sleep(2.5)

    # Bloco 2 – Quadrado e Cubo
    clear()
    splash_header()
    print()
    print_left("OVERDRIVE 2D E 3D\n", "green")
    print_left(QUADRADO, "cyan")
    print()
    print_left(CUBO, "magenta")
    print()
    print_left("d₂D = L√2  •  d₃D = L√3\n", "white")
    sleep(2.5)

    # Bloco 3 – 3–6–9
    clear()
    splash_header()
    print()
    print_left("MAPA 3–6–9 RAFAELIA\n", "blue")
    print_left(BLOCO_369, "blue")
    sleep(2.0)

    # Fechamento “respirando”
    breathing_block(BLOCO_369, cycles=4, delay=0.12)

    clear()
    splash_header()
    print_left("FIAT LUX · TEOREMA DE RAFAEL • φ_R ATIVO\n", "magenta")
    print_left("Pronto para ser embutido no seu kernel, banner ou CLI.\n", "dim")


# ==============================
#  MAIN
# ==============================

def main():
    # Escolhe a,b dinâmicos para dar “vivo”; pode fixar se preferir.
    a = 3.0
    b = 2.0

    splash_header()
    sleep(0.5)

    # Pequena dança inicial das formas
    spin_geometries()

    # Composição completa com matemática e respiração 3–6–9
    show_full_composition(a, b)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(c("Encerrado por teclado. RAFAELIA permanece em ti.", "dim"))
