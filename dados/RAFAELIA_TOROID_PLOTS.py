#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA_TOROID_PLOTS
---------------------
Gera 4 gráficos de dispersão para as sementes Bitraf:

1) mean_radius vs phi_span_2pi
2) maxP       vs phi_span_2pi
3) den        vs phi_span_2pi
4) den        vs mean_radius

As cores representam famílias de denominadores:
- low  (≈ 47–81)  → azul
- mid  (≈ 94–107) → laranja
- high (≈ 115–122)→ verde
"""

import matplotlib.pyplot as plt

# -------------------------------------------------------------------------
# 1. Dados das sementes (hardcoded a partir do RAFAELIA_TOROID_PERIOD_LINK)
# -------------------------------------------------------------------------

SEEDS = [
    # den, base2, base8, base10, base16, maxP,  phi_span_2pi, mean_radius,      std_radius
    (47,    23,    23,    46,     23,    46,   0.886719,     7.508654,  6.126548e-01),
    (53,    52,    52,    13,     13,    52,   0.996094,     8.460751,  6.128343e-01),
    (59,    58,    58,    58,     29,    58,   0.992188,     9.413425,  6.129631e-01),
    (61,    60,    20,    60,     15,    60,   0.984375,     9.731082,  6.129980e-01),
    (67,    66,    22,    33,     33,    66,   0.996094,    10.684286,  6.130853e-01),
    (81,    54,    18,     9,     27,    54,   0.988281,    12.909425,  6.132209e-01),
    (94,    23,    23,    46,     23,    46,   0.886719,    14.976434,  6.132982e-01),
    (97,    48,    16,     0,     12,    48,   0.988281,    15.453513,  6.133120e-01),
    (103,   51,    17,    34,     51,    51,   0.949219,    16.407737,  6.133362e-01),
    (106,   52,    52,    13,     13,    52,   0.996094,    16.884879,  6.133468e-01),
    (107,    0,     0,    53,     53,    53,   0.984375,    17.043931,  6.133502e-01),
    (115,   44,    44,    22,     11,    44,   0.933594,    18.316407,  6.133742e-01),
    (118,   58,    58,    58,     29,    58,   0.988281,    18.793612,  6.133820e-01),
    (119,   24,     8,    48,      6,    48,   0.867188,    18.952684,  6.133845e-01),
    (121,    0,     0,    22,     55,    55,   0.996094,    19.270831,  6.133893e-01),
    (122,   60,    20,    60,     15,    60,   0.984375,    19.429906,  6.133916e-01),
]

# famílias por faixa de n
FAMILY_LOW  = {47, 53, 59, 61, 67, 81}
FAMILY_MID  = {94, 97, 103, 106, 107}
FAMILY_HIGH = {115, 118, 119, 121, 122}

COLOR_MAP = {
    "low":  "tab:blue",
    "mid":  "tab:orange",
    "high": "tab:green",
}
LABEL_MAP = {
    "low":  "family low (≈ 47–81)",
    "mid":  "family mid (≈ 94–107)",
    "high": "family high (≈ 115–122)",
}

def get_family(den: int) -> str:
    """Classifica denominador em low/mid/high."""
    if den in FAMILY_LOW:
        return "low"
    if den in FAMILY_MID:
        return "mid"
    if den in FAMILY_HIGH:
        return "high"
    # fallback (não deve acontecer com o conjunto atual)
    return "low"

# -------------------------------------------------------------------------
# 2. Função utilitária para scatter com cores + labels de n
# -------------------------------------------------------------------------

def scatter_by_family(x, y, dens, xlabel, ylabel, title, fname):
    """
    Desenha scatter com cores por família e rótulos dos denominadores.
    Salva figura em fname (PNG, alta resolução).
    """
    plt.figure(figsize=(11, 7))  # tamanho grande para boa definição

    # plota por família para legenda ficar limpa
    for fam in ("low", "mid", "high"):
        xs = []
        ys = []
        ns = []
        for xi, yi, n in zip(x, y, dens):
            if get_family(n) == fam:
                xs.append(xi)
                ys.append(yi)
                ns.append(n)
        if not xs:
            continue
        plt.scatter(xs, ys, label=LABEL_MAP[fam], s=40, alpha=0.9,
                    color=COLOR_MAP[fam])
        # anota cada ponto com o denominador
        for xi, yi, n in zip(xs, ys, ns):
            plt.text(xi, yi, str(n), fontsize=9,
                     ha="center", va="bottom")

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.5)
    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig(fname, dpi=300)
    print(f"[OK] Figura salva em: {fname}")
    plt.close()


# -------------------------------------------------------------------------
# 3. Extração dos vetores a partir de SEEDS
# -------------------------------------------------------------------------

dens        = [row[0] for row in SEEDS]
maxP        = [row[5] for row in SEEDS]
phi_span    = [row[6] for row in SEEDS]
mean_radius = [row[7] for row in SEEDS]

# -------------------------------------------------------------------------
# 4. Geração dos 4 gráficos
# -------------------------------------------------------------------------

if __name__ == "__main__":
    # 1) mean_radius vs phi_span_2pi
    scatter_by_family(
        mean_radius,
        phi_span,
        dens,
        xlabel="mean_radius (toroid mean |(x,y,z)|)",
        ylabel="phi_span_2pi (normalized angular coverage)",
        title="RAFAELIA – mean_radius vs ToroidΔπφ angular span",
        fname="RAFAELIA_mean_radius_vs_phi_span.png",
    )

    # 2) maxP vs phi_span_2pi
    scatter_by_family(
        maxP,
        phi_span,
        dens,
        xlabel="maxP (maximum period over bases {2,8,10,16})",
        ylabel="phi_span_2pi (normalized angular coverage)",
        title="RAFAELIA – maxP vs ToroidΔπφ angular span",
        fname="RAFAELIA_maxP_vs_phi_span.png",
    )

    # 3) den vs phi_span_2pi
    scatter_by_family(
        dens,
        phi_span,
        dens,
        xlabel="denominator n",
        ylabel="phi_span_2pi (normalized angular coverage)",
        title="RAFAELIA – den vs ToroidΔπφ angular span",
        fname="RAFAELIA_den_vs_phi_span.png",
    )

    # 4) den vs mean_radius
    scatter_by_family(
        dens,
        mean_radius,
        dens,
        xlabel="denominator n",
        ylabel="mean_radius (toroid mean |(x,y,z)|)",
        title="RAFAELIA – den vs ToroidΔπφ scale",
        fname="RAFAELIA_den_vs_mean_radius.png",
    )
