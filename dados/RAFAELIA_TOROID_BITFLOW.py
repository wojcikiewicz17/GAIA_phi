#!/usr/bin/env python3
# RAFAELIA_TOROID_BITFLOW.py
# Map Bitraf bitflows (0/1) into toroidal trajectories and extract
# geometric/phase signatures per seed.
#
# Version v2:
#   - Automatically generates bitflows as binary expansions of 1/den
#     for the 16 fallback denominators discovered by RAFAELIA_BITRAF_PRIME_CORE.
#
# Design goals:
#   - Deterministic, reproducible flows (1/den in base 2, 256 bits).
#   - Clear separation between:
#       (1) flow generation
#       (2) torus mapping
#       (3) signature analysis
#
# This module is intentionally side-effect free except for analyze_all_bitflows().

import math
from typing import Dict, List, Tuple

# --- Core Rafaelian constants ---

phi_R = math.sqrt(3.0) / 2.0  # Rafaelian symbolic constant

# --- Denominator seeds (from RAFAELIA_BITRAF_PRIME_CORE fallback) ---

BITRAF_DEN_SEEDS = [
    67, 61, 122, 59, 118, 121, 81, 107,
    53, 106, 103, 119, 97, 47, 94, 115,
]


# --- Bitflow generation helpers ---

def binary_bitflow_for_den(den: int, n_bits: int = 256) -> str:
    """
    Generate a deterministic binary bitflow for a given denominator 'den',
    using the binary expansion of 1/den up to n_bits bits.

    Algorithm:
      r = 1 % den
      for i in range(n_bits):
          r *= 2
          if r >= den:
              bit = '1'
              r -= den
          else:
              bit = '0'

    This avoids floating point and is reproducible across runs.

    Args:
        den: positive integer denominator (den != 0).
        n_bits: number of bits to generate.

    Returns:
        A string of '0'/'1' characters of length n_bits.

    Error handling:
        Raises ValueError if den <= 0 or n_bits <= 0.
    """
    if den <= 0:
        raise ValueError("Denominator must be positive.")
    if n_bits <= 0:
        raise ValueError("Number of bits must be positive.")

    r = 1 % den
    bits: List[str] = []

    for _ in range(n_bits):
        r *= 2
        if r >= den:
            bits.append("1")
            r -= den
        else:
            bits.append("0")

    return "".join(bits)


def generate_all_bitraf_flows(
    dens: List[int],
    n_bits: int = 256,
) -> Dict[int, str]:
    """
    Generate bitflows for a list of denominators.

    Returns:
        A dictionary {den: bitflow_str}.
    """
    flows: Dict[int, str] = {}
    for den in dens:
        flows[den] = binary_bitflow_for_den(den, n_bits=n_bits)
    return flows


# Automatically generated Bitraf flows for all seeds.
BITRAF_BITFLOWS: Dict[int, str] = generate_all_bitraf_flows(
    BITRAF_DEN_SEEDS,
    n_bits=256,
)


# --- Toroid mapping helpers ---

def build_torus_points_from_bits(
    den: int,
    bits: str,
    samples_per_bit: int = 1,
) -> Tuple[List[Tuple[float, float, float]], List[float], float, float]:
    """
    Map a bitstring onto a torus:
      - major radius R is derived from the denominator (den / 2π)
      - minor radius r is derived from phi_R and clamped to keep r < 0.5*R
      - each bit governs how the trajectory winds in φ while θ sweeps [0, 2π]

    Args:
        den: denominator associated with the seed (e.g. 67 for DEN_67).
        bits: string of '0' and '1' characters (Bitraf flow).
        samples_per_bit: number of sub-samples per bit (for smoother paths).

    Returns:
        points: list of (x, y, z) coordinates on the torus.
        phis: list of φ angles used (for winding analysis).
        R: major radius used.
        r: minor radius used.

    Error handling:
        Raises ValueError if bits is empty or contains no valid 0/1 chars.
    """
    if not bits:
        raise ValueError("Empty bitstring not allowed for torus mapping.")

    # Major radius from denominator
    R = den / (2.0 * math.pi)

    # Minor radius from Rafaelian constant, clamped for stability
    r_raw = phi_R
    r = min(r_raw, 0.5 * R)

    valid_bits = [b for b in bits if b in ("0", "1")]
    if not valid_bits:
        raise ValueError("Bitstring must contain at least one '0' or '1'.")

    total_bits = len(valid_bits)
    total_samples = total_bits * max(1, samples_per_bit)

    points: List[Tuple[float, float, float]] = []
    phis: List[float] = []

    ones_prefix = 0

    for i, b in enumerate(valid_bits):
        bit_val = int(b)
        ones_prefix += bit_val

        # Fraction of ones seen so far (cumulative density of '1')
        frac_ones = ones_prefix / total_bits

        for s in range(samples_per_bit):
            # Global sample index across all bits
            idx = i * samples_per_bit + s

            # Normalized parameter for θ sweep in [0, 2π]
            t = idx / max(1, (total_samples - 1))
            theta = 2.0 * math.pi * t

            # φ is driven by cumulative ones + local bit value
            phi = 2.0 * math.pi * ((frac_ones + 0.5 * bit_val) % 1.0)

            # Standard torus parameterization
            x = (R + r * math.cos(theta)) * math.cos(phi)
            y = (R + r * math.cos(theta)) * math.sin(phi)
            z = r * math.sin(theta)

            points.append((x, y, z))
            phis.append(phi)

    return points, phis, R, r


