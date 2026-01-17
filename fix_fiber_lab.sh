#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
#  RAFAELIA :: FIBER-H LAB FIXER v1.0
#  - Corrige bench de avalanche (POSIX macro)
#  - Corrige Stress Lab (linha '#' solta)
#  - Corrige console (função duplicada run_decide_and_bench)
#  - Cria stub fiber_ops.h (compat com fiber_hash.h)
# ==============================================================================

set -o errexit
set -o nounset
set -o pipefail

# ----------------------------
#  ASCII Art (Minozinho)
# ----------------------------
cat << 'ART'
   ______ _ _                 _   _  _   _ 
  |  ____(_) |               | | | || | | |
  | |__   _| | ___  _ __ __ _| |_| || |_| |
  |  __| | | |/ _ \| '__/ _` | __|__   _  |
  | |    | | | (_) | | | (_| | |_   | | | |
  |_|    |_|_|\___/|_|  \__,_|\__|  |_| |_|

        RAFAELIA FIBER-H LAB FIXER
        Avalanche · Bench · Stress Lab
ART

# ----------------------------
#  Helpers de log
# ----------------------------
BOLD="\033[1m"
DIM="\033[2m"
RESET="\033[0m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
CYAN="\033[36m"

msg()  { printf "${CYAN}[INFO]${RESET} %s\n" "$*"; }
ok()   { printf "${GREEN}[OK]${RESET} %s\n" "$*"; }
warn() { printf "${YELLOW}[WARN]${RESET} %s\n" "$*"; }
err()  { printf "${RED}[ERRO]${RESET} %s\n" "$*"; }

usage() {
    echo
    echo "Uso:"
    echo "  ./fix_fiber_lab.sh          -> aplica todos os fixes padrão"
    echo "  ./fix_fiber_lab.sh --dry    -> mostra o que faria, sem alterar arquivos"
    echo "  ./fix_fiber_lab.sh -h       -> mostra esta ajuda"
    echo
    echo "Arquivos esperados no diretório atual:"
    echo "  - bench_fiber_lanes6_mode.c"
    echo "  - fiber_stress_lab.c"
    echo "  - fiber_console.sh"
    echo "  - fiber_hash.h"
    echo
}

DRY_RUN=0

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
elif [[ "${1:-}" == "--dry" ]]; then
    DRY_RUN=1
    warn "Modo DRY-RUN: nenhuma modificação será escrita em disco."
fi

# ----------------------------
#  Função de patch segura
# ----------------------------
apply_sed() {
    local desc="$1"
    shift
    if (( DRY_RUN )); then
        warn "[DRY] sed $*  # $desc"
    else
        msg "$desc"
        sed "$@"
    fi
}

apply_awk() {
    local desc="$1"
    shift
    if (( DRY_RUN )); then
        warn "[DRY] awk $*"
    else
        msg "$desc"
        awk "$@"
    fi
}

# ----------------------------
#  Verificações iniciais
# ----------------------------
need_file() {
    local f="$1"
    if [[ ! -f "$f" ]]; then
        err "Arquivo obrigatório não encontrado: $f"
        exit 1
    fi
}

need_file "bench_fiber_lanes6_mode.c"
need_file "fiber_stress_lab.c"
need_file "fiber_console.sh"
need_file "fiber_hash.h"

ok "Arquivos base encontrados."

# ==============================================================================
# 1) FIX: bench_fiber_lanes6_mode.c (macro POSIX para clock/time)
# ==============================================================================
if grep -q '_POSIX_C_SOURCE' bench_fiber_lanes6_mode.c 2>/dev/null; then
    ok "bench_fiber_lanes6_mode.c já possui _POSIX_C_SOURCE (nenhuma ação)."
else
    if (( DRY_RUN )); then
        warn "[DRY] Inseriria '#define _POSIX_C_SOURCE 199309L' no topo de bench_fiber_lanes6_mode.c"
    else
        msg "Inserindo macro POSIX em bench_fiber_lanes6_mode.c..."
        # Insere na primeira linha
        sed -i '1i#define _POSIX_C_SOURCE 199309L' bench_fiber_lanes6_mode.c
        ok "bench_fiber_lanes6_mode.c atualizado com _POSIX_C_SOURCE 199309L."
    fi
fi

# ==============================================================================
# 2) FIX: fiber_stress_lab.c (# solto que quebra o preprocessor)
# ==============================================================================
if grep -nE '^#\s*$' fiber_stress_lab.c >/dev/null 2>&1; then
    if (( DRY_RUN )); then
        warn "[DRY] Removeria linhas com '#' isolado em fiber_stress_lab.c (provável lixo pós-banner)."
    else
        msg "Removendo linhas com '#' isolado (préprocessador inválido) em fiber_stress_lab.c..."
        # Apenas no cabeçalho (primeiras 60 linhas) para evitar efeitos colaterais
        sed -i '1,60{/^#\s*$/d}' fiber_stress_lab.c
        ok "fiber_stress_lab.c sem '#' solto no cabeçalho."
    fi
else
    ok "fiber_stress_lab.c não possui '#' solto no cabeçalho (nenhuma ação)."
fi

# ==============================================================================
# 3) FIX: fiber_console.sh (função run_decide_and_bench duplicada)
# ==============================================================================
if (( DRY_RUN )); then
    if grep -q 'run_decide_and_bench()' fiber_console.sh; then
        warn "[DRY] Verificaria e removeria a segunda definição de run_decide_and_bench() em fiber_console.sh."
    fi
else
    if [[ "$(grep -c 'run_decide_and_bench()' fiber_console.sh || true)" -gt 1 ]]; then
        msg "Removendo segunda definição de run_decide_and_bench() em fiber_console.sh..."
        awk '
            /run_decide_and_bench\(\) \{/ {
                count++;
                if (count == 2) {
                    skip=1;
                }
            }
            skip && /# Fallback caso não exista ou falhe fiber_decide_and_bench\.sh/ {
                skip=0;
            }
            !skip { print }
        ' fiber_console.sh > fiber_console.sh.tmp
        mv fiber_console.sh.tmp fiber_console.sh
        ok "fiber_console.sh agora possui apenas uma definição de run_decide_and_bench()."
    else
        ok "fiber_console.sh já não possui duplicação de run_decide_and_bench()."
    fi
fi

# Garante permissão de execução
if (( ! DRY_RUN )); then
    chmod +x fiber_console.sh || true
fi

# ==============================================================================
# 4) FIX: Gerar stub fiber_ops.h se não existir
# ==============================================================================
if [[ -f "fiber_ops.h" ]]; then
    ok "fiber_ops.h já existe (nenhuma ação)."
else
    if (( DRY_RUN )); then
        warn "[DRY] Criaria stub fiber_ops.h mínimo para compatibilidade com fiber_hash.h."
    else
        msg "Criando stub fiber_ops.h mínimo..."
        cat << 'EOF_OPS' > fiber_ops.h
#ifndef FIBER_OPS_H
#define FIBER_OPS_H

/*
 * FIBER-OPS – Stub mínimo para builds scalar / laboratório
 * --------------------------------------------------------
 * - Mantém compatibilidade com fiber_hash.h
 * - Não define nenhuma API de LANES6 aqui.
 * - Quando o módulo real de micro-ops estiver pronto,
 *   basta substituir este arquivo pelo definitivo.
 */

#endif /* FIBER_OPS_H */
EOF_OPS
        ok "fiber_ops.h stub criado."
    fi
fi

# ==============================================================================
# 5) Sanity check dos scripts .sh
# ==============================================================================
if (( DRY_RUN )); then
    warn "[DRY] Não executarei bash -n nos scripts."
else
    msg "Rodando bash -n para validar sintaxe dos scripts..."
    if bash -n fiber_console.sh; then
        ok "fiber_console.sh: sintaxe OK."
    else
        err "fiber_console.sh: erro de sintaxe após patch!"
    fi

    if [[ -f "fiber_decide_and_bench.sh" ]]; then
        if bash -n fiber_decide_and_bench.sh; then
            ok "fiber_decide_and_bench.sh: sintaxe OK."
        else
            err "fiber_decide_and_bench.sh: erro de sintaxe!"
        fi
    else
        warn "fiber_decide_and_bench.sh não encontrado (ignorado)."
    fi

    if [[ -f "build_run_fiber_kernel.sh" ]]; then
        if bash -n build_run_fiber_kernel.sh; then
            ok "build_run_fiber_kernel.sh: sintaxe OK."
        else
            err "build_run_fiber_kernel.sh: erro de sintaxe!"
        fi
    fi
fi

# ==============================================================================
# 6) Resumo
# ==============================================================================
echo
echo "-------------------------------------------"
echo " RESUMO FIBER-H LAB FIXER"
echo "-------------------------------------------"
echo " - bench_fiber_lanes6_mode.c : POSIX macro _POSIX_C_SOURCE 199309L verificada/inserida."
echo " - fiber_stress_lab.c        : linha '#' solta removida (se existia)."
echo " - fiber_console.sh          : duplicação de run_decide_and_bench() sanada (se existia)."
echo " - fiber_ops.h               : stub criado se não existia."
echo
echo "Próximos passos sugeridos:"
echo "  1) Recompilar o bench LANES6:"
echo "       gcc -std=c99 -O3 -Wall -Wextra bench_fiber_lanes6_mode.c -o bench_fiber_lanes6_mode -lm"
echo "  2) Recompilar o Stress Lab (ajuste os .c do kernel conforme seu layout):"
echo "       gcc -std=c99 -O3 -Wall -Wextra fiber_stress_lab.c fiber_hash.c -o fiber_stress_lab -lm"
echo "  3) Executar:"
echo "       ./bench_fiber_lanes6_mode"
echo "       ./fiber_stress_lab            # menu interativo com avalanche/monobit/stress"
echo
ok "FIBER-H LAB FIX concluído."
