#!/usr/bin/env bash
# RAFAELIA_BITRAF_RUN_ALL.sh
# Unified driver for the Bitraf + Toroid + Seeds pipeline.
# Design: simple, linear, fail-fast. Good for Termux.

set -euo pipefail

echo "==================================================================="
echo "RAFAELIA_BITRAF_RUN_ALL – full pipeline"
echo "==================================================================="
echo "[1/7] Generating RAFAELIA_DIZIMA_INDEX.tsv..."
python RAFAELIA_DIZIMA_INDEX_GERADOR.py

echo "[2/7] Building constant bridge (RAFAELIA_DIZIMA_CONSTANT_BRIDGE)..."
python RAFAELIA_DIZIMA_CONSTANT_BRIDGE.py

echo "[3/7] Discovering Bitraf seeds (PRIME_CORE + fallback)..."
python RAFAELIA_BITRAF_PRIME_CORE.py

echo "[4/7] Generating toroidal plots (v2)..."
python RAFAELIA_TOROID_PLOTS_v2.py

echo "[5/7] Exporting seeds + profiles to JSON..."
python RAFAELIA_BITRAF_SEEDS_EXPORT.py

echo "[6/7] Generating minimal Python module and C header..."
python RAFAELIA_BITRAF_SEEDS_GEN.py

echo "[7/7] Creating timestamped snapshot of current artifacts..."
./RAFAELIA_BITRAF_SNAPSHOT.sh

echo "-------------------------------------------------------------------"
echo "[OK] RAFAELIA Bitraf pipeline finished successfully."
echo "     Artifacts atuais:"
echo "       - RAFAELIA_TOROID_PLOTS_v2*.png / .svg"
echo "       - RAFAELIA_BITRAF_SEEDS.json"
echo "       - RAFAELIA_BITRAF_SEEDS_MIN.py"
echo "       - RAFAELIA_BITRAF_SEEDS_HEADER.h"
echo "     Snapshot salvo em RAFAELIA_BITRAF_SNAPSHOTS/<timestamp>/"
echo "==================================================================="
