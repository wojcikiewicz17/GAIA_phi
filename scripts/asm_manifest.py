#!/usr/bin/env python3
"""Generate assembly manifest with register/addressing auto-identification.

No external dependencies: Python stdlib only.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
from typing import Dict, List, Set

REGISTER_PATTERNS = {
    "x86_64": re.compile(r"\b%?(?:r(?:[0-9]|1[0-5]|[abcd]x|[sb]p|[sd]i)|e(?:ax|bx|cx|dx|sp|bp|si|di)|[abcd][lh])\b", re.IGNORECASE),
    "aarch64": re.compile(r"\b(?:[wx](?:[12]?\d|3[01])|sp|xzr|wzr)\b", re.IGNORECASE),
    "armv7": re.compile(r"\b(?:r(?:1?\d)|sp|lr|pc|ip)\b", re.IGNORECASE),
}

ADDRESSING_PATTERNS = [
    ("x86_mem", re.compile(r"\([^\)]*\)")),
    ("arm_bracket", re.compile(r"\[[^\]]+\]")),
    ("arm_literal", re.compile(r"=0x[0-9a-fA-F]+")),
    ("immediate", re.compile(r"[#$]-?0x?[0-9a-fA-F]+")),
]


def detect_arch(path: pathlib.Path) -> str:
    text = path.as_posix()
    if "x86_64" in text:
        return "x86_64"
    if "aarch64" in text:
        return "aarch64"
    if "armv7" in text:
        return "armv7"
    return "generic"


def parse_source(path: pathlib.Path) -> Dict[str, List[str]]:
    content = path.read_text(encoding="utf-8")
    arch = detect_arch(path)
    reg_pattern = REGISTER_PATTERNS.get(arch)

    registers: Set[str] = set()
    if reg_pattern:
        registers.update(m.group(0).lower() for m in reg_pattern.finditer(content))

    addressing: Set[str] = set()
    for label, pattern in ADDRESSING_PATTERNS:
        if pattern.search(content):
            addressing.add(label)

    return {
        "arch": arch,
        "registers": sorted(registers),
        "addressing_modes": sorted(addressing),
    }


def find_object_files(build_root: pathlib.Path, stem: str) -> List[pathlib.Path]:
    return sorted(build_root.rglob(f"{stem}.S.o")) + sorted(build_root.rglob(f"{stem}.s.o"))


def collect_symbols(obj_file: pathlib.Path) -> List[str]:
    try:
        out = subprocess.check_output(["nm", "-g", str(obj_file)], text=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    symbols = []
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 3:
            symbols.append(parts[2])
    return sorted(set(symbols))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", required=True)
    ap.add_argument("--build-root", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    source_root = pathlib.Path(args.source_root)
    build_root = pathlib.Path(args.build_root)
    output = pathlib.Path(args.output)

    entries = []
    for src in sorted(source_root.rglob("*.S")):
        parsed = parse_source(src)
        stem = src.stem
        obj_files = find_object_files(build_root, stem)
        entry = {
            "source": src.as_posix(),
            **parsed,
            "objects": [p.as_posix() for p in obj_files],
            "symbols": sorted({s for obj in obj_files for s in collect_symbols(obj)}),
        }
        entries.append(entry)

    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": 1,
        "entries": entries,
    }
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"[asm_manifest] wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
