#!/usr/bin/env python3
# RAFAELIA_STATE_SCAN_v2.py
# Extended exploration of Rafaelian geometric states including:
#   - Triangle / circle invariant I = d3D / C
#   - Toroid invariants (area, volume, dimensionless ratios)
#   - Phase texture linked to ToroidΔπφ and phi_R
#
# Design notes:
# - Keeps computations numerically stable (avoid division by zero).
# - Uses Bitraf prime/fallback seeds as discrete inputs (denominators).

import math
import random
import statistics

# --- Core constants ---

phi_R = math.sqrt(3.0) / 2.0                  # Rafaelian constant
I_TARGET = math.sqrt(3.0) / (2.0 * math.pi)   # triangle/circle invariant

# Parameter grids
E_SET = [
    2.0,
    3.0,
    math.pi,
    phi_R,
    0.5,
    1.5,
]

K_SET = [
    math.pi,
    2.0 * math.pi,
    math.pi ** 2,
    math.sqrt(3.0),
    phi_R,
    math.sqrt(4.0 / 3.0),
]

FIB_MODES = ["forward", "reverse", "inverse"]

# Bitraf denominators discovered by RAFAELIA_BITRAF_PRIME_CORE (fallback mode)
BITRAF_DEN_SEEDS = [
    67, 61, 122, 59, 118, 121, 81, 107,
    53, 106, 103, 119, 97, 47, 94, 115,
]


# --- Fibonacci helpers ---

