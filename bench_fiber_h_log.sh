#!/data/data/com.termux/files/usr/bin/bash
# Run benchmark and log result as JSONL (for ISO 27001 / NIST CSF style auditing)

set -euo pipefail

LOG_FILE="FIBER_H_BENCH.log.jsonl"
TMP_OUT="$(mktemp)"

TOTAL_MIB="${1:-256}"
BLOCK_SIZE="${2:-1024}"

# Ensure bench_fiber_h exists
if [ ! -x ./bench_fiber_h ]; then
  echo "[*] bench_fiber_h not found, building..."
  CC="${CC:-clang}"
  CFLAGS="${CFLAGS:--O3 -march=native -Wall -Wextra}"
  CPU_FREQ_MHZ="${CPU_FREQ_MHZ:-2800.0}"
  ${CC} ${CFLAGS} -DFIBER_CPU_FREQ_MHZ=${CPU_FREQ_MHZ} bench_fiber_h.c fiber_hash.c -o bench_fiber_h
fi

echo "[*] Running FIBER-H benchmark (log mode)..."
./bench_fiber_h "${TOTAL_MIB}" "${BLOCK_SIZE}" | tee "${TMP_OUT}"

TIME_S=$(grep 'Time elapsed'   "${TMP_OUT}" | awk '{print $4}')
MBPS=$(grep 'Throughput'       "${TMP_OUT}" | awk '{print $4}')
CPB=$(grep 'Cycles per byte'   "${TMP_OUT}" | awk '{print $4}')
CHECKSUM=$(grep 'Checksum'     "${TMP_OUT}" | awk '{print $4}')

TEST_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
CPU_FREQ_MHZ="${CPU_FREQ_MHZ:-2800.0}"

JSON_ENTRY=$(cat <<-END_JSON
{"timestamp":"${TEST_DATE}",
 "algorithm":"FIBER-H",
 "version":"v1.1",
 "cpu_mhz":${CPU_FREQ_MHZ},
 "total_mib":${TOTAL_MIB},
 "block_size":${BLOCK_SIZE},
 "results":{"time_s":${TIME_S},"mbps":${MBPS},"cycles_per_byte":${CPB},"checksum":"${CHECKSUM}"}}
END_JSON
)

echo "${JSON_ENTRY}" >> "${LOG_FILE}"
echo "[*] Logged to ${LOG_FILE}"

rm -f "${TMP_OUT}"
