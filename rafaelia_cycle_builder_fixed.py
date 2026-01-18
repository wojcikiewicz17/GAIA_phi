#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
RAFAELIA Cycle Builder (portable version)

Gera:
  - RAFAELIA_CYCLE_REPORT.md
  - RAFAELIA_CYCLE_INDEX.json

Salva no diretório atual (funciona no Termux).
"""

import os
import json
import hashlib
from datetime import datetime, timezone

OUT_REPORT = "RAFAELIA_CYCLE_REPORT.md"
OUT_INDEX = "RAFAELIA_CYCLE_INDEX.json"

def sha3_file(path):
    h = hashlib.sha3_256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def scan_tree(root="."):
    index = []
    for base, dirs, files in os.walk(root):
        for name in files:
            if name.endswith((".py", ".c", ".h", ".md", ".txt", ".json", ".sh")):
                path = os.path.join(base, name)
                try:
                    size = os.path.getsize(path)
                    h = sha3_file(path)
                    index.append({
                        "path": path,
                        "size": size,
                        "sha3_256": h
                    })
                except Exception as e:
                    index.append({
                        "path": path,
                        "error": str(e)
                    })
    return index

def build_report(index):
    lines = []
    lines.append("# RAFAELIA – Cycle Report")
    lines.append("")
    lines.append(f"Generated at: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    lines.append("## Files indexed")
    lines.append("")
    for item in index[:200]:
        if "sha3_256" in item:
            lines.append(f"- `{item['path']}` ({item['size']} bytes)  sha3={item['sha3_256'][:16]}…")
        else:
            lines.append(f"- `{item['path']}` ERROR: {item['error']}")
    lines.append("")
    lines.append("*(Full index in RAFAELIA_CYCLE_INDEX.json)*")
    return "\n".join(lines)

def main():
    print("[*] Scanning current directory tree...")
    index = scan_tree(".")

    with open(OUT_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    report = build_report(index)
    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write(report)

    print("[OK] Files generated:")
    print(" -", OUT_REPORT)
    print(" -", OUT_INDEX)

if __name__ == "__main__":
    main()
