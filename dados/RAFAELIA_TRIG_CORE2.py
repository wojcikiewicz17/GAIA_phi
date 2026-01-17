#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA_TRIG_CORE
===================

Core trigonometric utilities for the RAFAELIA framework.

This module provides:
    - Spiral generator using the √3/2 scaling factor (Spiral√3/2).
    - Yin-Yang spiral pair with exactly 42 points (21 + 21).
    - ToroidΔπφ parametrization utilities (torus in R³).
    - Time → (sin, cos) encoders for cyclic features.
    - Symbolic frequency mapping (e.g. 963, 999, 1008, 144 kHz).

Design goals:
    - Pure Python, standard library only (math + typing + dataclasses).
    - Numerically simple, deterministic, side-effect free.
    - Safe parameter checks and explicit error messages.

Author (symbolic): ∆RafaelVerboΩ (RAFAELIA / RAFCODE-Φ)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PI: float = math.pi
TAU: float = 2.0 * math.pi  # Full turn in radians
SQRT3_OVER_2: float = math.sqrt(3.0) / 2.0  # cos(30°) = sin(60°)


# ---------------------------------------------------------------------------
# Symbolic frequency model
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SymbolicFrequency:
    """Symbolic RAFAELIA frequency as numeric value plus metadata."""
    name: str
    hz: float
    meaning: str


SYMBOLIC_FREQUENCIES: Dict[str, SymbolicFrequency] = {
    "963": SymbolicFrequency(
        name="fΩ_963",
        hz=963.0,
        meaning="Long-horizon / high-coherence frequency (symbolic-ethical anchor).",
    ),
    "999": SymbolicFrequency(
        name="fΩ_999",
        hz=999.0,
        meaning="Limit / edge / stress-test frequency (symbolic boundary).",
    ),
    "1008": SymbolicFrequency(
        name="fΩ_1008",
        hz=1008.0,
        meaning="Full-cycle symbolic frequency (e.g. 7×144, 42×24 cycles).",
    ),
    "144k": SymbolicFrequency(
        name="fΩ_144k",
        hz=144_000.0,
        meaning="High-frequency symbolic carrier (144 kHz).",
    ),
}


def get_symbolic_frequency(key: str) -> SymbolicFrequency:
    """Fetch a symbolic RAFAELIA frequency by key (e.g. '963', '999')."""
    if key not in SYMBOLIC_FREQUENCIES:
        raise KeyError(
            f"Unknown symbolic frequency key '{key}'. "
            f"Available keys: {sorted(SYMBOLIC_FREQUENCIES.keys())}"
        )
    return SYMBOLIC_FREQUENCIES[key]


# ---------------------------------------------------------------------------
# Spiral√3/2 generators
# ---------------------------------------------------------------------------

def generate_spiral_sqrt3_over_2(
    n_turns: int,
    steps_per_turn: int,
    r0: float = 1.0,
    direction: int = 1,
) -> List[Tuple[float, float]]:
    """
    Generate a 2D spiral using the √3/2 scaling factor (Spiral√3/2).

    r(k) = r0 * (SQRT3_OVER_2) ** k
    θ(k) = sign(direction) * 2π * k / steps_per_turn
    """
    if n_turns < 1:
        raise ValueError("n_turns must be >= 1.")
    if steps_per_turn < 1:
        raise ValueError("steps_per_turn must be >= 1.")
    if r0 <= 0.0:
        raise ValueError("r0 must be > 0.0.")
    if direction == 0:
        raise ValueError("direction must be non-zero (use +1 or -1).")

    total_steps: int = n_turns * steps_per_turn
    sign: int = 1 if direction > 0 else -1

    points: List[Tuple[float, float]] = []
    for k in range(total_steps + 1):  # +1 → include k=0 and k=total_steps
        radius = r0 * (SQRT3_OVER_2 ** k)
        theta = sign * TAU * (k / float(steps_per_turn))
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        points.append((x, y))

    return points


def generate_spiral_yinyang_42(
    r0: float = 1.0,
) -> List[Tuple[float, float]]:
    """
    Generate a Yin-Yang pair of spirals using the √3/2 scaling factor.

    Returns exactly 42 points:
        - 21 points for the "Yin" spiral (counter-clockwise),
        - 21 points for the "Yang" spiral (clockwise).

    Both spirals:
        n_turns = 1
        steps_per_turn = 20  →  20 + 1 = 21 points each
    """
    if r0 <= 0.0:
        raise ValueError("r0 must be > 0.0.")

    # Yin: counter-clockwise
    yin = generate_spiral_sqrt3_over_2(
        n_turns=1,
        steps_per_turn=20,
        r0=r0,
        direction=1,
    )

    # Yang: clockwise
    yang = generate_spiral_sqrt3_over_2(
        n_turns=1,
        steps_per_turn=20,
        r0=r0,
        direction=-1,
    )

    return yin + yang  # 21 + 21 = 42 points


