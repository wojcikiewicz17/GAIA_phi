#!/bin/bash
BASE="$HOME/FCEA_QUANTIC_MOUC"
DAEMON="$BASE/QUANTIC_MOUC_DAEMON.sh"
LOG="$BASE/logs/bootlog_$(date +%s).log"
echo "🚨 Ativando FCEA_MOUC_VECTORS_BOOT: $(date)" >> "$LOG"

if [ -x "$DAEMON" ]; then
  echo "🧠 Executando Daemon QUANTIC_MOUC..." >> "$LOG"
  nohup bash "$DAEMON" >> "$BASE/logs/daemon_nohup.log" 2>&1 &
  echo $! > "$BASE/daemon/pid.txt"
  echo "✅ Daemon ativo com PID $(cat $BASE/daemon/pid.txt)" >> "$LOG"
else
  echo "❌ Daemon não encontrado ou sem permissão de execução" >> "$LOG"
fi
