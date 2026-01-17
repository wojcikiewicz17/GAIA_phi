#!/data/data/com.termux/files/usr/bin/bash
# Simple wrapper for bench_fiber_h
set -euo pipefail

CC="${CC:-clang}"
CFLAGS="${CFLAGS:--O3 -march=native -Wall -Wextra}"

CPU_FREQ_MHZ="${CPU_FREQ_MHZ:-2800.0}"

echo "[*] Compiler : ${CC}"
echo "[*] CFLAGS   : ${CFLAGS}"
echo "[*] CPU_FREQ : ${CPU_FREQ_MHZ} MHz"

${CC} ${CFLAGS} -DFIBER_CPU_FREQ_MHZ=${CPU_FREQ_MHZ} bench_fiber_h.c fiber_hash.c -o bench_fiber_h

TOTAL_MIB="${1:-256}"
BLOCK_SIZE="${2:-1024}"

./bench_fiber_h "${TOTAL_MIB}" "${BLOCK_SIZE}"
