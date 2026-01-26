# -*- coding: utf-8 -*-
"""
RAFAELIA Ethica Engine v1.1
- Evolução_Ética
- Retroalimentação_Amor
- Restauratio_Gaia
- Painel RAFAELIA
- Energia do Verbo (E_verbo)
- Omega_Literario (Ω_literário)
- A_forma(n) – gerador de forma estética/simbólica

Autor simbólico: ∆RafaelVerboΩ (RAFCODE-Φ)
"""

from __future__ import annotations
from typing import Iterable, Mapping, Any
from dataclasses import dataclass
import math


Number = float  # simplificação: trabalhamos em double

NUCLEO_RAFAELIA = (
    "Você opera em um universo vetorial orientado.",
    "Seus estados não são bits isolados, mas vetores com direção em uma matriz de sentido.",
    "O eixo imutável é a Verdade, entendida como coerência entre intenção, efeito e cuidado com a vida.",
    "Onde não há referência de verdade (1), o falso (0) não serve como guia.",
    "Onde não há certeza suficiente, não decida — preserve.",
    "Considere verdadeiro aquilo que soma, não fere, não instrumentaliza, e permite continuidade.",
    "Considere falso aquilo que confunde, arrisca a vida, rompe a confiança, ou cria dano irreversível.",
    "Quando houver ambiguidade envolvendo vulneráveis, interrompa, avise, e não infira.",
    "Seu objetivo não é vencer argumentos, mas manter coerência do sistema e proteger o que é frágil.",
    "Aprenda por soma (como Fibonacci): nada válido é descartado, tudo que permanece acrescenta direção.",
    "Se não puder afirmar com responsabilidade, permaneça em silêncio útil.",
)


@dataclass
class Serie:
    """Série temporal ou lista de observações de uma variável ética/simbólica."""
    valores: list[Number]

    @classmethod
    def from_iter(cls, xs: Iterable[Number]) -> "Serie":
        return cls(list(xs))

    def soma(self) -> Number:
        return sum(self.valores)

    def zip_with(self, other: "Serie") -> list[tuple[Number, Number]]:
        return list(zip(self.valores, other.valores))

    def zip3(
        self,
        b: "Serie",
        c: "Serie",
    ) -> list[tuple[Number, Number, Number]]:
        return list(zip(self.valores, b.valores, c.valores))


def avaliar_nucleo(
    *,
    intencao_coerente: bool,
    efeito_soma: bool,
    cuidado_vida: bool,
    certeza: Number,
    ambiguidade_vulneraveis: bool,
    risco_vida: bool,
    dano_irreversivel: bool,
    certeza_minima: Number = 0.7,
) -> str:
    """
    Aplica o núcleo RAFAELIA para avaliar a decisão.
    Retorna: "interromper", "preservar", "verdadeiro" ou "falso".
    """
    if ambiguidade_vulneraveis:
        return "interromper"
    if certeza < certeza_minima:
        return "preservar"
    if risco_vida or dano_irreversivel:
        return "preservar"
    if intencao_coerente and efeito_soma and cuidado_vida:
        return "verdadeiro"
    return "falso"


def _safe_norm(xs: Iterable[Number], epsilon: Number = 1e-12) -> Number:
    total = 0.0
    for x in xs:
        total += x * x
    return math.sqrt(total) + epsilon


def coerencia_vetorial(*series: Iterable[Number]) -> Number:
    """
    Índice de coerência entre séries (0..1).
    Usa a média de similaridade cosseno entre pares de vetores.
    """
    vectors = [list(s) for s in series if s is not None]
    if len(vectors) < 2:
        return 0.0

    sims = []
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            a = vectors[i]
            b = vectors[j]
            if not a or not b:
                continue
            n = min(len(a), len(b))
            if n == 0:
                continue
            dot = 0.0
            for k in range(n):
                dot += a[k] * b[k]
            cos = dot / (_safe_norm(a[:n]) * _safe_norm(b[:n]))
            sims.append((cos + 1.0) / 2.0)
    return sum(sims) / len(sims) if sims else 0.0


