#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA_TOROID_MASTER
----------------------
Unified driver for this RAFAELIA session:

1) Encodes Bitraf seeds (DEN_n) taken from RAFAELIA_BITRAF_PRIME_CORE.
2) Stores toroidal signatures (mean_radius, phi_span_2pi, etc).
3) Provides a small "state scan" to verify geometric invariants:
   - I = d3D / C ≈ sqrt(3) / (2*pi)
   - J_toro = V / (A * r) = 0.5
   - C_toro = A / (4*pi^2 * R * r) = 1.0
4) Generates 4 color scatter plots with families low/mid/high.
5) Prints DALL·E prompts in a Van Gogh / RAFAELIA style.

Comments are in English for maintainability.
"""

import sys
import math
import random
from dataclasses import dataclass
from typing import List, Dict, Tuple

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# 1. Data model
# ---------------------------------------------------------------------


@dataclass
class SeedToroid:
    """Basic container for a Bitraf seed and its toroidal signature."""
    den: int
    base2: int
    base8: int
    base10: int
    base16: int
    maxP: int
    phi_span_2pi: float
    mean_radius: float
    std_radius: float


# Seed table extracted from RAFAELIA_TOROID_PERIOD_LINK output.
SEEDS: List[SeedToroid] = [
    SeedToroid(47,   23, 23, 46, 23, 46, 0.886719,  7.508654, 6.126548e-01),
    SeedToroid(53,   52, 52, 13, 13, 52, 0.996094,  8.460751, 6.128343e-01),
    SeedToroid(59,   58, 58, 58, 29, 58, 0.992188,  9.413425, 6.129631e-01),
    SeedToroid(61,   60, 20, 60, 15, 60, 0.984375,  9.731082, 6.129980e-01),
    SeedToroid(67,   66, 22, 33, 33, 66, 0.996094, 10.684286, 6.130853e-01),
    SeedToroid(81,   54, 18,  9, 27, 54, 0.988281, 12.909425, 6.132209e-01),
    SeedToroid(94,   23, 23, 46, 23, 46, 0.886719, 14.976434, 6.132982e-01),
    SeedToroid(97,   48, 16,  0, 12, 48, 0.988281, 15.453513, 6.133120e-01),
    SeedToroid(103,  51, 17, 34, 51, 51, 0.949219, 16.407737, 6.133362e-01),
    SeedToroid(106,  52, 52, 13, 13, 52, 0.996094, 16.884879, 6.133468e-01),
    SeedToroid(107,   0,  0, 53, 53, 53, 0.984375, 17.043931, 6.133502e-01),
    SeedToroid(115,  44, 44, 22, 11, 44, 0.933594, 18.316407, 6.133742e-01),
    SeedToroid(118,  58, 58, 58, 29, 58, 0.988281, 18.793612, 6.133820e-01),
    SeedToroid(119,  24,  8, 48,  6, 48, 0.867188, 18.952684, 6.133845e-01),
    SeedToroid(121,   0,  0, 22, 55, 55, 0.996094, 19.270831, 6.133893e-01),
    SeedToroid(122,  60, 20, 60, 15, 60, 0.984375, 19.429906, 6.133916e-01),
]

# Families by denominator range
FAMILY_LOW = {47, 53, 59, 61, 67, 81}
FAMILY_MID = {94, 97, 103, 106, 107}
FAMILY_HIGH = {115, 118, 119, 121, 122}

COLOR_MAP = {
    "low": "tab:blue",
    "mid": "tab:orange",
    "high": "tab:green",
}
LABEL_MAP = {
    "low": "family low (≈ 47–81)",
    "mid": "family mid (≈ 94–107)",
    "high": "family high (≈ 115–122)",
}


def get_family(den: int) -> str:
    """Return family name for a given denominator."""
    if den in FAMILY_LOW:
        return "low"
    if den in FAMILY_MID:
        return "mid"
    if den in FAMILY_HIGH:
        return "high"
    return "low"  # default fallback


# ---------------------------------------------------------------------
# 2. Invariants: triangle/circle and toroid
# ---------------------------------------------------------------------


def invariant_I_triangle_circle(K: float, L: float) -> float:
    """
    Compute I = d3D / C where:
    - d3D ~ diagonal of equilateral-based 3D structure: K*L*sqrt(3)
    - C   ~ circle circumference: 2*pi*K*L
    This is engineered so I ≡ sqrt(3)/(2*pi), independent of K and L.
    """
    d3D = K * L * math.sqrt(3.0)
    C = 2.0 * math.pi * K * L
    return d3D / C


def torus_volume(R: float, r: float) -> float:
    """Volume of a standard torus."""
    return 2.0 * math.pi**2 * R * r**2


def torus_area(R: float, r: float) -> float:
    """Surface area of a standard torus."""
    return 4.0 * math.pi**2 * R * r


def toroid_invariants(R: float, r: float) -> Tuple[float, float]:
    """
    Compute toroidal invariants:
    J_toro = V / (A * r)
    C_toro = A / (4*pi^2 * R * r)
    For an ideal torus, they should be exactly 0.5 and 1.0.
    """
    V = torus_volume(R, r)
    A = torus_area(R, r)
    J_toro = V / (A * r)
    C_toro = A / (4.0 * math.pi**2 * R * r)
    return J_toro, C_toro


# ---------------------------------------------------------------------
# 3. State scan (random states over E, K, Fibonacci modes, etc.)
# ---------------------------------------------------------------------


E_VALUES = [2.0, 3.0, math.pi, math.sqrt(3.0) / 2.0]  # sample exponents
K_VALUES = [math.pi, math.pi**2, math.sqrt(3.0), 1.1547]  # scaling constants


def run_state_scan(num_states: int = 1000) -> None:
    """
    Randomly explores states (E, K, L) and verifies:
    - I ≈ sqrt(3)/(2*pi) for triangle/circle configuration.
    - J_toro ≈ 0.5 and C_toro ≈ 1.0 over random torus radii.

    This is a symbolic "sanity check" of the invariants,
    not a Monte Carlo proof.
    """
    I_target = math.sqrt(3.0) / (2.0 * math.pi)
    I_values: List[float] = []
    J_values: List[float] = []
    C_values: List[float] = []

    for _ in range(num_states):
        # Random geometric state
        E = random.choice(E_VALUES)  # currently unused but kept for future use
        K = random.choice(K_VALUES)
        L = random.uniform(0.8, 1.8)

        I = invariant_I_triangle_circle(K, L)
        I_values.append(I)

        # Random torus (R >> r for a thin torus)
        R = random.uniform(7.0, 20.0)
        r = random.uniform(0.7, 2.0)
        J_toro, C_toro = toroid_invariants(R, r)
        J_values.append(J_toro)
        C_values.append(C_toro)

    def stats(arr: List[float]) -> Tuple[float, float, float, float]:
        return (float(np.mean(arr)),
                float(np.std(arr)),
                float(np.min(arr)),
                float(np.max(arr)))

    mean_I, std_I, min_I, max_I = stats(I_values)
    mean_J, std_J, min_J, max_J = stats(J_values)
    mean_C, std_C, min_C, max_C = stats(C_values)

    print("=== RAFAELIA :: State Scan (Triangle + Toroid) ===")
    print(f"States generated: {num_states}")
    print(f"I_TARGET = sqrt(3)/(2*pi) ≈ {I_target:.12f}\n")

    print(">> Invariant I = d3D / C")
    print(f"  mean(I) = {mean_I:.12f}")
    print(f"  std(I)  = {std_I:.3e}")
    print(f"  min(I)  = {min_I:.12f}")
    print(f"  max(I)  = {max_I:.12f}\n")

    print(">> Toroid invariant J_toro = V / (A * r)")
    print(f"  mean(J_toro) = {mean_J:.12f}")
    print(f"  std(J_toro)  = {std_J:.3e}")
    print(f"  min(J_toro)  = {min_J:.12f}")
    print(f"  max(J_toro)  = {max_J:.12f}\n")

    print(">> Toroid invariant C_toro = A / (4*pi^2*R*r)")
    print(f"  mean(C_toro) = {mean_C:.12f}")
    print(f"  std(C_toro)  = {std_C:.3e}")
    print(f"  min(C_toro)  = {min_C:.12f}")
    print(f"  max(C_toro)  = {max_C:.12f}\n")


# ---------------------------------------------------------------------
# 4. Scatter plots with families and optional polynomial fit
# ---------------------------------------------------------------------


def scatter_by_family(
    x: List[float],
    y: List[float],
    dens: List[int],
    xlabel: str,
    ylabel: str,
    title: str,
    fname_prefix: str,
    poly_fit: bool = False,
    poly_degree: int = 1,
) -> None:
    """
    Draws a scatter plot:
    - color-coded by family (low/mid/high),
    - each point labeled with its denominator,
    - optional polynomial fit y(x) with given degree.

    This function is designed for visual exploration and uses
    straightforward plotting arguments for clarity.
    """
    plt.figure(figsize=(11, 7))

    # Plot each family separately for a clear legend
    for fam in ("low", "mid", "high"):
        xs: List[float] = []
        ys: List[float] = []
        ns: List[int] = []
        for xi, yi, n in zip(x, y, dens):
            if get_family(n) == fam:
                xs.append(xi)
                ys.append(yi)
                ns.append(n)
        if not xs:
            continue
        plt.scatter(
            xs,
            ys,
            s=50,
            alpha=0.9,
            color=COLOR_MAP[fam],
            edgecolors="black",
            linewidths=0.5,
            label=LABEL_MAP[fam],
        )
        for xi, yi, n in zip(xs, ys, ns):
            plt.text(xi, yi, str(n), fontsize=9, ha="center", va="bottom")

    # Optional global polynomial fit (all points together)
    if poly_fit and len(x) >= poly_degree + 1:
        x_arr = np.array(x, dtype=float)
        y_arr = np.array(y, dtype=float)
        coeffs = np.polyfit(x_arr, y_arr, deg=poly_degree)
        poly = np.poly1d(coeffs)

        x_min, x_max = float(min(x_arr)), float(max(x_arr))
        x_line = np.linspace(x_min, x_max, 256)
        y_line = poly(x_line)

        plt.plot(
            x_line,
            y_line,
            linestyle="-",
            linewidth=1.5,
            color="gray",
            alpha=0.8,
            label=f"poly fit (deg={poly_degree})",
        )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
    plt.legend(loc="best")
    plt.tight_layout()

    png_name = f"{fname_prefix}.png"
    svg_name = f"{fname_prefix}.svg"
    plt.savefig(png_name, dpi=300)
    plt.savefig(svg_name)
    print(f"[OK] Saved: {png_name}, {svg_name}")
    plt.close()


def generate_all_plots() -> None:
    """Generate the four main RAFAELIA toroidal scatter plots."""
    dens = [s.den for s in SEEDS]
    maxP = [s.maxP for s in SEEDS]
    phi_span = [s.phi_span_2pi for s in SEEDS]
    mean_radius = [s.mean_radius for s in SEEDS]

    # 1) mean_radius vs phi_span_2pi
    scatter_by_family(
        mean_radius,
        phi_span,
        dens,
        xlabel="mean_radius (toroid mean |(x,y,z)|)",
        ylabel="phi_span_2pi (normalized angular coverage)",
        title="RAFAELIA – mean_radius vs ToroidΔπφ angular span",
        fname_prefix="RAFAELIA_mean_radius_vs_phi_span_v2",
        poly_fit=False,
    )

    # 2) maxP vs phi_span_2pi
    scatter_by_family(
        maxP,
        phi_span,
        dens,
        xlabel="maxP (maximum period over bases {2,8,10,16})",
        ylabel="phi_span_2pi (normalized angular coverage)",
        title="RAFAELIA – maxP vs ToroidΔπφ angular span",
        fname_prefix="RAFAELIA_maxP_vs_phi_span_v2",
        poly_fit=False,
    )

    # 3) den vs phi_span_2pi
    scatter_by_family(
        dens,
        phi_span,
        dens,
        xlabel="denominator n",
        ylabel="phi_span_2pi (normalized angular coverage)",
        title="RAFAELIA – den vs ToroidΔπφ angular span",
        fname_prefix="RAFAELIA_den_vs_phi_span_v2",
        poly_fit=False,
    )

    # 4) den vs mean_radius (with linear polynomial fit)
    scatter_by_family(
        dens,
        mean_radius,
        dens,
        xlabel="denominator n",
        ylabel="mean_radius (toroid mean |(x,y,z)|)",
        title="RAFAELIA – den vs ToroidΔπφ scale",
        fname_prefix="RAFAELIA_den_vs_mean_radius_v2",
        poly_fit=True,
        poly_degree=1,
    )


# ---------------------------------------------------------------------
# 5. Artistic / DALL·E prompts (Van Gogh + RAFAELIA geometry)
# ---------------------------------------------------------------------


def print_art_prompts() -> None:
    """
    Print a set of DALL·E prompts based on the toroidal geometry,
    Bitraf seeds and Van Gogh style. These prompts are textual only.
    """
    print("=== RAFAELIA :: Van Gogh × ToroidΔπφ prompts ===\n")

    I_target = math.sqrt(3.0) / (2.0 * math.pi)

    prompt_1 = f"""
