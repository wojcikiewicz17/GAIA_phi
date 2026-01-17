#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA_TRIG_CORE
===================

Core trigonometric utilities for the RAFAELIA framework.

This module provides:
    - Spiral generator using the √3/2 scaling factor (Spiral√3/2).
    - ToroidΔπφ parametrization utilities (torus in R³).
    - Time → (sin, cos) encoders for cyclic features.
    - Symbolic frequency mapping (e.g. 963, 999, 1008, 144 kHz).

Design goals:
    - Pure Python, standard library only (math + typing + dataclasses).
    - Numerically simple, deterministic, side-effect free.
    - Safe parameter checks and explicit error messages.
    - Ready to be used in ML pipelines, numerical experiments or plotting code.

NOTE:
    - This file does not perform any plotting itself; it only computes values.
    - For visualizations, plug the outputs into matplotlib or another library.

Author (symbolic): ∆RafaelVerboΩ (RAFAELIA / RAFCODE-Φ)
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple


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
    """
    Represents a symbolic RAFAELIA frequency as a concrete numeric value plus metadata.

    Attributes
    ----------
    name : str
        Short label used to identify the frequency (e.g. "fΩ_963").
    hz : float
        Frequency in Hertz. Can be a physical or symbolic frequency.
    meaning : str
        Human-readable description of what this frequency represents
        in the RAFAELIA context (ethics, stress test, full cycle, etc.).
    """
    name: str
    hz: float
    meaning: str


# Core symbolic frequencies used in the RAFAELIA ecosystem.
# You can extend this dict as needed in your own code.
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
        meaning="Full-cycle symbolic frequency (e.g. 7×144, 42×24 style cycles).",
    ),
    "144k": SymbolicFrequency(
        name="fΩ_144k",
        hz=144_000.0,
        meaning="High-frequency symbolic carrier (144 kHz).",
    ),
}


def get_symbolic_frequency(key: str) -> SymbolicFrequency:
    """
    Fetch a symbolic RAFAELIA frequency by key.

    Parameters
    ----------
    key : str
        One of the keys in SYMBOLIC_FREQUENCIES (e.g. "963", "999", "1008", "144k").

    Returns
    -------
    SymbolicFrequency
        Frequency descriptor.

    Raises
    ------
    KeyError
        If the key is not found in SYMBOLIC_FREQUENCIES.

    Implementation notes
    --------------------
    - Using explicit KeyError avoids silently falling back to incorrect values.
    - This helps keep the semantics and licensing clear in higher-level code.
    """
    if key not in SYMBOLIC_FREQUENCIES:
        raise KeyError(
            f"Unknown symbolic frequency key '{key}'. "
            f"Available keys: {sorted(SYMBOLIC_FREQUENCIES.keys())}"
        )
    return SYMBOLIC_FREQUENCIES[key]


# ---------------------------------------------------------------------------
# Spiral√3/2 generator
# ---------------------------------------------------------------------------

