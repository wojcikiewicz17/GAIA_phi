#!/data/data/com.termux/files/usr/bin/bash
# ============================================================================
# RAFAELIA :: FIBER-H DECIDE & BENCH (v963↔999)
#  - Decide modo (scalar vs LANES6) com base em BLOCK_SIZE
#  - Executa o bench correspondente (bench_fiber_h / bench_fiber_lanes6_mode)
#  - Pensado para ser chamado pelo fiber_console.sh
# ============================================================================

set -o errexit
set -o nounset
set -o pipefail

# ----------------------------
#  Defaults de ambiente
# ----------------------------
BLOCK_SIZE="${BLOCK_SIZE:-1024}"          # bytes
TOTAL_MIB="${TOTAL_MIB:-256}"             # MiB
SCRIPT="${SCRIPT:-RAFCODE-Φ-BITRAF64}"    # script de micro-ops (para lanes6)

# ----------------------------
#  Helpers
# ----------------------------
info()  { printf "\033[36m[INFO]\033[0m %s\n"  "$*"; }
warn()  { printf "\033[33m[WARN]\033[0m %s\n"  "$*"; }
error() { printf "\033[31m[ERRO]\033[0m %s\n"  "$*"; }

need_exec() {
    local path="$1" desc="$2"
    if [[ ! -f "$path" ]]; then
        error "Arquivo não encontrado: $path ($desc)"
        return 1
    fi
    if [[ ! -x "$path" ]]; then
        warn  "'$path' não é executável ($desc). Tentando chmod +x..."
        chmod +x "$path" 2>/dev/null || {
            error "Falha ao tornar '$path' executável."
            return 1
        }
    fi
}

# ----------------------------
#  Decisão de modo (espelho do kernel)
# ----------------------------
decide_mode() {
    local b="$1"

    # Regras alinhadas ao fiber_kernel.c:
    #  - B <= 64  → scalar (singularidade de cache, ~120k MB/s)
    #  - B >= 1024 → LANES6 (vetorizado, ~1.8k MB/s, mais estável)
    #  - zona intermediária: <128 → scalar, senão LANES6
    if (( b <= 64 )); then
        printf "scalar\n"
    elif (( b >= 1024 )); then
        printf "lanes6\n"
    elif (( b < 128 )); then
        printf "scalar\n"
    else
        printf "lanes6\n"
    fi
}

# ----------------------------
#  Execução dos benchmarks
# ----------------------------
run_scalar_bench() {
    info "Modo escolhido: FIBER-H scalar (BLOCK_SIZE=${BLOCK_SIZE}, TOTAL_MIB=${TOTAL_MIB})"

    if [[ -f "./bench_fiber_h.sh" ]]; then
        need_exec "./bench_fiber_h.sh" "Wrapper bench_fiber_h"
        BLOCK_SIZE="$BLOCK_SIZE" TOTAL_MIB="$TOTAL_MIB" ./bench_fiber_h.sh
    elif [[ -f "./bench_fiber_h" ]]; then
        need_exec "./bench_fiber_h" "Binário bench_fiber_h"
        ./bench_fiber_h
    else
        error "bench_fiber_h(.sh) não encontrado."
        return 1
    fi
}

run_lanes6_bench() {
    info "Modo escolhido: FIBER-H LANES6 (BLOCK_SIZE=${BLOCK_SIZE}, TOTAL_MIB=${TOTAL_MIB}, SCRIPT=\"${SCRIPT}\")"

    if [[ -f "./run_bench_fiber_lanes6_mode.sh" ]]; then
        need_exec "./run_bench_fiber_lanes6_mode.sh" "Wrapper lanes6"
        BLOCK_SIZE="$BLOCK_SIZE" TOTAL_MIB="$TOTAL_MIB" SCRIPT="$SCRIPT" ./run_bench_fiber_lanes6_mode.sh
    elif [[ -f "./bench_fiber_lanes6_mode" ]]; then
        need_exec "./bench_fiber_lanes6_mode" "Binário lanes6"
        BLOCK_SIZE="$BLOCK_SIZE" TOTAL_MIB="$TOTAL_MIB" SCRIPT="$SCRIPT" ./bench_fiber_lanes6_mode
    else
        error "bench_fiber_lanes6_mode(.sh) não encontrado."
        return 1
    fi
}

# ----------------------------
#  Main
# ----------------------------
main() {
    printf "────────────────────────────────────────────────────────────\n"
    printf " Orquestrador FIBER-H (decide & bench)\n"
    printf " BLOCK_SIZE = %s bytes · TOTAL_MIB = %s MiB · SCRIPT = \"%s\"\n" \
        "$BLOCK_SIZE" "$TOTAL_MIB" "$SCRIPT"
    printf "────────────────────────────────────────────────────────────\n"

    local mode
    mode="$(decide_mode "$BLOCK_SIZE")"

    case "$mode" in
        scalar)
            run_scalar_bench
            ;;
        lanes6)
            run_lanes6_bench
            ;;
        *)
            error "Modo inválido decidido: $mode"
            return 1
            ;;
    esac
}

main "$@"
