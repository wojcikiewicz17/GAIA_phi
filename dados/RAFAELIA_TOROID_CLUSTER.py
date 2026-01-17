#!/usr/bin/env python3
# RAFAELIA_TOROID_CLUSTER.py
# Compare Bitraf toroidal signatures across multiple denominators (DEN_n).
#
# Requirements:
#   - RAFAELIA_TOROID_BITFLOW.py in the same directory
#   - BITRAF_BITFLOWS populated with one or more bitflows
#
# The script:
#   1) Reuses the torus mapping and analysis functions.
#   2) Extracts a feature vector per denominator:
#        [center_x, center_y, center_z, mean_radius, std_radius, phi_span_2pi]
#   3) Computes pairwise Euclidean distances between seeds.
#   4) Prints a compact similarity matrix and nearest neighbors.

import math
from typing import Dict, List, Tuple

from RAFAELIA_TOROID_BITFLOW import (
    BITRAF_BITFLOWS,
    build_torus_points_from_bits,
    analyze_torus_points,
)


def compute_features_for_den(
    den: int,
    bits: str,
    samples_per_bit: int = 1,
) -> Tuple[Dict[str, float], List[float]]:
    """
    Compute toroidal signature and feature vector for a given denominator.

    Returns:
        sig: dictionary with geometric/phase metrics (center, radii, span).
        feat: feature vector [cx, cy, cz, mean_radius, std_radius, phi_span_2pi].
    """
    points, phis, R, r = build_torus_points_from_bits(
        den=den,
        bits=bits,
        samples_per_bit=samples_per_bit,
    )
    sig = analyze_torus_points(points, phis, R, r)

    feat = [
        sig["center_x"],
        sig["center_y"],
        sig["center_z"],
        sig["mean_radius"],
        sig["std_radius"],
        sig["phi_span_2pi"],
    ]
    return sig, feat


def euclidean_distance(v1: List[float], v2: List[float]) -> float:
    """Compute Euclidean distance between two same-length vectors."""
    if len(v1) != len(v2):
        raise ValueError("Feature vectors must have the same length.")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def cluster_bitraf_toroids(samples_per_bit: int = 1) -> None:
    """
    Main clustering / comparison routine:
      - loops over BITRAF_BITFLOWS
      - computes feature vectors
      - prints per-seed signatures
      - prints pairwise distance table and nearest neighbors
    """
    print("===================================================================")
    print("RAFAELIA_TOROID_CLUSTER – ToroidΔπφ families for Bitraf seeds")
    print("===================================================================\n")

    if not BITRAF_BITFLOWS:
        print("[!] No Bitraf bitflows registered. Update BITRAF_BITFLOWS first.")
        return

    # Step 1: compute signatures and feature vectors
    features: Dict[int, List[float]] = {}
    signatures: Dict[int, Dict[str, float]] = {}

    for den, bits in BITRAF_BITFLOWS.items():
        print(f"[i] Processing DEN_{den} (bitlength={len(bits)})...")
        sig, feat = compute_features_for_den(
            den=den,
            bits=bits,
            samples_per_bit=samples_per_bit,
        )
        features[den] = feat
        signatures[den] = sig

    print("\n--- Toroidal signatures per seed ---")
    for den, sig in signatures.items():
        print(f"\nDEN_{den}:")
        print(f"  center ≈ ({sig['center_x']:.6f}, "
              f"{sig['center_y']:.6f}, {sig['center_z']:.6f})")
        print(f"  mean_radius       = {sig['mean_radius']:.6f}")
        print(f"  std_radius        = {sig['std_radius']:.6e}")
        print(f"  phi_span_2pi      = {sig['phi_span_2pi']:.6f}")

    # If only one seed is present, we cannot compute pairwise distances.
    dens = sorted(features.keys())
    if len(dens) < 2:
        print("\n[i] Only one DEN_n registered. "
              "Add more bitflows to compute pairwise distances.")
        return

    # Step 2: compute pairwise distance matrix
    print("\n--- Pairwise distances (Euclidean on feature vectors) ---")
    dist_matrix: Dict[Tuple[int, int], float] = {}

    for i, di in enumerate(dens):
        for dj in dens[i + 1 :]:
            d = euclidean_distance(features[di], features[dj])
            dist_matrix[(di, dj)] = d

    # Print matrix header
    header = "       " + " ".join(f"{d:>8}" for d in dens)
    print(header)
    for di in dens:
        row = [f"DEN_{di:>3}"]
        for dj in dens:
            if di == dj:
                row.append(f"{0.0:8.4f}")
            else:
                key = (di, dj) if (di, dj) in dist_matrix else (dj, di)
                val = dist_matrix.get(key, float("nan"))
                row.append(f"{val:8.4f}")
        print(" ".join(row))

    # Step 3: nearest neighbors per seed
    print("\n--- Nearest neighbors ---")
    for di in dens:
        dists = []
        for dj in dens:
            if dj == di:
                continue
            key = (di, dj) if (di, dj) in dist_matrix else (dj, di)
            val = dist_matrix.get(key, float("nan"))
            dists.append((dj, val))
        dists = [p for p in dists if not math.isnan(p[1])]
        if not dists:
            continue
        dists.sort(key=lambda x: x[1])
        nn = dists[0]
        print(f"  DEN_{di} closest to DEN_{nn[0]}  (distance ≈ {nn[1]:.6f})")


if __name__ == "__main__":
    # Increase samples_per_bit if you want smoother trajectories.
    cluster_bitraf_toroids(samples_per_bit=1)
