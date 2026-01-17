#!/data/data/com.termux/files/usr/bin/bash
# fiber_suite.sh
# End-to-end pipeline:
#  - Build core + bench
#  - Run self-test
#  - Run benchmark and log
#  - Run comparison view

set -euo pipefail

CC="${CC:-clang}"
CFLAGS="${CFLAGS:--O3 -march=native -Wall -Wextra}"
CPU_FREQ_MHZ="${CPU_FREQ_MHZ:-2800.0}"

TOTAL_MIB="${FIBER_TOTAL_MIB:-256}"
BLOCK_SIZE="${FIBER_BLOCK_SIZE:-1024}"

echo "[*] --- BUILD PHASE (Core + Bench) ---"
echo "[*] CC      : ${CC}"
echo "[*] CFLAGS  : ${CFLAGS}"
echo "[*] CPU_MHz : ${CPU_FREQ_MHZ}"
echo "[*] TOTAL_MIB  : ${TOTAL_MIB}"
echo "[*] BLOCK_SIZE : ${BLOCK_SIZE}"

${CC} ${CFLAGS} -DFIBER_CPU_FREQ_MHZ=${CPU_FREQ_MHZ} bench_fiber_h.c fiber_hash.c -o bench_fiber_h

echo "[*] --- SELF-TEST PHASE ---"
./bench_fiber_h selftest

echo "[*] --- BENCH + LOG PHASE ---"
chmod +x bench_fiber_h_log.sh
./bench_fiber_h_log.sh "${TOTAL_MIB}" "${BLOCK_SIZE}"

echo "[*] --- COMPARE PHASE ---"
chmod +x bench_compare_hashes.sh
./bench_compare_hashes.sh

echo "[*] Done."
