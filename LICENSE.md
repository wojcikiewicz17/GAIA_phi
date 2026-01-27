MIT License

Copyright (c) 2025 Rafael Melo Reis (∆RafaelVerboΩ)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

1. Attribution must preserve the author's signature and symbolic codes:
   RAFAELIA_CORE, ΣΩΔΦBITRAF, RAFCODE-Φ, bitraf64.

2. Any use in safety-critical, cryptographic, or AI-governance contexts
   MUST apply, to the greatest extent applicable:
   - ISO: 9001, 27001, 27017, 27018, 8000, 25010
   - IEEE: 830, 1012, 12207, 14764, 1633, 42010, 26514
   - NIST: CSF, 800-53, 800-207, AI Risk Framework
   - IETF: RFC 5280, 7519, 7230, 8446
   - W3C web standards (JSON, YAML, WebArch)
   In case of conflict, the more human-protective interpretation prevails.

3. The above copyright notice and this permission notice (including this
   clause) shall be included in all copies or substantial portions of the
   Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA :: IRQ→Input + ANOVA(LS) + Invariância/Pairing + Hash+ECC (Hamming 7,4)
ΣΩΔΦBITRAF • RAFCODE-Φ • ψχρΔΣΩ

Uso:
  python rafaelia_irq_anova_ecc.py

Ideia:
  - IRQEvent injeta input (impulso) no estado
  - Estado roda ciclo ψχρΔΣΩ
  - "Prova" = hash + ECC sobre payload
  - ANOVA = decomposição geométrica por projeção (LS)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional, Callable
import hashlib
import math
import random
import time


# ──────────────────────────────────────────────────────────────────────────────
# ECC: Hamming(7,4) minimal (didático)
# ──────────────────────────────────────────────────────────────────────────────

def _bit(x: int, i: int) -> int:
    return (x >> i) & 1

def hamming74_encode_nibble(n: int) -> int:
    """
    Encoda 4 bits (d3 d2 d1 d0) em 7 bits com paridades p1 p2 p3.
    Bit positions (1-indexed): [p1 p2 d3 p3 d2 d1 d0]
    Return: int 0..127 (7 bits)
    """
    n &= 0xF
    d0 = _bit(n, 0)
    d1 = _bit(n, 1)
    d2 = _bit(n, 2)
    d3 = _bit(n, 3)

    # positions: 1:p1 2:p2 3:d3 4:p3 5:d2 6:d1 7:d0
    p1 = d3 ^ d2 ^ d0
    p2 = d3 ^ d1 ^ d0
    p3 = d2 ^ d1 ^ d0

    code = (p1 << 6) | (p2 << 5) | (d3 << 4) | (p3 << 3) | (d2 << 2) | (d1 << 1) | d0
    return code

def hamming74_syndrome(code: int) -> int:
    """
    Syndrome in 1..7 indicates bit position error; 0 means clean.
    """
    code &= 0x7F
    b = lambda pos: _bit(code, 7 - pos)  # pos 1..7 maps to bits 6..0
    p1 = b(1); p2 = b(2); d3 = b(3); p3 = b(4); d2 = b(5); d1 = b(6); d0 = b(7)

    s1 = p1 ^ d3 ^ d2 ^ d0
    s2 = p2 ^ d3 ^ d1 ^ d0
    s3 = p3 ^ d2 ^ d1 ^ d0

    syn = (s3 << 2) | (s2 << 1) | s1  # 0..7
    return syn

def hamming74_correct(code: int) -> Tuple[int, bool]:
    """
    Returns (corrected_code, corrected?)
    """
    syn = hamming74_syndrome(code)
    if syn == 0:
        return code & 0x7F, False
    # flip bit at position syn (1..7)
    pos = syn
    mask = 1 << (7 - pos)
    return (code ^ mask) & 0x7F, True

