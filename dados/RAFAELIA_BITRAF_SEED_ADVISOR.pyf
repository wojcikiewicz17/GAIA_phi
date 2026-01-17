#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA_BITRAF_SEED_ADVISOR
====================================================================
Purpose:
    Combine discrete Bitraf period structure (from RAFAELIA_DIZIMA_INDEX.tsv)
    with toroidal geometric signatures (RAFAELIA_TOROID_BITFLOW / PERIOD_LINK)
    to produce a ranked, human-readable recommendation list of DEN_n seeds.

Design goals:
    - Keep it short and practical to run from Termux (single CLI script).
    - Reuse existing work: no recomputation of heavy math if avoidable.
    - Provide a consistent composite score plus "tags" (words) that describe
      each seed's qualitative behavior (ergodic / lacunar / stable / noisy).
    - Help a human choose seeds according to the analysis, not arbitrary picks.

Usage:
    python RAFAELIA_BITRAF_SEED_ADVISOR.py

Outputs:
    - Printed table sorted by composite score (best first).
    - For each DEN_n: periods, torus metrics, normalized score and tags.
====================================================================
"""

from __future__ import annotations

import math
from typing import Dict, List, Any

# We reuse the existing linkage utilities so that we stay in sync
# with the Bitraf / Toroid pipelines.
from RAFAELIA_TOROID_PERIOD_LINK import (
    BITRAF_DEN_SEEDS,
    INDEX_PATH,
    load_periods_for_seeds,
    compute_toroid_signatures_for_seeds,
)

# -------------------------------------------------------------------
# High-level profiles for intent-based selection
# -------------------------------------------------------------------

# Each profile defines:
#   - min_score: minimal composite score.
#   - required_tags: tags that must be present in a seed.
#   - forbidden_tags: tags that must NOT be present in a seed.
SEED_PROFILES = {
    "CORE_STRONG": {
        "min_score": 0.70,
        "required_tags": ["ergodic_full"],
        "forbidden_tags": ["angular_gap"],
        # Typical use: cryptographic / PRNG core streams.
    },
    "HIGH_ALT_STRONG": {
        "min_score": 0.60,
        "required_tags": ["high_radius", "ergodic_full"],
        "forbidden_tags": ["angular_gap"],
        # Typical use: high-radius beacons / remote channels.
    },
    "MASK_GAP": {
        "min_score": 0.20,
        "required_tags": ["angular_gap"],
        "forbidden_tags": [],
        # Typical use: masking, slotting, "windows" on the torus.
    },
}


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def _safe_get_period(
    periods: Dict[int, Dict[int, int]],
    den: int,
    base: int,
    default: int = -1,
) -> int:
    """Return period length for (den, base) or a default if missing."""
    return periods.get(den, {}).get(base, default)


def _compute_period_metrics(
    per_bases: Dict[int, int],
) -> Dict[str, float]:
    """
    Compute simple aggregate metrics from base-wise periods.

    Returns:
        - maxP: maximum period across bases (>= 0).
        - sumP: sum of periods across bases (>= 0).
        - avgP: average period across bases that are present (>= 0).
    """
    vals = [p for p in per_bases.values() if p >= 0]
    if not vals:
        return {"maxP": 0.0, "sumP": 0.0, "avgP": 0.0}
    maxP = float(max(vals))
    sumP = float(sum(vals))
    avgP = sumP / float(len(vals))
    return {"maxP": maxP, "sumP": sumP, "avgP": avgP}


def _normalize(value: float, min_v: float, max_v: float) -> float:
    """
    Normalize a scalar value into [0, 1] given (min_v, max_v).

    For robustness, if min_v == max_v, returns 0.5 (constant feature).
    Values outside [min_v, max_v] are clamped.
    """
    if max_v <= min_v:
        return 0.5
    v = max(min(value, max_v), min_v)
    return (v - min_v) / (max_v - min_v)


def _composite_score(
    den: int,
    per_metrics: Dict[str, float],
    sig: Dict[str, float],
    all_periods: List[Dict[str, float]],
    all_signatures: List[Dict[str, float]],
) -> float:
    """
    Compute a composite score for a given seed, combining:

        - Period metrics (maxP, sumP).
        - Toroidal ergodicity (phi_span_2pi close to 1).
        - Radial stability (smaller std_radius is better).

    The function uses min/max across all seeds to normalize features so that
    the score is scale-invariant and comparable between different runs.

    This is intentionally simple and transparent rather than overfitted.
    """
    # Collect global bounds
    maxPs = [pm["maxP"] for pm in all_periods]
    sumPs = [pm["sumP"] for pm in all_periods]
    phi_spans = [s["phi_span_2pi"] for s in all_signatures]
    std_rads = [s["std_radius"] for s in all_signatures]

    g_min_maxP, g_max_maxP = min(maxPs), max(maxPs)
    g_min_sumP, g_max_sumP = min(sumPs), max(sumPs)
    g_min_phi, g_max_phi = min(phi_spans), max(phi_spans)
    g_min_std, g_max_std = min(std_rads), max(std_rads)

    # Normalize each component
    maxP_n = _normalize(per_metrics["maxP"], g_min_maxP, g_max_maxP)
    sumP_n = _normalize(per_metrics["sumP"], g_min_sumP, g_max_sumP)
    phi_n = _normalize(sig["phi_span_2pi"], g_min_phi, g_max_phi)

    # For std_radius we invert the normalization:
    # smaller std_radius (more stable radius) should yield a higher score.
    std_n_raw = _normalize(sig["std_radius"], g_min_std, g_max_std)
    std_n = 1.0 - std_n_raw

    # Weighted combination:
    #   - favor maxP and phi-span strongly,
    #   - sumP and stability contribute as refinements.
    w_maxP = 0.40
    w_phi = 0.30
    w_sumP = 0.15
    w_std = 0.15

    score = (
        w_maxP * maxP_n
        + w_phi * phi_n
        + w_sumP * sumP_n
        + w_std * std_n
    )
    return score


def _classify_seed(
    den: int,
    per_metrics: Dict[str, float],
    sig: Dict[str, float],
) -> List[str]:
    """
    Produce a small set of human-friendly tags ("words") for this seed.

    The tags are intentionally simple and interpretable; they describe:
        - scale band (low/mid/high radius),
        - ergodicity (angular coverage),
        - radial stability.
    """
    tags: List[str] = []

    # Scale band by denominator (proxy for R = den / (2π))
    if den <= 80:
        tags.append("low_radius")
    elif den <= 110:
        tags.append("mid_radius")
    else:
        tags.append("high_radius")

    # Angular coverage via phi_span_2pi
    phi = sig.get("phi_span_2pi", 0.0)
    if phi >= 0.985:
        tags.append("ergodic_full")
    elif phi >= 0.95:
        tags.append("ergodic_partial")
    else:
        tags.append("angular_gap")

    # Radial stability via std_radius
    std_r = sig.get("std_radius", 0.0)
    if std_r <= 1e-2:
        tags.append("radial_ultrastable")
    elif std_r <= 5e-2:
        tags.append("radial_stable")
    else:
        tags.append("radial_diffuse")

    # Period dominance
    maxP = per_metrics.get("maxP", 0.0)
    if maxP >= 60:
        tags.append("long_period")
    elif maxP >= 40:
        tags.append("medium_period")
    else:
        tags.append("short_period")

    return tags


def recommend_seeds_for_profile(
    records: List[Dict[str, Any]],
    profile_name: str,
    max_n: int = 4,
) -> List[Dict[str, Any]]:
    """
    Filter and rank seeds according to a named profile configuration.

    Args:
        records: list of seed records as built in main().
        profile_name: key in SEED_PROFILES dict.
        max_n: maximum number of seeds to return.

    Returns:
        A list (possibly empty) of records that satisfy the profile,
        sorted again by score (descending).
    """
    profile = SEED_PROFILES.get(profile_name)
    if profile is None:
        return []

    min_score = profile.get("min_score", 0.0)
    required_tags = set(profile.get("required_tags", []))
    forbidden_tags = set(profile.get("forbidden_tags", []))

    selected: List[Dict[str, Any]] = []
    for r in records:
        if r["score"] < min_score:
            continue
        tags = set(r.get("tags", []))
        if not required_tags.issubset(tags):
            continue
        if forbidden_tags.intersection(tags):
            continue
        selected.append(r)

    selected.sort(key=lambda rr: rr["score"], reverse=True)
    if max_n > 0:
        selected = selected[:max_n]
    return selected


# -------------------------------------------------------------------
# CLI / main
# -------------------------------------------------------------------

def main() -> None:
    print("===================================================================")
    print("RAFAELIA_BITRAF_SEED_ADVISOR – Composite ranking of DEN_n seeds")
    print("===================================================================\n")

    # 1) Load period data for the 16 Bitraf denominators
    try:
        periods = load_periods_for_seeds(INDEX_PATH)
    except Exception as e:
        print(f"[!] Error while reading {INDEX_PATH}: {e}")
        return

    # 2) Compute toroidal signatures reusing the existing Bitflow mapping
    signatures = compute_toroid_signatures_for_seeds(
        n_bits=256,
        samples_per_bit=1,
    )

    # 3) Build per-seed records including metrics and scores
    records: List[Dict[str, Any]] = []

    period_metrics_list: List[Dict[str, float]] = []
    signature_list: List[Dict[str, float]] = []

    tmp_per_metrics: Dict[int, Dict[str, float]] = {}
    tmp_sig: Dict[int, Dict[str, float]] = {}

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

    # 4) Compute composite scores with global context
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

    # 5) Sort by composite score (descending)
    records.sort(key=lambda r: r["score"], reverse=True)

    # 5a) Print ranked table
    print("--- Ranked Bitraf seeds (best first) ---\n")
    header = (
        "den  | score   | maxP | p2  p8  p10  p16 | "
        "phi_span_2pi | mean_r    | std_r      | tags"
    )
    print(header)
    print("-" * len(header))

    for r in records:
        tags_str = ",".join(r["tags"])
        print(
            f"{r['den']:4d} | "
            f"{r['score']:7.4f} | "
            f"{int(r['maxP']):4d} | "
            f"{r['p2']:3d} {r['p8']:3d} {r['p10']:4d} {r['p16']:4d} | "
            f"{r['phi_span_2pi']:12.6f} | "
            f"{r['mean_radius']:9.4f} | "
            f"{r['std_radius']:11.6e} | "
            f"{tags_str}"
        )

    # 6) Profile-based recommendations
    print("\n--- Profile-based recommendations ---\n")

    for profile_name in ("CORE_STRONG", "HIGH_ALT_STRONG", "MASK_GAP"):
        recs = recommend_seeds_for_profile(records, profile_name, max_n=4)
        print(f"[profile] {profile_name}:")
        if not recs:
            print("  (no seeds match criteria)\n")
            continue
        for r in recs:
            tags_str = ",".join(r["tags"])
            print(
                f"  den={r['den']:3d} | score={r['score']:.4f} | "
                f"maxP={int(r['maxP']):3d} | tags={tags_str}"
            )
        print()

    print(
        "[info] 'tags' provide quick qualitative hints: radius band, "
        "ergodicity, radial stability, and period length."
    )
    print(
        "[info] Profiles (CORE_STRONG / HIGH_ALT_STRONG / MASK_GAP) give "
        "ready-made sets of seeds for different uses."
    )


if __name__ == "__main__":
    main()
