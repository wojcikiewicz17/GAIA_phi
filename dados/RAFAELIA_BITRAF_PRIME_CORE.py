#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA_BITRAF_PRIME_CORE
====================================================================
Núcleo Bitraf para extrair sementes a partir de:

  - RAFAELIA_DIZIMA_INDEX.tsv
      den, base, label, type, pre_len, period_len, pre, period

  - RAFAELIA_DIZIMA_CONSTANT_BRIDGE.tsv
      valor, freq, frac_part, best_n, best_diff,
      period_len_bin, period_len_oct, period_len_dec, period_len_hex,
      terminante_dec, full_reptend_dec

Ideia:
  1) Para cada constante (valor) no BRIDGE, usar o best_n (denominador).
  2) Olhar em DIZIMA_INDEX como 1/best_n se comporta em bases 2, 8, 10, 16.
  3) Filtrar sementes com períodos longos (≥ min_period).
  4) Atribuir um score Bitraf (período total, frequência, erro pequeno).
  5) Expor um gerador de fluxo binário a partir da dízima (estado periódico).

Use:
  python RAFAELIA_BITRAF_PRIME_CORE.py
====================================================================
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

DIZIMA_INDEX_FILE = "RAFAELIA_DIZIMA_INDEX.tsv"
BRIDGE_FILE = "RAFAELIA_DIZIMA_CONSTANT_BRIDGE.tsv"


# -------------------------------------------------------------------
# Utilitários
# -------------------------------------------------------------------

def _to_int(v, default: int = 0) -> int:
    try:
        if v is None or v == "":
            return default
        return int(v)
    except Exception:
        return default


def _to_float(v, default: float = 0.0) -> float:
    try:
        if v is None or v == "":
            return default
        return float(v)
    except Exception:
        return default


def _to_bool(v, default: bool = False) -> bool:
    if v is None:
        return default
    s = str(v).strip().lower()
    if s in ("1", "true", "t", "yes", "y", "sim"):
        return True
    if s in ("0", "false", "f", "no", "n", "nao", "não"):
        return False
    return default


# -------------------------------------------------------------------
# Estruturas de dados
# -------------------------------------------------------------------

@dataclass
class DizimaRow:
    den: int
    base: int
    label: str
    type: str
    pre_len: int
    period_len: int
    pre: str
    period: str


@dataclass
class ConstantSummary:
    valor: float
    freq: int
    frac_part: float
    best_n: Optional[int]
    best_diff: float
    period_len_bin: int
    period_len_oct: int
    period_len_dec: int
    period_len_hex: int
    terminante_dec: bool
    full_reptend_dec: bool


@dataclass
class BitrafSeed:
    id: str
    valor: float
    freq: int
    best_n: int
    best_diff: float
    periods: Dict[int, int]
    patterns: Dict[int, str]
    terminante_dec: bool
    full_reptend_dec: bool
    score: float


# -------------------------------------------------------------------
# Leitura dos arquivos TSV
# -------------------------------------------------------------------

def load_dizima_index(path: str) -> Dict[Tuple[int, int], DizimaRow]:
    """
    Lê RAFAELIA_DIZIMA_INDEX.tsv em um dicionário:
      (den, base) -> DizimaRow
    """
    out: Dict[Tuple[int, int], DizimaRow] = {}
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            den = _to_int(row.get("den"))
            base = _to_int(row.get("base"))
            label = row.get("label", "")
            type_ = row.get("type", "")
            pre_len = _to_int(row.get("pre_len"))
            period_len = _to_int(row.get("period_len"))
            pre = row.get("pre", "") or ""
            period = row.get("period", "") or ""
            key = (den, base)
            out[key] = DizimaRow(
                den=den,
                base=base,
                label=label,
                type=type_,
                pre_len=pre_len,
                period_len=period_len,
                pre=pre,
                period=period,
            )
    return out


def load_constant_summaries(path: str) -> List[ConstantSummary]:
    """
    Lê RAFAELIA_DIZIMA_CONSTANT_BRIDGE.tsv em uma lista de ConstantSummary.
    """
    out: List[ConstantSummary] = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            valor = _to_float(row.get("valor"))
            freq = _to_int(row.get("freq"), 1)
            frac_part = _to_float(row.get("frac_part"))
            best_n = _to_int(row.get("best_n"), 0)
            if best_n <= 0:
                best_n = None
            best_diff = _to_float(row.get("best_diff"))
            period_len_bin = _to_int(row.get("period_len_bin"))
            period_len_oct = _to_int(row.get("period_len_oct"))
            period_len_dec = _to_int(row.get("period_len_dec"))
            period_len_hex = _to_int(row.get("period_len_hex"))
            terminante_dec = _to_bool(row.get("terminante_dec"))
            full_reptend_dec = _to_bool(row.get("full_reptend_dec"))
            out.append(
                ConstantSummary(
                    valor=valor,
                    freq=freq,
                    frac_part=frac_part,
                    best_n=best_n,
                    best_diff=best_diff,
                    period_len_bin=period_len_bin,
                    period_len_oct=period_len_oct,
                    period_len_dec=period_len_dec,
                    period_len_hex=period_len_hex,
                    terminante_dec=terminante_dec,
                    full_reptend_dec=full_reptend_dec,
                )
            )
    return out


