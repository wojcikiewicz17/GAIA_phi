#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
#  RAFAELIA :: FIBER-H TREE+LAB FIX v2.0
#  - Implementa fiber_h_tree (fiber_hash_tree.c)
#  - Corrige warning de HEX em fiber_stress_lab.c
#  - Recria fiber_lab_all.sh compilando com fiber_hash_tree.c
# ==============================================================================

set -o errexit
set -o nounset
set -o pipefail

BOLD="\033[1m"
RESET="\033[0m"
CYAN="\033[36m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"

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

   RAFAELIA FIBER-H TREE+LAB FIX v2.0
   fiber_h_tree · Stress Lab · All-in-one
ART

# ---------------------------------------------------------------------------
# 0) Verificações básicas
# ---------------------------------------------------------------------------
for f in fiber_hash.h fiber_stress_lab.c; do
    if [[ ! -f "$f" ]]; then
        err "Arquivo obrigatório não encontrado: $f"
        exit 1
    fi
done
ok "Arquivos base encontrados (fiber_hash.h, fiber_stress_lab.c)."

# ---------------------------------------------------------------------------
# 1) Criar/atualizar fiber_hash_tree.c com implementação real de fiber_h_tree
# ---------------------------------------------------------------------------
msg "Gerando/atualizando fiber_hash_tree.c (implementação de fiber_h_tree)..."

cat << 'EOF_TREE_IMPL' > fiber_hash_tree.c
/*
 * FIBER-H – Tree Mode (fiber_hash_tree.c)
 * ---------------------------------------
 * Implementação simples de hash em árvore sobre o kernel fiber_h().
 *
 *  - Divide a mensagem em folhas de tamanho leaf_size (última pode ser menor).
 *  - Calcula fiber_h() de cada folha -> vetor de hashes de 32 bytes.
 *  - Sobe a árvore combinando pares: H_parent = fiber_h( H_left || H_right ).
 *  - Se número de nós for ímpar, o último é duplicado (right = left).
 *
 * Observação:
 *  - Este módulo PODE usar malloc/free, isolando heap do kernel núcleo.
 */

#include "fiber_hash.h"
#include <stdlib.h> /* malloc, free */

void fiber_h_tree(const fiber_u8 *data,
                  fiber_size_t len,
                  fiber_u8 out[32],
                  fiber_size_t leaf_size)
{
    /* Casos degenerados: usa direto o kernel base */
    if (!data || len == 0) {
        fiber_h((const fiber_u8 *)"", (fiber_size_t)0, out);
        return;
    }
    if (leaf_size == 0 || leaf_size >= len) {
        fiber_h(data, len, out);
        return;
    }

    /* Número de folhas (ceil) */
    fiber_size_t n_leaves = (len + leaf_size - 1u) / leaf_size;

    /* Cada folha gera 32 bytes */
    fiber_u8 *hashes = (fiber_u8 *)malloc((size_t)n_leaves * 32u);
    if (!hashes) {
        /* Fallback: sem memória, volta para modo linear */
        fiber_h(data, len, out);
        return;
    }

    /* 1) Hash de cada folha */
    for (fiber_size_t i = 0; i < n_leaves; ++i) {
        fiber_size_t offset = i * leaf_size;
        fiber_size_t chunk_len = leaf_size;
        if (offset + chunk_len > len) {
            chunk_len = len - offset;
        }
        fiber_h(data + offset, chunk_len, hashes + (i * 32u));
    }

    /* 2) Sobe árvore até restar apenas 1 nó (raiz) */
    fiber_size_t cur_nodes = n_leaves;
    while (cur_nodes > 1u) {
        fiber_size_t next_nodes = (cur_nodes + 1u) / 2u;

        for (fiber_size_t i = 0; i < next_nodes; ++i) {
            fiber_u8 buf[64];
            fiber_u8 *left  = hashes + (size_t)(2u * i) * 32u;
            fiber_u8 *right = NULL;

            if ((2u * i + 1u) < cur_nodes) {
                right = hashes + (size_t)(2u * i + 1u) * 32u;
            } else {
                /* Duplicamos o último nó se não houver par */
                right = left;
            }

            for (int j = 0; j < 32; ++j) {
                buf[j]      = left[j];
                buf[32 + j] = right[j];
            }

            fiber_h(buf, (fiber_size_t)64u, hashes + (i * 32u));
        }

        cur_nodes = next_nodes;
    }

    /* 3) A raiz é o hash final */
    for (int j = 0; j < 32; ++j) {
        out[j] = hashes[j];
    }

    free(hashes);
}
EOF_TREE_IMPL

ok "fiber_hash_tree.c escrito com sucesso."

# ---------------------------------------------------------------------------
# 2) Corrigir warning de HEX em fiber_stress_lab.c
#    (trocar [16] por [] para evitar warning de 'unterminated-string')
# ---------------------------------------------------------------------------
if grep -q 'static const char HEX\[16\]' fiber_stress_lab.c; then
    msg "Corrigindo definição de HEX em fiber_stress_lab.c..."
    sed -i 's/static const char HEX\[16\]/static const char HEX[]/' fiber_stress_lab.c
    ok "HEX agora é static const char HEX[] (sem warning)."
else
    warn "Padrão 'static const char HEX[16]' não encontrado em fiber_stress_lab.c (nenhuma ação)."
fi

# ---------------------------------------------------------------------------
# 3) Recriar fiber_lab_all.sh apontando para fiber_hash_tree.c
# ---------------------------------------------------------------------------
msg "Recriando fiber_lab_all.sh (ALL-IN-ONE com tree)..."

cat << 'EOF_LAB_ALL' > fiber_lab_all.sh
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
EOF_LAB_ALL

chmod +x fiber_lab_all.sh

ok "fix_fiber_tree_and_lab.sh finalizado. Rode: ./fiber_lab_all.sh all"
