#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""RAFAELIA Cycle Builder

Goal:
  - Read the extracted project folders (zips) and their Markdown docs.
  - Produce a single report that:
      (1) maps what exists (programs/modules)
      (2) extracts "commitments" (hypothesis/metric/baseline)
      (3) proposes a coherent ψ→χ→ρ→Δ→Σ→Ω cycle for iteration

No external deps.
"""

from __future__ import annotations

import os
import re
import json
import hashlib
import datetime as dt
from dataclasses import dataclass
from typing import List, Dict, Tuple


ROOTS = [
    ("FILES14_ENGINE_ND", "/mnt/data/_files14"),
    ("FILES19_MANDELBROT_ASM", "/mnt/data/_files19"),
    ("GAIA_PHI", "/mnt/data/_gaia/GAIA_phi-main"),
    ("RAFGITTOOLS", "/mnt/data/_rafgittools/RafGitTools-main"),
    ("LLAMA_RAFAELIA", "/mnt/data/_llamarafaelia/llamaRafaelia-master"),
]


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha3_256_hex(b: bytes) -> str:
    return hashlib.sha3_256(b).hexdigest()


def read_text(path: str, max_bytes: int = 200_000) -> str:
    with open(path, "rb") as f:
        data = f.read(max_bytes)
    try:
        return data.decode("utf-8", errors="replace")
    except Exception:
        return data.decode(errors="replace")


def find_files(root: str, exts: Tuple[str, ...]) -> List[str]:
    out = []
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith(exts):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def md_head(path: str, n_lines: int = 40) -> str:
    txt = read_text(path)
    lines = txt.splitlines()[:n_lines]
    return "\n".join(lines).strip()


def extract_h1_h2(md: str) -> List[str]:
    hs = []
    for line in md.splitlines():
        if line.startswith("# ") or line.startswith("## "):
            hs.append(line.strip())
    return hs[:40]


def project_fingerprint(root: str) -> Dict:
    # lightweight fingerprint: count files by extension + sha of README heads
    exts = [".c", ".h", ".cpp", ".cc", ".hpp", ".py", ".sh", ".kt", ".java", ".md", ".asm", ".s"]
    counts = {e: 0 for e in exts}
    total = 0
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            total += 1
            l = fn.lower()
            for e in exts:
                if l.endswith(e):
                    counts[e] += 1
                    break
    md_files = find_files(root, (".md",))
    head_concat = []
    for p in md_files[:6]:
        head_concat.append(md_head(p, 24))
    head_bytes = "\n\n---\n\n".join(head_concat).encode("utf-8", errors="replace")
    return {
        "root": root,
        "total_files": total,
        "counts": {k: v for k, v in counts.items() if v},
        "md_count": len(md_files),
        "md_head_sha3": sha3_256_hex(head_bytes),
    }


def summarize_project(name: str, root: str) -> Dict:
    md_files = find_files(root, (".md",))
    key_docs = []
    for p in md_files:
        base = os.path.basename(p).lower()
        if base in ("readme.md", "architecture.md", "methodology.md", "gaia_documentation.md", "llama_rafaelia_design.md", "rafaelia_implementation.md", "implementation_summary.md"):
            key_docs.append(p)
    if not key_docs:
        key_docs = md_files[:3]

    docs = []
    for p in key_docs[:6]:
        head = md_head(p, 60)
        hs = extract_h1_h2(head)
        docs.append({
            "path": p.replace("/mnt/data/", ""),
            "head": head,
            "headings": hs,
        })

    return {
        "name": name,
        "fingerprint": project_fingerprint(root),
        "docs": docs,
    }


def build_cycle_map(projects: List[Dict]) -> str:
    # Coherent cycle mapping across repos.
    return """## Ciclo ψ→χ→ρ→Δ→Σ→Ω (operacional, auditável)

**ψ (intenção)**
- Definir 1 hipótese por vez (ex.: “2 quadrados ⇒ 6 setores / assinatura hex”).
- Fixar *o que é observável* (métrica) e *contra o quê* (baseline).

**χ (observação)**
- Rodar geradores (ND / Mandelbrot / GAIA ingest) com parâmetros fixos.
- Registrar: tempo, seed, manifest, checksums/hashes.

**ρ (ruído = retorno)**
- FAIL ≠ erro moral; é **feedback do sistema**:
  - métrica fraca, baseline forte, ou hipótese mal especificada.
- Capturar delta, variância, distribuição (não só média).

**Δ (transmutação ética/técnica)**
- Patch mínimo (1–3 mudanças) → re-rodar.
- Trocar a métrica antes de “trocar a realidade”.

**Σ (memória coerente)**
- Guardar logs + hashes (SHA3), e “artefatos” (PGM/.mat, Nexus, ZipRaf).
- Indexar: GAIA Nexus/MMAP e/ou ZipRaf layers por tema (geometry/series/graph).

**Ω (completude prática)**
- Produzir 1 artefato utilizável:
  - CLI que gera imagem + manifest + hash
  - biblioteca (C) + teste
  - relatório (MD) com resultados reprodutíveis

