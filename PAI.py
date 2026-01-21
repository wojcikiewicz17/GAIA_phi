#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PAI.py — Núcleo Unificador (Formas ⊕ Pitágoras ⊕ Fibonacci/Tribonacci ⊕ Mandelbrot ⊕ Ciclos/42 ⊕ Projeções)
Autor: Rafael (integração assistida)
Licença: uso livre para estudo/experimento

Dependências:
  pip install numpy pillow matplotlib

Exemplos:
  python PAI.py --out out_run --mandelbrot --shapes --cycle42 --bases 10 7 14 60 20 18 13
  python PAI.py --out out_choice --choice3 --img ./minha.jpg --steps 42
"""

import argparse
import math
import os
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt


# -------------------------
# Utilidades básicas
# -------------------------

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def save_png(arr_u8: np.ndarray, path: str) -> None:
    Image.fromarray(arr_u8).save(path)


def clamp01(x: np.ndarray) -> np.ndarray:
    return np.clip(x, 0.0, 1.0)


def to_u8(x01: np.ndarray) -> np.ndarray:
    return (clamp01(x01) * 255.0 + 0.5).astype(np.uint8)


def rgb_to_gray01(rgb_u8: np.ndarray) -> np.ndarray:
    # luminância simples
    r = rgb_u8[..., 0].astype(np.float32) / 255.0
    g = rgb_u8[..., 1].astype(np.float32) / 255.0
    b = rgb_u8[..., 2].astype(np.float32) / 255.0
    return 0.299 * r + 0.587 * g + 0.114 * b


# -------------------------
# Base numérica (sem régua)
# -------------------------

_DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def to_base_general(n: int, base: int) -> str:
    """
    Converte inteiro para base:
      - 2..36: usa 0-9A-Z
      - 37..256: usa representação em colchetes [d0,d1,...] (dígitos numéricos)
      - 60: usa sexagesimal com separador ':' (ex: 1:05:23)
    """
    if base < 2 or base > 256:
        raise ValueError("base fora do intervalo suportado (2..256)")

    if n == 0:
        return "0"

    sign = "-" if n < 0 else ""
    n = abs(n)

    # Base 60: formato sexagesimal (como tempo)
    if base == 60:
        digs = []
        while n > 0:
            n, r = divmod(n, 60)
            digs.append(r)
        digs = list(reversed(digs))
        # primeira sem zero-padding, resto com 2 dígitos (00..59)
        out = [str(digs[0])] + [f"{d:02d}" for d in digs[1:]]
        return sign + ":".join(out)

    # Bases 2..36: alfabeto compacto
    if base <= len(_DIGITS):
        out = []
        while n > 0:
            n, r = divmod(n, base)
            out.append(_DIGITS[r])
        return sign + "".join(reversed(out))

    # Bases 37..256: dígitos numéricos (lista)
    digs = []
    while n > 0:
        n, r = divmod(n, base)
        digs.append(r)
    digs = list(reversed(digs))
    return sign + "[" + ",".join(map(str, digs)) + "]"


def explain_bases(values: List[int], bases: List[int]) -> str:
    lines = []
    for v in values:
        lines.append(f"v={v}")
        for b in bases:
            lines.append(f"  base {b:>3}: {to_base_general(v, b)}")
    return "\n".join(lines)


# -------------------------
# Fibonacci (n-2) e Tribonacci (n-3)
# -------------------------

def fibonacci(n: int) -> List[int]:
    if n <= 0:
        return []
    if n == 1:
        return [0]
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]


def tribonacci(n: int) -> List[int]:
    if n <= 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 0]
    seq = [0, 0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2] + seq[-3])
    return seq[:n]


# -------------------------
# Pitágoras / diagonais (√2, √3)
# -------------------------

@dataclass
class PythagorasReport:
    a: float
    b: float
    c: float
    d: float  # |a-b|
    identity_ok: bool


def pythagoras_report(a: float, b: float) -> PythagorasReport:
    c = math.sqrt(a * a + b * b)
    d = abs(a - b)
    # identidade: c^2 = (a-b)^2 + 2ab
    lhs = c * c
    rhs = d * d + 2 * a * b
    ok = abs(lhs - rhs) < 1e-6 * max(1.0, abs(lhs), abs(rhs))
    return PythagorasReport(a=a, b=b, c=c, d=d, identity_ok=ok)


# -------------------------
# Formas (máscaras) em matriz
# -------------------------

def poly_mask(n_sides: int, size: int, radius: float, rotation_deg: float = 0.0) -> np.ndarray:
    """
    Máscara binária [0,1] de um polígono regular centralizado.
    """
    h = w = size
    cy = (h - 1) / 2.0
    cx = (w - 1) / 2.0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    x = (xx - cx) / (w / 2.0)
    y = (yy - cy) / (h / 2.0)

    # pontos do polígono
    theta0 = math.radians(rotation_deg)
    pts = []
    for k in range(n_sides):
        th = theta0 + 2.0 * math.pi * k / n_sides
        pts.append((radius * math.cos(th), radius * math.sin(th)))

    # algoritmo half-space (convexo): para cada aresta, manter lado interno
    mask = np.ones((h, w), dtype=np.float32)
    for i in range(n_sides):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n_sides]
        # vetor da aresta
        ex, ey = (x2 - x1), (y2 - y1)
        # normal apontando pra dentro (ajuste por orientação CCW)
        nx, ny = (-ey, ex)

        # ponto na aresta e teste (x-x1,y-y1)·n >= 0
        mask *= (((x - x1) * nx + (y - y1) * ny) >= 0.0).astype(np.float32)

    return mask


def circle_mask(size: int, radius: float) -> np.ndarray:
    h = w = size
    cy = (h - 1) / 2.0
    cx = (w - 1) / 2.0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    x = (xx - cx) / (w / 2.0)
    y = (yy - cy) / (h / 2.0)
    r2 = x * x + y * y
    return (r2 <= radius * radius).astype(np.float32)


def overlay_masks(masks: List[np.ndarray]) -> np.ndarray:
    acc = np.zeros_like(masks[0], dtype=np.float32)
    for m in masks:
        acc = np.maximum(acc, m.astype(np.float32))
    return acc


# -------------------------
# Rotação / projeção “parede” (amostragem em círculo)
# -------------------------

def rotate_image_u8(img_u8: np.ndarray, angle_deg: float) -> np.ndarray:
    im = Image.fromarray(img_u8)
    # expand=False mantém tamanho; resample=BICUBIC dá suavidade
    out = im.rotate(angle_deg, resample=Image.BICUBIC, expand=False)
    return np.array(out)


def sample_circle_wall(gray01: np.ndarray, steps: int = 42, radius: float = 0.95) -> np.ndarray:
    """
    Amostra pontos na circunferência (a “parede”) em steps posições.
    Retorna vetor [steps] com valores 0..1.
    """
    h, w = gray01.shape
    cy = (h - 1) / 2.0
    cx = (w - 1) / 2.0
    rr = radius * min(h, w) / 2.0

    vals = np.zeros((steps,), dtype=np.float32)
    for k in range(steps):
        th = 2.0 * math.pi * k / steps
        x = cx + rr * math.cos(th)
        y = cy + rr * math.sin(th)
        xi = int(round(x))
        yi = int(round(y))
        xi = max(0, min(w - 1, xi))
        yi = max(0, min(h - 1, yi))
        vals[k] = gray01[yi, xi]
    return vals


def symmetry_score(gray01: np.ndarray) -> float:
    """
    Escore simples de simetria horizontal+vertical (quanto menor a diferença, maior o score).
    Retorna score 0..1 (aprox).
    """
    a = gray01
    flip_h = np.fliplr(a)
    flip_v = np.flipud(a)
    # erro médio
    eh = float(np.mean(np.abs(a - flip_h)))
    ev = float(np.mean(np.abs(a - flip_v)))
    # converte em score
    return float(np.exp(-3.0 * (eh + ev) / 2.0))


# -------------------------
# Mandelbrot (imagem)
# -------------------------

def mandelbrot(
    size: int = 768,
    center: Tuple[float, float] = (-0.5, 0.0),
    scale: float = 2.8,
    max_iter: int = 256,
) -> np.ndarray:
    """
    Retorna imagem grayscale 0..1 do conjunto de Mandelbrot (escape-time).
    """
    cx, cy = center
    w = h = size
    # grade complexa
    x = np.linspace(cx - scale / 2.0, cx + scale / 2.0, w, dtype=np.float32)
    y = np.linspace(cy - scale / 2.0, cy + scale / 2.0, h, dtype=np.float32)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C, dtype=np.complex64)

    it = np.zeros((h, w), dtype=np.int32)
    mask = np.ones((h, w), dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] * Z[mask] + C[mask]
        escaped = np.abs(Z) > 2.0
        newly = escaped & mask
        it[newly] = i
        mask &= ~escaped
        if not mask.any():
            break

    # normaliza e faz uma curva suave
    t = it.astype(np.float32) / float(max_iter)
    img = 1.0 - np.sqrt(t)
    return clamp01(img)


# -------------------------
# “Escolha de 3” (protótipo/simetria) em imagens
# -------------------------

def deform_image_u8(img_u8: np.ndarray, strength: float) -> np.ndarray:
    """
    Deformação simples radial (warp) para simular "variação extrema vs média".
    strength > 0 aumenta distorção.
    """
    h, w = img_u8.shape[:2]
    cy = (h - 1) / 2.0
    cx = (w - 1) / 2.0
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    x = (xx - cx) / (w / 2.0)
    y = (yy - cy) / (h / 2.0)
    r = np.sqrt(x * x + y * y) + 1e-6

    # warp radial: r' = r + k*r^3
    k = strength
    rp = r + k * (r**3)
    xp = x * (rp / r)
    yp = y * (rp / r)

    # map back para pixels
    xpx = xp * (w / 2.0) + cx
    ypx = yp * (h / 2.0) + cy

    # amostragem nearest (rápida)
    xi = np.clip(np.round(xpx).astype(np.int32), 0, w - 1)
    yi = np.clip(np.round(ypx).astype(np.int32), 0, h - 1)

    out = img_u8[yi, xi]
    return out


def prototype_choice_3(
    img_u8: np.ndarray,
    steps: int = 42,
    strengths: Tuple[float, float, float] = (-0.25, 0.0, +0.25),
) -> Dict[str, object]:
    """
    Gera 3 variações: extremo-, médio, extremo+.
    Calcula escores: simetria e “parede circular” (variância baixa = mais estável).
    Retorna relatório e qual item é "mais protótipo" (argmax score).
    """
    vars_u8 = []
    scores = []
    walls = []
    for s in strengths:
        v = deform_image_u8(img_u8, s)
        vars_u8.append(v)
        g = rgb_to_gray01(v)
        sym = symmetry_score(g)
        wall = sample_circle_wall(g, steps=steps, radius=0.95)
        stab = float(np.exp(-3.0 * np.var(wall)))  # mais estável => maior
        score = 0.55 * sym + 0.45 * stab
        scores.append(score)
        walls.append(wall)

    best = int(np.argmax(scores))
    return {
        "strengths": strengths,
        "scores": scores,
        "best_index": best,
        "best_strength": strengths[best],
        "wall_var": [float(np.var(w)) for w in walls],
    }


# -------------------------
# Pipeline principal
# -------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Pasta de saída")
    ap.add_argument("--size", type=int, default=768, help="Tamanho base das imagens")
    ap.add_argument("--steps", type=int, default=42, help="Passos do círculo (42 padrão)")
    ap.add_argument(
        "--bases",
        nargs="*",
        type=int,
        default=[10, 7, 14, 60, 20, 18, 13],
        help="Bases para conversão",
    )
    ap.add_argument(
        "--values",
        nargs="*",
        type=int,
        default=[7, 12, 30, 42, 56, 70, 144],
        help="Valores para conversão",
    )
    ap.add_argument("--mandelbrot", action="store_true", help="Gerar Mandelbrot")
    ap.add_argument("--shapes", action="store_true", help="Gerar formas e sobreposições")
    ap.add_argument("--cycle42", action="store_true", help="Gerar relatório do círculo/parede em 42 passos")
    ap.add_argument("--choice3", action="store_true", help="Rodar escolha de 3 (protótipo) usando imagem")
    ap.add_argument("--img", type=str, default="", help="Caminho de imagem para choice3/cycle42")
    ap.add_argument("--a", type=float, default=12.0, help="cateto a (Pitágoras)")
    ap.add_argument("--b", type=float, default=5.0, help="cateto b (Pitágoras)")
    ap.add_argument("--fib", type=int, default=20, help="N termos Fibonacci/Tribonacci")
    args = ap.parse_args()

    ensure_dir(args.out)

    # 1) Bases / números
    base_txt = explain_bases(args.values, args.bases)
    with open(os.path.join(args.out, "bases.txt"), "w", encoding="utf-8") as f:
        f.write(base_txt + "\n")

    # 2) Fibonacci / Tribonacci
    fib_seq = fibonacci(args.fib)
    tri_seq = tribonacci(args.fib)
    with open(os.path.join(args.out, "recorrencias.txt"), "w", encoding="utf-8") as f:
        f.write("Fibonacci (n-2):\n")
        f.write(", ".join(map(str, fib_seq)) + "\n\n")
        f.write("Tribonacci (n-3):\n")
        f.write(", ".join(map(str, tri_seq)) + "\n")

    # 3) Pitágoras
    rep = pythagoras_report(args.a, args.b)
    with open(os.path.join(args.out, "pythagoras.txt"), "w", encoding="utf-8") as f:
        f.write(f"a={rep.a}, b={rep.b}\n")
        f.write(f"c=sqrt(a^2+b^2)={rep.c}\n")
        f.write(f"d=|a-b|={rep.d}\n")
        f.write(f"identidade c^2 = (a-b)^2 + 2ab : {rep.identity_ok}\n")
        f.write("\nNotas:\n")
        f.write("- diagonal quadrado: a=b => c=a*sqrt(2)\n")
        f.write("- diagonal cubo: d=a*sqrt(3)\n")

    # 4) Mandelbrot
    if args.mandelbrot:
        mb = mandelbrot(size=args.size, center=(-0.5, 0.0), scale=2.8, max_iter=384)
        save_png(to_u8(mb), os.path.join(args.out, "mandelbrot.png"))

        # salva um plot com escala (opcional)
        plt.figure()
        plt.imshow(mb, cmap="gray")
        plt.title("Mandelbrot (grayscale)")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(os.path.join(args.out, "mandelbrot_plot.png"), dpi=150)
        plt.close()

    # 5) Formas + sobreposição
    if args.shapes:
        size = args.size
        circ = circle_mask(size=size, radius=0.95)
        tri = poly_mask(3, size=size, radius=0.80, rotation_deg=-90)
        sq = poly_mask(4, size=size, radius=0.75, rotation_deg=45)
        hexm = poly_mask(6, size=size, radius=0.82, rotation_deg=0)
        octm = poly_mask(8, size=size, radius=0.85, rotation_deg=22.5)

        # pentágono regular (aproximação — mesmo mask regular já é exata como polígono)
        pent = poly_mask(5, size=size, radius=0.82, rotation_deg=-90)

        # sobreposição “parede do círculo”
        stack = overlay_masks([tri, sq, hexm, octm, pent])
        inside = stack * circ

        save_png(to_u8(circ), os.path.join(args.out, "circle_mask.png"))
        save_png(to_u8(tri), os.path.join(args.out, "tri_mask.png"))
        save_png(to_u8(sq), os.path.join(args.out, "square_mask.png"))
        save_png(to_u8(hexm), os.path.join(args.out, "hex_mask.png"))
        save_png(to_u8(octm), os.path.join(args.out, "oct_mask.png"))
        save_png(to_u8(pent), os.path.join(args.out, "pent_mask.png"))
        save_png(to_u8(inside), os.path.join(args.out, "overlay_inside_circle.png"))

        # rotaciona o quadrado em passos (0..90) e amostra parede
        # (mostra “quantas posições” num ciclo fundamental discretizado)
        walls = []
        angles = np.linspace(0.0, 90.0, num=args.steps, endpoint=False)
        sq_img = np.stack([to_u8(sq)] * 3, axis=-1)
        for ang in angles:
            rimg = rotate_image_u8(sq_img, float(ang))
            g = rgb_to_gray01(rimg)
            walls.append(sample_circle_wall(g, steps=args.steps, radius=0.95))
        walls = np.array(walls)  # [steps, steps]
        np.save(os.path.join(args.out, "square_wall_samples.npy"), walls)

        # salva visualização do "mapa de parede"
        plt.figure()
        plt.imshow(walls, aspect="auto", cmap="gray")
        plt.title("Square -> Wall samples (angle x step)")
        plt.xlabel("wall step")
        plt.ylabel("angle step")
        plt.tight_layout()
        plt.savefig(os.path.join(args.out, "square_wall_samples.png"), dpi=150)
        plt.close()

    # 6) Cycle42 / parede (com imagem)
    if args.cycle42:
        if args.img and os.path.isfile(args.img):
            im = Image.open(args.img).convert("RGB")
            im = ImageOps.fit(im, (args.size, args.size), method=Image.BICUBIC)
            img_u8 = np.array(im)
        else:
            # fallback: usa o mandelbrot como “memória no plano”
            mb = mandelbrot(size=args.size, max_iter=256)
            img_u8 = np.stack([to_u8(mb)] * 3, axis=-1)

        g = rgb_to_gray01(img_u8)
        wall = sample_circle_wall(g, steps=args.steps, radius=0.95)
        # salva a imagem e o vetor
        save_png(img_u8.astype(np.uint8), os.path.join(args.out, "cycle_input.png"))
        np.save(os.path.join(args.out, "cycle_wall.npy"), wall)

        with open(os.path.join(args.out, "cycle_report.txt"), "w", encoding="utf-8") as f:
            f.write(f"steps={args.steps}\n")
            f.write(f"wall_mean={float(np.mean(wall))}\n")
            f.write(f"wall_var={float(np.var(wall))}\n")
            f.write(f"symmetry_score={symmetry_score(g)}\n")

        plt.figure()
        plt.plot(wall)
        plt.title("Wall samples (circumference)")
        plt.tight_layout()
        plt.savefig(os.path.join(args.out, "cycle_wall_plot.png"), dpi=150)
        plt.close()

    # 7) Choice3 (protótipo)
    if args.choice3:
        if not (args.img and os.path.isfile(args.img)):
            raise SystemExit("--choice3 precisa de --img caminho/arquivo")
        im = Image.open(args.img).convert("RGB")
        im = ImageOps.fit(im, (args.size, args.size), method=Image.BICUBIC)
        img_u8 = np.array(im)

        res = prototype_choice_3(img_u8, steps=args.steps, strengths=(-0.28, 0.0, +0.28))

        # salva variações
        strengths = res["strengths"]
        for i, s in enumerate(strengths):
            v = deform_image_u8(img_u8, s)
            save_png(v.astype(np.uint8), os.path.join(args.out, f"choice_var_{i}_s{str(s).replace('.', 'p')}.png"))

        with open(os.path.join(args.out, "choice3_report.txt"), "w", encoding="utf-8") as f:
            f.write(f"strengths={strengths}\n")
            f.write(f"scores={res['scores']}\n")
            f.write(f"wall_var={res['wall_var']}\n")
            f.write(f"best_index={res['best_index']}\n")
            f.write(f"best_strength={res['best_strength']}\n")

    # relatório mestre
    with open(os.path.join(args.out, "README_RUN.txt"), "w", encoding="utf-8") as f:
        f.write("PAI.py — saídas geradas:\n")
        f.write("- bases.txt (conversões)\n")
        f.write("- recorrencias.txt (Fibo/Tribo)\n")
        f.write("- pythagoras.txt (métrica)\n")
        f.write("- mandelbrot.png / mandelbrot_plot.png (se --mandelbrot)\n")
        f.write("- masks e overlay (se --shapes)\n")
        f.write("- cycle_* (se --cycle42)\n")
        f.write("- choice3_* (se --choice3)\n")

    print(f"[OK] Saída em: {args.out}")


if __name__ == "__main__":
    main()
