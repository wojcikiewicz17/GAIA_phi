#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA_DIZIMA_CONSTANT_BRIDGE
--------------------------------
Ponte entre:
  - RAFAELIA_MATH_CONSTANTS.tsv (constantes numéricas do corpus)
  - RAFAELIA_DIZIMA_INDEX.tsv   (dízimas 1/n em bases 2,8,10,16)

Para cada constante:
  - calcula parte fracionária;
  - procura os melhores 1/n (n_min..n_max) que aproximam essa fração;
  - coleta, para esses n, os comprimentos de período em cada base;
  - marca candidatos a 'full-reptend' em base 10 (período = n-1);
  - grava resumo em TSV + relatório em Markdown.

Compatível com RAFAELIA_DIZIMA_INDEX.tsv com cabeçalho:
  den, base, label, type, pre_len, period_len, pre, period
"""

import csv
import math
from collections import defaultdict
from typing import Dict, Any, List, Tuple

CONST_FILE = "RAFAELIA_MATH_CONSTANTS.tsv"
DIZIMA_FILE = "RAFAELIA_DIZIMA_INDEX.tsv"
OUT_TSV = "RAFAELIA_DIZIMA_CONSTANT_BRIDGE.tsv"
OUT_REPORT = "RAFAELIA_DIZIMA_CONSTANT_BRIDGE_REPORT.md"


# --------------------------------------------------------------------
# Utilitários
# --------------------------------------------------------------------

def frac_part(x: float) -> float:
    """Retorna a parte fracionária de x em [0,1)."""
    f = abs(x) - math.floor(abs(x))
    if abs(f) < 1e-15:
        return 0.0
    return f


def safe_float(s: str, default: float = 0.0) -> float:
    try:
        return float(str(s).strip())
    except Exception:
        return default


def infer_dizima_columns(header: List[str]) -> Dict[str, str]:
    """
    Mapeia os nomes das colunas de RAFAELIA_DIZIMA_INDEX.tsv.

    Cabeçalho esperado (o seu):

        ['den', 'base', 'label', 'type', 'pre_len',
         'period_len', 'pre', 'period']

    Mas deixo resiliente a pequenas variações.
    """
    h_lower = {name.lower(): name for name in header}

    def get_exact(name: str, fallback_contains: str = None) -> str:
        if name.lower() in h_lower:
            return h_lower[name.lower()]
        if fallback_contains:
            for k, v in h_lower.items():
                if fallback_contains in k:
                    return v
        raise KeyError(f"Coluna '{name}' não encontrada em {header}")

    # Mapeamento principal
    den_col = get_exact("den", "den")
    base_col = get_exact("base", "base")
    period_len_col = get_exact("period_len", "period_len")

    # 'type' indica T/R (terminante/repetente)
    term_col = h_lower.get("type", None)
    if term_col is None and "type" in header:
        term_col = "type"
    # Se não existir, ficará None e tratamos como "não informado"
    if term_col is None:
        # tenta qualquer coluna contendo 'type'
        for k, v in h_lower.items():
            if "type" in k:
                term_col = v
                break

    return {
        "den": den_col,
        "base": base_col,
        "period_len": period_len_col,
        "terminante": term_col,   # mapeia para 'type' (T/R) quando existir
        "repr": h_lower.get("period", "period"),  # parte periódica
    }


# --------------------------------------------------------------------
# Leitura do índice de dízimas
# --------------------------------------------------------------------

def load_dizima_index(path: str) -> Dict[int, Dict[int, Dict[str, Any]]]:
    """
    Lê RAFAELIA_DIZIMA_INDEX.tsv e retorna:

        dizimas[den][base] = {
            'period_len': int,
            'terminante': bool,   # True se type == 'T'
            'repr': str,
            ...
        }
    """
    dizimas: Dict[int, Dict[int, Dict[str, Any]]] = defaultdict(dict)

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        header = reader.fieldnames or []
        cols = infer_dizima_columns(header)

        for row in reader:
            try:
                den = int(row[cols["den"]])
                base = int(row[cols["base"]])
            except Exception:
                continue

            try:
                period_len = int(row[cols["period_len"]])
            except Exception:
                period_len = 0

            terminante = False
            term_col = cols.get("terminante")
            if term_col and term_col in row:
                tval = str(row[term_col]).strip().upper()
                # convenciona: 'T' = terminante, 'R' = repetente
                terminante = (tval == "T")

            repr_str = ""
            if cols.get("repr") and cols["repr"] in row:
                repr_str = row[cols["repr"]].strip()

            dizimas[den][base] = {
                "period_len": period_len,
                "terminante": terminante,
                "repr": repr_str,
                **{k: v for k, v in row.items()},
            }

    return dizimas


# --------------------------------------------------------------------
# Leitura das constantes RAFAELIA
# --------------------------------------------------------------------

def load_constants(path: str) -> List[Dict[str, Any]]:
    """
    Lê RAFAELIA_MATH_CONSTANTS.tsv gerado por rafaelia_math_deep_scan.py.

    Cabeçalho típico:
        valor  freq  aprox_pi  aprox_e  aprox_phi  aprox_sqrt2  ...
    """
    consts: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            row["valor_float"] = safe_float(row.get("valor", "0"))
            consts.append(row)
    return consts


# --------------------------------------------------------------------
# Matching: constante ↔ 1/n
# --------------------------------------------------------------------

def best_matches_for_fraction(
    frac: float,
    n_min: int,
    n_max: int,
    max_results: int = 3
) -> List[Tuple[int, float]]:
    """
    Dado frac in [0,1), procura 1/n (n_min..n_max) mais próximos.
    Retorna [(n, diff), ...] ordenado por diff crescente.
    """
    candidates: List[Tuple[int, float]] = []
    for n in range(n_min, n_max + 1):
        target = 1.0 / n
        diff = abs(frac - target)
        candidates.append((n, diff))

    candidates.sort(key=lambda x: x[1])
    return candidates[:max_results]


# --------------------------------------------------------------------
# Pipeline principal
# --------------------------------------------------------------------

def main():
    print("=" * 67)
    print("RAFAELIA_DIZIMA_CONSTANT_BRIDGE – Ponte constantes ↔ dízimas ↔ bases")
    print("=" * 67)

    # 1) Índice de dízimas
    print(f"[+] Lendo índice de dízimas: {DIZIMA_FILE}")
    dizimas = load_dizima_index(DIZIMA_FILE)

    # 2) Constantes
    print(f"[+] Lendo constantes: {CONST_FILE}")
    consts = load_constants(CONST_FILE)
    print(f"[i] Constantes carregadas: {len(consts)}")

    fieldnames = [
        "valor",
        "freq",
        "frac_part",
        "best_n",
        "best_diff",
        "period_len_bin",
        "period_len_oct",
        "period_len_dec",
        "period_len_hex",
        "terminante_dec",
        "full_reptend_dec",
    ]

    bridge_rows: List[Dict[str, Any]] = []

    with open(OUT_TSV, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

        for row in consts:
            v = row.get("valor_float", 0.0)
            frac = frac_part(v)

            matches = best_matches_for_fraction(frac, 2, 128, max_results=1)
            if not matches:
                continue

            best_n, best_diff = matches[0]

            base_info = dizimas.get(best_n, {})
            b2 = base_info.get(2, {})
            b8 = base_info.get(8, {})
            b10 = base_info.get(10, {})
            b16 = base_info.get(16, {})

            period_bin = int(b2.get("period_len", 0) or 0)
            period_oct = int(b8.get("period_len", 0) or 0)
            period_dec = int(b10.get("period_len", 0) or 0)
            period_hex = int(b16.get("period_len", 0) or 0)
            terminante_dec = bool(b10.get("terminante", False))

            full_reptend_dec = (
                (not terminante_dec) and period_dec == (best_n - 1)
            )

            out_row = {
                "valor": row.get("valor", ""),
                "freq": row.get("freq", ""),
                "frac_part": f"{frac:.12f}",
                "best_n": best_n,
                "best_diff": f"{best_diff:.12e}",
                "period_len_bin": period_bin,
                "period_len_oct": period_oct,
                "period_len_dec": period_dec,
                "period_len_hex": period_hex,
                "terminante_dec": int(terminante_dec),
                "full_reptend_dec": int(full_reptend_dec),
            }
            writer.writerow(out_row)
            bridge_rows.append(out_row)

    print(f"[OK] Ponte salva em: {OUT_TSV}")

    # 4) Relatório
    full_reptend_hits = [r for r in bridge_rows if r["full_reptend_dec"]]
    full_reptend_hits_sorted = sorted(
        full_reptend_hits, key=lambda r: float(r["best_diff"])
    )

    with open(OUT_REPORT, "w", encoding="utf-8") as f_rep:
        f_rep.write("# RAFAELIA_DIZIMA_CONSTANT_BRIDGE – Relatório Técnico\n\n")
        f_rep.write("Resumo do casamento entre constantes RAFAELIA\n")
        f_rep.write("e dízimas 1/n (2 ≤ n ≤ 128) em bases 2, 8, 10, 16.\n\n")

        f_rep.write("## 1. Estatísticas gerais\n\n")
        f_rep.write(f"- Constantes analisadas: {len(consts)}\n")
        f_rep.write(f"- Linhas de ponte geradas: {len(bridge_rows)}\n")
        f_rep.write(f"- Constantes com n full-reptend em base 10: {len(full_reptend_hits)}\n\n")

        f_rep.write("## 2. Top matches com full-reptend em base 10\n\n")
        f_rep.write("| valor | frac_part | best_n | best_diff | period_dec |\n")
        f_rep.write("|-------|-----------|--------|-----------|------------|\n")
        for r in full_reptend_hits_sorted[:20]:
            f_rep.write(
                f"| {r['valor']} "
                f"| {r['frac_part']} "
                f"| {r['best_n']} "
                f"| {r['best_diff']} "
                f"| {r['period_len_dec']} |\n"
            )

        f_rep.write("\n## 3. Leitura conceitual para Bitraf/T.I.\n\n")
        f_rep.write(
            "- Cada constante do teu corpus ganha um 'endereço' discreto 1/n\n"
            "  e um perfil de dízima em múltiplas bases (2, 8, 10, 16).\n"
        )
        f_rep.write(
            "- Denominadores com período máximo (full-reptend em base 10)\n"
            "  funcionam como órbitas completas, úteis para PRNG, hashing\n"
            "  e codificações Bitraf-aware.\n"
        )
        f_rep.write(
            "- Assim, a Matemática Viva (φ, √2, √3, φ_R, razões de diagonais,\n"
            "  volumes n-D, etc.) fica diretamente ligada a estruturas de\n"
            "  repetição digital que você pode usar em kernels, compressão\n"
            "  e protocolos RAFAELIA.\n"
        )

    print(f"[OK] Relatório salvo em: {OUT_REPORT}")
    print("=== FIM RAFAELIA_DIZIMA_CONSTANT_BRIDGE ===")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Encerrado por teclado.")