> Regra: **nenhuma opinião externa entra no loop** — só dados (métrica/baseline/log)."""


def main() -> int:
    projects = []
    for name, root in ROOTS:
        if os.path.isdir(root):
            projects.append(summarize_project(name, root))

    out_md = []
    out_md.append(f"# RAFAELIA — Mapa dos Zips + Ciclo de Retroalimentação (auto-gerado)\n")
    out_md.append(f"Gerado em: `{now_utc()}`\n")

    # Quick map
    out_md.append("## Mapa rápido (o que existe)\n")
    for p in projects:
        fp = p["fingerprint"]
        counts = ", ".join([f"{k}:{v}" for k, v in sorted(fp["counts"].items())])
        out_md.append(f"- **{p['name']}** — arquivos={fp['total_files']} | md={fp['md_count']} | tipos=({counts}) | md_head_sha3={fp['md_head_sha3']}")

    out_md.append("\n---\n")

    # Cycle
    out_md.append(build_cycle_map(projects))
    out_md.append("\n---\n")

    # Per project distilled
    out_md.append("## Observação por projeto (extraído dos MDs)\n")

    for p in projects:
        out_md.append(f"### {p['name']}\n")
        fp = p["fingerprint"]
        out_md.append(f"- Root: `{fp['root']}`")
        out_md.append(f"- Fingerprint: files={fp['total_files']} md={fp['md_count']} md_head_sha3={fp['md_head_sha3']}")
        out_md.append("- O que isso é (1 linha):")

        # heuristic description
        name = p["name"]
        if "ENGINE_ND" in name:
            out_md.append("  - Motor SOC N-dimensional em C (toppling/avalanche), com OpenMP e bitstack atômico.")
            out_md.append("  - Papel no ciclo: **gerador de dinâmica + fonte de ruído/retorno** (ρ) + logs/hashes (Σ).")
        elif "MANDELBROT" in name:
            out_md.append("  - Suite Mandelbrot multi-ISA em Assembly, com probe runtime, PGM+manifest+.mat e metodologia de benchmark.")
            out_md.append("  - Papel no ciclo: **visualização determinística + prova de performance** (χ) + artefatos (Σ).")
        elif "GAIA" in name:
            out_md.append("  - Vetorização 3D determinística + memória persistente (MMAP Nexus) + atenção/scan + VecDB/ZipRaf.")
            out_md.append("  - Papel no ciclo: **memória coerente** (Σ) + consulta/atenção para integrar textos/imagens/logs.")
        elif "RAFGITTOOLS" in name:
            out_md.append("  - App Android (Kotlin) para Git/GitHub/Terminal; roadmap grande (muito do README é especificação/escopo).")
            out_md.append("  - Papel no ciclo: **orquestração/UX**: transformar os núcleos (C/ASM) em produto utilizável.")
        elif "LLAMA" in name:
            out_md.append("  - Fork de llama.cpp com módulo Rafaelia Baremetal (42 tools, bitraf/zipraf/rafstore/toroid).")
            out_md.append("  - Papel no ciclo: **camada de inferência/integração** (Ω), onde o corpus vira agente/serviço local.")
        else:
            out_md.append("  - (descrição não inferida)")

        out_md.append("\n**Docs-chave (heads):**")
        for d in p["docs"]:
            out_md.append(f"- `{d['path']}`")
            if d["headings"]:
                out_md.append("  - " + " | ".join(d["headings"][:8]))

        out_md.append("\n")

    # Practical next cycle
    out_md.append("---\n")
    out_md.append("## Próximo ciclo (1 semana, sem fantasia)\n")
    out_md.append("1) **Fixar artefato único de geometria**: `.mat` (files19) como fonte de verdade para parâmetros de rotação/escala + checksum.\n")
    out_md.append("2) **Rodar geração visual determinística**: Mandelbrot FIXED → PGM + manifest + sha256/sha3.\n")
    out_md.append("3) **Rodar dinâmica ND** com mesmos seeds → log de eventos + hash.\n")
    out_md.append("4) **Ingest no GAIA**: enviar (manifest + logs + notas) para Nexus/ZipRaf com tags `geometry/series/graph`.\n")
    out_md.append("5) **Commitment**: usar `rafaelia_commitment*.py` como validador (métrica/baseline) e anexar no ZipRaf layer correspondente.\n")
    out_md.append("6) **Ω produto mínimo**: um comando que retorna: `artefato + hash + delta + link do log`.\n")

    report = "\n".join(out_md).strip() + "\n"

    out_path = "/mnt/data/RAFAELIA_CYCLE_REPORT.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    # also emit a small JSON index
    idx = {
        "utc": now_utc(),
        "projects": [{"name": p["name"], **p["fingerprint"]} for p in projects],
        "report": "RAFAELIA_CYCLE_REPORT.md",
    }
    with open("/mnt/data/RAFAELIA_CYCLE_INDEX.json", "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)

    print(out_path)
    print("/mnt/data/RAFAELIA_CYCLE_INDEX.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
