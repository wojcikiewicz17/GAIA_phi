#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
EXPECTED_DIR="$ROOT_DIR/tests/expected"
OUTPUT_DIR="$ROOT_DIR/tests/output"
DRY_DIR="$ROOT_DIR/tests/output_dry"

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

if ! command_exists python3; then
  echo "python3 não encontrado."
  exit 1
fi

rm -rf "$OUTPUT_DIR" "$DRY_DIR"

python3 "$ROOT_DIR/gaia_core.py" manifest \
  --root tests/fixtures/sample \
  --ext .txt,.c \
  --out-dir "$OUTPUT_DIR" \
  --format json,jsonl,md \
  --strict

diff -u "$EXPECTED_DIR/manifest.json" "$OUTPUT_DIR/manifest.json"
diff -u "$EXPECTED_DIR/manifest.jsonl" "$OUTPUT_DIR/manifest.jsonl"
diff -u "$EXPECTED_DIR/manifest.md" "$OUTPUT_DIR/manifest.md"

echo "Teste 1 OK: manifesto determinístico confere."

python3 "$ROOT_DIR/gaia_core.py" manifest \
  --root tests/fixtures/sample \
  --ext .txt,.c \
  --out-dir "$DRY_DIR" \
  --format json,jsonl,md \
  --dry-run

if [ -d "$DRY_DIR" ]; then
  if [ "$(find "$DRY_DIR" -type f | wc -l)" -ne 0 ]; then
    echo "Dry-run falhou: arquivos foram criados."
    exit 1
  fi
fi

echo "Teste 2 OK: dry-run não gerou arquivos."

set +e
python3 "$ROOT_DIR/gaia_core.py" manifest --root tests/fixtures/missing --strict
STATUS=$?
set -e

if [ "$STATUS" -eq 0 ]; then
  echo "Teste 3 falhou: strict deveria falhar em root inexistente."
  exit 1
fi

echo "Teste 3 OK: strict falhou em root inexistente."
