#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA_BITRAF_SEEDS_GEN
====================================================================
Generate:

  - RAFAELIA_BITRAF_SEEDS_MIN.py   (minimal Python module)
  - RAFAELIA_BITRAF_SEEDS_HEADER.h (C header)

from:
  - RAFAELIA_BITRAF_SEEDS.json

This JSON is produced by RAFAELIA_BITRAF_SEEDS_EXPORT.py and contains
for each DEN_n:

  den, p2, p8, p10, p16, maxP, sumP,
  phi_span_2pi, mean_radius, std_radius,
  score, tags, profiles.

The goal here is to create static artifacts that can be embedded into
kernels / C code / other Python modules without needing JSON at runtime.
====================================================================
"""

from __future__ import annotations

import json
from typing import Any, Dict, List


JSON_PATH = "RAFAELIA_BITRAF_SEEDS.json"
PY_MIN_PATH = "RAFAELIA_BITRAF_SEEDS_MIN.py"
C_HEADER_PATH = "RAFAELIA_BITRAF_SEEDS_HEADER.h"


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def gen_python_min(payload: Dict[str, Any]) -> str:
    seeds: List[Dict[str, Any]] = payload.get("seeds", [])
    profiles: Dict[str, Any] = payload.get("profiles", {})

    lines: List[str] = []
    lines.append("# -*- coding: utf-8 -*-")
    lines.append('"""')
    lines.append("RAFAELIA_BITRAF_SEEDS_MIN")
    lines.append("Auto-generated minimal module. DO NOT EDIT BY HAND.")
    lines.append('"""')
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("# List of Bitraf seeds with metrics")
    lines.append("BITRAF_SEEDS = [")
    for s in seeds:
        # We keep only essential fields; you can add/remove as needed.
        lines.append("    {")
        lines.append(f"        'den': {s['den']},")
        lines.append(f"        'p2': {s['p2']},")
        lines.append(f"        'p8': {s['p8']},")
        lines.append(f"        'p10': {s['p10']},")
        lines.append(f"        'p16': {s['p16']},")
        lines.append(f"        'maxP': {float(s['maxP'])},")
        lines.append(f"        'sumP': {float(s['sumP'])},")
        lines.append(f"        'phi_span_2pi': {float(s['phi_span_2pi'])},")
        lines.append(f"        'mean_radius': {float(s['mean_radius'])},")
        lines.append(f"        'std_radius': {float(s['std_radius'])},")
        lines.append(f"        'score': {float(s['score'])},")
        lines.append(f"        'tags': {s['tags']!r},")
        lines.append(f"        'profiles': {s.get('profiles', [])!r},")
        lines.append("    },")
    lines.append("]")
    lines.append("")
    lines.append("# Mapping from profile name to list of denominators")
    lines.append("BITRAF_PROFILES = {")
    for pname in profiles.keys():
        # compute dens for this profile
        dens = [
            int(s["den"])
            for s in seeds
            if pname in s.get("profiles", [])
        ]
        dens_str = ", ".join(str(d) for d in dens)
        lines.append(f"    {pname!r}: [{dens_str}],")
    lines.append("}")
    lines.append("")
    lines.append("__all__ = ['BITRAF_SEEDS', 'BITRAF_PROFILES']")
    lines.append("")
    return "\n".join(lines)


def gen_c_header(payload: Dict[str, Any]) -> str:
    seeds: List[Dict[str, Any]] = payload.get("seeds", [])
    profiles: Dict[str, Any] = payload.get("profiles", {})

    lines: List[str] = []
    lines.append("/*")
    lines.append(" * RAFAELIA_BITRAF_SEEDS_HEADER.h")
    lines.append(" * Auto-generated header. DO NOT EDIT BY HAND.")
    lines.append(" *")
    lines.append(" * Contains:")
    lines.append(" *   - struct RafaeliaBitrafSeed")
    lines.append(" *   - RAFAELIA_BITRAF_SEEDS[] array")
    lines.append(" *   - profile index lists (per profile)")
    lines.append(" */")
    lines.append("")
    lines.append("#ifndef RAFAELIA_BITRAF_SEEDS_HEADER_H")
    lines.append("#define RAFAELIA_BITRAF_SEEDS_HEADER_H")
    lines.append("")
    lines.append("#ifdef __cplusplus")
    lines.append('extern "C" {')
    lines.append("#endif")
    lines.append("")
    lines.append("#include <stddef.h>")
    lines.append("")
    lines.append("typedef struct {")
    lines.append("    int   den;")
    lines.append("    int   p2;")
    lines.append("    int   p8;")
    lines.append("    int   p10;")
    lines.append("    int   p16;")
    lines.append("    double maxP;")
    lines.append("    double sumP;")
    lines.append("    double phi_span_2pi;")
    lines.append("    double mean_radius;")
    lines.append("    double std_radius;")
    lines.append("    double score;")
    lines.append("} RafaeliaBitrafSeed;")
    lines.append("")
    lines.append("static const RafaeliaBitrafSeed RAFAELIA_BITRAF_SEEDS[] = {")
    for s in seeds:
        lines.append(
            "    { %d, %d, %d, %d, %d, %.10f, %.10f, %.10f, %.10f, %.10e, %.10f }," % (
                int(s["den"]),
                int(s["p2"]),
                int(s["p8"]),
                int(s["p10"]),
                int(s["p16"]),
                float(s["maxP"]),
                float(s["sumP"]),
                float(s["phi_span_2pi"]),
                float(s["mean_radius"]),
                float(s["std_radius"]),
                float(s["score"]),
            )
        )
    lines.append("};")
    lines.append("")
    lines.append("static const size_t RAFAELIA_BITRAF_SEEDS_COUNT = ")
    lines.append("    (sizeof(RAFAELIA_BITRAF_SEEDS) / sizeof(RafaeliaBitrafSeed));")
    lines.append("")

    # Profile arrays
    for pname in profiles.keys():
        dens = [
            int(s["den"])
            for s in seeds
            if pname in s.get("profiles", [])
        ]
        if not dens:
            continue
        arr_name = f"RAFAELIA_PROFILE_{pname}"
        lines.append("static const int %s[] = {" % arr_name)
        lines.append("    " + ", ".join(str(d) for d in dens) + ",")
        lines.append("};")
        lines.append(
            "static const size_t %s_COUNT = sizeof(%s) / sizeof(int);" % (
                arr_name,
                arr_name,
            )
        )
        lines.append("")

    lines.append("#ifdef __cplusplus")
    lines.append("}  /* extern \"C\" */")
    lines.append("#endif")
    lines.append("")
    lines.append("#endif /* RAFAELIA_BITRAF_SEEDS_HEADER_H */")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    print("===================================================================")
    print("RAFAELIA_BITRAF_SEEDS_GEN – generating Python + C artifacts")
    print("===================================================================")

    payload = load_json(JSON_PATH)

    py_text = gen_python_min(payload)
    with open(PY_MIN_PATH, "w", encoding="utf-8") as f:
        f.write(py_text)
    print(f"[OK] Generated {PY_MIN_PATH}")

    c_text = gen_c_header(payload)
    with open(C_HEADER_PATH, "w", encoding="utf-8") as f:
        f.write(c_text)
    print(f"[OK] Generated {C_HEADER_PATH}")


if __name__ == "__main__":
    main()
