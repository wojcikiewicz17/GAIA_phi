#!/data/data/com.termux/files/usr/bin/bash
# ==============================================================================
#  RAFAELIA :: FIBER-H PRINT_HEX FIX v1.0
#  - Marca print_hex como unused para limpar warning
#  - Recompila fiber_stress_lab via fiber_lab_all.sh (build)
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

   RAFAELIA FIBER-H PRINT_HEX FIX
   limpando warnings do Stress Lab
ART

if [[ ! -f fiber_stress_lab.c ]]; then
    err "fiber_stress_lab.c não encontrado no diretório atual."
    exit 1
fi

# Patch: adicionar atributo unused na função print_hex
if grep -q 'static void print_hex(const uint8_t h\[32\])' fiber_stress_lab.c; then
    msg "Marcando print_hex como __attribute__((unused)) em fiber_stress_lab.c..."
    sed -i 's/static void print_hex(const uint8_t h\[32\]) {/static void __attribute__((unused)) print_hex(const uint8_t h[32]) {/' fiber_stress_lab.c
    ok "print_hex agora possui atributo unused."
else
    warn "Assinatura exata de print_hex não encontrada; nenhuma alteração feita."
fi

# Rebuild somente o Stress Lab, se fiber_lab_all.sh existir
if [[ -x ./fiber_lab_all.sh ]]; then
    msg "Recompilando Stress Lab via ./fiber_lab_all.sh build..."
    ./fiber_lab_all.sh build || warn "Build via fiber_lab_all.sh falhou; verifique saída acima."
else
    warn "fiber_lab_all.sh não encontrado ou não executável. Compile manualmente:"
    echo "  gcc -std=c99 -O3 -Wall -Wextra fiber_stress_lab.c fiber_hash.c fiber_hash_tree.c -o fiber_stress_lab -lm"
fi

ok "fix_fiber_printhex.sh concluído."