# -------------------------------------------------------------------
# Scoring de semente Bitraf
# -------------------------------------------------------------------

def _score_seed(const: ConstantSummary, periods: Dict[int, int]) -> float:
    """
    Define um score para a semente Bitraf:

      - soma dos períodos nas bases disponíveis, com pesos,
      - favorece constantes com alta frequência de ocorrência (freq),
      - penaliza best_diff grande.

    Ajuste fino pode ser feito depois.
    """
    # pesos simples por base (2, 8, 10, 16)
    weights = {2: 1.3, 8: 1.1, 10: 1.5, 16: 1.2}
    total_period = 0.0
    for base, p in periods.items():
        w = weights.get(base, 1.0)
        total_period += w * float(p)

    # normaliza com log da frequência (para não explodir, mas premiar freq alta)
    freq_factor = 1.0 + math.log(max(const.freq, 1), 2)

    # penalização suave pelo erro best_diff
    # adiciona 1 para evitar divisão por zero
    diff_penalty = 1.0 + abs(const.best_diff)

    score = (total_period * freq_factor) / diff_penalty
    return score


# -------------------------------------------------------------------
# Descoberta de sementes (via constantes)
# -------------------------------------------------------------------

def discover_bitraf_seeds(
    dizima_index: Dict[Tuple[int, int], DizimaRow],
    consts: List[ConstantSummary],
    min_period: int = 16,
    max_seeds: int = 16,
) -> List[BitrafSeed]:
    """
    Explora as constantes + índice de dízimas para encontrar sementes:

      - Usa best_n de cada ConstantSummary, se presente.
      - Procura representações de 1/best_n em bases 2, 8, 10, 16.
      - Filtra por período máximo >= min_period.
      - Calcula score Bitraf.
    """
    seeds: List[BitrafSeed] = []

    for i, c in enumerate(consts):
        if c.best_n is None or c.best_n <= 1:
            continue

        den = c.best_n
        periods: Dict[int, int] = {}
        patterns: Dict[int, str] = {}

        for base in (2, 8, 10, 16):
            row = dizima_index.get((den, base))
            if row is None:
                continue
            if row.period_len <= 0:
                continue

            periods[base] = row.period_len
            patterns[base] = row.period

        if not periods:
            # não temos info em nenhuma base
            continue

        max_period = max(periods.values())
        if max_period < min_period:
            continue

        score = _score_seed(c, periods)
        seed_id = f"VAL_{c.valor:.6g}_n{den}"

        seeds.append(
            BitrafSeed(
                id=seed_id,
                valor=c.valor,
                freq=c.freq,
                best_n=den,
                best_diff=c.best_diff,
                periods=periods,
                patterns=patterns,
                terminante_dec=c.terminante_dec,
                full_reptend_dec=c.full_reptend_dec,
                score=score,
            )
        )

    # Ordena: maior período, maior score
    seeds.sort(
        key=lambda s: (max(s.periods.values()), s.score),
        reverse=True,
    )

    if max_seeds > 0:
        seeds = seeds[:max_seeds]

    return seeds


def discover_bitraf_seeds_from_index(
    dizima_index: Dict[Tuple[int, int], DizimaRow],
    min_period: int = 32,
    max_seeds: int = 16,
) -> List[BitrafSeed]:
    """
    Fallback: descobre sementes usando apenas o índice de dízimas,
    sem depender de vincular a uma constante específica.

    - Agrupa por denominador (den).
    - Olha as bases 2, 8, 10, 16.
    - Seleciona quem tiver período máximo >= min_period.
    """
    buckets: Dict[int, Dict[int, DizimaRow]] = defaultdict(dict)
    for (den, base), row in dizima_index.items():
        buckets[den][base] = row

    seeds: List[BitrafSeed] = []

    for den, per_base in buckets.items():
        periods: Dict[int, int] = {}
        patterns: Dict[int, str] = {}

        for base in (2, 8, 10, 16):
            r = per_base.get(base)
            if r is None:
                continue
            if r.period_len <= 0:
                continue
            periods[base] = r.period_len
            patterns[base] = r.period

        if not periods:
            continue

        maxP = max(periods.values())
        if maxP < min_period:
            continue

        # Constante "fake" só para reutilizar o _score_seed
        fake_const = ConstantSummary(
            valor=0.0,
            freq=1,
            frac_part=0.0,
            best_n=den,
            best_diff=0.0,
            period_len_bin=periods.get(2, 0),
            period_len_oct=periods.get(8, 0),
            period_len_dec=periods.get(10, 0),
            period_len_hex=periods.get(16, 0),
            terminante_dec=False,
            full_reptend_dec=False,
        )

        score = _score_seed(fake_const, periods)

        seeds.append(
            BitrafSeed(
                id=f"DEN_{den}",
                valor=0.0,
                freq=1,
                best_n=den,
                best_diff=0.0,
                periods=periods,
                patterns=patterns,
                terminante_dec=False,
                full_reptend_dec=False,
                score=score,
            )
        )

    seeds.sort(
        key=lambda s: (max(s.periods.values()), s.score),
        reverse=True,
    )

    if max_seeds > 0:
        seeds = seeds[:max_seeds]

    return seeds


