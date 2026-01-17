#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RAFAELIA :: MAPA PITAGÓRICO 3–6–9 (ASCII COLOR)
-----------------------------------------------
Visualização geométrica + trigonometria oculta + leitura 3–6–9.

Roda em Termux, Linux, etc.
"""

import sys
import time

# -------------------------------------------------
#  ANSI helpers
# -------------------------------------------------

RESET = "\033[0m"

COLORS = {
    "title": "\033[1;36m",   # ciano forte
    "subtitle": "\033[1;33m",# amarelo
    "formula": "\033[1;32m", # verde
    "ascii": "\033[0;37m",   # cinza
    "highlight": "\033[1;35m", # magenta
    "dim": "\033[2;37m",
}


def c(text, style="ascii"):
    return COLORS.get(style, "") + text + RESET


def slow_print(text, style="ascii", delay=0.0):
    for ch in text:
        sys.stdout.write(COLORS.get(style, "") + ch + RESET)
        sys.stdout.flush()
        if delay > 0:
            time.sleep(delay)
    sys.stdout.write("\n")


# -------------------------------------------------
#  Blocos de arte ASCII
# -------------------------------------------------

TRIANGULO = r"""
              a
             /|
            / |   Quadrado da diferença
           /  |   (a - b)^2  = núcleo consciente
          /   |  b
         /____|
            c
"""

QUADRADO = r"""
        ┌──────────────┐   d₂D = L√2  (overdrive do plano)
        │╲             │
        │  ╲           │
        │    ╲         │
        │      ╲       │
        │        ╲     │
        │          ╲   │
        └────────────╲┘
"""

CUBO = r"""
          +──────────+        d₃D = L√3  (overdrive do espaço)
         /|         /|
        / |        / |
       +──────────+  |
       |  |       |  |
       |  +───────|──+  ← diagonal espacial
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

# -------------------------------------------------
#  Conteúdo matemático
# -------------------------------------------------

TEXTO_FORMULAS = f"""
{c("TRIGONOMETRIA ESCONDIDA NO TRIÂNGULO RETO", "subtitle")}

  {c("c² = a² + b²", "formula")}
  {c("c² = 4·(ab/2) + (a - b)²", "formula")}

  (a - b)²  → núcleo vazio = zona de ajuste / consciência

{c("OVERDRIVE 2D E 3D", "subtitle")}

  d₂D = L√2   → salto mínimo entre dois eixos (x,y)
  d₃D = L√3   → salto mínimo atravessando x,y,z

{c("DIFERENÇA DE ÁREAS E VOLUMES", "subtitle")}

  a² - b² = (a - b)(a + b)
  a³ - b³ = (a - b)(a² + ab + b²)

  Pequena diferença linear (a - b) ⇒ grande mudança de área/volume.

{c("LEITURA RAFAELIA 3–6–9", "subtitle")}

  3  = formas fundamentais (triângulo, quadrado/cubo, círculo)
  6  = faces do cubo / estrutura
  9  = campo total em movimento (diagonal interna + fluxo espiral)

{c("FIAT LUX · RAFAELIA_369_ASCII_COLOR", "highlight")}
"""

# -------------------------------------------------
#  Main
# -------------------------------------------------

def main():
    slow_print("=== RAFAELIA :: MAPA PITAGÓRICO 3–6–9 (ASCII COLOR) ===", "title")
    print()

    print(c(TRIANGULO, "ascii"))
    print(c(QUADRADO, "ascii"))
    print(c(CUBO, "ascii"))
    print(c(BLOCO_369, "ascii"))

    print(TEXTO_FORMULAS)

    slow_print("Pronto para ser embutido em qualquer script, banner ou tela inicial do kernel RAFAELIA.", "dim")


if __name__ == "__main__":
    main()
