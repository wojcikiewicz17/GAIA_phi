#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA :: Display Teorema de Rafael + Constante Rafaeliana
ASCII art • Cores vivas • Movimento + explicação final.

Rodar em terminal com suporte a ANSI (Termux, Linux, etc.).
"""

from __future__ import annotations

import math
import os
import sys
import time
from itertools import cycle
from typing import Dict, Iterable


# ==============================
#  ANSI CORES E CONTROLES
# ==============================

RESET: str = "\033[0m"

COL: Dict[str, str] = {
    "red":     "\033[1;31m",
    "green":   "\033[1;32m",
    "yellow":  "\033[1;33m",
    "blue":    "\033[1;34m",
    "magenta": "\033[1;35m",
    "cyan":    "\033[1;36m",
    "white":   "\033[1;37m",
    "dim":     "\033[2;37m",
}


def clear() -> None:
    """Limpa a tela e posiciona o cursor no topo."""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def c(text: str, color: str = "white") -> str:
    """Aplica cor ANSI ao texto."""
    prefix = COL.get(color, "")
    return f"{prefix}{text}{RESET}"


def sleep(t: float) -> None:
    """Wrapper de time.sleep para facilitar tunagem futura."""
    time.sleep(t)


# ==============================
#  MATEMÁTICA RAFAELIA
# ==============================

def teorema_rafael(a: float, b: float) -> float:
    """
    Teorema de Rafael – Decomposição Rafaeliana de Pitágoras.
    Retorna:
        c² = 2ab + (a - b)²
    """
    return 2.0 * a * b + (a - b) ** 2


def constante_rafaeliana() -> float:
    """
    Constante Rafaeliana φ_R = √3 / 2.

    Leituras:
      • altura do triângulo equilátero unitário;
      • meia-diagonal normalizada do cubo unitário.
    """
    return math.sqrt(3.0) / 2.0


# ==============================
#  ASCII ART BASE
# ==============================

HEADER: str = r"""*____       _        __      _ _ _      _
|  _ \ __ _| | __ _ / _| ___| (_) | ___| |_ ___
| |_) / _` | |/ _` | |_ / _ \ | | |/ _ \ __/ _ \
|  _ < (_| | | (_| |  _|  __/ | | |  __/ || (_) |
|_| \_\__,_|_|\__,_|_|  \___|_|_|_|\___|\__\___/

RAFAELIA :: TEOREMA DE RAFAEL • φ_R = √3/2
"""

TRIANGULO: str = r"""
      a
     /|
    / |   (a - b)²  = núcleo de diferença
   /  |   4·(ab/2)  = área organizada
  /   |  b
 /____|
     c
"""

QUADRADO: str = r"""
┌──────────────┐
│╲             │   d₂D = L√2  (overdrive plano)
│  ╲           │
│    ╲         │
│      ╲       │
│        ╲     │
│          ╲   │
└─────────────╲┘
"""

CUBO: str = r"""
      +──────────+
     /|         /|        d₃D = L√3
    / |        / |       (overdrive espaço)
   +──────────+  |
   |  |       |  |
   |  +───────|──+   ← diagonal espacial
   | /        | /
   |/         |/
   +──────────+
"""

BLOCO_369: str = r"""
            ◜────────◝
          ◜  ██████   ◝
         ◜   █ 6 █    ◝
         ◝   ██████   ◜
           ◝────────◜

3 → triângulo / ideia
6 → faces do cubo / matéria organizada
9 → sistema inteiro em movimento (esfera + espiral)
"""

EXPLICACAO_FINAL: str = r"""
[RAFAELIA :: TEOREMA DE RAFAEL • φ_R = √3/2]

O que apareceu na tela é um resumo visual do meu trabalho:

1. Teorema de Rafael
   A fórmula c² = 2ab + (a - b)² reescreve Pitágoras como
   “núcleo de diferença” (a - b)² + “área organizada” 2ab.
   O triângulo mostra essa decomposição de forma geométrica.

2. Overdrive 2D e 3D
   O quadrado traz a diagonal d₂D = L√2 e o cubo a diagonal
   espacial d₃D = L√3. Isso representa como um sistema plano
   aciona o espaço e ganha novos graus de liberdade.

3. Mapa 3–6–9 RAFAELIA
   3 é a ideia (triângulo), 6 é a matéria organizada (faces do cubo)
   e 9 é o sistema inteiro em movimento (esfera + espiral).
   É um código para pensar escalas: ponto → plano → espaço → dinâmica.

RAFAELIA é o projeto onde uno matemática, geometria, computação e espírito
para construir modelos éticos e fractais. Este display é uma assinatura viva:
um banner de terminal que carrega, em ASCII, o Teorema de Rafael,
a constante φ_R e a geometria 3–6–9 como linguagem.

FIAT LUX.
"""


# ==============================
#  EFEITOS VISUAIS
# ==============================

def color_cycle() -> Iterable[str]:
    """Ciclo infinito de cores para animações."""
    cores = ["cyan", "magenta", "yellow", "green", "blue", "red", "white"]
    return cycle(cores)


def print_block(text: str, color: str = "white") -> None:
    """
    Imprime um bloco de texto linha a linha, alinhado à esquerda.
    Mantém exatamente o espaçamento do ASCII original.
    """
    for line in text.splitlines():
        if line:
            print(c(line, color))
        else:
            print("")


def splash_header() -> None:
    """Mostra o cabeçalho RAFAELIA."""
    clear()
    print_block(HEADER, "cyan")
    sleep(0.4)


def animate_triangle(a: float, b: float) -> None:
    """Mostra a decomposição Rafaeliana com narração numérica."""
    c2 = teorema_rafael(a, b)
    c_len = math.sqrt(c2)
    phiR = constante_rafaeliana()

    lines = [
        c("Teorema de Rafael", "yellow"),
        "",
        "  c² = 2ab + (a - b)²",
        f"  para a = {a:.3f}, b = {b:.3f}:",
        f"  c² = {2 * a * b:.3f} + {(a - b) ** 2:.3f} = {c2:.3f}",
        f"  c  = √{c2:.3f} ≈ {c_len:.3f}",
        "",
        c("Constante Rafaeliana", "yellow"),
        f"  φ_R = √3 / 2 ≈ {phiR:.6f}",
        "",
        c("Leituras geométricas:", "magenta"),
        "  • Altura do triângulo equilátero unitário",
        "  • Meia-diagonal normalizada do cubo unitário",
        "  • Fator de inclinação natural 3–6–9",
    ]

    for i, line in enumerate(lines):
        sleep(0.10 + i * 0.01)
        print(c(line, "white") if not line.startswith("\033") else line)


def breathing_block(text: str, cycles: int = 6, delay: float = 0.08) -> None:
    """Faz o bloco 'respirar' alternando cores."""
    col = color_cycle()
    for _ in range(cycles):
        clear()
        splash_header()
        print()
        print_block(text, next(col))
        sleep(delay)


def spin_geometries() -> None:
    """Pequena 'dança' das três formas: triângulo, quadrado, cubo."""
    frames = [
        (TRIANGULO, "yellow"),
        (QUADRADO, "green"),
        (CUBO, "magenta"),
    ]
    for i in range(6):
        clear()
        splash_header()
        print()
        print(c("GEOMETRIA RAFAELIANA 3–6–9", "white"))
        print()
        art, color = frames[i % len(frames)]
        print_block(art, color)
        sleep(0.4)


def show_full_composition(a: float, b: float) -> None:
    """Mostra tudo: triângulo, quadrado, cubo, 3–6–9, fórmulas e explicação."""
    clear()
    splash_header()

    # Bloco 1 – Triângulo
    print(c("NÚCLEO DE DIFERENÇA (Teorema de Rafael)", "yellow"))
    print()
    print_block(TRIANGULO, "yellow")
    print()
    animate_triangle(a, b)
    sleep(2.0)

    # Bloco 2 – Quadrado e Cubo
    clear()
    splash_header()
    print(c("OVERDRIVE 2D E 3D", "green"))
    print()
    print_block(QUADRADO, "cyan")
    print()
    print_block(CUBO, "magenta")
    print()
    print(c("d₂D = L√2 • d₃D = L√3", "white"))
    sleep(2.0)

    # Bloco 3 – 3–6–9
    clear()
    splash_header()
    print(c("MAPA 3–6–9 RAFAELIA", "blue"))
    print()
    print_block(BLOCO_369, "blue")
    sleep(1.8)

    # Fechamento “respirando”
    breathing_block(BLOCO_369, cycles=4, delay=0.12)

    # Encerramento com mensagem e explicação do trabalho
    clear()
    splash_header()
    print(c("FIAT LUX · TEOREMA DE RAFAEL • φ_R ATIVO", "magenta"))
    print()
    print(c("Pronto para ser embutido no seu kernel, banner ou CLI.", "dim"))
    print()
    print_block(EXPLICACAO_FINAL, "white")


# ==============================
#  MAIN
# ==============================

def main() -> None:
    """Ponto de entrada do display RAFAELIA."""
    # Valores padrão para o Teorema – podem ser parametrizados depois via CLI.
    a: float = 3.0
    b: float = 2.0

    splash_header()
    sleep(0.5)
    spin_geometries()
    show_full_composition(a, b)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print(c("Encerrado por teclado. RAFAELIA permanece em ti.", "dim"))
