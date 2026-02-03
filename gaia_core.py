#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from hashlib import sha3_256
from pathlib import Path
from typing import Iterable

DEFAULT_EXCLUDE_DIRS = {".git", "__pycache__"}


@dataclass(frozen=True)
class ManifestEntry:
    path: str
    size: int
    sha3_256: str


def parse_extensions(ext_arg: str | None) -> set[str] | None:
    if not ext_arg:
        return None
    raw = [item.strip() for item in ext_arg.split(",") if item.strip()]
    normalized = set()
    for item in raw:
        normalized.add(item if item.startswith(".") else f".{item}")
    return normalized or None


def iter_files(root: Path, exclude_dirs: set[str]) -> Iterable[Path]:
    for path in root.rglob("*"):
        if path.is_dir():
            if path.name in exclude_dirs:
                continue
            continue
        if any(part in exclude_dirs for part in path.parts):
            continue
        yield path


def sha3_256_hex(path: Path, prefer_openssl: bool, errors: list[str], strict: bool) -> str:
    if prefer_openssl:
        openssl = shutil.which("openssl")
        if openssl:
            result = subprocess.run(
                [openssl, "dgst", "-sha3-256", "-r", str(path)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                if output:
                    return output.split(" ")[0]
            errors.append(f"openssl_failed:{path}")
            if strict:
                raise RuntimeError(f"OpenSSL SHA3-256 failed for {path}")

    digest = sha3_256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def build_manifest(
    root: Path,
    extensions: set[str] | None,
    exclude_dirs: set[str],
    prefer_openssl: bool,
    strict: bool,
    include_no_ext: bool,
) -> tuple[list[ManifestEntry], dict[str, int], list[str]]:
    entries: list[ManifestEntry] = []
    errors: list[str] = []
    total_bytes = 0

    for path in sorted(iter_files(root, exclude_dirs)):
        if extensions is not None and path.suffix.lower() not in extensions:
            if not (include_no_ext and path.suffix == ""):
                continue
        rel_path = path.relative_to(root).as_posix()
        try:
            size = path.stat().st_size
            digest = sha3_256_hex(path, prefer_openssl, errors, strict)
        except Exception as exc:  # noqa: BLE001 - narrow handling is not required for CLI
            errors.append(f"read_failed:{rel_path}:{exc}")
            if strict:
                raise
            continue
        entries.append(ManifestEntry(path=rel_path, size=size, sha3_256=digest))
        total_bytes += size

    summary = {
        "files": len(entries),
        "bytes": total_bytes,
        "errors": len(errors),
    }
    return entries, summary, errors


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_jsonl(path: Path, entries: list[ManifestEntry]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(
                json.dumps(
                    {"path": entry.path, "size": entry.size, "sha3_256": entry.sha3_256},
                    ensure_ascii=False,
                )
                + "\n"
            )


def write_md(path: Path, summary: dict[str, int], entries: list[ManifestEntry], errors: list[str]) -> None:
    lines = [
        "# Manifesto GAIA_CORE",
        "",
        "## Resumo",
        f"- Arquivos: {summary['files']}",
        f"- Bytes: {summary['bytes']}",
        f"- Erros: {summary['errors']}",
        "",
        "## Arquivos",
        "| Caminho | Bytes | SHA3-256 |",
        "|---|---:|---|",
    ]
    for entry in entries:
        lines.append(f"| `{entry.path}` | {entry.size} | `{entry.sha3_256}` |")
    if errors:
        lines.extend(["", "## Erros"])
        lines.extend([f"- {error}" for error in errors])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_outputs(
    out_dir: Path,
    formats: set[str],
    root_label: str,
    extensions: set[str] | None,
    summary: dict[str, int],
    entries: list[ManifestEntry],
    errors: list[str],
) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    payload = {
        "root": root_label,
        "filters": {
            "extensions": sorted(extensions) if extensions else None,
        },
        "summary": summary,
        "errors": errors,
        "entries": [
            {"path": entry.path, "size": entry.size, "sha3_256": entry.sha3_256}
            for entry in entries
        ],
    }

    if "json" in formats:
        json_path = out_dir / "manifest.json"
        write_json(json_path, payload)
        outputs.append(json_path)

    if "jsonl" in formats:
        jsonl_path = out_dir / "manifest.jsonl"
        write_jsonl(jsonl_path, entries)
        outputs.append(jsonl_path)

    if "md" in formats:
        md_path = out_dir / "manifest.md"
        write_md(md_path, summary, entries, errors)
        outputs.append(md_path)

    return outputs


def run_manifest(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"[ERRO] Diretório raiz não encontrado: {root}")
        return 2

    extensions = parse_extensions(args.ext)
    exclude_dirs = set(DEFAULT_EXCLUDE_DIRS)
    if args.exclude_dir:
        exclude_dirs.update(args.exclude_dir)

    try:
        entries, summary, errors = build_manifest(
            root=root,
            extensions=extensions,
            exclude_dirs=exclude_dirs,
            prefer_openssl=args.openssl,
            strict=args.strict,
            include_no_ext=args.include_no_ext,
        )
    except Exception as exc:  # noqa: BLE001 - CLI should surface any manifest errors
        print(f"[ERRO] Falha ao gerar manifesto: {exc}")
        return 2

    if args.dry_run:
        print("[DRY-RUN] Manifesto gerado em memória.")
        print(json.dumps({"summary": summary, "errors": errors}, ensure_ascii=False))
        return 1 if args.strict and errors else 0

    formats = {fmt.strip().lower() for fmt in args.format.split(",") if fmt.strip()}
    if not formats:
        formats = {"json"}

    out_dir = Path(args.out_dir).resolve()
    outputs = write_outputs(
        out_dir=out_dir,
        formats=formats,
        root_label=args.root,
        extensions=extensions,
        summary=summary,
        entries=entries,
        errors=errors,
    )

    print("[OK] Manifesto gerado:")
    for output in outputs:
        print(f"- {output}")

    return 1 if args.strict and errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gaia_core",
        description="GAIA_CORE CLI: manifesto determinístico e utilitários básicos.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    manifest = subparsers.add_parser(
        "manifest",
        help="Gera manifesto determinístico (JSON/JSONL/MD) com SHA3-256.",
    )
    manifest.add_argument(
        "--root",
        default=os.getcwd(),
        help="Diretório raiz para varredura (default: diretório atual).",
    )
    manifest.add_argument(
        "--ext",
        help="Extensões filtradas (ex.: .c,.h,.py). Se omitido, inclui tudo.",
    )
    manifest.add_argument(
        "--include-no-ext",
        action="store_true",
        help="Inclui arquivos sem extensão quando --ext estiver ativo.",
    )
    manifest.add_argument(
        "--exclude-dir",
        action="append",
        default=[],
        help="Diretórios para excluir (pode repetir).",
    )
    manifest.add_argument(
        "--format",
        default="json,jsonl,md",
        help="Formatos de saída: json,jsonl,md.",
    )
    manifest.add_argument(
        "--out-dir",
        default="./gaia_core_manifest",
        help="Diretório de saída para os manifests.",
    )
    manifest.add_argument(
        "--openssl",
        action="store_true",
        help="Preferir OpenSSL para SHA3-256 (fallback em hashlib).",
    )
    manifest.add_argument(
        "--dry-run",
        action="store_true",
        help="Não grava arquivos; apenas imprime o resumo.",
    )
    manifest.add_argument(
        "--strict",
        action="store_true",
        help="Falha se ocorrerem erros durante a varredura.",
    )
    manifest.set_defaults(func=run_manifest)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