def analyze_torus_points(
    points: List[Tuple[float, float, float]],
    phis: List[float],
    R: float,
    r: float,
) -> Dict[str, float]:
    """
    Compute geometric and phase signatures of a torus trajectory:
      - center of mass (x,y,z)
      - mean and std of radial distance from origin
      - approximate φ-span in units of 2π (winding measure)

    Args:
        points: list of (x, y, z) coordinates.
        phis: angles φ for each point.
        R, r: radii used (for context).

    Returns:
        dict with center, mean_radius, std_radius, phi_span_2pi, R, r.

    Error handling:
        Raises ValueError if points or phis are empty or mismatched.
    """
    if not points or not phis or len(points) != len(phis):
        raise ValueError("Points and phis must be non-empty and of equal length.")

    n = len(points)
    xs, ys, zs = zip(*points)

    cx = sum(xs) / n
    cy = sum(ys) / n
    cz = sum(zs) / n

    radii = [math.sqrt(x * x + y * y + z * z) for x, y, z in points]
    mean_radius = sum(radii) / n
    var_radius = sum((rv - mean_radius) ** 2 for rv in radii) / n
    std_radius = math.sqrt(var_radius)

    phis_sorted = sorted(phis)
    phi_span = (phis_sorted[-1] - phis_sorted[0]) / (2.0 * math.pi)

    return {
        "center_x": cx,
        "center_y": cy,
        "center_z": cz,
        "mean_radius": mean_radius,
        "std_radius": std_radius,
        "phi_span_2pi": phi_span,
        "R": R,
        "r": r,
    }


def analyze_all_bitflows(samples_per_bit: int = 1) -> None:
    """
    Run the torus mapping + analysis for all generated BITRAF_BITFLOWS
    and print a compact report per denominator.
    """
    print("===================================================================")
    print("RAFAELIA_TOROID_BITFLOW – Bitraf flows on ToroidΔπφ (auto v2)")
    print("===================================================================")

    if not BITRAF_BITFLOWS:
        print("[!] No Bitraf bitflows registered. BITRAF_BITFLOWS is empty.")
        return

    for den, bits in BITRAF_BITFLOWS.items():
        print(f"\n--- Analyzing DEN_{den} ---")
        print(f"[i] Bitflow length: {len(bits)} bits")

        try:
            points, phis, R, r = build_torus_points_from_bits(
                den=den,
                bits=bits,
                samples_per_bit=samples_per_bit,
            )
            sig = analyze_torus_points(points, phis, R, r)
        except ValueError as e:
            print(f"[!] Error analyzing DEN_{den}: {e}")
            continue

        print(f"[i] R (major radius)  = {sig['R']:.6f}")
        print(f"[i] r (minor radius)  = {sig['r']:.6f}")
        print(f"[i] center ≈ ({sig['center_x']:.6f}, "
              f"{sig['center_y']:.6f}, {sig['center_z']:.6f})")
        print(f"[i] mean radius       = {sig['mean_radius']:.6f}")
        print(f"[i] std radius        = {sig['std_radius']:.6e}")
        print(f"[i] φ-span / 2π       = {sig['phi_span_2pi']:.6f}")


if __name__ == "__main__":
    # You can increase samples_per_bit for smoother trajectories.
    analyze_all_bitflows(samples_per_bit=1)
