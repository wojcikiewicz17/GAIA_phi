#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

CC="${CC:-clang}"
CFLAGS="${CFLAGS:--O3 -march=native -Wall -Wextra}"

echo "[*] Building bench_compare_hashes..."
${CC} ${CFLAGS} bench_compare_hashes.c -o bench_compare_hashes

if [ ! -f FIBER_H_BENCH.log.jsonl ]; then
  echo "[*] No FIBER_H_BENCH.log.jsonl found, running bench_fiber_h_log.sh..."
  ./bench_fiber_h_log.sh
fi

./bench_compare_hashes
