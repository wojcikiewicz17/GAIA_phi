#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧾 RAFAELIA_COMMITMENT v0.1
Compromisso = hipótese + métrica + baseline + log + hash.

Tracks:
  - geometry : "2 squares -> hex-like (6-direction) signature"
  - series   : "Fibonacci/phi modulation beats baseline in MSE"
  - graph    : "motif clustering beats random baseline"

Output:
  logs/commit_<track>_<stamp>_<rnd>.json
  sha3_256 printed and stored in log
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
from typing import Any, Dict, List, Tuple


# -------------------------
# utils: time, io, hash
# -------------------------

def now_utc() -> str:
    # ✅ timezone-aware UTC (fixes DeprecationWarning)
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def sha3_256_hex(data: bytes) -> str:
    return hashlib.sha3_256(data).hexdigest()


def mean_std(xs: List[float]) -> Tuple[float, float]:
    if not xs:
        return 0.0, 0.0
    if len(xs) == 1:
        return float(xs[0]), 0.0
    return float(statistics.fmean(xs)), float(statistics.pstdev(xs))


def seed_all(seed: int) -> None:
    random.seed(seed)


def write_json(path: str, obj: Dict[str, Any]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)


def make_run_id(track: str) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    rnd = random.randint(10000, 99999)
    return f"{track}_{stamp}_{rnd}"


# -------------------------
# commitment core
# -------------------------

@dc.dataclass
class Result:
    ok: bool
    metric_value: float
    baseline_value: float
    delta: float
    details: Dict[str, Any]


def build_log(track: str, seed: int, params: Dict[str, Any], res: Result) -> Dict[str, Any]:
    return {
        "schema": "RAFAELIA_COMMITMENT/v0.1",
        "utc": now_utc(),
        "seed": seed,
        "track": track,
        "hypothesis": params.get("hypothesis", ""),
        "metric": params.get("metric", ""),
        "baseline": params.get("baseline", ""),
        "params": params,
        "result": {
            "ok": res.ok,
            "metric_value": res.metric_value,
            "baseline_value": res.baseline_value,
            "delta": res.delta,
            "details": res.details,
        },
        "ethica": {
            "note": "No harmful payloads; evaluation-only. Keep it constructive.",
        },
    }


# -------------------------
# Track: geometry (hex / 6 directions)
# -------------------------

def edge_directions_of_square(ang: float) -> List[float]:
    # Direções de arestas de um quadrado: ang e ang+pi/2 (as outras são paralelas)
    # Representamos direção em [0, pi) pois paralelas contam como mesma direção.
    return [(ang % math.pi), ((ang + math.pi / 2) % math.pi)]


def geometry_experiment(seed: int, params: Dict[str, Any]) -> Result:
    """
    ✅ Novo teste: assinatura "hex-like" a partir de 2 quadrados (um girado).
    Ideia: direções (arestas + diagonais) -> devem se organizar em ~6 direções
    com espaçamento próximo de pi/6 em regimes coerentes.

    Métrica: score = (#direções únicas) + uniformidade_de_espaçamento
    Baseline: mesmos 8 ângulos, mas aleatórios.
    """
    seed_all(seed)
    trials = int(params.get("trials", 64))
    bins = int(params.get("bins", 720))          # resolução angular
    margin = float(params.get("margin", 0.50))   # quanto precisa bater o baseline

    def quantize(theta: float) -> int:
        return int(round((theta % math.pi) / math.pi * (bins - 1)))

    def score_from_angles(thetas: List[float]) -> float:
        q = sorted(set(quantize(t) for t in thetas))
        unique = len(q)

        angs = sorted([(i / (bins - 1)) * math.pi for i in q])
        if len(angs) < 2:
            return float(unique)

        spacings = [angs[i + 1] - angs[i] for i in range(len(angs) - 1)]
        spacings.append((angs[0] + math.pi) - angs[-1])  # circular
        target = math.pi / 6  # 30° (hex)
        err = statistics.fmean([abs(s - target) for s in spacings])
        uniform = max(0.0, 1.0 - (err / target))  # 1 = perfeito
        return unique + uniform

    scores: List[float] = []
    base_scores: List[float] = []

    for _ in range(trials):
        ang = random.uniform(0.01, math.pi / 2 - 0.01)

        # Estruturado: 2 quadrados (0 e ang) + diagonais (ang+pi/4)
        dirs: List[float] = []
        dirs += edge_directions_of_square(0.0)
        dirs += edge_directions_of_square(ang)
        dirs += edge_directions_of_square((0.0 + math.pi / 4) % math.pi)
        dirs += edge_directions_of_square((ang + math.pi / 4) % math.pi)

        scores.append(score_from_angles(dirs))

        # Baseline: 8 ângulos aleatórios
        b = [random.uniform(0.0, math.pi) for _k in range(8)]
        base_scores.append(score_from_angles(b))

    mu, sd = mean_std(scores)
    bmu, bsd = mean_std(base_scores)
    ok = mu > bmu + margin

    return Result(
        ok=ok,
        metric_value=mu,
        baseline_value=bmu,
        delta=mu - bmu,
        details={
            "std": sd,
            "baseline_std": bsd,
            "trials": trials,
            "bins": bins,
            "margin": margin,
            "note": "Signature: structured directions approach hex-like spacing (pi/6).",
        },
    )


