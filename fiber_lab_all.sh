#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
#  RAFAELIA :: FIBER-H LAB ALL-IN-ONE v2.0
#  - Build do bench LANES6
#  - Build do Stress Lab (fiber_stress_lab + fiber_hash + fiber_hash_tree)
#  - Execução guiada: build | bench | stress | all
# ==============================================================================

set -o errexit
set -o nounset
set -o pipefail

BOLD="\033[1m"
RESET="\033[0m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
CYAN="\033[36m"

msg()  { printf "${CYAN}[INFO]${RESET} %s\n" "$*"; }
ok()   { printf "${GREEN}[OK]${RESET} %s\n" "$*"; }
warn() { printf "${YELLOW}[WARN]${RESET} %s\n" "$*"; }
err()  { printf "${RED}[ERRO]${RESET} %s\n" "$*"; }

cat << 'ART'
   ______ _ _                 _   _  _   _
  |  ____(_) |               | | | || | | |
  | |__   _| | ___  _ __ __ _| |_| || |_| |
  |  __| | | |/ _ \| '__/ _` | __|__   _  |
  | |    | | | (_) | | | (_| | |_   | | | |
  |_|    |_|_|\___/|_|  \__,_|\__|  |_| |_|

        RAFAELIA FIBER-H LAB ALL-IN-ONE v2.0
        Build · Bench LANES6 · Stress Lab (Tree)
ART

usage() {
    echo
    echo "${BOLD}Uso:${RESET}"
    echo "  ./fiber_lab_all.sh                -> build + bench + stress"
    echo "  ./fiber_lab_all.sh build          -> só compila tudo que for possível"
    echo "  ./fiber_lab_all.sh bench          -> compila (se preciso) e roda bench LANES6"
    echo "  ./fiber_lab_all.sh stress         -> compila (se possível) e roda Stress Lab"
    echo "  ./fiber_lab_all.sh help | -h      -> mostra esta ajuda"
    echo
    echo "${BOLD}Arquivos esperados:${RESET}"
    echo "  - bench_fiber_lanes6_mode.c"
    echo "  - fiber_stress_lab.c"
    echo "  - fiber_hash.c"
    echo "  - fiber_hash_tree.c  (gerado pelo fix)"
    echo
}

if [[ "${1:-}" == "help" || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
fi

# ----------------------------
#  BUILD: bench LANES6
# ----------------------------
build_bench() {
    if [[ ! -f bench_fiber_lanes6_mode.c ]]; then
        err "bench_fiber_lanes6_mode.c não encontrado."
        return 1
    fi

    msg "Compilando bench_fiber_lanes6_mode.c -> bench_fiber_lanes6_mode ..."
    if gcc -std=c99 -O3 -Wall -Wextra \
           bench_fiber_lanes6_mode.c \
           -o bench_fiber_lanes6_mode \
           -lm; then
        ok "Bench LANES6 compilado: ./bench_fiber_lanes6_mode"
    else
        err "Falha ao compilar bench_fiber_lanes6_mode.c"
        return 1
    fi
}

# ----------------------------
#  BUILD: Stress Lab
# ----------------------------
build_stress() {
    if [[ ! -f fiber_stress_lab.c ]]; then
        err "fiber_stress_lab.c não encontrado."
        return 1
    fi
    if [[ ! -f fiber_hash.c ]]; then
        err "fiber_hash.c não encontrado (necessário para fiber_h)."
        return 1
    fi
    if [[ ! -f fiber_hash_tree.c ]]; then
        err "fiber_hash_tree.c não encontrado (rode fix_fiber_tree_and_lab.sh)."
        return 1
    fi

    msg "Compilando Stress Lab -> fiber_stress_lab ..."
    if gcc -std=c99 -O3 -Wall -Wextra \
           fiber_stress_lab.c \
           fiber_hash.c \
           fiber_hash_tree.c \
           -o fiber_stress_lab \
           -lm; then
        ok "Stress Lab compilado: ./fiber_stress_lab"
    else
        err "Falha ao compilar/linkar Stress Lab."
        return 1
    fi
}

# ----------------------------
#  RUN: bench
# ----------------------------
run_bench() {
    if [[ ! -x ./bench_fiber_lanes6_mode ]]; then
        warn "bench_fiber_lanes6_mode não existe; tentando build..."
        build_bench || return 1
    fi
    msg "Rodando bench LANES6..."
    ./bench_fiber_lanes6_mode
}

# ----------------------------
#  RUN: stress
# ----------------------------
run_stress() {
    if [[ ! -x ./fiber_stress_lab ]]; then
        warn "fiber_stress_lab não existe; tentando build..."
        build_stress || return 1
    fi
    msg "Rodando Stress Lab (menu avalanche/monobit/stress)..."
    ./fiber_stress_lab
}

# ----------------------------
#  Dispatcher
# ----------------------------
MODE="${1:-all}"

case "$MODE" in
    build)
        build_bench || true
        build_stress || true
        ;;
    bench)
        build_bench || true
        run_bench
        ;;
    stress)
        build_stress || true
        run_stress
        ;;
    all)
        build_bench || true
        build_stress || true
        echo
        echo "-------------------------------------------"
        echo " BENCH LANES6 – EXECUTANDO"
        echo "-------------------------------------------"
        run_bench || warn "Falha ao executar bench LANES6."

        echo
        echo "-------------------------------------------"
        echo " STRESS LAB – EXECUTANDO"
        echo "-------------------------------------------"
        run_stress || warn "Falha ao executar Stress Lab."
        ;;
    *)
        err "Modo desconhecido: $MODE"
        usage
        exit 1
        ;;
esac

ok "fiber_lab_all.sh v2.0 finalizado."
