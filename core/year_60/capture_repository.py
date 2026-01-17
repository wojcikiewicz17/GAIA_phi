from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET_DIR = ROOT / "core" / "year_60" / "snapshot"
MANIFEST = ROOT / "core" / "year_60" / "manifest.jsonl"
EXCLUDE_DIRS = {".git", "snapshot"}


def sha256_bytes(data: bytes) -> str:
    digest = hashlib.sha256()
    digest.update(data)
    return digest.hexdigest()


def should_skip(path: Path) -> bool:
    if ".git" in path.parts:
        return True
    if "core" in path.parts and "year_60" in path.parts:
        return True
    return False


def capture() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    entries = []

    for path in ROOT.rglob("*"):
        if path.is_dir():
            if path.name in EXCLUDE_DIRS:
                continue
            continue
        if should_skip(path):
            continue

        relative = path.relative_to(ROOT)
        target_path = TARGET_DIR / relative
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target_path)

        data = path.read_bytes()
        entries.append(
            {
                "path": relative.as_posix(),
                "size": len(data),
                "sha256": sha256_bytes(data),
            }
        )

    entries.sort(key=lambda item: item["path"])
    with MANIFEST.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    capture()
