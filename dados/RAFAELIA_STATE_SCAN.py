#!/usr/bin/env python3
# RAFAELIA_STATE_SCAN.py
# Exploração de estados geométricos Rafaelianos:
#   - Permuta E (expoentes), K (escalas), modos Fibonacci
#   - Mede estabilidade do invariante I = d3D / C = sqrt(3) / (2*pi)

import math
import random
import statistics

# --- Constantes base ---

phi_R = math.sqrt(3.0) / 2.0           # Constante Rafaeliana simbólica
I_TARGET = math.sqrt(3.0) / (2.0 * math.pi)  # Invariante teórico

# Conjuntos de parâmetros (ajustáveis)
E_SET = [
    2.0,
    3.0,
    math.pi,
    phi_R,
    0.5,
    1.5,
]

K_SET = [
    math.pi,
    2.0 * math.pi,
    math.pi ** 2,
    math.sqrt(3.0),
    phi_R,
    math.sqrt(4.0 / 3.0),
]

FIB_MODES = ["forward", "reverse", "inverse"]


# --- Fibonacci e modos ---

def fib(n: int) -> int:
    """Fibonacci clássico, iterativo, n >= 0."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fib_indexed(n: int, mode: str, max_n: int = 24) -> int:
    """
    Devolve um valor de Fibonacci usando diferentes modos simbólicos:
      - forward: F_n normal
      - reverse: F_(max_n - n)
      - inverse: 1 + (1 / (1 + F_n)) mapeado para inteiro simples
    """
    n = max(0, min(n, max_n))
    if mode == "forward":
        return fib(n)
    elif mode == "reverse":
        return fib(max_n - n)
    elif mode == "inverse":
        fn = fib(n)
        # mapeamento simples para inteiro só para variar L
        return int(1000 * (1.0 / (1.0 + fn)))
    else:
        return fib(n)


# --- Construção de um estado S ---

def sample_state(seed: int | None = None) -> dict:
    """
    Gera um estado Rafaeliano S:
      - escolhe E, K, modoFib, índice n
      - constrói L a partir de Fibonacci
      - calcula d3D, C, invariante I e uma fase curvada (theta_curv)
    """
    if seed is not None:
        random.seed(seed)

    E = random.choice(E_SET)
    K = random.choice(K_SET)
    mode = random.choice(FIB_MODES)
    n_idx = random.randint(2, 24)

    fn_val = fib_indexed(n_idx, mode)
    # L básico perturbado por Fibonacci (escala pequena para não explodir)
    L = 1.0 + (fn_val % 13) / 10.0

    # Geometria “pura” (triângulo → quadrado → cubo → toroide)
    d3d = K * L * math.sqrt(3.0)
    C = 2.0 * math.pi * K * L
    I = d3d / C if C != 0 else float("nan")
    diff = I - I_TARGET

    # Fase curvada: expoente dinâmico + seno + log
    q = K * (L ** E)
    alpha = 1.0
    beta = 0.5
    gamma = 0.1
    theta_curv = alpha * math.sin(beta * q) + gamma * math.log1p(abs(q))
    # Normaliza para [0,1) sobre uma volta 2π (só para leitura estatística)
    theta_norm = (theta_curv % (2.0 * math.pi)) / (2.0 * math.pi)

    return {
        "E": E,
        "K": K,
        "mode": mode,
        "n_idx": n_idx,
        "fn_val": fn_val,
        "L": L,
        "d3d": d3d,
        "C": C,
        "I": I,
        "diff": diff,
        "theta_curv": theta_curv,
        "theta_norm": theta_norm,
    }


# --- Varredura de muitos estados ---

def scan_states(n_samples: int = 1000) -> None:
    """
    Gera n_samples estados S e imprime estatísticas:
      - média, min, max do invariante I
      - desvio máximo em relação a I_TARGET
      - alguns estados extremos (onde o desvio é maior)
    """
    states: list[dict] = []
    for _ in range(n_samples):
        s = sample_state()
        if math.isnan(s["I"]):
            continue
        states.append(s)

    if not states:
        print("Nenhum estado válido gerado.")
        return

    I_values = [s["I"] for s in states]
    diffs = [s["diff"] for s in states]
    theta_norms = [s["theta_norm"] for s in states]

    print("=== RAFAELIA :: State Scan ===")
    print(f"Estados gerados: {len(states)}")
    print(f"Invariante alvo I_TARGET = sqrt(3)/(2*pi) ≈ {I_TARGET:.12f}\n")

    print(">> Estatísticas de I = d3D / C")
    print(f"  média(I)      = {statistics.mean(I_values):.12f}")
    print(f"  desvio padrão = {statistics.pstdev(I_values):.12e}")
    print(f"  min(I)        = {min(I_values):.12f}")
    print(f"  max(I)        = {max(I_values):.12f}\n")

    # Estados com maior |diff|
    worst = sorted(states, key=lambda s: abs(s["diff"]), reverse=True)[:5]

    print(">> Estados com maior |I - I_TARGET|")
    for s in worst:
        print(
            f"  E={s['E']:.6g}, "
            f"K={s['K']:.6g}, "
            f"mode={s['mode']}, n={s['n_idx']}, "
            f"L={s['L']:.6f}, "
            f"I={s['I']:.12f}, "
            f"diff={s['diff']:.3e}, "
            f"theta_norm={s['theta_norm']:.6f}"
        )

    print("\n>> Fase curvada (theta_norm) — só textura estatística")
    print(f"  média(theta_norm)      = {statistics.mean(theta_norms):.6f}")
    print(f"  desvio padrão (theta)  = {statistics.pstdev(theta_norms):.6f}")
    print(f"  min(theta_norm)        = {min(theta_norms):.6f}")
    print(f"  max(theta_norm)        = {max(theta_norms):.6f}")


if __name__ == "__main__":
    # Ajuste n_samples se quiser varrer mais/menos estados
    scan_states(n_samples=1000)