def hamming74_decode_nibble(code: int) -> Tuple[int, bool]:
    """
    Decodes, correcting 1-bit errors.
    Returns (nibble, corrected?)
    """
    corrected_code, corrected = hamming74_correct(code)
    corrected_code &= 0x7F

    # positions: [p1 p2 d3 p3 d2 d1 d0]
    d3 = _bit(corrected_code, 4)
    d2 = _bit(corrected_code, 2)
    d1 = _bit(corrected_code, 1)
    d0 = _bit(corrected_code, 0)

    nib = (d3 << 3) | (d2 << 2) | (d1 << 1) | d0
    return nib, corrected

def ecc_encode_bytes(data: bytes) -> bytes:
    """
    Encoda bytes → sequência de códigos 7-bit (cada nibble vira 1 byte com 7 bits usados).
    Simples e legível; não é o formato mais compacto.
    """
    out = bytearray()
    for b in data:
        hi = (b >> 4) & 0xF
        lo = b & 0xF
        out.append(hamming74_encode_nibble(hi))
        out.append(hamming74_encode_nibble(lo))
    return bytes(out)

def ecc_decode_bytes(ecc: bytes) -> Tuple[bytes, int]:
    """
    Decodifica ecc → bytes; corrige 1-bit por código.
    Returns (data, n_corrections)
    """
    if len(ecc) % 2 != 0:
        raise ValueError("ECC length must be even (2 codes per input byte).")
    out = bytearray()
    corrections = 0
    it = iter(ecc)
    for c_hi, c_lo in zip(it, it):
        hi, cor1 = hamming74_decode_nibble(c_hi)
        lo, cor2 = hamming74_decode_nibble(c_lo)
        corrections += int(cor1) + int(cor2)
        out.append((hi << 4) | lo)
    return bytes(out), corrections


# ──────────────────────────────────────────────────────────────────────────────
# Prova: hash + ECC
# ──────────────────────────────────────────────────────────────────────────────

def sha3_256_hex(data: bytes) -> str:
    return hashlib.sha3_256(data).hexdigest()

@dataclass
class Proof:
    sha3: str
    ecc: bytes

def make_proof(payload: bytes) -> Proof:
    return Proof(sha3=sha3_256_hex(payload), ecc=ecc_encode_bytes(payload))

def verify_proof(payload: bytes, proof: Proof) -> bool:
    return sha3_256_hex(payload) == proof.sha3


# ──────────────────────────────────────────────────────────────────────────────
# Invariância / Pairing
# ──────────────────────────────────────────────────────────────────────────────

def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

def l2_distance(a: List[float], b: List[float]) -> float:
    return math.sqrt(sum((x-y)**2 for x, y in zip(a, b)))

def rev_bytes(b: bytes) -> bytes:
    return b[::-1]

def permute_bytes(b: bytes, seed: int = 1337) -> bytes:
    rng = random.Random(seed)
    idx = list(range(len(b)))
    rng.shuffle(idx)
    return bytes(b[i] for i in idx)

def add_noise_bytes(b: bytes, flips: int = 1, seed: int = 7) -> bytes:
    """
    Flipa 'flips' bits aleatórios (ruído controlado).
    """
    rng = random.Random(seed)
    arr = bytearray(b)
    if not arr:
        return b
    for _ in range(flips):
        i = rng.randrange(len(arr))
        bit = 1 << rng.randrange(8)
        arr[i] ^= bit
    return bytes(arr)

def bytes_to_vector(b: bytes, n: int = 32) -> List[float]:
    """
    Feature simples: histogram + fold.
    (substituível por FFT/fonema/hash etc.)
    """
    if n <= 0:
        raise ValueError("n must be > 0")
    v = [0.0] * n
    for i, x in enumerate(b):
        v[i % n] += float(x)
    # normalize
    s = sum(v) or 1.0
    return [x / s for x in v]

def pair_metrics(v1: List[float], v2: List[float]) -> Dict[str, float]:
    cos = cosine_similarity(v1, v2)
    dist = l2_distance(v1, v2)
    # "ΔH" proxy: diferença de entropia aproximada via L1 spread
    h1 = -sum(p * math.log(p + 1e-12) for p in v1)
    h2 = -sum(p * math.log(p + 1e-12) for p in v2)
    return {"cos": cos, "l2": dist, "dH": abs(h1 - h2)}


