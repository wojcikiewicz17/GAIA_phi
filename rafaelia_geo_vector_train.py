#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RAFAELIA | Geo-Vector Trainer (prototype)
- Fibonacci radii (direct/inverse/reverse)
- Polygons + circle sampling -> vertices/edges
- Invariants (Δ, Σ, H; √2, √3; area/perimeter; symmetry k)
- Torus point-cloud from (R,r) tied to Fibonacci/Δ/Σ
- Graph linking by cosine similarity
- Lightweight geometric embedding training (skip-gram + neg sampling) in NumPy
- Optional plots (matplotlib)

Dependencies: numpy, math, argparse
Optional: matplotlib (for --plot)
"""

import argparse
import math
import random
from dataclasses import dataclass
from typing import List, Tuple, Dict

import numpy as np


# --------------------------
# Core helpers
# --------------------------

def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

def l2norm(v, eps=1e-12):
    return v / (np.linalg.norm(v) + eps)

def cosine(a, b, eps=1e-12):
    return float(np.dot(a, b) / ((np.linalg.norm(a) + eps) * (np.linalg.norm(b) + eps)))

def polygon_area(pts: np.ndarray) -> float:
    # Shoelace formula; pts shape (N,2) closed or open
    x = pts[:, 0]
    y = pts[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

def polygon_perimeter(pts: np.ndarray) -> float:
    d = np.roll(pts, -1, axis=0) - pts
    return float(np.sum(np.linalg.norm(d, axis=1)))

def regular_polygon(k: int, r: float, theta0: float = 0.0) -> np.ndarray:
    # vertices on circle radius r
    ang = theta0 + (2 * math.pi / k) * np.arange(k)
    return np.stack([r * np.cos(ang), r * np.sin(ang)], axis=1).astype(np.float64)

def circle_points(r: float, m: int = 64) -> np.ndarray:
    ang = (2 * math.pi / m) * np.arange(m)
    return np.stack([r * np.cos(ang), r * np.sin(ang)], axis=1).astype(np.float64)

def rotate_pts(pts: np.ndarray, theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    R = np.array([[c, -s], [s, c]], dtype=np.float64)
    return pts @ R.T

def square_points(r: float, theta0: float = 0.0) -> np.ndarray:
    # square as regular polygon k=4 but aligned by theta0
    return regular_polygon(4, r, theta0=theta0)

def bhaskara_pythagoras_invariants(a: float, b: float) -> Tuple[float, float, float]:
    # Δ, Σ, H
    Delta = abs(a - b)
    Sigma = a + b
    H = math.sqrt(a * a + b * b)
    return Delta, Sigma, H


# --------------------------
# Fibonacci radii engine
# --------------------------

def fibonacci(n: int) -> List[int]:
    if n <= 0:
        return []
    if n == 1:
        return [1]
    F = [1, 1]
    while len(F) < n:
        F.append(F[-1] + F[-2])
    return F

def fibonacci_radii(n: int, mode: str = "direct", normalize: str = "max") -> np.ndarray:
    """
    mode: direct | inverse | reverse
    normalize: max | first | none
    """
    F = np.array(fibonacci(n), dtype=np.float64)
    if mode == "direct":
        r = F
    elif mode == "inverse":
        r = 1.0 / F
    elif mode == "reverse":
        r = F[::-1].copy()
    else:
        raise ValueError("mode must be direct|inverse|reverse")

    if normalize == "max":
        r = r / (np.max(r) + 1e-12)
    elif normalize == "first":
        r = r / (r[0] + 1e-12)
    elif normalize == "none":
        pass
    else:
        raise ValueError("normalize must be max|first|none")

    return r


# --------------------------
# Shapes / nodes
# --------------------------

@dataclass
class ShapeNode:
    name: str
    kind: str          # triangle | square | hex | circle | overlap_squares
    k_sym: int         # symmetry order (approx/declared)
    pts2d: np.ndarray  # (N,2) sampled vertices/points
    params: Dict[str, float]
    feat: np.ndarray   # invariant feature vector


def make_overlap_squares(r: float, theta: float) -> np.ndarray:
    """
    Two congruent squares centered at origin. One rotated by theta.
    We just sample boundary points (not exact polygon union/intersection),
    enough for invariants + similarity geometry.
    """
    sq1 = square_points(r, theta0=0.0)
    sq2 = rotate_pts(square_points(r, theta0=0.0), theta)

    # sample edges for both squares
    def sample_edges(poly, m_per_edge=16):
        res = []
        for i in range(len(poly)):
            p = poly[i]
            q = poly[(i + 1) % len(poly)]
            for t in np.linspace(0, 1, m_per_edge, endpoint=False):
                res.append((1 - t) * p + t * q)
        return np.array(res, dtype=np.float64)

    pts = np.vstack([sample_edges(sq1, 16), sample_edges(sq2, 16)])
    return pts


def shape_features(pts: np.ndarray, k_sym: int, extra: Dict[str, float]) -> np.ndarray:
    """
    Build a compact invariant-ish vector:
    [area, perimeter, compactness, k_sym,
     Δ, Σ, H, sqrt2, sqrt3,
     mean_r, std_r]
    """
    # For circle-sampled points, area via polygon approx is OK.
    A = polygon_area(pts)
    P = polygon_perimeter(pts)
    compactness = (4 * math.pi * A) / ((P * P) + 1e-12)  # 1 for perfect circle
    mean_r = float(np.mean(np.linalg.norm(pts, axis=1)))
    std_r = float(np.std(np.linalg.norm(pts, axis=1)))

    a = float(extra.get("a", 1.0))
    b = float(extra.get("b", 1.0))
    Delta, Sigma, H = bhaskara_pythagoras_invariants(a, b)

    v = np.array([
        A, P, compactness,
        float(k_sym),
        Delta, Sigma, H,
        math.sqrt(2.0), math.sqrt(3.0),
        mean_r, std_r
    ], dtype=np.float64)

    # normalize scale-heavy terms a bit (log1p)
    v2 = v.copy()
    for idx in [0, 1, 4, 5, 6, 9, 10]:
        v2[idx] = math.log1p(max(v2[idx], 0.0))
    return v2


# --------------------------
# Torus point cloud (3D)
# --------------------------

def torus_points(R: float, r: float, n_theta: int = 48, n_phi: int = 24) -> np.ndarray:
    theta = np.linspace(0, 2 * math.pi, n_theta, endpoint=False)
    phi = np.linspace(0, 2 * math.pi, n_phi, endpoint=False)
    pts = []
    for th in theta:
        for ph in phi:
            x = (R + r * math.cos(ph)) * math.cos(th)
            y = (R + r * math.cos(ph)) * math.sin(th)
            z = r * math.sin(ph)
            pts.append((x, y, z))
    return np.array(pts, dtype=np.float64)


# --------------------------
# Graph building
# --------------------------

def build_graph(nodes: List[ShapeNode], k_neighbors: int = 4) -> Dict[int, List[int]]:
    feats = np.stack([l2norm(n.feat) for n in nodes], axis=0)
    N = feats.shape[0]
    G = {i: [] for i in range(N)}
    for i in range(N):
        sims = []
        for j in range(N):
            if i == j:
                continue
            sims.append((cosine(feats[i], feats[j]), j))
        sims.sort(reverse=True, key=lambda x: x[0])
        nbrs = [j for _, j in sims[:k_neighbors]]
        G[i] = nbrs
    return G


# --------------------------
# Skip-gram training on graph (numpy)
# --------------------------

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def train_graph_embeddings(
    G: Dict[int, List[int]],
    n_nodes: int,
    dim: int = 24,
    epochs: int = 200,
    lr: float = 0.05,
    neg_k: int = 6,
    seed: int = 42
) -> np.ndarray:
    """
    Classic word2vec-style skip-gram on graph neighborhoods.
    Returns embedding matrix E (n_nodes, dim).
    """
    rng = np.random.default_rng(seed)
    W_in = rng.normal(0, 0.1, size=(n_nodes, dim)).astype(np.float64)
    W_out = rng.normal(0, 0.1, size=(n_nodes, dim)).astype(np.float64)

    nodes = list(range(n_nodes))
    # simple negative sampling distribution: uniform
    for ep in range(epochs):
        random.shuffle(nodes)
        loss_ep = 0.0
        for u in nodes:
            u_vec = W_in[u]
            for v in G[u]:
                # positive
                score_pos = np.dot(u_vec, W_out[v])
                p_pos = sigmoid(score_pos)
                loss_ep += -math.log(p_pos + 1e-12)

                grad = (p_pos - 1.0)  # d/dscore of -log(sigmoid)
                W_out[v] -= lr * grad * u_vec
                u_vec -= lr * grad * W_out[v]

                # negatives
                for _ in range(neg_k):
                    neg = rng.integers(0, n_nodes)
                    if neg == v or neg == u:
                        continue
                    score_neg = np.dot(u_vec, W_out[neg])
                    p_neg = sigmoid(score_neg)
                    loss_ep += -math.log(1.0 - p_neg + 1e-12)

                    gradn = p_neg  # d/dscore of -log(1-sigmoid)=sigmoid
                    W_out[neg] -= lr * gradn * u_vec
                    u_vec -= lr * gradn * W_out[neg]

            W_in[u] = u_vec

        # tiny anneal
        if (ep + 1) % 50 == 0:
            lr *= 0.85
            # print sparse progress
            print(f"[train] epoch {ep+1}/{epochs} loss~{loss_ep:.3f} lr={lr:.4f}")

    E = (W_in + W_out) / 2.0
    return E


# --------------------------
# Dataset assembly
# --------------------------

def build_nodes(n_radii: int = 12) -> Tuple[List[ShapeNode], np.ndarray, np.ndarray]:
    """
    Returns (nodes, torus_pts, torus_params_vector)
    """
    # radii banks
    r_dir = fibonacci_radii(n_radii, mode="direct", normalize="max")
    r_inv = fibonacci_radii(n_radii, mode="inverse", normalize="max")
    r_rev = fibonacci_radii(n_radii, mode="reverse", normalize="max")

    nodes: List[ShapeNode] = []

    # Basic families: triangle/square/hex/circle using different radii modes
    families = [
        ("triangle", 3, 3),
        ("square",   4, 4),
        ("hex",      6, 6),
    ]

    # couple of (a,b) catetos to inject Δ/Σ/H variation
    catetos = [(3,4), (5,12), (7,9), (9,9), (8,15)]

    # create multiple variants per family
    for idx, (kind, k, ksym) in enumerate(families):
        for t, (a, b) in enumerate(catetos[:4]):
            r = float(0.35 + 0.6 * r_dir[(idx + t) % n_radii])
            theta0 = (t * math.pi) / (k * 2)
            pts = regular_polygon(k, r, theta0=theta0)
            feat = shape_features(pts, ksym, {"a": a, "b": b})
            nodes.append(ShapeNode(
                name=f"{kind}_dir_{t}",
                kind=kind,
                k_sym=ksym,
                pts2d=pts,
                params={"r": r, "theta0": theta0, "a": a, "b": b},
                feat=feat
            ))

        # inverse variants (tighter core)
        for t, (a, b) in enumerate(catetos[1:5]):
            r = float(0.25 + 0.75 * r_inv[(idx + t) % n_radii])
            theta0 = (t * math.pi) / (k)
            pts = regular_polygon(k, r, theta0=theta0)
            feat = shape_features(pts, ksym, {"a": a, "b": b})
            nodes.append(ShapeNode(
                name=f"{kind}_inv_{t}",
                kind=kind,
                k_sym=ksym,
                pts2d=pts,
                params={"r": r, "theta0": theta0, "a": a, "b": b},
                feat=feat
            ))

    # circle variants
    for t, (a, b) in enumerate(catetos):
        r = float(0.3 + 0.7 * r_rev[t % n_radii])
        pts = circle_points(r, m=72)
        feat = shape_features(pts, k_sym=0, extra={"a": a, "b": b})
        nodes.append(ShapeNode(
            name=f"circle_rev_{t}",
            kind="circle",
            k_sym=0,
            pts2d=pts,
            params={"r": r, "a": a, "b": b},
            feat=feat
        ))

    # Overlapped squares (your “hex + 6 tri” vibe) – sampled boundary points
    thetas = [math.pi/12, math.pi/10, math.pi/8, math.pi/6, math.pi/5, math.pi/4]
    for i, th in enumerate(thetas):
        r = float(0.25 + 0.7 * r_dir[(i * 2) % n_radii])
        pts = make_overlap_squares(r, th)
        # k_sym is "emergent" – not exact; treat as 2 or 4 depending on angle.
        ksym = 2 if abs(th - math.pi/4) > 1e-6 else 4
        feat = shape_features(pts, k_sym=ksym, extra={"a": 5 + i, "b": 8 + i})
        nodes.append(ShapeNode(
            name=f"overlap_sq_{i}",
            kind="overlap_squares",
            k_sym=ksym,
            pts2d=pts,
            params={"r": r, "theta": th},
            feat=feat
        ))

    # Torus parameters from Δ/Σ + Fibonacci (one clean choice)
    # Choose a,b from a stable triangle (3,4) and mix with fibonacci
    a, b = 3.0, 4.0
    Delta, Sigma, H = bhaskara_pythagoras_invariants(a, b)
    # normalize radii to keep torus sane
    R = float((Sigma / 2.0) * (0.8 + 0.4 * r_dir[3]))   # "energia" orbita
    r = float((Delta / 2.0) * (0.8 + 0.4 * r_inv[5]))   # "diferença" tubo

    tor_pts = torus_points(R, r, n_theta=64, n_phi=28)
    tor_param_vec = np.array([R, r, Delta, Sigma, H, math.sqrt(2), math.sqrt(3)], dtype=np.float64)

    return nodes, tor_pts, tor_param_vec


# --------------------------
# Main
# --------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dim", type=int, default=24, help="embedding dimension")
    ap.add_argument("--epochs", type=int, default=250, help="training epochs")
    ap.add_argument("--lr", type=float, default=0.05, help="learning rate")
    ap.add_argument("--knn", type=int, default=5, help="graph neighbors per node")
    ap.add_argument("--neg", type=int, default=6, help="negative samples")
    ap.add_argument("--seed", type=int, default=42, help="random seed")
    ap.add_argument("--plot", action="store_true", help="plot 2D shapes + torus cloud")
    args = ap.parse_args()

    nodes, tor_pts, tor_param_vec = build_nodes(n_radii=12)

    # feature matrix & graph
    F = np.stack([l2norm(n.feat) for n in nodes], axis=0)
    G = build_graph(nodes, k_neighbors=args.knn)

    print(f"[data] nodes={len(nodes)} feat_dim={F.shape[1]} torus_pts={tor_pts.shape[0]}")
    print(f"[torus] R={tor_param_vec[0]:.4f} r={tor_param_vec[1]:.4f} Δ={tor_param_vec[2]:.4f} Σ={tor_param_vec[3]:.4f} H={tor_param_vec[4]:.4f}")

    # train embeddings on graph neighborhoods
    E = train_graph_embeddings(
        G=G,
        n_nodes=len(nodes),
        dim=args.dim,
        epochs=args.epochs,
        lr=args.lr,
        neg_k=args.neg,
        seed=args.seed
    )

    # show nearest neighbors in learned embedding space
    E_n = np.stack([l2norm(e) for e in E], axis=0)
    print("\n[NN] nearest neighbors by embedding cosine:")
    for i in range(min(10, len(nodes))):
        sims = []
        for j in range(len(nodes)):
            if i == j:
                continue
            sims.append((cosine(E_n[i], E_n[j]), j))
        sims.sort(reverse=True, key=lambda x: x[0])
        top = sims[:5]
        line = ", ".join([f"{nodes[j].name}({s:.2f})" for s, j in top])
        print(f"  {nodes[i].name:>16} -> {line}")

    # optional plot
    if args.plot:
        try:
            import matplotlib.pyplot as plt
            from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

            # Plot a few 2D shapes
            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.set_title("2D shapes (samples)")

            picks = [0, 5, 10, 16, 22, 30, len(nodes)-1]
            for idx in picks:
                pts = nodes[idx].pts2d
                ax.plot(np.r_[pts[:,0], pts[0,0]], np.r_[pts[:,1], pts[0,1]], linewidth=1)
                ax.text(pts[0,0], pts[0,1], nodes[idx].kind, fontsize=8)

            ax.set_aspect('equal', adjustable='box')

            # Plot torus cloud
            fig2 = plt.figure()
            ax3 = fig2.add_subplot(111, projection='3d')
            ax3.set_title("Torus point cloud (R,r from Δ/Σ + Fibonacci)")
            ax3.scatter(tor_pts[:,0], tor_pts[:,1], tor_pts[:,2], s=2)

            plt.show()
        except Exception as e:
            print(f"[plot] matplotlib not available or failed: {e}")

if __name__ == "__main__":
    main()