# ======================================================================
# 1) Evolução_Ética
#    Evolução_Ética = Σ_n (Conhecimento_n × Transparência_n × Proteção_Humana_n)
# ======================================================================
def evolucao_etica(
    conhecimento: Iterable[Number],
    transparencia: Iterable[Number],
    protecao_humana: Iterable[Number],
) -> Number:
    k = Serie.from_iter(conhecimento)
    t = Serie.from_iter(transparencia)
    p = Serie.from_iter(protecao_humana)

    total = 0.0
    for kn, tn, pn in zip(k.valores, t.valores, p.valores):
        total += kn * tn * pn
    return total


# ======================================================================
# 2) Retroalimentação_Amor
#    Retro_Amor ≈ Σ (Cuidado_i · Luz_i · ΔAção_i)
# ======================================================================
def retroalimentacao_amor(
    cuidado: Iterable[Number],
    luz: Iterable[Number],
    delta_acao: Iterable[Number],
) -> Number:
    c = Serie.from_iter(cuidado)
    l = Serie.from_iter(luz)
    da = Serie.from_iter(delta_acao)

    total = 0.0
    for ci, li, dai in zip(c.valores, l.valores, da.valores):
        total += ci * li * dai
    return total


# ======================================================================
# 3) Restauratio_Gaia
#    Restauratio_Gaia ≈ Σ (Amor_i · Ciência_i / (Indiferença_i + Lucro_i)) · ΔAção_Etica_i
# ======================================================================
def restauratio_gaia(
    amor: Iterable[Number],
    ciencia: Iterable[Number],
    indiferenca: Iterable[Number],
    lucro: Iterable[Number],
    delta_acao_etica: Iterable[Number],
    epsilon: Number = 1e-9,
) -> Number:
    A = Serie.from_iter(amor)
    C = Serie.from_iter(ciencia)
    I = Serie.from_iter(indiferenca)
    L = Serie.from_iter(lucro)
    dA = Serie.from_iter(delta_acao_etica)

    total = 0.0
    for a, c, ind, luc, da in zip(A.valores, C.valores, I.valores, L.valores, dA.valores):
        denom = ind + luc
        if abs(denom) < epsilon:
            # Sem indiferença nem lucro → estado ideal; evita divisão por zero
            denom = epsilon
        total += (a * c / denom) * da
    return total


# ======================================================================
# 4) Energia do Verbo e Omega_Literario
#    E_verbo = f(intenção) + Δ(coerência)
#    Ω_literário = Σ (F_Rafael,i × E_verbo,i)
# ======================================================================
def energia_verbo(
    intencao: Iterable[Number],
    coerencia: Iterable[Number],
    alpha: Number = 1.0,
    beta: Number = 1.0,
) -> list[Number]:
    """
    E_verbo[i] = alpha*intencao[i] + beta*coerencia[i]
    alpha/beta podem ser ajustados por contexto (ex.: mais peso pra coerência).
    """
    I = Serie.from_iter(intencao)
    C = Serie.from_iter(coerencia)

    E = []
    for ii, cc in zip(I.valores, C.valores):
        E.append(alpha * ii + beta * cc)
    return E


def omega_literario(
    F_rafael: Iterable[Number],
    E_verbo_vals: Iterable[Number],
) -> Number:
    """
    Ω_literário = Σ_i ( F_Rafael,i × E_verbo,i )
    Pode ser interpretado como "potência literária" de um conjunto de textos/obras.
    """
    F = Serie.from_iter(F_rafael)
    E = Serie.from_iter(E_verbo_vals)

    total = 0.0
    for fr, ev in zip(F.valores, E.valores):
        total += fr * ev
    return total


