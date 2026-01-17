#!/usr/bin/env bash
# RAFAELIA_BITRAF_SNAPSHOT.sh
# Cria um snapshot versionado dos artefatos Bitraf/Toroid.

set -euo pipefail

BASE_DIR="${PWD}"
SNAP_BASE="${BASE_DIR}/RAFAELIA_BITRAF_SNAPSHOTS"

# Timestamp simples: AAAAMMDD_HHMMSS
TS="$(date +%Y%m%d_%H%M%S)"
SNAP_DIR="${SNAP_BASE}/${TS}"

echo "==================================================================="
echo "RAFAELIA_BITRAF_SNAPSHOT – criando snapshot em:"
echo "  ${SNAP_DIR}"
echo "==================================================================="

mkdir -p "${SNAP_DIR}"

# Arquivos principais de sementes
for f in \
  RAFAELIA_BITRAF_SEEDS.json \
  RAFAELIA_BITRAF_SEEDS_MIN.py \
  RAFAELIA_BITRAF_SEEDS_HEADER.h
do
  if [ -f "${f}" ]; then
    cp "${f}" "${SNAP_DIR}/"
  fi
done

# Plots v2 (PNG + SVG), se existirem
for f in \
  RAFAELIA_mean_radius_vs_phi_span_v2.png \
  RAFAELIA_mean_radius_vs_phi_span_v2.svg \
  RAFAELIA_maxP_vs_phi_span_v2.png \
  RAFAELIA_maxP_vs_phi_span_v2.svg \
  RAFAELIA_den_vs_phi_span_v2.png \
  RAFAELIA_den_vs_phi_span_v2.svg \
  RAFAELIA_den_vs_mean_radius_v2.png \
  RAFAELIA_den_vs_mean_radius_v2.svg
do
  if [ -f "${f}" ]; then
    cp "${f}" "${SNAP_DIR}/"
  fi
done

echo "[OK] Snapshot criado com sucesso:"
echo "     ${SNAP_DIR}"
echo "-------------------------------------------------------------------"
echo "Dica: use 'ls RAFAELIA_BITRAF_SNAPSHOTS' para ver o histórico."
echo "==================================================================="