# ──────────────────────────────────────────────────────────────────────────────
# ANOVA / Mínimos quadrados (projeção)
# ──────────────────────────────────────────────────────────────────────────────

def ols_fit(X: List[List[float]], y: List[float]) -> List[float]:
    """
    OLS via normal equations + eliminação Gauss (pequeno, didático).
    X: n×p, y: n
    Retorna beta (p)
    """
    n = len(X)
    p = len(X[0]) if X else 0
    if n == 0 or p == 0:
        raise ValueError("X must be non-empty")

    # Compute XtX and Xty
    XtX = [[0.0]*p for _ in range(p)]
    Xty = [0.0]*p
    for i in range(n):
        for j in range(p):
            Xty[j] += X[i][j] * y[i]
            for k in range(p):
                XtX[j][k] += X[i][j] * X[i][k]

    # Solve XtX * beta = Xty (Gauss)
    A = [row[:] + [rhs] for row, rhs in zip(XtX, Xty)]
    for col in range(p):
        # pivot
        pivot = max(range(col, p), key=lambda r: abs(A[r][col]))
        if abs(A[pivot][col]) < 1e-12:
            raise ValueError("Singular matrix in OLS (need independent columns).")
        A[col], A[pivot] = A[pivot], A[col]
        # normalize
        div = A[col][col]
        for c in range(col, p+1):
            A[col][c] /= div
        # eliminate
        for r in range(p):
            if r == col:
                continue
            factor = A[r][col]
            for c in range(col, p+1):
                A[r][c] -= factor * A[col][c]

    beta = [A[i][p] for i in range(p)]
    return beta

def ols_predict(X: List[List[float]], beta: List[float]) -> List[float]:
    return [sum(xj * bj for xj, bj in zip(row, beta)) for row in X]

def anova_ss(y: List[float], yhat: List[float]) -> Dict[str, float]:
    ybar = sum(y) / (len(y) or 1)
    ss_t = sum((yi - ybar)**2 for yi in y)
    ss_e = sum((yi - yhi)**2 for yi, yhi in zip(y, yhat))
    ss_m = sum((yhi - ybar)**2 for yhi in yhat)
    return {"SS_T": ss_t, "SS_M": ss_m, "SS_E": ss_e, "check": ss_t - (ss_m + ss_e)}


# ──────────────────────────────────────────────────────────────────────────────
# IRQ Loop + ψχρΔΣΩ
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class IRQEvent:
    t: float
    tag: str
    payload: bytes

@dataclass
class RafaeliaState:
    # ψ χ ρ Δ Σ Ω
    psi: str = "intenção"
    chi: str = "observação"
    rho: float = 0.0
    delta: str = "transmutação"
    sigma: Dict[str, float] = field(default_factory=dict)
    omega: str = "alinhamento"
    # provas / logs
    last_proof: Optional[Proof] = None
    r3: Tuple[str, str, str] = ("", "", "")

