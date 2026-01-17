#!/data/data/com.termux/files/usr/bin/bash
# ============================================================================
# RAFAELIA FIBER-H CONSOLE (v963↔999)
#  - Painel interativo / CLI para FIBER-H scalar / LANES6
#  - Integra: fiber_kernel_opt + fiber_decide_and_bench.sh + benches
#  - Foco: usabilidade, cores, métricas e disciplina Zero Trust
# ============================================================================

set -o errexit
set -o nounset
set -o pipefail

# ----------------------------
#  Cores / Estilo (ANSI)
# ----------------------------
BOLD="\033[1m"
DIM="\033[2m"
RESET="\033[0m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
CYAN="\033[36m"
WHITE="\033[37m"

# ----------------------------
#  Defaults de Execução
# ----------------------------
DEFAULT_BLOCK_SIZE=1024
DEFAULT_TOTAL_MIB=256
DEFAULT_SCRIPT="RAFCODE-Φ-BITRAF64"
DEFAULT_LOG_FILE="$HOME/RAFAELIA_REALIZACOES.log.jsonl"

# ----------------------------
#  Helpers visuais
# ----------------------------
print_line() {
    printf "${DIM}%s${RESET}\n" "────────────────────────────────────────────────────────────"
}

banner() {
    print_line
    printf "${BOLD}${CYAN} RAFAELIA :: FIBER-H CONSOLE v963↔999${RESET}\n"
    printf "${DIM} Kernel-Switch Inteligente · Zero Trust · IOPS Alto${RESET}\n"
    print_line
    cat << 'ART'
   ______ _ _                 _   _  _   _ 
  |  ____(_) |               | | | || | | |
  | |__   _| | ___  _ __ __ _| |_| || |_| |
  |  __| | | |/ _ \| '__/ _` | __|__   _  |
  | |    | | | (_) | | | (_| | |_   | | | |
  |_|    |_|_|\___/|_|  \__,_|\__|  |_| |_|

          F I B E R - H   K E R N E L
ART
    print_line
}

# ----------------------------
#  Verificações de ambiente
# ----------------------------

need_file() {
    # $1 = caminho, $2 = descrição
    if [[ ! -f "$1" ]]; then
        printf "${RED}[ERRO]${RESET} Arquivo ausente: %s (%s)\n" "$1" "$2"
        return 1
    fi
}

need_exec() {
    # $1 = caminho, $2 = descrição
    if [[ ! -x "$1" ]]; then
        printf "${YELLOW}[WARN]${RESET} '%s' não é executável (%s). Tentando chmod +x...\n" "$1" "$2"
        chmod +x "$1" 2>/dev/null || {
            printf "${RED}[ERRO]${RESET} Falha ao tornar '%s' executável.\n" "$1"
            return 1
        }
    fi
}

# ----------------------------
#  Kernel: build + autotest
# ----------------------------

run_kernel_autotest() {
    print_line
    printf "${BOLD}${BLUE}[KERNEL] Auto-test FIBER-H KERNEL CORE${RESET}\n"

    if [[ -f "./build_run_fiber_kernel.sh" ]]; then
        need_exec "./build_run_fiber_kernel.sh" "Script de build do kernel"
        ./build_run_fiber_kernel.sh
    elif [[ -f "./fiber_kernel_opt" ]]; then
        need_exec "./fiber_kernel_opt" "Binário do kernel"
        ./fiber_kernel_opt
    else
        printf "${RED}[ERRO]${RESET} Nem build_run_fiber_kernel.sh nem fiber_kernel_opt encontrados.\n"
        return 1
    fi
}

# ----------------------------
#  Benchmark (decide + bench)
# ----------------------------
run_decide_and_bench() {
    local bs="${BLOCK_SIZE:-$DEFAULT_BLOCK_SIZE}"
    local mib="${TOTAL_MIB:-$DEFAULT_TOTAL_MIB}"

    print_line
    printf "${BOLD}${MAGENTA}[BENCH] Orquestrador FIBER-H${RESET}\n"
    printf "${DIM}BLOCK_SIZE = %s bytes · TOTAL_MIB = %s MiB · SCRIPT = \"%s\"${RESET}\n" \
        "$bs" "$mib" "${SCRIPT_CODE:-$DEFAULT_SCRIPT}"
    print_line

    if [[ -f "./fiber_decide_and_bench.sh" ]]; then
        need_exec "./fiber_decide_and_bench.sh" "Orquestrador de benchmark"
        if ! BLOCK_SIZE="$bs" TOTAL_MIB="$mib" SCRIPT="${SCRIPT_CODE:-$DEFAULT_SCRIPT}" \
             ./fiber_decide_and_bench.sh; then
            printf "${YELLOW}[WARN]${RESET} fiber_decide_and_bench.sh falhou. Fazendo fallback simples.\n"
            if ! fallback_simple_bench "$bs" "$mib"; then
                printf "${RED}[ERRO]${RESET} Fallback simples também falhou.\n"
                return 1
            fi
        fi
    else
        printf "${YELLOW}[WARN]${RESET} fiber_decide_and_bench.sh não encontrado. Fazendo fallback simples.\n"
        if ! fallback_simple_bench "$bs" "$mib"; then
            printf "${RED}[ERRO]${RESET} Fallback simples falhou.\n"
            return 1
        fi
    fi
}


# Fallback caso não exista ou falhe fiber_decide_and_bench.sh
fallback_simple_bench() {
    local bs="$1"
    local mib="$2"

    if (( bs <= 64 )); then
        printf "${CYAN}[INFO]${RESET} BLOCK_SIZE=%s → preferindo scalar (bench_fiber_h).\n" "$bs"
        if [[ -f "./bench_fiber_h.sh" ]]; then
            need_exec "./bench_fiber_h.sh" "Wrapper bench_fiber_h"
            BLOCK_SIZE="$bs" TOTAL_MIB="$mib" ./bench_fiber_h.sh
        elif [[ -f "./bench_fiber_h" ]]; then
            need_exec "./bench_fiber_h" "Binário bench_fiber_h"
            ./bench_fiber_h
        else
            printf "${RED}[ERRO]${RESET} bench_fiber_h(.sh) não encontrado.\n"
            return 1
        fi
    else
        printf "${CYAN}[INFO]${RESET} BLOCK_SIZE=%s → preferindo LANES6 (bench_fiber_lanes6_mode).\n" "$bs"
        if [[ -f "./run_bench_fiber_lanes6_mode.sh" ]]; then
            need_exec "./run_bench_fiber_lanes6_mode.sh" "Wrapper lanes6"
            BLOCK_SIZE="$bs" TOTAL_MIB="$mib" SCRIPT="${SCRIPT_CODE:-$DEFAULT_SCRIPT}" \
                ./run_bench_fiber_lanes6_mode.sh
        elif [[ -f "./bench_fiber_lanes6_mode" ]]; then
            need_exec "./bench_fiber_lanes6_mode" "Binário lanes6"
            BLOCK_SIZE="$bs" TOTAL_MIB="$mib" SCRIPT="${SCRIPT_CODE:-$DEFAULT_SCRIPT}" \
                ./bench_fiber_lanes6_mode
        else
            printf "${RED}[ERRO]${RESET} bench_fiber_lanes6_mode(.sh) não encontrado.\n"
            return 1
        fi
    fi
}

# ----------------------------
#  Stress / brute-style (BBS)
# ----------------------------

run_stress_loop() {
    local loops="${1:-5}"
    local bs="${BLOCK_SIZE:-$DEFAULT_BLOCK_SIZE}"
    local mib="${TOTAL_MIB:-$DEFAULT_TOTAL_MIB}"

    print_line
    printf "${BOLD}${YELLOW}[STRESS] Loop de benchmark estilo BBS${RESET}\n"
    printf "${DIM}Loops = %s · BLOCK_SIZE = %s · TOTAL_MIB = %s${RESET}\n" "$loops" "$bs" "$mib"

    for ((i=1; i<=loops; ++i)); do
        print_line
        printf "${BOLD}Rodada %d/%d${RESET}\n" "$i" "$loops"
        if ! BLOCK_SIZE="$bs" TOTAL_MIB="$mib" run_decide_and_bench; then
            printf "${RED}[ERRO]${RESET} Falha na rodada %d. Abortando stress.\n" "$i"
            return 1
        fi
    done
}

# ----------------------------
#  Visualizar últimos eventos RAFAELIA
# ----------------------------

show_last_events() {
    local file="${RAFAELIA_LOG:-$DEFAULT_LOG_FILE}"

    print_line
    printf "${BOLD}${BLUE}[LOG] Últimos eventos RAFAELIA (FIBER-H)${RESET}\n"
    printf "${DIM}Arquivo: %s${RESET}\n" "$file"

    if [[ ! -f "$file" ]]; then
        printf "${YELLOW}[WARN]${RESET} Arquivo de log não encontrado.\n"
        return 0
    fi

    tail -n 5 "$file" | sed "s/^/${DIM}> ${RESET}/"
}

# ----------------------------
#  Menu / Ajuda
# ----------------------------

usage() {
    cat << USAGE
Uso: ${BOLD}./fiber_console.sh${RESET} [comando] [opções]

Comandos principais:
  ${BOLD}menu${RESET}                 Abre menu interativo (padrão se nada for passado)
  ${BOLD}kernel${RESET}               Compila e roda o auto-test do kernel (fiber_kernel_opt)
  ${BOLD}bench${RESET}                Executa decisão + benchmark (kernel decide + bench real)
  ${BOLD}stress [N]${RESET}           Roda N loops de benchmark (default: 5) – estilo BBS
  ${BOLD}logs${RESET}                 Mostra últimos eventos RAFAELIA (FIBER-H) no JSONL
  ${BOLD}help${RESET}                 Mostra esta ajuda

Variáveis úteis (podem ser exportadas antes de rodar):
  BLOCK_SIZE   Tamanho do bloco (bytes) – ex: 64, 1024
  TOTAL_MIB    Tamanho total processado (MiB) – ex: 256, 512
  SCRIPT_CODE  Script de micro-ops (p.ex. "RAFCODE-Φ-BITRAF64")
  RAFAELIA_LOG Caminho do log JSONL (default: $DEFAULT_LOG_FILE)

Exemplos:
  BLOCK_SIZE=64 TOTAL_MIB=256 ./fiber_console.sh bench
  BLOCK_SIZE=1024 TOTAL_MIB=512 ./fiber_console.sh stress 10
  ./fiber_console.sh kernel
  ./fiber_console.sh logs
USAGE
}

menu_interativo() {
    while :; do
        banner
        printf "${BOLD}Selecione uma opção:${RESET}\n"
        printf "  [1] Kernel auto-test (T1/T3)\n"
        printf "  [2] Benchmark único (decide + bench)\n"
        printf "  [3] Stress test (loops)\n"
        printf "  [4] Ver últimos logs RAFAELIA\n"
        printf "  [5] Ajuda (help)\n"
        printf "  [0] Sair\n"
        print_line
        printf "${BOLD}Opção: ${RESET}"
        read -r opt

        case "$opt" in
            1) run_kernel_autotest ;;
            2) run_decide_and_bench ;;
            3)
                printf "Número de loops (default 5): "
                read -r loops
                [[ -z "${loops}" ]] && loops=5
                run_stress_loop "$loops"
                ;;
            4) show_last_events ;;
            5) usage ;;
            0)
                printf "Saindo.\n"
                break
                ;;
            *)
                printf "${RED}[ERRO]${RESET} Opção inválida.\n"
                ;;
        esac

        printf "\n[ENTER] para voltar ao menu..."
        read -r _
    done
}

# ----------------------------
#  Dispatch principal (CLI)
# ----------------------------

main() {
    local cmd="${1:-menu}"
    shift || true

    case "$cmd" in
        menu)
            menu_interativo
            ;;
        kernel)
            banner
            run_kernel_autotest
            ;;
        bench)
            banner
            run_decide_and_bench
            ;;
        stress)
            banner
            local loops="${1:-5}"
            run_stress_loop "$loops"
            ;;
        logs)
            banner
            show_last_events
            ;;
        help|-h|--help)
            banner
            usage
            ;;
        *)
            banner
            printf "${RED}[ERRO]${RESET} Comando desconhecido: %s\n" "$cmd"
            usage
            return 1
            ;;
    esac
}

main "$@"