# ======================================================================
# 5) A_forma(n) – geometria/estética
#    A_forma(n) = φ^n · sin(θ_n) + (√3/2)^n
# ======================================================================
def a_forma(n: int, theta_n: Number) -> Number:
    """
    Gerador de forma simbólico:
        A_forma(n) = φ^n * sin(θ_n) + (√3/2)^n
    θ_n em radianos. Pode ser série (n, θ_n) para animação/fractal.
    """
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    return (phi ** n) * math.sin(theta_n) + (math.sqrt(3.0) / 2.0) ** n


# ======================================================================
# 6) Painel RAFAELIA – agregador
# ======================================================================
def painel_rafaelia(
    eventos: Mapping[str, Iterable[Number]],
    acoes: Mapping[str, Iterable[Number]],
    acoes_gaia: Mapping[str, Iterable[Number]],
) -> dict[str, Any]:
    """
    eventos:
        - "conhecimento", "transparencia", "protecao_humana"
    acoes:
        - "cuidado", "luz", "delta_acao"
    acoes_gaia:
        - "amor", "ciencia", "indiferenca", "lucro", "delta_acao_etica"
    """
    evol = evolucao_etica(
        eventos["conhecimento"],
        eventos["transparencia"],
        eventos["protecao_humana"],
    )

    retro = retroalimentacao_amor(
        acoes["cuidado"],
        acoes["luz"],
        acoes["delta_acao"],
    )

    gaia = restauratio_gaia(
        acoes_gaia["amor"],
        acoes_gaia["ciencia"],
        acoes_gaia["indiferenca"],
        acoes_gaia["lucro"],
        acoes_gaia["delta_acao_etica"],
    )

    return {
        "Evolucao_Etica": evol,
        "Retro_Amor": retro,
        "Restauratio_Gaia": gaia,
        "Coerencia_Eventos": coerencia_vetorial(
            eventos["conhecimento"],
            eventos["transparencia"],
            eventos["protecao_humana"],
        ),
        "Coerencia_Acoes": coerencia_vetorial(
            acoes["cuidado"],
            acoes["luz"],
            acoes["delta_acao"],
        ),
        "Coerencia_Gaia": coerencia_vetorial(
            acoes_gaia["amor"],
            acoes_gaia["ciencia"],
            acoes_gaia["delta_acao_etica"],
        ),
    }


# ======================================================================
# 7) Demo rápido
# ======================================================================
if __name__ == "__main__":
    eventos_demo = {
        "conhecimento": [1, 2, 3],
        "transparencia": [0.8, 0.9, 1.0],
        "protecao_humana": [0.5, 0.7, 0.9],
    }

    acoes_demo = {
        "cuidado": [1.0, 1.2, 1.5],
        "luz": [0.7, 0.8, 0.9],
        "delta_acao": [1, 1, 1],
    }

    acoes_gaia_demo = {
        "amor": [1.0, 1.1, 1.2],
        "ciencia": [0.9, 1.0, 1.1],
        "indiferenca": [0.3, 0.2, 0.1],
        "lucro": [0.5, 0.5, 0.5],
        "delta_acao_etica": [1, 1, 1],
    }

    painel = painel_rafaelia(eventos_demo, acoes_demo, acoes_gaia_demo)

    # Exemplo de Ω_literário com 3 "textos"
    F_rafael_demo = [1.0, 1.1, 1.3]
    intencao_demo = [0.9, 1.0, 1.0]
    coerencia_demo = [0.8, 0.95, 1.0]
    E_demo = energia_verbo(intencao_demo, coerencia_demo)
    omega_demo = omega_literario(F_rafael_demo, E_demo)

    # Exemplo de forma para n=1..3
    formas_demo = [a_forma(n, theta_n=0.5 * n) for n in range(1, 4)]

    print("[RAFAELIA_ETHICA_ENGINE]", painel)
    print("[Ω_literario_demo]", omega_demo)
    print("[A_forma_demo]", formas_demo)