# -------------------------------------------------------------------
# Gerador de fluxo Bitraf
# -------------------------------------------------------------------

def generate_bitraf_stream(
    seed: BitrafSeed,
    base: int = 2,
    length: int = 256,
) -> str:
    """
    Gera um fluxo binário de tamanho `length` a partir da dízima armazenada
    em `seed.patterns[base]`.

    Por enquanto:

      - Usa somente a parte periódica (period);
      - Se base != 2, converte cada dígito em bit via paridade (d & 1);
      - Repete o padrão até atingir o tamanho `length`.
    """
    if base not in seed.patterns:
        raise ValueError(f"Seed não possui padrão na base {base}")

    period_str = seed.patterns[base]
    if not period_str:
        raise ValueError("Período vazio na seed")

    if base == 2:
        # já é binário
        bits = period_str
    else:
        # converte dígitos na base para bits (paridade simples)
        bits_list = []
        for ch in period_str:
            # para base 8/10/16, ch é 0-9A-F
            try:
                d = int(ch, base)
            except ValueError:
                # fallback: só ignora
                continue
            bits_list.append(str(d & 1))
        bits = "".join(bits_list) or "0"

    # repete o padrão até atingir o tamanho desejado
    if not bits:
        bits = "0"
    out = []
    while len("".join(out)) < length:
        out.append(bits)
    stream = "".join(out)[:length]
    return stream


# -------------------------------------------------------------------
# CLI / Demo
# -------------------------------------------------------------------

def main() -> None:
    print("=" * 67)
    print("RAFAELIA_BITRAF_PRIME_CORE – Núcleo de Sementes a partir de Dízimas")
    print("=" * 67)
    print(f"[+] Lendo índice de dízimas: {DIZIMA_INDEX_FILE}")
    diz_idx = load_dizima_index(DIZIMA_INDEX_FILE)
    print(f"[i] Entradas em DIZIMA_INDEX: {len(diz_idx)}")
    print(f"[+] Lendo resumo de constantes: {BRIDGE_FILE}")
    consts = load_constant_summaries(BRIDGE_FILE)
    print(f"[i] Constantes no BRIDGE: {len(consts)}")

    print("[+] Descobrindo sementes Bitraf (vinculadas às constantes)...")
    seeds = discover_bitraf_seeds(
        dizima_index=diz_idx,
        consts=consts,
        min_period=16,
        max_seeds=16,
    )
    print(f"[i] Sementes (constantes) encontradas: {len(seeds)}")

    if not seeds:
        print("[!] Nenhuma semente ligada às constantes com os critérios atuais.")
        print("[+] Ativando modo fallback: sementes puras a partir do índice de dízimas...")
        seeds = discover_bitraf_seeds_from_index(
            dizima_index=diz_idx,
            min_period=32,
            max_seeds=16,
        )
        print(f"[i] Sementes (fallback) encontradas: {len(seeds)}")
        if not seeds:
            print("[!] Mesmo no fallback, nenhuma semente encontrada.")
            print("    Sugestão: reduzir min_period para 16 ou 8 dentro de discover_bitraf_seeds_from_index().")
            return

    print()
    print("===================================================================")
    print("SEMENTES BITRAF SELECIONADAS")
    print("===================================================================")
    for s in seeds:
        max_period = max(s.periods.values())
        print(
            f"- {s.id:24s} | n={s.best_n:4d} | maxP={max_period:4d} | "
            f"freq={s.freq:3d} | score={s.score:10.4f}"
        )

    print()
    # Escolhe a melhor semente
    best = seeds[0]
    print("-------------------------------------------------------------------")
    print("MELHOR SEMENTE SELECIONADA:")
    print("-------------------------------------------------------------------")
    print(f"id           : {best.id}")
    print(f"valor       : {best.valor}")
    print(f"freq        : {best.freq}")
    print(f"best_n      : {best.best_n}")
    print(f"best_diff   : {best.best_diff}")
    print(f"terminante? : {best.terminante_dec}")
    print(f"full_reptend: {best.full_reptend_dec}")
    print(f"períodos    : {best.periods}")
    print()
    try:
        stream = generate_bitraf_stream(best, base=2, length=256)
        print("Fluxo[256 bits]:")
        print(stream)
    except Exception as e:
        print(f"[!] Não foi possível gerar fluxo: {e}")

    print()
    print("=== FIM RAFAELIA_BITRAF_PRIME_CORE – use estas sementes em Bitraf/T.I. ===")


if __name__ == "__main__":
    main()