def fib(n: int) -> int:
    """Standard Fibonacci (iterative), n >= 0. Small n to avoid overflow."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fib_indexed(n: int, mode: str, max_n: int = 24) -> int:
    """
    Returns a Fibonacci-related value under different symbolic modes:
      - "forward": F_n
      - "reverse": F_(max_n - n)
      - "inverse": simple mapped integer from 1 / (1 + F_n)
    This is intentionally low-risk (bounded n) to avoid large integer growth.
    """
    n = max(0, min(n, max_n))
    if mode == "forward":
        return fib(n)
    elif mode == "reverse":
        return fib(max_n - n)
    elif mode == "inverse":
        fn = fib(n)
        return int(1000 * (1.0 / (1.0 + fn)))
    else:
        return fib(n)


# --- Toroid helpers ---

def build_toroid(R: float, r: float) -> dict:
    """
    Computes toroid geometric quantities and invariants.
    Uses standard formulas:
      A = 4 * pi^2 * R * r
      V = 2 * pi^2 * R * r^2
    Returns:
      - A, V
      - J_toro = V / (A * r)  (expected ~ 0.5, dimensionless)
      - C_toro = A / (4*pi^2 * R * r) (expected ~ 1.0, dimensionless)
    """
    if R <= 0.0 or r <= 0.0:
        # Invalid geometry, return NaNs to signal error.
        return {
            "A": float("nan"),
            "V": float("nan"),
            "J_toro": float("nan"),
            "C_toro": float("nan"),
        }

    A = 4.0 * (math.pi ** 2) * R * r
    V = 2.0 * (math.pi ** 2) * R * (r ** 2)

    denom_J = A * r
    denom_C = 4.0 * (math.pi ** 2) * R * r

    J_toro = V / denom_J if denom_J != 0.0 else float("nan")
    C_toro = A / denom_C if denom_C != 0.0 else float("nan")

    return {
        "A": A,
        "V": V,
        "J_toro": J_toro,
        "C_toro": C_toro,
    }


# --- State sampling (v2) ---

def sample_state_v2() -> dict:
    """
    Generates an extended Rafaelian state S including:
      - geometric invariant I (triangle/circle)
      - toroid invariants from Bitraf-derived radii
      - phase texture combined into a ToroidΔπφ-like scalar in [0,1)
    This function is pure (no I/O), returning a dictionary with all fields.
    """
    # Random choices for E, K, Fibonacci mode, index and Bitraf denominator
    E = random.choice(E_SET)
    K = random.choice(K_SET)
    mode = random.choice(FIB_MODES)
    n_idx = random.randint(2, 24)
    den = random.choice(BITRAF_DEN_SEEDS)

    fn_val = fib_indexed(n_idx, mode)
    # Base length L perturbed by Fibonacci residue
    L = 1.0 + (fn_val % 13) / 10.0

    # --- Triangle / circle invariant ---

    d3d = K * L * math.sqrt(3.0)
    C = 2.0 * math.pi * K * L
    I = d3d / C if C != 0.0 else float("nan")
    diff_I = I - I_TARGET

    # --- Phase curvature (same as v1, reused for ToroidΔπφ) ---

    q = K * (L ** E)
    alpha = 1.0
    beta = 0.5
    gamma = 0.1
    theta_curv = alpha * math.sin(beta * q) + gamma * math.log1p(abs(q))
    theta_norm = (theta_curv % (2.0 * math.pi)) / (2.0 * math.pi)

    # --- Toroid radii from Bitraf seed and L, phi_R ---

    # R: scale of the major ring, proportional to denominator
    R = den / (2.0 * math.pi)
    # r: minor radius linked to L and phi_R, then clamped to keep r < 0.5*R
    r_raw = L * phi_R
    r = min(r_raw, 0.5 * R)

    toroid = build_toroid(R, r)

    # --- ToroidΔπφ-like phase invariant ---
    # Combine:
    #   - ratio r/R
    #   - I_TARGET (triangle/circle invariant)
    #   - phi_R
    #   - theta_norm (curved phase)
    # into a scalar in [0,1) for statistical exploration.
    ratio_rR = r / R if R != 0.0 else float("nan")

    combo = (
        (ratio_rR if not math.isnan(ratio_rR) else 0.0)
        * I_TARGET
        * phi_R
        + theta_norm
    )
    toroid_phase = combo % 1.0

    return {
        "E": E,
        "K": K,
        "mode": mode,
        "n_idx": n_idx,
        "fn_val": fn_val,
        "den": den,
        "L": L,
        "d3d": d3d,
        "C": C,
        "I": I,
        "diff_I": diff_I,
        "theta_curv": theta_curv,
        "theta_norm": theta_norm,
        "R": R,
        "r": r,
        "ratio_rR": ratio_rR,
        "A_toro": toroid["A"],
        "V_toro": toroid["V"],
        "J_toro": toroid["J_toro"],
        "C_toro": toroid["C_toro"],
        "toroid_phase": toroid_phase,
    }


# --- Scan function (v2) ---

def scan_states_v2(n_samples: int = 1000) -> None:
    """
    Generates n_samples states and prints:
      - statistics for I (triangle/circle invariant)
      - statistics for toroid invariants J_toro and C_toro
      - statistics for r/R ratio and toroid_phase distribution
      - a few "worst" examples where |I - I_TARGET| or |J_toro - 0.5|
        deviate the most (should be near numerical noise).
    """
    states: list[dict] = []
    for _ in range(n_samples):
        s = sample_state_v2()
        if math.isnan(s["I"]) or math.isnan(s["J_toro"]) or math.isnan(s["C_toro"]):
            continue
        states.append(s)

    if not states:
        print("No valid states generated.")
        return

    # Collect series
    I_values = [s["I"] for s in states]
    diff_I_values = [s["diff_I"] for s in states]
    J_values = [s["J_toro"] for s in states]
    C_values = [s["C_toro"] for s in states]
    ratio_rR_values = [s["ratio_rR"] for s in states if not math.isnan(s["ratio_rR"])]
    phase_values = [s["toroid_phase"] for s in states]

    print("=== RAFAELIA :: State Scan v2 (Triangle + Toroid) ===")
    print(f"Generated states: {len(states)}")
    print(f"I_TARGET (triangle/circle) = sqrt(3)/(2*pi) ≈ {I_TARGET:.12f}")
    print("Expected toroid invariants: J_toro ≈ 0.5, C_toro ≈ 1.0\n")

    # --- I statistics ---
    print(">> Invariant I = d3D / C")
    print(f"  mean(I)        = {statistics.mean(I_values):.12f}")
    print(f"  std(I)         = {statistics.pstdev(I_values):.12e}")
    print(f"  min(I)         = {min(I_values):.12f}")
    print(f"  max(I)         = {max(I_values):.12f}\n")

    # --- Toroid invariants ---
    print(">> Toroid invariant J_toro = V / (A * r)")
    print(f"  mean(J_toro)   = {statistics.mean(J_values):.12f}")
    print(f"  std(J_toro)    = {statistics.pstdev(J_values):.12e}")
    print(f"  min(J_toro)    = {min(J_values):.12f}")
    print(f"  max(J_toro)    = {max(J_values):.12f}\n")

    print(">> Toroid invariant C_toro = A / (4*pi^2*R*r)")
    print(f"  mean(C_toro)   = {statistics.mean(C_values):.12f}")
    print(f"  std(C_toro)    = {statistics.pstdev(C_values):.12e}")
    print(f"  min(C_toro)    = {min(C_values):.12f}")
    print(f"  max(C_toro)    = {max(C_values):.12f}\n")

    # --- r/R and phase ---
    print(">> r/R ratio statistics")
    print(f"  mean(r/R)      = {statistics.mean(ratio_rR_values):.12f}")
    print(f"  std(r/R)       = {statistics.pstdev(ratio_rR_values):.12f}")
    print(f"  min(r/R)       = {min(ratio_rR_values):.12f}")
    print(f"  max(r/R)       = {max(ratio_rR_values):.12f}\n")

    print(">> ToroidΔπφ phase (toroid_phase in [0,1))")
    print(f"  mean(phase)    = {statistics.mean(phase_values):.12f}")
    print(f"  std(phase)     = {statistics.pstdev(phase_values):.12f}")
    print(f"  min(phase)     = {min(phase_values):.12f}")
    print(f"  max(phase)     = {max(phase_values):.12f}\n")

    # --- Worst states for I and J_toro ---

    worst_I = sorted(states, key=lambda s: abs(s["diff_I"]), reverse=True)[:5]
    worst_J = sorted(states, key=lambda s: abs(s["J_toro"] - 0.5), reverse=True)[:5]

    print(">> States with largest |I - I_TARGET| (numerical stress)")
    for s in worst_I:
        print(
            f"  den={s['den']}, E={s['E']:.6g}, K={s['K']:.6g}, "
            f"mode={s['mode']}, n={s['n_idx']}, L={s['L']:.6f}, "
            f"I={s['I']:.12f}, diff_I={s['diff_I']:.3e}"
        )

    print("\n>> States with largest |J_toro - 0.5| (toroid stress)")
    for s in worst_J:
        print(
            f"  den={s['den']}, R={s['R']:.6f}, r={s['r']:.6f}, "
            f"J_toro={s['J_toro']:.12f}, C_toro={s['C_toro']:.12f}, "
            f"ratio_rR={s['ratio_rR']:.6f}, phase={s['toroid_phase']:.6f}"
        )


if __name__ == "__main__":
    # You can tune n_samples for deeper scans.
    scan_states_v2(n_samples=1000)
