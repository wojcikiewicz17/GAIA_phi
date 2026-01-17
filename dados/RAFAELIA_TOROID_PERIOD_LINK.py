#!/usr/bin/env python3
# RAFAELIA_TOROID_PERIOD_LINK.py
# Link discrete period structure from RAFAELIA_DIZIMA_INDEX.tsv
# to toroidal geometric families from RAFAELIA_TOROID_BITFLOW.py.
#
# Steps:
#   - read RAFAELIA_DIZIMA_INDEX.tsv
#   - filter rows for the 16 Bitraf denominators
#   - collect period lengths per base (2, 8, 10, 16)
#   - compute summary per denominator (max period, by base)
#   - import toroidal signatures (mean_radius, std_radius, phi_span_2pi)
#   - print a consolidated table per denominator

import csv
import math
from typing import Dict, List, Tuple

from RAFAELIA_TOROID_BITFLOW import (
    BITRAF_DEN_SEEDS,
    generate_all_bitraf_flows,
    build_torus_points_from_bits,
    analyze_torus_points,
)

INDEX_PATH = "RAFAELIA_DIZIMA_INDEX.tsv"


def detect_columns(header: List[str]) -> Tuple[int, int, int]:
    """
    Detects the indices of columns 'n', 'base', 'period_len' (or variants).
    Tries several common patterns to be robust.
    """
    lower = [h.strip().lower() for h in header]

    def find_one(candidates: List[str]) -> int:
        for c in candidates:
            if c in lower:
                return lower.index(c)
        return -1

    idx_n = find_one(["n", "den", "denominator"])
    idx_base = find_one(["base", "radix"])
    idx_period = find_one(["period_len", "period", "period_length"])

    if idx_n < 0 or idx_base < 0 or idx_period < 0:
        raise ValueError(
            f"Could not detect required columns in RAFAELIA_DIZIMA_INDEX.tsv.\n"
            f"Header seen: {header}\n"
            f"Need something like: n / den / denominator, base / radix, period_len / period."
        )

    return idx_n, idx_base, idx_period


def load_periods_for_seeds(path: str) -> Dict[int, Dict[int, int]]:
    """
    Load period lengths from RAFAELIA_DIZIMA_INDEX.tsv for the denominators
    in BITRAF_DEN_SEEDS.

    Returns:
        periods[den][base] = period_len
    """
    periods: Dict[int, Dict[int, int]] = {den: {} for den in BITRAF_DEN_SEEDS}

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("RAFAELIA_DIZIMA_INDEX.tsv is empty.")

        idx_n, idx_base, idx_period = detect_columns(header)

        for row in reader:
            if not row or len(row) <= max(idx_n, idx_base, idx_period):
                continue
            try:
                den = int(row[idx_n])
                base = int(row[idx_base])
                period_len = int(row[idx_period])
            except ValueError:
                # Non-numeric row, skip
                continue

            if den in periods:
                periods[den][base] = period_len

    return periods


def compute_toroid_signatures_for_seeds(
    n_bits: int = 256,
    samples_per_bit: int = 1,
) -> Dict[int, Dict[str, float]]:
    """
    For each denominator in BITRAF_DEN_SEEDS:
      - generate flow for 1/den (n_bits bits)
      - map to torus
      - compute signature (center, mean_radius, std_radius, phi_span_2pi)
    """
    signatures: Dict[int, Dict[str, float]] = {}

    flows = generate_all_bitraf_flows(BITRAF_DEN_SEEDS, n_bits=n_bits)

    for den in BITRAF_DEN_SEEDS:
        bits = flows[den]
        points, phis, R, r = build_torus_points_from_bits(
            den=den,
            bits=bits,
            samples_per_bit=samples_per_bit,
        )
        sig = analyze_torus_points(points, phis, R, r)
        signatures[den] = sig

    return signatures


def main() -> None:
    print("===================================================================")
    print("RAFAELIA_TOROID_PERIOD_LINK – Períodos de dízimas × ToroidΔπφ")
    print("===================================================================\n")

    # 1) Carregar períodos da RAFAELIA_DIZIMA_INDEX.tsv
    try:
        periods = load_periods_for_seeds(INDEX_PATH)
    except Exception as e:
        print(f"[!] Erro ao ler {INDEX_PATH}: {e}")
        return

    # 2) Calcular assinaturas toroidais (reaproveita o núcleo existente)
    signatures = compute_toroid_signatures_for_seeds(
        n_bits=256,
        samples_per_bit=1,
    )

    # 3) Imprimir tabela consolidada
    print("--- Resumo por denominador ---")
    print("den | base2 | base8 | base10 | base16 | maxP | "
          "phi_span_2pi | mean_radius | std_radius")

    for den in sorted(BITRAF_DEN_SEEDS):
        per = periods.get(den, {})
        p2 = per.get(2, -1)
        p8 = per.get(8, -1)
        p10 = per.get(10, -1)
        p16 = per.get(16, -1)
        maxP = max([p for p in [p2, p8, p10, p16] if p >= 0], default=-1)

        sig = signatures.get(den, {})
        phi_span = sig.get("phi_span_2pi", float("nan"))
        mean_r = sig.get("mean_radius", float("nan"))
        std_r = sig.get("std_radius", float("nan"))

        print(
            f"{den:3d} | "
            f"{p2:5d} | {p8:5d} | {p10:6d} | {p16:6d} | "
            f"{maxP:4d} | "
            f"{phi_span:11.6f} | {mean_r:11.6f} | {std_r:10.6e}"
        )

    print("\n[info] Valores -1 significam 'sem dado encontrado' naquela base.")
    print("[info] Use esta tabela para ver se famílias toroidais coincidem "
          "com padrões de período (maxP, ou bases específicas).")


if __name__ == "__main__":
    main()
