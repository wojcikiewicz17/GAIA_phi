#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RAFAELIA | Geo-Vector Trainer v2 (hex/tri from rotated squares)
- Shapes: triangle/square/hex/circle + overlap squares
- NEW: exact convex intersection polygon of two squares (can be hex or octagon, etc.)
- NEW: triangulation fan -> explicit triangles (hex => 6 triangles)
- Invariants feat_dim=11
- Torus point-cloud + graph kNN + skip-gram neg-sampling embeddings (NumPy)
"""

import argparse, math, random
from dataclasses import dataclass
from typing import List, Tuple, Dict
import numpy as np


# --------------------------
# Basics
# --------------------------

def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    na = np.linalg.norm(a) + 1e-12
    nb = np.linalg.norm(b) + 1e-12
    return float(np.dot(a, b) / (na * nb))

def rotate_pts(pts: np.ndarray, theta: float) -> np.ndarray:
    c, s = math.cos(theta), math.sin(theta)
    R = np.array([[c, -s], [s, c]], dtype=np.float64)
    return pts @ R.T

def regular_polygon(k: int, r: float, theta0: float = 0.0) -> np.ndarray:
    ang = theta0 + (2 * math.pi / k) * np.arange(k)
    return np.stack([r * np.cos(ang), r * np.sin(ang)], axis=1).astype(np.float64)

def square_points(r: float, theta0: float = 0.0) -> np.ndarray:
    return regular_polygon(4, r, theta0=theta0)

def circle_points(r: float, m: int = 72) -> np.ndarray:
    ang = (2 * math.pi / m) * np.arange(m)
    return np.stack([r * np.cos(ang), r * np.sin(ang)], axis=1).astype(np.float64)

def polygon_area(P: np.ndarray) -> float:
    x, y = P[:, 0], P[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

def polygon_perimeter(P: np.ndarray) -> float:
    Q = np.roll(P, -1, axis=0)
    return float(np.sum(np.linalg.norm(Q - P, axis=1)))

def centroid(P: np.ndarray) -> np.ndarray:
    return np.mean(P, axis=0)

def bhaskara_pythagoras_invariants(a: float, b: float) -> Tuple[float, float, float]:
    Delta = abs(a - b)
    Sigma = a + b
    H = math.sqrt(a * a + b * b)
    return Delta, Sigma, H


# --------------------------
# Convex polygon clipping (Sutherland–Hodgman)
# --------------------------

def _is_left(a, b, p) -> float:
    # cross((b-a),(p-a))
    return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])

def _line_intersect(a, b, p, q) -> np.ndarray:
    # intersection of segments (a->b) and (p->q) for clipping (as lines)
    ax, ay = a; bx, by = b
    px, py = p; qx, qy = q
    r = np.array([bx-ax, by-ay], dtype=np.float64)
    s = np.array([qx-px, qy-py], dtype=np.float64)
    denom = r[0]*s[1] - r[1]*s[0]
    if abs(denom) < 1e-12:
        return np.array([bx, by], dtype=np.float64)  # fallback (parallel)
    t = ((px-ax)*s[1] - (py-ay)*s[0]) / denom
    return np.array([ax + t*r[0], ay + t*r[1]], dtype=np.float64)

def convex_clip(subject: np.ndarray, clipper: np.ndarray) -> np.ndarray:
    """
    Clip a convex polygon (subject) by another convex polygon (clipper).
    Both must be CCW. Returns CCW polygon (possibly empty).
    """
    out = subject.copy()
    for i in range(len(clipper)):
        A = clipper[i]
        B = clipper[(i+1) % len(clipper)]
        inp = out
        if len(inp) == 0:
            return inp
        out_list = []
        S = inp[-1]
        for E in inp:
            Ein = _is_left(A, B, E) >= 0
            Sin = _is_left(A, B, S) >= 0
            if Ein:
                if not Sin:
                    out_list.append(_line_intersect(S, E, A, B))
                out_list.append(E)
            elif Sin:
                out_list.append(_line_intersect(S, E, A, B))
            S = E
        out = np.array(out_list, dtype=np.float64)
    return out

def ensure_ccw(P: np.ndarray) -> np.ndarray:
    # signed area
    x, y = P[:,0], P[:,1]
    s = 0.5*(np.dot(x, np.roll(y,-1)) - np.dot(y, np.roll(x,-1)))
    return P if s >= 0 else P[::-1].copy()

def triangulate_fan(P: np.ndarray) -> List[np.ndarray]:
    """
    Fan triangulation around centroid: returns list of triangles (3x2).
    For a convex n-gon, yields n triangles if you include centroid as hub.
    Hex => 6 triangles.
    """
    if len(P) < 3:
        return []
    c = centroid(P)
    tris = []
    for i in range(len(P)):
        a = P[i]
        b = P[(i+1) % len(P)]
        tris.append(np.stack([c, a, b], axis=0))
    return tris


# --------------------------
# Features (feat_dim=11)
# --------------------------

def shape_features(pts: np.ndarray, k_sym: int, extra: Dict[str, float]) -> np.ndarray:
    """
    [area, perimeter, compactness, k_sym,
     Δ, Σ, H, sqrt2, sqrt3,
     mean_r, std_r]
    """
    P = pts
    a = polygon_area(P)
    p = polygon_perimeter(P)
    compact = (4 * math.pi * a / (p * p + 1e-12)) if p > 0 else 0.0

    c = centroid(P)
    radii = np.linalg.norm(P - c, axis=1)
    mean_r = float(np.mean(radii))
    std_r = float(np.std(radii))

    Delta = float(extra.get("Delta", 0.0))
    Sigma = float(extra.get("Sigma", 0.0))
    H = float(extra.get("H", 0.0))

    v = np.array([
        a, p, compact, float(k_sym),
        Delta, Sigma, H,
        math.sqrt(2.0), math.sqrt(3.0),
        mean_r, std_r
    ], dtype=np.float64)

    v2 = v.copy()
    for idx in [0, 1, 4, 5, 6, 9, 10]:
        v2[idx] = math.log1p(max(v2[idx], 0.0))
    return v2


# --------------------------
# Fibonacci radii
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

def radii_bank(n: int = 12) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    F = np.array(fibonacci(n + 2), dtype=np.float64)
    F = F[2:]  # drop first two 1s
    F = F / (F.max() + 1e-12)
    direct = F
    inv = 1.0 / (F + 1e-9)
    inv = inv / inv.max()
    rev = direct[::-1].copy()
    return direct, inv, rev


# --------------------------
# Torus
# --------------------------

def torus_points(R: float, r: float, n_theta: int = 56, n_phi: int = 32) -> np.ndarray:
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
# Graph + Embedding
# --------------------------

def build_knn_graph(feats: np.ndarray, k_neighbors: int = 6) -> Dict[int, List[int]]:
    G: Dict[int, List[int]] = {}
    n = feats.shape[0]
    for i in range(n):
        sims = []
        for j in range(n):
            if i == j:
                continue
            sims.append((cosine(feats[i], feats[j]), j))
        sims.sort(reverse=True, key=lambda x: x[0])
        G[i] = [j for _, j in sims[:k_neighbors]]
    return G

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def train_graph_embeddings(
    G: Dict[int, List[int]],
    dim: int = 16,
    epochs: int = 250,
    lr: float = 0.03,
    neg_k: int = 6,
    seed: int = 42,
    verbose: bool = True
) -> np.ndarray:
    random.seed(seed)
    np.random.seed(seed)

    nodes = sorted(G.keys())
    n = len(nodes)

    W_in = 0.01 * np.random.randn(n, dim).astype(np.float64)
    W_out = 0.01 * np.random.randn(n, dim).astype(np.float64)

    all_idx = list(range(n))

    for ep in range(epochs):
        loss_ep = 0.0
        random.shuffle(nodes)
        for u in nodes:
            u_vec = W_in[u].copy()
            for v in G[u]:
                score = np.dot(u_vec, W_out[v])
                p = sigmoid(score)
                loss_ep += -math.log(p + 1e-12)

                grad = (p - 1.0)
                W_out[v] -= lr * grad * u_vec
                u_vec -= lr * grad * W_out[v]

                for _ in range(neg_k):
                    neg = random.choice(all_idx)
                    if neg == v or neg == u:
                        continue
                    score_neg = np.dot(u_vec, W_out[neg])
                    p_neg = sigmoid(score_neg)
                    loss_ep += -math.log(1.0 - p_neg + 1e-12)

                    gradn = p_neg
                    W_out[neg] -= lr * gradn * u_vec
                    u_vec -= lr * gradn * W_out[neg]

            W_in[u] = u_vec

        if (ep + 1) % 50 == 0:
            lr *= 0.85
            if verbose:
                print(f"[train] epoch {ep+1}/{epochs} loss~{loss_ep:.3f} lr={lr:.4f}")

    return (W_in + W_out) / 2.0


# --------------------------
# Nodes
# --------------------------

@dataclass
class ShapeNode:
    name: str
    kind: str
    k_sym: int
    pts2d: np.ndarray
    params: Dict[str, float]
    feat: np.ndarray

def build_nodes(n_radii: int = 12) -> Tuple[List[ShapeNode], np.ndarray, np.ndarray]:
    direct, inv, rev = radii_bank(n_radii)

    # "catetos" base (pode trocar por sua tabela depois)
    catetos = [(1,1), (1,2), (2,3), (3,5), (5,8), (8,13), (13,21)]
    nodes: List[ShapeNode] = []

    # base shapes
    base = [
        ("triangle", 3),
        ("square", 4),
        ("hex", 6),
    ]

    # triangle/square/hex variants
    for kind, k in base:
        for t, (a, b) in enumerate(catetos):
            Delta, Sigma, H = bhaskara_pythagoras_invariants(float(a), float(b))
            r = float(0.4 + 0.9 * direct[t % n_radii])
            theta0 = (t % k) * (math.pi / k)
            pts = regular_polygon(k, r, theta0=theta0)
            feat = shape_features(pts, k_sym=k, extra={"Delta": Delta, "Sigma": Sigma, "H": H})
            nodes.append(ShapeNode(
                name=f"{kind}_dir_{t}",
                kind=kind,
                k_sym=k,
                pts2d=pts,
                params={"r": r, "theta0": theta0, "a": a, "b": b},
                feat=feat
            ))

            # inverse variant
            r2 = float(0.4 + 0.9 * inv[t % n_radii])
            pts2 = regular_polygon(k, r2, theta0=-theta0)
            feat2 = shape_features(pts2, k_sym=k, extra={"Delta": Delta, "Sigma": Sigma, "H": H})
            nodes.append(ShapeNode(
                name=f"{kind}_inv_{t}",
                kind=kind,
                k_sym=k,
                pts2d=pts2,
                params={"r": r2, "theta0": -theta0, "a": a, "b": b},
                feat=feat2
            ))

    # circle variants
    for t, (a, b) in enumerate(catetos):
        Delta, Sigma, H = bhaskara_pythagoras_invariants(float(a), float(b))
        r = float(0.3 + 0.7 * rev[t % n_radii])
        pts = circle_points(r, m=72)
        feat = shape_features(pts, k_sym=0, extra={"Delta": Delta, "Sigma": Sigma, "H": H})
        nodes.append(ShapeNode(
            name=f"circle_rev_{t}",
            kind="circle",
            k_sym=0,
            pts2d=pts,
            params={"r": r, "a": a, "b": b},
            feat=feat
        ))

    # overlap squares -> exact intersection polygon + triangles
    for t, (a, b) in enumerate(catetos[:5]):
        Delta, Sigma, H = bhaskara_pythagoras_invariants(float(a), float(b))

        r = float(0.6 + 0.9 * direct[t % n_radii])
        sq1 = ensure_ccw(square_points(r, theta0=0.0))
        # giro (você controla: π/12, π/10, π/8, etc.)
        theta = (t + 1) * (math.pi / 12.0)
        sq2 = ensure_ccw(square_points(r, theta0=theta))

        inter = convex_clip(sq1, sq2)
        if len(inter) >= 3:
            inter = ensure_ccw(inter)
            nV = len(inter)
            kind = "hex_from_sq" if nV == 6 else f"poly{nV}_from_sq"
            feat = shape_features(inter, k_sym=nV, extra={"Delta": Delta, "Sigma": Sigma, "H": H})
            nodes.append(ShapeNode(
                name=f"{kind}_{t}",
                kind=kind,
                k_sym=nV,
                pts2d=inter,
                params={"r": r, "theta": theta, "a": a, "b": b},
                feat=feat
            ))

            tris = triangulate_fan(inter)
            # hex => 6 triangles
            for i, tri in enumerate(tris):
                ftri = shape_features(tri, k_sym=3, extra={"Delta": Delta, "Sigma": Sigma, "H": H})
                nodes.append(ShapeNode(
                    name=f"tri_from_{kind}_{t}_{i}",
                    kind="triangle_from_poly",
                    k_sym=3,
                    pts2d=tri,
                    params={"src": t, "i": i},
                    feat=ftri
                ))

    feats = np.stack([n.feat for n in nodes], axis=0)

    # torus params tied to mean Δ/Σ/H
    Dm = float(np.mean(feats[:, 4]))
    Sm = float(np.mean(feats[:, 5]))
    Hm = float(np.mean(feats[:, 6]))
    R = 1.5 + Dm
    r_minor = 0.2 + 0.4 * clamp(Hm / (Sm + 1e-9), 0.0, 1.0)
    tor = torus_points(R=R, r=r_minor, n_theta=56, n_phi=32)

    tor_params = np.array([R, r_minor, Dm, Sm, Hm], dtype=np.float64)
    return nodes, tor, tor_params


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plot", action="store_true", help="matplotlib plots")
    ap.add_argument("--epochs", type=int, default=250)
    ap.add_argument("--dim", type=int, default=16)
    ap.add_argument("--lr", type=float, default=0.03)
    ap.add_argument("--k", type=int, default=6, help="kNN neighbors")
    args = ap.parse_args()

    nodes, tor, torp = build_nodes()
    feats = np.stack([n.feat for n in nodes], axis=0)

    print(f"[data] nodes={len(nodes)} feat_dim={feats.shape[1]} torus_pts={len(tor)}")
    print(f"[torus] R={torp[0]:.4f} r={torp[1]:.4f} Δ={torp[2]:.4f} Σ={torp[3]:.4f} H={torp[4]:.4f}")

    G = build_knn_graph(feats, k_neighbors=args.k)
    E = train_graph_embeddings(G, dim=args.dim, epochs=args.epochs, lr=args.lr, neg_k=6, seed=42, verbose=True)

    # nearest neighbors by embedding cosine
    print("\n[NN] nearest neighbors by embedding cosine:")
    for i, n in enumerate(nodes[:12]):
        sims = []
        for j in range(len(nodes)):
            if i == j:
                continue
            sims.append((cosine(E[i], E[j]), j))
        sims.sort(reverse=True, key=lambda x: x[0])
        top = sims[:5]
        msg = ", ".join([f"{nodes[j].name}({s:.2f})" for s, j in top])
        print(f"    {n.name} -> {msg}")

    if args.plot:
        import matplotlib.pyplot as plt

        # plot some shapes
        plt.figure()
        for idx in range(min(10, len(nodes))):
            P = nodes[idx].pts2d
            Q = np.vstack([P, P[:1]])
            plt.plot(Q[:,0], Q[:,1], linewidth=1)
        plt.axis("equal")
        plt.title("RAFAELIA shapes (first 10)")
        plt.show()

        # plot torus cloud
        from mpl_toolkits.mplot3d import Axes3D  # noqa
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(tor[:,0], tor[:,1], tor[:,2], s=2)
        ax.set_title("Torus point cloud")
        plt.show()


if __name__ == "__main__":
    main()
