#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
COGNITIO_GEOMETRICA.py
Sistema unificado de:
geometria ⊕ recorrência ⊕ percepção ⊕ campo ⊕ decisão

Compatível com Termux / Linux / Python 3.9+
Requer: numpy, pillow, matplotlib
"""

import argparse
import math
import os

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# =========================
# UTILIDADES BÁSICAS
# =========================

def ensure(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def save(arr: np.ndarray, path: str) -> None:
    Image.fromarray(arr).save(path)


def u8(x: np.ndarray) -> np.ndarray:
    return np.clip(x * 255, 0, 255).astype(np.uint8)


# =========================
# RECORRÊNCIAS
# =========================

def fibonacci(n: int) -> list[int]:
    f = [0, 1]
    for _ in range(2, n):
        f.append(f[-1] + f[-2])
    return f[:n]


def tribonacci(n: int) -> list[int]:
    t = [0, 0, 1]
    for _ in range(3, n):
        t.append(t[-1] + t[-2] + t[-3])
    return t[:n]


# =========================
# MÉTRICA
# =========================

def pythagoras(a: float, b: float) -> tuple[float, float, float, float]:
    c = math.sqrt(a * a + b * b)
    return a, b, c, abs(a - b)


# =========================
# GEOMETRIA (MÁSCARAS)
# =========================

def polygon(n: int, size: int = 512, r: float = 0.8) -> np.ndarray:
    h = w = size
    cx = cy = size // 2
    y, x = np.ogrid[:h, :w]
    x = (x - cx) / cx
    y = (y - cy) / cy

    mask = np.zeros((h, w))
    for i in range(n):
        th1 = 2 * math.pi * i / n
        th2 = 2 * math.pi * (i + 1) / n
        x1, y1 = r * math.cos(th1), r * math.sin(th1)
        x2, y2 = r * math.cos(th2), r * math.sin(th2)
        a = y2 - y1
        b = x1 - x2
        c = a * x1 + b * y1
        mask += (a * x + b * y) <= c
    return (mask == n).astype(float)


def circle(size: int = 512, r: float = 0.9) -> np.ndarray:
    cx = cy = size // 2
    y, x = np.ogrid[:size, :size]
    x = (x - cx) / cx
    y = (y - cy) / cy
    return ((x * x + y * y) <= r * r).astype(float)


# =========================
# MANDELBROT
# =========================

def mandelbrot(size: int = 512, max_iter: int = 200) -> np.ndarray:
    x = np.linspace(-2, 1, size)
    y = np.linspace(-1.5, 1.5, size)
    c = x[None, :] + 1j * y[:, None]
    z = np.zeros_like(c)
    m = np.zeros(c.shape)

    for i in range(max_iter):
        mask = np.abs(z) <= 2
        z[mask] = z[mask] ** 2 + c[mask]
        m[mask] = i
    return m / max_iter


# =========================
# PERCEPÇÃO / SIMETRIA
# =========================

def symmetry_score(img: np.ndarray) -> float:
    flip_h = np.fliplr(img)
    flip_v = np.flipud(img)
    return 1.0 - (np.mean(np.abs(img - flip_h)) + np.mean(np.abs(img - flip_v))) / 2


def wall_sample(img: np.ndarray, steps: int = 42) -> np.ndarray:
    h, w = img.shape
    cx, cy = w // 2, h // 2
    r = min(cx, cy) * 0.95
    vals = []
    for i in range(steps):
        th = 2 * math.pi * i / steps
        x = int(cx + r * math.cos(th))
        y = int(cy + r * math.sin(th))
        vals.append(img[y, x])
    return np.array(vals)


# =========================
# ESCOLHA COGNITIVA
# =========================

def cognitive_choice(img: np.ndarray) -> tuple[list[float], int]:
    variants = [
        img,
        np.clip(img * 0.9, 0, 1),
        np.clip(img * 1.1, 0, 1),
    ]

    scores = []
    for v in variants:
        s = symmetry_score(v)
        w = wall_sample(v)
        stab = math.exp(-np.var(w))
        scores.append(0.6 * s + 0.4 * stab)

    return scores, int(np.argmax(scores))


# =========================
# PIPELINE
# =========================

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--steps", type=int, default=42)
    args = ap.parse_args()

    ensure(args.out)

    # Recorrências
    fib = fibonacci(20)
    tri = tribonacci(20)

    with open(f"{args.out}/recorrencia.txt", "w", encoding="utf-8") as f:
        f.write("Fibonacci:\n" + str(fib) + "\n\n")
        f.write("Tribonacci:\n" + str(tri))

    # Geometria
    shapes = {
        "tri": polygon(3, args.size),
        "square": polygon(4, args.size),
        "pent": polygon(5, args.size),
        "hex": polygon(6, args.size),
        "oct": polygon(8, args.size),
        "circle": circle(args.size),
    }

    for k, v in shapes.items():
        save(u8(v), f"{args.out}/{k}.png")

    overlay = np.maximum.reduce(list(shapes.values()))
    save(u8(overlay), f"{args.out}/overlay.png")

    # Mandelbrot
    mb = mandelbrot(args.size)
    save(u8(mb), f"{args.out}/mandelbrot.png")

    # Campo combinado
    field = (overlay + mb) / 2
    save(u8(field), f"{args.out}/field.png")

    # Análise perceptiva
    sym = symmetry_score(field)
    wall = wall_sample(field, args.steps)
    scores, winner = cognitive_choice(field)

    with open(f"{args.out}/analysis.txt", "w", encoding="utf-8") as f:
        f.write(f"Symmetry: {sym}\n")
        f.write(f"Wall variance: {np.var(wall)}\n")
        f.write(f"Choice scores: {scores}\n")
        f.write(f"Best index: {winner}\n")

    print(f"[OK] Sistema gerado em {args.out}")


if __name__ == "__main__":
    main()
