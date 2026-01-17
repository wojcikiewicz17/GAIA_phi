#!/bin/bash
BASE="$HOME/FCEA_QUANTIC_MOUC"
ABS_DIR="$BASE/absence"
LOG="$BASE/logs/absence_$(date +%s).log"
INDEX="$ABS_DIR/index.txt"

echo "🌀 Iniciando AbsenceIndex: $(date)" >> "$LOG"
mkdir -p "$ABS_DIR"
echo "📁 Absence Index :: $(date)" > "$INDEX"

check_absence() {
  DESC="$1"
  CMD="$2"
  OUTPUT=$(eval "$CMD" 2>&1)
  if echo "$OUTPUT" | grep -qiE 'not found|no such file|fail|error|missing|indisponível|cannot|unavailable|undefined'; then
    echo "❌ $DESC — $CMD" >> "$INDEX"
  else
    echo "✅ $DESC — OK" >> "$INDEX"
  fi
}

# 🧬 CAMADA 1: SISTEMA
check_absence "termux-api (wifi)" "termux-wifi-connectioninfo"
check_absence "termux-api (battery)" "termux-battery-status"
check_absence "comando logcat" "logcat -d | tail -n 5"
check_absence "procrank" "procrank"
check_absence "toybox (free)" "toybox free"
check_absence "free -h fallback" "free -h"

# 🧬 CAMADA 2: REDE
check_absence "ping externo" "ping -c 1 1.1.1.1"
check_absence "resolução DNS" "getprop net.dns1"
check_absence "rota IP" "ip route"

# 🧬 CAMADA 3: USUÁRIO E AMBIENTE
check_absence "Variável \$USER" "echo \$USER"
check_absence "HOME disponível" "ls \$HOME"
check_absence ".bashrc presente" "ls -la \$HOME/.bashrc"

# 🧬 CAMADA 4: INTERPRETAÇÃO SIMBÓLICA
check_absence "RAFAELIA_BOOT_CORE presente" "test -f \$HOME/RAFAELIA_BOOT_CORE/RAFAELIA_BOOT.sh && echo ok"
check_absence "Daemon ativo" "test -f \$BASE/daemon/pid.txt && ps -p \$(cat \$BASE/daemon/pid.txt)"

echo "🧩 Indexação concluída: $(date)" >> "$LOG"
cat "$INDEX" >> "$LOG"
