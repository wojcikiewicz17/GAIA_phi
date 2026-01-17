#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA_BITRAF_SEEDS_EXPORT
====================================================================
Goal:
    Export Bitraf DEN_n seeds, their composite metrics and profile
    memberships to a JSON file, reusing the existing advisor logic.

Output:
    - RAFAELIA_BITRAF_SEEDS.json  (UTF-8, human-readable)

This file can be consumed by:
    - kernels (via preprocessing),
    - other Python tools,
    - external systems that want a stable view of RAFAELIA seeds.
====================================================================
"""

from __future__ import annotations

import json
import math
from typing import Dict, List, Any

from RAFAELIA_TOROID_PERIOD_LINK import (
    BITRAF_DEN_SEEDS,
    INDEX_PATH,
    load_periods_for_seeds,
    compute_toroid_signatures_for_seeds,
)

from RAFAELIA_BITRAF_SEED_ADVISOR import (
    _compute_period_metrics,
    _composite_score,
    _classify_seed,
    recommend_seeds_for_profile,
    SEED_PROFILES,
)


def build_seed_records() -> List[Dict[str, Any]]:
    """
    Build the full list of seed records with metrics, scores and tags,
    mirroring the logic used in RAFAELIA_BITRAF_SEED_ADVISOR.main().
    """
    try:
        periods = load_periods_for_seeds(INDEX_PATH)
    except Exception as e:
        raise RuntimeError(f"Error while reading {INDEX_PATH}: {e}")

    signatures = compute_toroid_signatures_for_seeds(
        n_bits=256,
        samples_per_bit=1,
    )

    records: List[Dict[str, Any]] = []

    period_metrics_list: List[Dict[str, float]] = []
    signature_list: List[Dict[str, float]] = []

    tmp_per_metrics: Dict[int, Dict[str, float]] = {}
    tmp_sig: Dict[int, Dict[str, float]] = {}

    # First pass: gather per-seed metrics
    for den in BITRAF_DEN_SEEDS:
        per_bases: Dict[int, int] = periods.get(den, {})
        per_metrics = _compute_period_metrics(per_bases)
        sig = signatures.get(den, {
            "center_x": 0.0,
            "center_y": 0.0,
            "center_z": 0.0,
            "mean_radius": 0.0,
            "std_radius": 0.0,
            "phi_span_2pi": 0.0,
            "R": den / (2.0 * math.pi),
            "r": 0.0,
        })

        tmp_per_metrics[den] = per_metrics
        tmp_sig[den] = sig
        period_metrics_list.append(per_metrics)
        signature_list.append(sig)

    # Second pass: compute scores and tags
    for den in BITRAF_DEN_SEEDS:
        per_metrics = tmp_per_metrics[den]
        sig = tmp_sig[den]

        score = _composite_score(
            den=den,
            per_metrics=per_metrics,
            sig=sig,
            all_periods=period_metrics_list,
            all_signatures=signature_list,
        )
        tags = _classify_seed(den, per_metrics, sig)

        per_bases = periods.get(den, {})
        p2 = per_bases.get(2, -1)
        p8 = per_bases.get(8, -1)
        p10 = per_bases.get(10, -1)
        p16 = per_bases.get(16, -1)

        rec: Dict[str, Any] = {
            "den": den,
            "p2": p2,
            "p8": p8,
            "p10": p10,
            "p16": p16,
            "maxP": per_metrics["maxP"],
            "sumP": per_metrics["sumP"],
            "phi_span_2pi": sig.get("phi_span_2pi", 0.0),
            "mean_radius": sig.get("mean_radius", 0.0),
            "std_radius": sig.get("std_radius", 0.0),
            "score": score,
            "tags": tags,
        }
        records.append(rec)

    # Sort by composite score, best first
    records.sort(key=lambda r: r["score"], reverse=True)
    return records


def attach_profile_memberships(
    records: List[Dict[str, Any]],
) -> None:
    """
    For each record, compute which profiles it belongs to and add
    a 'profiles' list field.
    """
    # Build a mapping profile_name -> set of dens
    profile_members: Dict[str, set] = {}
    for profile_name in SEED_PROFILES.keys():
        recs = recommend_seeds_for_profile(records, profile_name, max_n=0)
        dens = {r["den"] for r in recs}
        profile_members[profile_name] = dens

    # Attach profile list to each record
    for r in records:
        den = r["den"]
        memberships: List[str] = []
        for pname, dens in profile_members.items():
            if den in dens:
                memberships.append(pname)
        r["profiles"] = memberships


def export_to_json(
    records: List[Dict[str, Any]],
    output_path: str = "RAFAELIA_BITRAF_SEEDS.json",
) -> None:
    """
    Export the given records plus profile definitions to a JSON file.
    """
    payload = {
        "seeds": records,
        "profiles": SEED_PROFILES,
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"[OK] Exported {len(records)} seeds to: {output_path}")


def main() -> None:
    print("===================================================================")
    print("RAFAELIA_BITRAF_SEEDS_EXPORT – JSON export of DEN_n seeds")
    print("===================================================================")

    records = build_seed_records()
    attach_profile_memberships(records)
    export_to_json(records)


if __name__ == "__main__":
    main()