# ---------------------------------------------------------------------------
# ToroidΔπφ parametrization
# ---------------------------------------------------------------------------

def torus_point(
    R: float,
    r: float,
    u: float,
    v: float,
) -> Tuple[float, float, float]:
    """
    Parametrize a point on a torus embedded in R³.

    x = (R + r * cos v) * cos u
    y = (R + r * cos v) * sin u
    z = r * sin v
    """
    if R <= 0.0:
        raise ValueError("Major radius R must be > 0.")
    if r <= 0.0:
        raise ValueError("Minor radius r must be > 0.")

    cos_v = math.cos(v)
    sin_v = math.sin(v)
    cos_u = math.cos(u)
    sin_u = math.sin(u)

    x = (R + r * cos_v) * cos_u
    y = (R + r * cos_v) * sin_u
    z = r * sin_v
    return x, y, z


def torus_grid(
    R: float,
    r: float,
    n_u: int,
    n_v: int,
) -> List[Tuple[float, float, float]]:
    """
    Generate a regular grid of points on a torus surface.

    u_i = 2π * i / n_u
    v_j = 2π * j / n_v
    """
    if n_u < 1:
        raise ValueError("n_u must be >= 1.")
    if n_v < 1:
        raise ValueError("n_v must be >= 1.")

    points: List[Tuple[float, float, float]] = []
    for i in range(n_u):
        u = TAU * (i / float(n_u))
        for j in range(n_v):
            v = TAU * (j / float(n_v))
            points.append(torus_point(R, r, u, v))
    return points


# ---------------------------------------------------------------------------
# Time → (sin, cos) encoders
# ---------------------------------------------------------------------------

def encode_time_cycle(
    t: float,
    period: float,
) -> Tuple[float, float]:
    """
    Encode scalar time t into a 2D cyclic feature.

    phase = 2π * t / period
    return (cos phase, sin phase)
    """
    if period <= 0.0:
        raise ValueError("period must be > 0.0.")
    phase = TAU * (t / period)
    return math.cos(phase), math.sin(phase)


def encode_time_with_frequency(
    t: float,
    frequency_hz: float,
    phase_offset: float = 0.0,
) -> Tuple[float, float]:
    """
    Encode time t as a sinusoidal signal with frequency f.

    sin_part = sin(2π f t + φ)
    cos_part = cos(2π f t + φ)
    """
    omega = TAU * frequency_hz
    phase = omega * t + phase_offset
    return math.sin(phase), math.cos(phase)


def encode_time_with_symbolic_frequency(
    t: float,
    key: str,
    phase_offset: float = 0.0,
) -> Tuple[float, float]:
    """Same as encode_time_with_frequency, using a symbolic RAFAELIA key."""
    freq = get_symbolic_frequency(key)
    return encode_time_with_frequency(t, freq.hz, phase_offset=phase_offset)


# ---------------------------------------------------------------------------
# Utility: pure-Python linspace
# ---------------------------------------------------------------------------

def linspace(start: float, stop: float, num: int) -> List[float]:
    """Simple pure-Python linspace implementation."""
    if num < 1:
        raise ValueError("num must be >= 1.")
    if num == 1:
        return [float(start)]
    step = (stop - start) / float(num - 1)
    return [start + step * i for i in range(num)]


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== RAFAELIA_TRIG_CORE self-test ===")

    # Spiral generic
    spiral_points = generate_spiral_sqrt3_over_2(
        n_turns=2,
        steps_per_turn=10,
        r0=1.0,
        direction=1,
    )
    print(f"Spiral√3/2: generated {len(spiral_points)} points.")

    # Yin-Yang 42
    yy_points = generate_spiral_yinyang_42(r0=1.0)
    print(f"Spiral√3/2 Yin-Yang: generated {len(yy_points)} points (expected 42).")

    # Torus
    torus_points = torus_grid(R=2.0, r=0.5, n_u=4, n_v=4)
    print(f"ToroidΔπφ: generated {len(torus_points)} points.")

    # Time encoders
    cos_val, sin_val = encode_time_cycle(t=6.0, period=24.0)
    print("Time cycle encoding (t=6, period=24):", cos_val, sin_val)

    sin_f, cos_f = encode_time_with_symbolic_frequency(t=0.001, key="963")
    print("Symbolic frequency encoding (t=0.001, key='963'):", sin_f, cos_f)

    print("=== Self-test completed successfully ===")
