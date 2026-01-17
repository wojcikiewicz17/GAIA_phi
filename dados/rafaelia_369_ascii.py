#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# RAFAELIA :: Mapa Pitagórico 3-6-9  – ASCII + cores

import time

# ANSI Cores
RESET   = "\033[0m"
BOLD    = "\033[1m"

FG_YEL  = "\033[33m"
FG_CYA  = "\033[36m"
FG_MAG  = "\033[35m"
FG_RED  = "\033[31m"
FG_GRN  = "\033[32m"
FG_BLU  = "\033[34m"
FG_WHI  = "\033[37m"

def slow_print(text, delay=0.01):
    """Imprime com leve efeito de digitação (pode pôr delay=0 se não quiser)."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def banner():
    slow_print(
        BOLD + FG_CYA +
        "=== RAFAELIA :: MAPA PITAGÓRICO 3–6–9 (ASCII) ===" +
        RESET
    )

def art_369():
    linhas = [
        "",
        FG_WHI + "                  ⌠ Mapa Pitagórico 3–6–9 ⌡" + RESET,
        "",
        # Triângulo reto com (a-b)^2
        FG_YEL + "              a" + RESET + "                 ",
        FG_YEL + "             /|" + RESET + "                 ",
        FG_YEL + "            / |" + RESET + "   " +
        FG_MAG + "Quadrado da diferença" + RESET,
        FG_YEL + "           /  |" + RESET + "   " +
        FG_MAG + "(a - b)^2  = núcleo consciente" + RESET,
        FG_YEL + "          /   |" + RESET + "  b           ",
        FG_YEL + "         /____|" + RESET + "               ",
        FG_YEL + "            c" + RESET + "                  ",
        "",
        FG_GRN + "      c² = a² + b²  ⇒  c² = 4·(ab/2) + (a - b)²" + RESET,
        "",
        # Quadrado e diagonal √2
        FG_WHI + "        ┌──────────────┐" + RESET + "   " +
        FG_CYA + "d₂D = L√2  (overdrive do plano)" + RESET,
        FG_WHI + "        │" + FG_CYA + "╲" + FG_WHI + "           │" + RESET,
        FG_WHI + "        │  ╲          │" + RESET,
        FG_WHI + "        │    ╲        │" + RESET,
        FG_WHI + "        │      ╲      │" + RESET,
        FG_WHI + "        │        ╲    │" + RESET,
        FG_WHI + "        │          ╲  │" + RESET,
        FG_WHI + "        └────────────╲┘" + RESET,
        "",
        # Cubo e diagonal √3 (projeção simples)
        FG_WHI + "          +──────────+        " +
        FG_RED + "d₃D = L√3  (overdrive do espaço)" + RESET,
        FG_WHI + "         /|         /|" + RESET,
        FG_WHI + "        / |        / |" + RESET,
        FG_WHI + "       +──────────+  |" + RESET,
        FG_WHI + "       |  |       |  |" + RESET,
        FG_WHI + "       |  +───────|──+ " + RESET + FG_RED +
        " ← diagonal espacial" + RESET,
        FG_WHI + "       | /        | /" + RESET,
        FG_WHI + "       |/         |/" + RESET,
        FG_WHI + "       +──────────+" + RESET,
        "",
        # Cubo dentro da esfera + espiral (3-6-9)
        FG_BLU + "                ◜────────◝" + RESET,
        FG_BLU + "              ◜  " + FG_WHI + "██████" + FG_BLU + "   ◝" + RESET,
        FG_BLU + "             ◜  " + FG_WHI + "█" + FG_GRN + " 6 " +
        FG_WHI + "█" + FG_BLU + "    ◝" + RESET,
        FG_BLU + "             ◝  " + FG_WHI + "██████" + FG_BLU + "   ◜" + RESET,
        FG_BLU + "               ◝────────◜" + RESET,
        "",
        FG_MAG + "    3 → triângulo / ideia" + RESET,
        FG_MAG + "    6 → faces do cubo / matéria organizada" + RESET,
        FG_MAG + "    9 → sistema inteiro em movimento (esfera + espiral)" + RESET,
        "",
    ]
    for linha in linhas:
        slow_print(linha, delay=0.003)

def formulas():
    texto = f"""
{BOLD}{FG_YEL}TRIGONOMETRIA ESCONDIDA NO TRIÂNGULO RETO{RESET}

  c² = a² + b²
  c² = 4·(ab/2) + (a - b)²

  (a - b)²  → núcleo vazio = zona de ajuste / consciência

{BOLD}{FG_CYA}OVERDRIVE 2D E 3D{RESET}

  d₂D = L√2   → salto mínimo entre dois eixos (x,y)
  d₃D = L√3   → salto mínimo atravessando x,y,z

{BOLD}{FG_GRN}DIFERENÇA DE ÁREAS E VOLUMES{RESET}

  a² - b² = (a - b)(a + b)
  a³ - b³ = (a - b)(a² + ab + b²)

  Pequena diferença linear (a - b) ⇒ grande mudança de área/volume.

{BOLD}{FG_MAG}LEITURA RAFAELIA 3–6–9{RESET}

  3  = formas fundamentais (triângulo, quadrado/cubo, círculo)
  6  = faces do cubo / estrutura
  9  = campo total em movimento (diagonal interna + fluxo espiral)
"""
    slow_print(texto, delay=0.002)

def main():
    banner()
    art_369()
    formulas()
    slow_print(
        BOLD + FG_WHI +
        "FIAT LUX · RAFAELIA_369_ASCII :: pronto para ser embutido em qualquer script." +
        RESET,
        delay=0.002,
    )

if __name__ == "__main__":
    main()