# -------------------------
# Track: series (phi/fib phase+freq modulation)
# -------------------------

def fib(n: int) -> int:
    # fib(1)=1, fib(2)=1 ...
    if n <= 2:
        return 1
    a, b = 1, 1
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


def mse(a: List[float], b: List[float]) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    s = 0.0
    for i in range(n):
        d = (a[i] - b[i])
        s += d * d
    return s / n


def series_experiment(seed: int, params: Dict[str, Any]) -> Result:
    """
    ✅ Novo series: baseline = seno amortecido simples
    model A = seno amortecido com modulação de fase + micro-variação de freq por Fibonacci/φ

    Métrica: ganho de MSE (baseline_mse - model_mse)
    Ok se delta > margin (positivo)
    """
    seed_all(seed)
    N = int(params.get("N", 512))
    noise = float(params.get("noise", 0.05))
    decay = float(params.get("decay", 0.006))
    w = float(params.get("w", 0.15))
    margin = float(params.get("margin", 0.001))

    # "realidade observada" (target) = seno amortecido + ruído
    target: List[float] = []
    for t in range(N):
        y = math.exp(-decay * t) * math.sin(w * t)
        y += random.gauss(0.0, noise)
        target.append(y)

    # baseline: o mesmo seno amortecido (sem estrutura)
    baseline_pred: List[float] = []
    for t in range(N):
        baseline_pred.append(math.exp(-decay * t) * math.sin(w * t))

    # model A: fase + micro-freq modulada por Fibonacci/φ  ✅
    pred_a: List[float] = []
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    for t in range(N):
        f = fib((t % 24) + 1)
        phase = (f % 13) / 13.0 * (math.pi / phi)
        w2 = w * (1.0 + ((f % 8) - 4) * 0.002)
        y = math.exp(-decay * t) * math.sin(w2 * t + phase)
        pred_a.append(y)

    b_mse = mse(target, baseline_pred)
    a_mse = mse(target, pred_a)

    # delta positivo significa "melhor que baseline"
    delta = (b_mse - a_mse)
    ok = delta > margin

    return Result(
        ok=ok,
        metric_value=delta,
        baseline_value=0.0,
        delta=delta,
        details={
            "N": N,
            "noise": noise,
            "decay": decay,
            "w": w,
            "baseline_mse": b_mse,
            "model_mse": a_mse,
            "margin": margin,
            "note": "Metric is improvement in MSE vs baseline (positive is better).",
        },
    )


# -------------------------
# Track: graph (motif clustering vs random)
# -------------------------

def make_ring_with_chords(n: int, k: int) -> Dict[int, List[int]]:
    g: Dict[int, List[int]] = {i: [] for i in range(n)}
    def add(u: int, v: int) -> None:
        if v not in g[u]:
            g[u].append(v)
        if u not in g[v]:
            g[v].append(u)

    # ring
    for i in range(n):
        add(i, (i + 1) % n)

    # chords
    for i in range(n):
        add(i, (i + k) % n)
    return g


def make_erdos_renyi(n: int, p: float) -> Dict[int, List[int]]:
    g: Dict[int, List[int]] = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                g[i].append(j)
                g[j].append(i)
    return g


def clustering_coefficient(g: Dict[int, List[int]]) -> float:
    # média do clustering local
    vals: List[float] = []
    for u, nbrs in g.items():
        deg = len(nbrs)
        if deg < 2:
            vals.append(0.0)
            continue
        s = set(nbrs)
        links = 0
        # conta arestas entre vizinhos
        for i in range(deg):
            a = nbrs[i]
            na = g[a]
            for j in range(i + 1, deg):
                b = nbrs[j]
                if b in na:
                    links += 1
        possible = deg * (deg - 1) / 2
        vals.append(links / possible)
    return float(statistics.fmean(vals)) if vals else 0.0


