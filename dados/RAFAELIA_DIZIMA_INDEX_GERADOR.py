#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA :: DÍZIMA INDEX CORE
Gerador de índices de dízimas para 1/n em bases 10, 2, 8 e 16.

- Para cada n em [2..MAX_DEN], calcula a expansão de 1/n em cada base.
- Detecta:
    * Se é terminante (T) ou periódica (R).
    * Tamanho da parte não-periódica (pre_len).
    * Tamanho da parte periódica (period_len).
- Salva em TSV: RAFAELIA_DIZIMA_INDEX.tsv

Isso é útil para:
    - T.I. (compressão, codificação, padrões de repetição).
    - Matemática experimental RAFAELIA (ver onde as dízimas "moram").
"""

import sys
from fractions import Fraction

# ======================================================================
# CONFIGURAÇÃO
# ======================================================================

MAX_DEN = 128          # maior denominador n para 1/n
MAX_DIGITS = 80        # máximo de dígitos calculados na parte fracionária
OUTPUT_TSV = "RAFAELIA_DIZIMA_INDEX.tsv"

BASES = {
    10: "DEC",
    2:  "BIN",
    8:  "OCT",
    16: "HEX",
}

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


# ======================================================================
# FUNÇÕES BÁSICAS
# ======================================================================

def digit_to_char(d: int) -> str:
    """Converte dígito inteiro para caractere em base até 36."""
    if 0 <= d < len(DIGITS):
        return DIGITS[d]
    return "?"


def frac_expansion_base(num: int, den: int, base: int, max_digits: int = 80):
    """
    Expansão da fração num/den em base 'base', apenas parte fracionária.

    Retorna:
      pre  : string da parte NÃO-periódica
      rep  : string da parte periódica ("" se terminante)
      is_rep: bool (True se há dízima periódica, False se terminante)
    """
    if den == 0:
        raise ZeroDivisionError("Denominador zero não permitido.")

    # Assume 0 < num < den
    num = num % den

    # Mapa de resto -> posição do dígito onde apareceu
    seen = {}
    digits = []
    remainder = num
    repeat_start = None

    for i in range(max_digits):
        if remainder == 0:
            # Terminou: fracionário finito
            break

        if remainder in seen:
            repeat_start = seen[remainder]
            break

        seen[remainder] = i

        remainder *= base
        d = remainder // den
        remainder = remainder % den
        digits.append(digit_to_char(int(d)))

    if remainder == 0:
        # Terminante: tudo é "pré", não há período
        pre = "".join(digits)
        rep = ""
        is_rep = False
    else:
        # Periódica: separa pré-período e período
        if repeat_start is None:
            # Não detectou ciclo dentro do limite de dígitos
            pre = "".join(digits)
            rep = ""
            is_rep = False
        else:
            pre = "".join(digits[:repeat_start])
            rep = "".join(digits[repeat_start:])
            is_rep = True

    return pre, rep, is_rep


def analyze_fraction_1_over_n(n: int, base: int, max_digits: int = 80):
    """
    Analisa 1/n em base 'base' e retorna um dicionário com:
      - n
      - base
      - label (DEC/BIN/OCT/HEX)
      - type: 'T' (terminante) ou 'R' (periódica)
      - pre_len
      - period_len
      - pre
      - period
    """
    label = BASES.get(base, f"BASE{base}")
    pre, rep, is_rep = frac_expansion_base(1, n, base, max_digits=max_digits)
    typ = "R" if is_rep else "T"

    return {
        "n": n,
        "base": base,
        "label": label,
        "type": typ,
        "pre_len": len(pre),
        "period_len": len(rep),
        "pre": pre,
        "period": rep,
    }


# ======================================================================
# GERAÇÃO DO ÍNDICE COMPLETO
# ======================================================================

def generate_dizima_index(max_den: int = MAX_DEN,
                          bases = (10, 2, 8, 16),
                          max_digits: int = MAX_DIGITS,
                          output_file: str = OUTPUT_TSV):
    """
    Gera o índice de dízimas para 1/n, 2 <= n <= max_den,
    em todas as bases passadas.

    Salva em TSV com colunas:
    den, base, label, type, pre_len, period_len, pre, period
    """
    total_rows = 0
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("den\tbase\tlabel\ttype\tpre_len\tperiod_len\tpre\tperiod\n")
        for n in range(2, max_den + 1):
            for base in bases:
                info = analyze_fraction_1_over_n(n, base, max_digits)
                f.write(
                    f"{info['n']}\t"
                    f"{info['base']}\t"
                    f"{info['label']}\t"
                    f"{info['type']}\t"
                    f"{info['pre_len']}\t"
                    f"{info['period_len']}\t"
                    f"{info['pre']}\t"
                    f"{info['period']}\n"
                )
                total_rows += 1
    return total_rows


# ======================================================================
# EXEMPLOS NO TERMINAL
# ======================================================================

def print_sample_examples():
    """
    Mostra alguns exemplos clássicos no terminal:
    1/3, 1/7, 1/9, 1/11 em bases 10, 2, 8, 16.
    """
    samples_n = [3, 7, 9, 11]
    bases = [10, 2, 8, 16]

    print("===================================================================")
    print("RAFAELIA_DIZIMA_INDEX – Exemplos de dízimas por base")
    print("===================================================================\n")

    for n in samples_n:
        print(f"--- 1/{n} ---")
        for b in bases:
            info = analyze_fraction_1_over_n(n, b, MAX_DIGITS)
            typ = "terminante" if info["type"] == "T" else "periódica"
            # monta uma string curto-circuito para exibir
            if info["type"] == "T":
                frac_str = f"0.{info['pre']}"
            else:
                frac_str = f"0.{info['pre']}({info['period']})"
            print(
                f"  Base {b:>2} ({info['label']}): "
                f"{typ:11s}  pre_len={info['pre_len']:2d}, "
                f"period_len={info['period_len']:2d}  ->  {frac_str}"
            )
        print()

    print("===================================================================")
    print("Use o arquivo RAFAELIA_DIZIMA_INDEX.tsv para análise em T.I./RAFAELIA.")
    print("===================================================================\n")


# ======================================================================
# MAIN
# ======================================================================

def main():
    # Permite alterar MAX_DEN via linha de comando: python script.py 256
    max_den = MAX_DEN
    if len(sys.argv) >= 2:
        try:
            max_den = int(sys.argv[0 if False else 1])
        except ValueError:
            print("[AVISO] max_den inválido, usando padrão =", MAX_DEN)
            max_den = MAX_DEN

    print("===================================================================")
    print("RAFAELIA_DIZIMA_INDEX – Gerador de Índice de Dízimas (1/n)")
    print("===================================================================")
    print(f"Gerando índice para n = 2..{max_den}, bases = 10, 2, 8, 16...")
    total_rows = generate_dizima_index(max_den=max_den)
    print(f"[OK] Índice salvo em: {OUTPUT_TSV}")
    print(f"[OK] Linhas geradas: {total_rows}")
    print()

    # Mostra alguns exemplos clássicos direto no terminal
    print_sample_examples()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Execução interrompida pelo usuário.")
