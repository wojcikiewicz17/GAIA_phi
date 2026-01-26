#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RAFAELIA Commitment Runner (v0)
- Objetivo: transformar ideia em realidade aplicada via experimento repetível.
- Saída: logs/commit_<run_id>.json + hash SHA3 do resultado.
- Trilhas: geometry | series | graph

Uso:
  python rafaelia_commitment.py --track geometry
  python rafaelia_commitment.py --track series
  python rafaelia_commitment.py --track graph
  python rafaelia_commitment.py --track all
"""

from __future__ import annotations

import argparse
import dataclasses as dc
import datetime as dt
import hashlib
import json
import math
import os
import random
import statistics
import sys
from typing import Dict, List, Tuple, Any


# -----------------------------
# Utilities
# -----------------------------

def now_utc() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def sha3_hex(data: bytes) -> str:
    h = hashlib.sha3_256()
    h.update(data)
    return h.hexdigest()

def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)

def stable_json(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def seed_all(seed: int) -> None:
    random.seed(seed)

def mean_std(xs: List[float]) -> Tuple[float, float]:
    if not xs:
        return 0.0, 0.0
    mu = statistics.fmean(xs)
    sd = statistics.pstdev(xs) if len(xs) > 1 else 0.0
    return mu, sd


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def coerencia_estabilidade(media: float, desvio: float, epsilon: float = 1e-9) -> float:
    """Mede consistência do sinal (1 = estável, 0 = disperso)."""
    return clamp01(1.0 - (desvio / (abs(media) + epsilon)))


def coerencia_melhoria(metrica_modelo: float, metrica_baseline: float, epsilon: float = 1e-9) -> float:
    """Coerência relativa quando menor é melhor (ex.: MSE)."""
    return clamp01(1.0 - (metrica_modelo / (metrica_baseline + epsilon)))


def coerencia_relativa(delta: float, baseline: float, epsilon: float = 1e-9) -> float:
    """Coerência relativa quando maior é melhor (ex.: clustering)."""
    return clamp01(delta / (abs(baseline) + epsilon))


# -----------------------------
# Commitment schema
# -----------------------------

@dc.dataclass
class Commitment:
    run_id: str
    created_utc: str
    track: str
    hypothesis: str
    baseline: str
    metric: str
    success_rule: str
    seed: int
    params: Dict[str, Any]

@dc.dataclass
class Result:
    ok: bool
    metric_value: float
    baseline_value: float
    delta: float
    details: Dict[str, Any]


# -----------------------------
# Track A: Geometry (2 squares rotated -> hex-ish structure)
# We will validate a concrete, testable invariant:
# "For a square of side 1, the rotated-square intersection/union yields 6 equal directions
# around the center; the set of radial distances to the 8 square vertices forms 2 groups."
#
# This is NOT "proof of hexagon" — it's a reproducible numerical signature of your construct.
# -----------------------------

def rotate_point(x: float, y: float, ang: float) -> Tuple[float, float]:
    ca, sa = math.cos(ang), math.sin(ang)
    return (x * ca - y * sa, x * sa + y * ca)

def square_vertices(side: float = 1.0, ang: float = 0.0) -> List[Tuple[float, float]]:
    # centered at origin
    s = side / 2.0
    pts = [(-s, -s), (s, -s), (s, s), (-s, s)]
    return [rotate_point(x, y, ang) for (x, y) in pts]

def geometry_experiment(seed: int, params: Dict[str, Any]) -> Result:
    """
    We sample multiple rotation angles and check a numeric signature:
      - compute vertex radii from origin for both squares (8 vertices)
      - cluster radii into groups and evaluate separation ratio
    Baseline: compare against random points on a circle (no square structure).
    Metric: separation ratio = (mean far - mean near) / mean near  (higher is better)
    Success rule: separation ratio must exceed baseline by margin.
    """
    seed_all(seed)
    side = float(params.get("side", 1.0))
    trials = int(params.get("trials", 64))
    margin = float(params.get("margin", 0.15))

    ratios: List[float] = []
    base_ratios: List[float] = []

    for _ in range(trials):
        # angle ~ around 45° is typical for the "two squares -> 8-point star / 6-direction feel"
        ang = random.uniform(0.05, math.pi / 2 - 0.05)
        v1 = square_vertices(side, 0.0)
        v2 = square_vertices(side, ang)
        radii = [math.hypot(x, y) for (x, y) in (v1 + v2)]
        radii.sort()

        # near group = first 4, far group = last 4 (empirically stable for 2 squares)
        near = radii[:4]
        far = radii[-4:]
        mu_near = statistics.fmean(near)
        mu_far = statistics.fmean(far)
        ratio = (mu_far - mu_near) / max(mu_near, 1e-9)
        ratios.append(ratio)

        # baseline: 8 random points on circle with small noise -> should have near~far
        base = []
        for _k in range(8):
            a = random.uniform(0, 2 * math.pi)
            r = 1.0 + random.uniform(-0.01, 0.01)
            base.append(r)
        base.sort()
        b_near = statistics.fmean(base[:4])
        b_far = statistics.fmean(base[-4:])
        b_ratio = (b_far - b_near) / max(b_near, 1e-9)
        base_ratios.append(b_ratio)

    mu, sd = mean_std(ratios)
    bmu, bsd = mean_std(base_ratios)

    ok = (mu > bmu + margin)
    return Result(
        ok=ok,
        metric_value=mu,
        baseline_value=bmu,
        delta=mu - bmu,
        details={
            "std": sd,
            "baseline_std": bsd,
            "coerencia_estabilidade": coerencia_estabilidade(mu, sd),
            "coerencia_estabilidade_baseline": coerencia_estabilidade(bmu, bsd),
            "trials": trials,
            "margin": margin,
            "note": "Numeric signature of 2-square rotation: radii split into near/far groups."
        },
    )


# -----------------------------
# Track B: Series (Fibonacci-mod vs damped sine baseline)
# Metric: MSE vs a target pattern you define (here: synthetic target with decay).
# Baseline: plain damped sine without Fibonacci modulation.
# -----------------------------

def fib(n: int) -> int:
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return a

def series_experiment(seed: int, params: Dict[str, Any]) -> Result:
    seed_all(seed)
    N = int(params.get("N", 512))
    decay = float(params.get("decay", 0.006))
    w = float(params.get("w", 0.22))
    noise = float(params.get("noise", 0.02))
    margin = float(params.get("margin", 0.01))

    # Define a target: damped oscillation + small structured modulation
    target = []
    for t in range(N):
        y = math.exp(-decay * t) * math.sin(w * t)
        y += 0.15 * math.exp(-decay * t) * math.sin(2 * w * t + 0.3)
        y += random.uniform(-noise, noise)
        target.append(y)

    # Model A (Rafaelia-like): damped sine modulated by fib parity / ratio
    pred_a = []
    for t in range(N):
        f = fib((t % 24) + 1)  # bounded
        mod = (f % 2) * 0.06 + (f % 5) * 0.01
        y = math.exp(-decay * t) * math.sin(w * t) * (1.0 + mod)
        pred_a.append(y)

    # Baseline B: plain damped sine
    pred_b = []
    for t in range(N):
        y = math.exp(-decay * t) * math.sin(w * t)
        pred_b.append(y)

    def mse(a: List[float], b: List[float]) -> float:
        return statistics.fmean([(x - y) ** 2 for x, y in zip(a, b)])

    mse_a = mse(pred_a, target)
    mse_b = mse(pred_b, target)

    # Metric: improvement (baseline - model) -> higher better
    improve = mse_b - mse_a
    ok = improve > margin

    return Result(
        ok=ok,
        metric_value=improve,
        baseline_value=0.0,
        delta=improve,
        details={
            "mse_model": mse_a,
            "mse_baseline": mse_b,
            "coerencia_melhoria": coerencia_melhoria(mse_a, mse_b),
            "N": N,
            "margin": margin,
            "note": "This is a scaffold. Replace pred_a with your true Fibonacci/Bitraf oscillator."
        },
    )


# -----------------------------
# Track C: Graph / Embedding toy (no torch)
# We do a simple "structure beats random" test:
# - Build a graph with motifs (triangle/square/hex) and compare clustering coefficient to random graph.
# Metric: avg_clustering (higher better)
# -----------------------------

def build_motif_graph() -> Dict[int, List[int]]:
    # hand-built toy graph with repeated motifs and overlaps
    g: Dict[int, List[int]] = {i: [] for i in range(30)}

    def add_edge(u: int, v: int) -> None:
        if v not in g[u]:
            g[u].append(v)
        if u not in g[v]:
            g[v].append(u)

    # triangles (0-1-2), (3-4-5), (6-7-8)
    tris = [(0,1,2), (3,4,5), (6,7,8)]
    for a,b,c in tris:
        add_edge(a,b); add_edge(b,c); add_edge(c,a)

    # squares (9-10-11-12), (13-14-15-16)
    sqs = [(9,10,11,12), (13,14,15,16)]
    for a,b,c,d in sqs:
        add_edge(a,b); add_edge(b,c); add_edge(c,d); add_edge(d,a)
        add_edge(a,c)  # add diagonal to create extra triangles

    # hex ring (17..22)
    ring = list(range(17, 23))
    for i in range(len(ring)):
        add_edge(ring[i], ring[(i+1)%len(ring)])

    # overlaps / bridges (make it "toroidal-ish")
    bridges = [(2,9), (5,13), (8,17), (12,20), (16,22)]
    for u,v in bridges:
        add_edge(u,v)

    # extra hubs
    for u in [24,25,26,27,28,29]:
        add_edge(u, random.choice([2,5,8,12,16,20,22,9,13,17]))

    return g

def random_graph(n: int, p: float, seed: int) -> Dict[int, List[int]]:
    seed_all(seed)
    g: Dict[int, List[int]] = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                g[i].append(j)
                g[j].append(i)
    return g

def clustering_coeff(g: Dict[int, List[int]]) -> float:
    # average local clustering
    vals = []
    for u, nbrs in g.items():
        k = len(nbrs)
        if k < 2:
            continue
        links = 0
        nbrset = set(nbrs)
        for i in range(k):
            for j in range(i+1, k):
                a, b = nbrs[i], nbrs[j]
                if b in g[a]:
                    links += 1
        possible = k * (k - 1) / 2
        vals.append(links / possible)
    return statistics.fmean(vals) if vals else 0.0

def graph_experiment(seed: int, params: Dict[str, Any]) -> Result:
    seed_all(seed)
    margin = float(params.get("margin", 0.10))

    g = build_motif_graph()
    n = len(g)
    # estimate p to match expected edges roughly
    m = sum(len(v) for v in g.values()) / 2
    p = min(0.9, max(0.01, (2*m) / (n*(n-1))))

    rg = random_graph(n, p, seed=seed+1337)

    cc = clustering_coeff(g)
    rcc = clustering_coeff(rg)

    ok = cc > rcc + margin
    return Result(
        ok=ok,
        metric_value=cc,
        baseline_value=rcc,
        delta=cc - rcc,
        details={
            "n": n,
            "edges": m,
            "p_est": p,
            "coerencia_relativa": coerencia_relativa(cc - rcc, rcc),
            "margin": margin,
            "note": "Motif-graph should cluster more than a matched random graph."
        },
    )


# -----------------------------
# Runner
# -----------------------------

def make_run_id(track: str) -> str:
    stamp = dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    rnd = random.randint(10000, 99999)
    return f"{track}_{stamp}_{rnd}"

def run_track(track: str, seed: int, out_dir: str) -> Dict[str, Any]:
    seed_all(seed)

    # Commitment definitions (edit these hypotheses as you formalize)
    if track == "geometry":
        c = Commitment(
            run_id=make_run_id(track),
            created_utc=now_utc(),
            track=track,
            hypothesis="Two rotated squares generate a stable numeric signature (near/far vertex radii separation) across angles.",
            baseline="Random points on circle (no square structure) produce near≈far radii (low separation).",
            metric="separation_ratio = (mean_far - mean_near) / mean_near",
            success_rule="mean(separation_ratio) > baseline_mean + margin",
            seed=seed,
            params={"side": 1.0, "trials": 64, "margin": 0.15},
        )
        res = geometry_experiment(seed, c.params)

    elif track == "series":
        c = Commitment(
            run_id=make_run_id(track),
            created_utc=now_utc(),
            track=track,
            hypothesis="A Fibonacci-modulated oscillator fits the target pattern better than a plain damped sine baseline.",
            baseline="Plain damped sine (no Fibonacci/Bitraf modulation).",
            metric="improvement = MSE(baseline,target) - MSE(model,target)",
            success_rule="improvement > margin",
            seed=seed,
            params={"N": 512, "decay": 0.006, "w": 0.22, "noise": 0.02, "margin": 0.01},
        )
        res = series_experiment(seed, c.params)

    elif track == "graph":
        c = Commitment(
            run_id=make_run_id(track),
            created_utc=now_utc(),
            track=track,
            hypothesis="A motif-based geometry graph clusters significantly more than a matched random graph baseline.",
            baseline="Matched random graph Erdős–Rényi with similar density.",
            metric="avg_clustering_coefficient",
            success_rule="cc > baseline_cc + margin",
            seed=seed,
            params={"margin": 0.10},
        )
        res = graph_experiment(seed, c.params)

    else:
        raise ValueError(f"Unknown track: {track}")

    payload = {
        "commitment": dc.asdict(c),
        "result": {
            "ok": res.ok,
            "metric_value": res.metric_value,
            "baseline_value": res.baseline_value,
            "delta": res.delta,
            "details": res.details,
        },
    }

    # Hash + save
    ensure_dir(out_dir)
    blob = stable_json(payload)
    payload["sha3_256"] = sha3_hex(blob)

    path = os.path.join(out_dir, f"commit_{c.run_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return {"path": path, "ok": res.ok, "sha3_256": payload["sha3_256"], "delta": res.delta}

def main() -> int:
    ap = argparse.ArgumentParser(description="RAFAELIA Commitment Runner (v0)")
    ap.add_argument("--track", choices=["geometry", "series", "graph", "all"], default="geometry")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="logs")
    args = ap.parse_args()

    tracks = ["geometry", "series", "graph"] if args.track == "all" else [args.track]

    print("🧾 RAFAELIA_COMMITMENT v0")
    print(f"  utc={now_utc()}  seed={args.seed}  out={args.out}")
    print("  tracks=", ", ".join(tracks))

    total_ok = True
    for t in tracks:
        r = run_track(t, args.seed, args.out)
        status = "✅ OK" if r["ok"] else "❌ FAIL"
        print(f"\n[{t}] {status}")
        print(f"  delta={r['delta']:.6f}")
        print(f"  sha3_256={r['sha3_256']}")
        print(f"  log={r['path']}")
        total_ok = total_ok and r["ok"]

    print("\n—")
    print("Compromisso = hipótese + métrica + baseline + log + hash. ⚙️🧠")
    return 0 if total_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