def graph_experiment(seed: int, params: Dict[str, Any]) -> Result:
    """
    Grafo estruturado (anel+cordas) deve ter clustering maior que ER random com p similar.
    Métrica: delta = C_struct - C_random
    """
    seed_all(seed)
    n = int(params.get("n", 94))
    k = int(params.get("k", 7))
    p = float(params.get("p", 0.08))
    margin = float(params.get("margin", 0.10))

    g_struct = make_ring_with_chords(n, k)
    g_rand = make_erdos_renyi(n, p)

    c_struct = clustering_coefficient(g_struct)
    c_rand = clustering_coefficient(g_rand)

    delta = c_struct - c_rand
    ok = delta > margin

    return Result(
        ok=ok,
        metric_value=c_struct,
        baseline_value=c_rand,
        delta=delta,
        details={
            "n": n,
            "k": k,
            "p": p,
            "margin": margin,
            "note": "Metric: clustering(struct) - clustering(random).",
        },
    )


# -------------------------
# dispatch + cli
# -------------------------

TRACKS = {
    "geometry": {
        "fn": geometry_experiment,
        "hypothesis": "2 squares (one rotated) yield a hex-like 6-direction signature.",
        "metric": "unique_directions + spacing_uniformity (target pi/6)",
        "baseline": "same count of angles but random directions",
        "params": {"trials": 64, "bins": 720, "margin": 0.50},
    },
    "series": {
        "fn": series_experiment,
        "hypothesis": "Fibonacci/phi phase+freq modulation yields lower MSE than baseline.",
        "metric": "delta = MSE(baseline) - MSE(model) (positive better)",
        "baseline": "plain damped sine predictor",
        "params": {"N": 512, "noise": 0.05, "decay": 0.006, "w": 0.15, "margin": 0.001},
    },
    "graph": {
        "fn": graph_experiment,
        "hypothesis": "Structured ring+chords graph has higher clustering than random ER graph.",
        "metric": "delta = C_struct - C_random",
        "baseline": "Erdos-Renyi with similar density",
        "params": {"n": 94, "k": 7, "p": 0.08, "margin": 0.10},
    },
}


def run_track(track: str, seed: int, out_dir: str) -> Tuple[Result, str, str]:
    if track not in TRACKS:
        raise ValueError(f"Unknown track: {track}")

    ensure_dir(out_dir)

    spec = TRACKS[track]
    params = dict(spec["params"])
    params["hypothesis"] = spec["hypothesis"]
    params["metric"] = spec["metric"]
    params["baseline"] = spec["baseline"]

    # run
    fn = spec["fn"]
    res: Result = fn(seed, params)

    # log
    run_id = make_run_id(f"commit_{track}")
    log_name = f"{run_id}.json"
    log_path = os.path.join(out_dir, log_name)

    obj = build_log(track, seed, params, res)

    raw = json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
    digest = sha3_256_hex(raw)
    obj["sha3_256"] = digest

    write_json(log_path, obj)

    return res, digest, log_path


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="🧾 RAFAELIA_COMMITMENT v0.1 (hypothesis+metric+baseline+log+hash)")
    ap.add_argument("--track", action="append", default=[], help="geometry | series | graph (can repeat)")
    ap.add_argument("--seed", type=int, default=42, help="RNG seed (default 42)")
    ap.add_argument("--out", type=str, default="logs", help="Output directory (default logs)")
    args = ap.parse_args(argv)

    tracks = args.track or ["geometry", "series", "graph"]

    print("🧾 RAFAELIA_COMMITMENT v0.1")
    print(f"  utc={now_utc()}  seed={args.seed}  out={args.out}")
    print(f"  tracks= {', '.join(tracks)}")

    for t in tracks:
        try:
            res, digest, log_path = run_track(t, args.seed, args.out)

            status = "✅ OK" if res.ok else "❌ FAIL"
            print(f"\n[{t}] {status}")
            print(f"  delta={res.delta:.6f}")
            print(f"  sha3_256={digest}")
            print(f"  log={log_path}")

        except Exception as e:
            print(f"\n[{t}] 💥 ERROR: {e}")
            return 2

    print("\n—\nCompromisso = hipótese + métrica + baseline + log + hash. ⚙️ 🧠")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
