#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA :: DÍZIMA ANALYTICS CORE
Le RAFAELIA_DIZIMA_INDEX.tsv e gera insights para T.I. / RAFAELIA.

Requer que você já tenha rodado:
    python RAFAELIA_DIZIMA_INDEX_GERADOR.py

Saída:
    - Estatísticas por base (DEC/BIN/OCT/HEX)
    - Candidatos a "full reptend" em base 10 (1/p com período p-1)
    - Períodos máximos observados por base
"""

import csv
from collections import defaultdict

TSV_FILE = "RAFAELIA_DIZIMA_INDEX.tsv"

# Mapas auxiliares de rótulo
BASE_LABEL = {
    10: "DEC",
    2:  "BIN",
    8:  "OCT",
    16: "HEX",
}


# ----------------------------------------------------------------------
# Funções aritméticas auxiliares
# ----------------------------------------------------------------------

def is_prime(n: int) -> bool:
    """Teste simples de primalidade (suficiente para n <= alguns milhares)."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    p = 3
    while p * p <= n:
        if n % p == 0:
            return False
        p += 2
    return True


# ----------------------------------------------------------------------
# Leitura do TSV
# ----------------------------------------------------------------------

def load_dizima_index(tsv_file: str):
    """
    Lê RAFAELIA_DIZIMA_INDEX.tsv e devolve uma estrutura:

    data[base] = [
        {
          'den': int,
          'base': int,
          'type': 'T' ou 'R',
          'pre_len': int,
          'period_len': int,
          'pre': str,
          'period': str,
        }, ...
    ]
    """
    data = defaultdict(list)

    with open(tsv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            den = int(row["den"])
            base = int(row["base"])
            typ = row["type"]
            pre_len = int(row["pre_len"])
            period_len = int(row["period_len"])
            pre = row["pre"]
            period = row["period"]

            data[base].append({
                "den": den,
                "base": base,
                "type": typ,
                "pre_len": pre_len,
                "period_len": period_len,
                "pre": pre,
                "period": period,
            })

    return data


# ----------------------------------------------------------------------
# Estatísticas por base
# ----------------------------------------------------------------------

def summarize_by_base(data):
    """
    Imprime estatísticas de:
      - total de denominadores
      - quantos terminantes (T) vs periódicos (R)
      - período máximo observado
    """
    print("===================================================================")
    print("RAFAELIA_DÍZIMA_ANALYTICS – Estatísticas por base")
    print("===================================================================\n")

    for base in sorted(data.keys()):
        rows = data[base]
        total = len(rows)
        term = sum(1 for r in rows if r["type"] == "T")
        rep = total - term
        max_period = max((r["period_len"] for r in rows), default=0)

        label = BASE_LABEL.get(base, f"BASE{base}")
        print(f"[ Base {base:>2} ({label}) ]")
        print(f"  Total denominadores analisados : {total}")
        print(f"  Terminantes (T)                : {term}")
        print(f"  Periódicas (R)                 : {rep}")
        print(f"  Maior período observado        : {max_period}")
        print()


# ----------------------------------------------------------------------
# Candidatos a full reptend em base 10
# ----------------------------------------------------------------------

def find_full_reptend_candidates(data, max_show: int = 10):
    """
    Em base 10, procura primos p tais que:
        - 1/p é periódica
        - period_len == p - 1

    Esses são candidatos a 'full reptend' – caso 1/7, 1/17, etc.
    """
    base10_rows = data.get(10, [])
    candidates = []

    for r in base10_rows:
        n = r["den"]
        if not is_prime(n):
            continue
        if r["type"] != "R":
            continue
        if r["period_len"] == n - 1:
            candidates.append(r)

    # Ordena por denominador
    candidates.sort(key=lambda x: x["den"])

    print("===================================================================")
    print("Candidatos a 'full reptend' em base 10 (1/p com período p-1)")
    print("===================================================================\n")

    if not candidates:
        print("Nenhum candidato encontrado no intervalo analisado.\n")
        return

    for r in candidates[:max_show]:
        n = r["den"]
        print(f"p = {n:>3}  ->  1/{n} = 0.({r['period']})  "
              f"[len(período)={r['period_len']}]")
    if len(candidates) > max_show:
        print(f"... (+{len(candidates) - max_show} outros)\n")
    else:
        print()


# ----------------------------------------------------------------------
# Top períodos por base
# ----------------------------------------------------------------------

def show_top_periods(data, top_k: int = 5):
    """
    Para cada base, mostra os 'top_k' maiores períodos, com seus
    denominadores associados.
    """
    print("===================================================================")
    print("Maiores períodos por base")
    print("===================================================================\n")

    for base in sorted(data.keys()):
        rows = [r for r in data[base] if r["type"] == "R"]
        if not rows:
            continue

        # Ordena por período decrescente, depois por denominador
        rows_sorted = sorted(
            rows,
            key=lambda r: (r["period_len"], -r["den"]),
            reverse=True
        )

        label = BASE_LABEL.get(base, f"BASE{base}")
        print(f"[ Base {base:>2} ({label}) ] – top {top_k} períodos:\n")

        shown = 0
        seen_periods = set()
        for r in rows_sorted:
            if shown >= top_k:
                break
            # Evita repetir o mesmo período em excesso
            key = (r["period_len"], r["period"])
            if key in seen_periods:
                continue
            seen_periods.add(key)

            print(f"  den = {r['den']:>3} "
                  f"period_len = {r['period_len']:>3} "
                  f" -> 0.{r['pre']}({r['period']})")
            shown += 1
        print()


# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------

def main():
    data = load_dizima_index(TSV_FILE)

    summarize_by_base(data)
    find_full_reptend_candidates(data, max_show=10)
    show_top_periods(data, top_k=5)

    print("===================================================================")
    print("FIM RAFAELIA_DÍZIMA_ANALYTICS – use estes padrões em Bitraf/T.I.")
    print("===================================================================")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Execução interrompida pelo usuário.")