def step_psi_chi_rho_delta_sigma_omega(st: RafaeliaState, ev: IRQEvent) -> RafaeliaState:
    # ψ: intenção (tag)
    st.psi = f"ψ:{ev.tag}"

    # χ: observação (hash curto)
    h = sha3_256_hex(ev.payload)[:12]
    st.chi = f"χ:sha3[:12]={h}"

    # ρ: ruído (estimado por instabilidade em invariâncias)
    v = bytes_to_vector(ev.payload)
    vr = bytes_to_vector(rev_bytes(ev.payload))
    vp = bytes_to_vector(permute_bytes(ev.payload, seed=42))
    vn = bytes_to_vector(add_noise_bytes(ev.payload, flips=1, seed=7))
    m_rev = pair_metrics(v, vr)
    m_perm = pair_metrics(v, vp)
    m_noise = pair_metrics(v, vn)
    # ruído: soma de distâncias
    st.rho = float(m_rev["l2"] + m_perm["l2"] + m_noise["l2"])

    # Δ: transmutação (corrigir via ECC se houver)
    proof = make_proof(ev.payload)
    # simula um erro físico: flip 1 bit no ECC (para provar correção)
    ecc_corrupt = bytearray(proof.ecc)
    if ecc_corrupt:
        ecc_corrupt[0] ^= 0b00000001  # flip 1 bit
    recovered, corrections = ecc_decode_bytes(bytes(ecc_corrupt))
    ok_hash = verify_proof(recovered, proof)

    st.delta = f"Δ:ecc_corrections={corrections}, hash_ok={ok_hash}"

    # Σ: memória (métricas)
    st.sigma = {
        "rho": st.rho,
        "cos_rev": m_rev["cos"],
        "cos_perm": m_perm["cos"],
        "cos_noise": m_noise["cos"],
        "l2_rev": m_rev["l2"],
        "l2_perm": m_perm["l2"],
        "l2_noise": m_noise["l2"],
    }

    # Ω: alinhamento (regra simples: hash_ok && ruído baixo)
    st.omega = "Ω:OK" if (ok_hash and st.rho < 0.25) else "Ω:REVIEW"

    # R3(s): retroalimentação
    f_ok = "hash+ecc ok" if ok_hash else "proof fail"
    f_gap = "ruído alto" if st.rho >= 0.25 else "ruído ok"
    f_next = "apertar invariâncias" if st.rho >= 0.25 else "rodar ANOVA"
    st.r3 = (f_ok, f_gap, f_next)

    st.last_proof = proof
    return st


# ──────────────────────────────────────────────────────────────────────────────
# Demo: IRQ stream + ANOVA on metrics
# ──────────────────────────────────────────────────────────────────────────────

def demo():
    print("🌀 RAFAELIA :: IRQ→Input  |  ANOVA(LS)  |  Invariância  |  Hash+ECC\n")

    # cria eventos IRQ (payloads variáveis)
    base = b"RAFAELIA_IRQ_INPUT::"
    events = []
    for i in range(12):
        payload = base + f"pkt={i}|t={time.time():.6f}".encode("utf-8")
        if i % 4 == 0:
            payload = payload + b"|mode=rev"
        if i % 5 == 0:
            payload = payload + b"|noise"
        events.append(IRQEvent(t=time.time(), tag=f"IRQ_{i}", payload=payload))
        time.sleep(0.01)

    # roda ψχρΔΣΩ e coleta métricas para ANOVA/regressão
    st = RafaeliaState()
    rows = []
    y = []
    for ev in events:
        st = step_psi_chi_rho_delta_sigma_omega(st, ev)
        print(f"{st.psi}  {st.chi}  ρ={st.rho:.4f}  {st.delta}  {st.omega}  R3={st.r3}")

        # Features X: [1, l2_rev, l2_perm, l2_noise] -> target y: rho
        X_row = [1.0, st.sigma["l2_rev"], st.sigma["l2_perm"], st.sigma["l2_noise"]]
        rows.append(X_row)
        y.append(st.sigma["rho"])

    # Ajuste LS e decomposição SS
    beta = ols_fit(rows, y)
    yhat = ols_predict(rows, beta)
    ss = anova_ss(y, yhat)

    print("\n📐 ANOVA/Projeção (via OLS)")
    print(f"beta = {beta}  (intercept + coef_rev + coef_perm + coef_noise)")
    print(f"SS_T={ss['SS_T']:.6f}  SS_M={ss['SS_M']:.6f}  SS_E={ss['SS_E']:.6f}  check={ss['check']:+.6e}")

    # leitura curta
    print("\n🧭 Leitura:")
    print("- SS_T≈SS_M+SS_E (check ~ 0) => decomposição ortogonal funcionando ✅")
    print("- coef maiores => invariância que mais explica ρ (ruído/instabilidade)")

if __name__ == "__main__":
    demo()