A Van Gogh-inspired oil painting of a night sky over a cosmic torus,
where the stars trace decimal spirals of 1/n with denominators
47, 53, 59, 61, 67 and 81. The main torus has a luminous band encoding
the invariant I = sqrt(3)/(2*pi) ≈ {I_target:.6f}, painted as a
subtle ratio between the diagonal of a glowing triangle and the orbit
of a circle. Swirling blues and yellows, strong brush strokes,
and tiny numbers 47–81 hidden in the constellations.
    """.strip()

    prompt_2 = """
A Van Gogh style painting showing three concentric families of tori:
the inner ring in deep blue (family low: 47–81), the middle ring
in orange (family mid: 94–107), and the outer ring in emerald green
(family high: 115–122). Each torus is labeled with its denominator n
and its angular coverage φ_span_2π, depicted as glowing arcs.
The texture of the paint suggests flowing binary streams wrapping
around each torus like Bitraf bitflows.
    """.strip()

    prompt_3 = """
An abstract Van Gogh-like landscape where fields of wheat are replaced
by hexagonal grids of triangles and circles. Along the horizon,
a translucent torus floats, and inside it the quadratic curve
of Bhaskara (a parabola) is drawn with pure light, intersecting
positions marked as 47, 67, 97, 121 and 122. The sky spirals into
a Fibonacci-like vortex, mixing π, √3 and golden tones.
    """.strip()

    for i, p in enumerate((prompt_1, prompt_2, prompt_3), start=1):
        print(f"[Prompt {i}]\n{p}\n")


# ---------------------------------------------------------------------
# 6. Summary and CLI
# ---------------------------------------------------------------------


def print_summary() -> None:
    """Print a compact summary of this master script."""
    print("=== RAFAELIA_TOROID_MASTER summary ===")
    print(f"Seeds loaded: {len(SEEDS)}")
    dens = [s.den for s in SEEDS]
    print(f"Denominators: {sorted(dens)}")
    print("Families:")
    print(f"  low : {sorted(FAMILY_LOW)}")
    print(f"  mid : {sorted(FAMILY_MID)}")
    print(f"  high: {sorted(FAMILY_HIGH)}\n")

    I_target = math.sqrt(3.0) / (2.0 * math.pi)
    print(f"Invariant I_target = sqrt(3)/(2*pi) ≈ {I_target:.12f}")
    print("Toroid invariants (ideal): J_toro = 0.5, C_toro = 1.0\n")

    print("Usage:")
    print("  python RAFAELIA_TOROID_MASTER.py           # this summary")
    print("  python RAFAELIA_TOROID_MASTER.py plots     # generate 4 plots")
    print("  python RAFAELIA_TOROID_MASTER.py scan      # run state scan")
    print("  python RAFAELIA_TOROID_MASTER.py art       # print DALL·E prompts")
    print()


def main(argv: List[str]) -> None:
    """Entry point with a simple CLI dispatcher."""
    if len(argv) <= 1:
        print_summary()
        return

    cmd = argv[1].lower()

    if cmd == "plots":
        generate_all_plots()
    elif cmd == "scan":
        run_state_scan(num_states=1000)
    elif cmd == "art":
        print_art_prompts()
    else:
        print(f"[WARN] Unknown command: {cmd}\n")
        print_summary()


if __name__ == "__main__":
    main(sys.argv)