def generate_spiral_sqrt3_over_2(
    n_turns: int,
    steps_per_turn: int,
    r0: float = 1.0,
    direction: int = 1,
) -> List[Tuple[float, float]]:
    """
    Generate a 2D spiral using the √3/2 scaling factor (Spiral√3/2).

    The radius evolves according to:
        r(k) = r0 * (SQRT3_OVER_2) ** k
    and the angle (theta) evolves linearly:
        theta(k) = direction * 2π * k / steps_per_turn

    Parameters
    ----------
    n_turns : int
        Number of full turns in the spiral (must be >= 1).
    steps_per_turn : int
        Number of steps per full turn (must be >= 1).
    r0 : float, optional
        Initial radius at k = 0. Must be > 0. Default is 1.0.
    direction : int, optional
        Spiral direction:
            +1 → counter-clockwise (standard mathematical orientation),
            -1 → clockwise.
        Any non-zero value will be normalized to its sign.

    Returns
    -------
    List[Tuple[float, float]]
        List of (x, y) coordinates describing the spiral.

    Raises
    ------
    ValueError
        If parameters are inconsistent (e.g. non-positive steps).

    Bug mitigation / safety notes
    -----------------------------
    - Parameter checks reduce the risk of infinite loops or NaN explosions.
    - The radius grows or shrinks exponentially; for large n, values may
      overflow double precision. Use moderate n_turns if stability is critical.
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
    for k in range(total_steps + 1):
        radius = r0 * (SQRT3_OVER_2 ** k)
        theta = sign * TAU * (k / float(steps_per_turn))
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        points.append((x, y))

    return points


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

    Standard parametrization:
        x = (R + r * cos(v)) * cos(u)
        y = (R + r * cos(v)) * sin(u)
        z = r * sin(v)

    Parameters
    ----------
    R : float
        Major radius (distance from center of hole to center of tube).
        Must be > 0.
    r : float
        Minor radius (radius of the tube). Must be > 0 and typically r < R.
    u : float
        Angle (in radians) around the "major circle" of the torus.
    v : float
        Angle (in radians) around the "minor circle" (tube cross-section).

    Returns
    -------
    Tuple[float, float, float]
        (x, y, z) coordinates in R³.

    Raises
    ------
    ValueError
        If R <= 0 or r <= 0.

    Implementation notes
    --------------------
    - This function is intentionally minimal for reuse in grids and meshes.
    - Higher-level code may quantize u and v, e.g. using linspace-style loops.
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

    Angles are sampled uniformly on [0, 2π):

        u_i = 2π * i / n_u
        v_j = 2π * j / n_v

    Parameters
    ----------
    R : float
        Major radius (must be > 0).
    r : float
        Minor radius (must be > 0).
    n_u : int
        Number of samples along the major circle (must be >= 1).
    n_v : int
        Number of samples along the minor circle (must be >= 1).

    Returns
    -------
    List[Tuple[float, float, float]]
        List of (x, y, z) points on the torus surface.

    Raises
    ------
    ValueError
        If any parameter is invalid.

    Bug mitigation / safety notes
    -----------------------------
    - Uses int-based loops instead of range over floats to avoid cumulative
      floating-point drift in angle increments.
    - Clients can decimate or subsample if they need fewer points.
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
# Time → (sin, cos) encoders for cyclic features
# ---------------------------------------------------------------------------

def encode_time_cycle(
    t: float,
    period: float,
) -> Tuple[float, float]:
    """
    Encode a scalar time t into a 2D cyclic feature using sin/cos.

    The encoding is:
        phase = 2π * t / period
        x = cos(phase)
        y = sin(phase)

    This ensures continuity at the period boundary and is suitable for:
        - Time-of-day encodings,
        - Day-of-year encodings,
        - Any periodic features in ML models.

    Parameters
    ----------
    t : float
        Time value (or any scalar in the same units as 'period').
    period : float
        Period of the cycle. Must be > 0.

    Returns
    -------
    Tuple[float, float]
        (cos_component, sin_component).

    Raises
    ------
    ValueError
        If period <= 0.

    Implementation notes
    --------------------
    - Using cos for the first coordinate and sin for the second is arbitrary
      but consistent; downstream models can treat both equally.
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
    Encode time t as a sinusoidal signal with a given frequency.

    Standard signal:
        x(t) = sin(2π f t + φ)
        y(t) = cos(2π f t + φ)

    Parameters
    ----------
    t : float
        Time scalar.
    frequency_hz : float
        Frequency in Hertz (can be symbolic/abstract).
    phase_offset : float, optional
        Phase offset in radians. Default is 0.

    Returns
    -------
    Tuple[float, float]
        (sin_component, cos_component) at time t.

    Implementation notes
    --------------------
    - This is useful when you want to generate synthetic features or signals
      tied to RAFAELIA's symbolic frequencies (963, 999, 1008, 144k, etc.).
    """
    omega = TAU * frequency_hz
    phase = omega * t + phase_offset
    return math.sin(phase), math.cos(phase)


def encode_time_with_symbolic_frequency(
    t: float,
    key: str,
    phase_offset: float = 0.0,
) -> Tuple[float, float]:
    """
    Encode time t using one of RAFAELIA's symbolic frequencies.

    This is a thin wrapper around `encode_time_with_frequency` that pulls
    the numeric frequency from SYMBOLIC_FREQUENCIES.

    Parameters
    ----------
    t : float
        Time scalar.
    key : str
        Symbolic frequency key (e.g. "963", "999", "1008", "144k").
    phase_offset : float, optional
        Phase offset in radians. Default is 0.

    Returns
    -------
    Tuple[float, float]
        (sin_component, cos_component) at time t.

    Raises
    ------
    KeyError
        If the symbolic frequency key is not registered.

    Security / correctness notes
    ----------------------------
    - By forcing the use of registered keys, we reduce silent mistakes where
      a typo in the frequency label would otherwise go unnoticed.
    """
    freq = get_symbolic_frequency(key)
    return encode_time_with_frequency(t, freq.hz, phase_offset=phase_offset)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def linspace(start: float, stop: float, num: int) -> List[float]:
    """
    Simple pure-Python linspace implementation.

    Parameters
    ----------
    start : float
        Start value (inclusive).
    stop : float
        Stop value (inclusive).
    num : int
        Number of points to generate. Must be >= 2 for a non-degenerate range.

    Returns
    -------
    List[float]
        List of evenly spaced points between start and stop (inclusive).

    Raises
    ------
    ValueError
        If num < 1.

    Notes
    -----
    - When num == 1, the function simply returns [start].
    - This avoids the need to depend on NumPy for simple grids.
    """
    if num < 1:
        raise ValueError("num must be >= 1.")
    if num == 1:
        return [float(start)]
    step = (stop - start) / float(num - 1)
    return [start + step * i for i in range(num)]


# ---------------------------------------------------------------------------
# Example usage (manual tests only)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # This block is for quick manual verification.
    # It will not run when the module is imported.

    print("=== RAFAELIA_TRIG_CORE self-test ===")

    # 1) Spiral test
    spiral_points = generate_spiral_sqrt3_over_2(
        n_turns=2,
        steps_per_turn=10,
        r0=1.0,
        direction=1,
    )
    print(f"Spiral√3/2: generated {len(spiral_points)} points.")
    print("  First point:", spiral_points[0])
    print("  Last point :", spiral_points[-1])

    # 2) Torus test
    torus_points = torus_grid(R=2.0, r=0.5, n_u=4, n_v=4)
    print(f"ToroidΔπφ: generated {len(torus_points)} points.")
    print("  Sample point:", torus_points[0])

    # 3) Time cycle encoding
    cos_val, sin_val = encode_time_cycle(t=6.0, period=24.0)
    print("Time cycle encoding (t=6, period=24):", cos_val, sin_val)

    # 4) Symbolic frequency encoding
    sin_f, cos_f = encode_time_with_symbolic_frequency(t=0.001, key="963")
    print("Symbolic frequency encoding (t=0.001, key='963'):", sin_f, cos_f)

    print("=== Self-test completed successfully ===")
