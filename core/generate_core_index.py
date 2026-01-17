from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "core" / "files_index.json"

EXTENSION_GROUPS = {
    "c": {".c"},
    "headers": {".h"},
    "python": {".py"},
    "shell": {".sh"},
    "asm": {".s", ".S", ".asm"},
    "rust": {".rs"},
    "markdown": {".md"},
    "text": {".txt", ".log", ".jsonl", ".csv"},
    "binary": {".o", ".so", ".zip", ".zipraf", ".svg"},
}


def classify_path(path: Path) -> str:
    suffix = path.suffix.lower()
    for group, extensions in EXTENSION_GROUPS.items():
        if suffix in extensions:
            return group
    return "other"


def build_index() -> dict:
    files = []
    for path in ROOT.rglob("*"):
        if path.is_dir():
            if path.name == ".git":
                continue
            continue
        if ".git" in path.parts:
            continue
        relative = path.relative_to(ROOT).as_posix()
        files.append(relative)

    files.sort()
    grouped: dict[str, list[str]] = {key: [] for key in EXTENSION_GROUPS}
    grouped["other"] = []

    for file_path in files:
        group = classify_path(Path(file_path))
        grouped[group].append(file_path)

    summary = {group: len(entries) for group, entries in grouped.items()}
    summary["total"] = len(files)

    return {
        "root": ROOT.name,
        "summary": summary,
        "files": grouped,
    }


def main() -> None:
    index = build_index()
    OUTPUT.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
