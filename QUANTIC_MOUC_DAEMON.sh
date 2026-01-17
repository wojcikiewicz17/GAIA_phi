#!/bin/bash
BASE="$HOME/FCEA_QUANTIC_MOUC"
LOG="$BASE/logs/daemon_$(date +%s).log"
INTERVALO=60  # segundos

echo "🔄 QUANTIC_MOUC_DAEMON iniciado às $(date)" >> "$LOG"

while true; do
  TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$TIMESTAMP] ♾️ Ciclo ativo" >> "$LOG"

  ping -c 2 1.1.1.1 | tee "$BASE/echo/ping_$(date +%s).log" | awk '/time=/{print $0 >> "'"$BASE"'/streams/latency_values.txt"}'
  (termux-wifi-connectioninfo 2>/dev/null || echo "sem termux-api") >> "$BASE/streams/net_stats.txt"
  (ip route 2>/dev/null || echo "ip route indisponível") >> "$BASE/streams/net_stats.txt"
  (logcat -d 2>/dev/null | grep -Ei 'fail|overflow|error|irq|fault' || echo "logcat indisponível") >> "$BASE/irq/irq_faults.txt"
  (procrank 2>/dev/null || echo "procrank indisponível") >> "$BASE/streams/mem_buffer.txt"
  (toybox free 2>/dev/null || free -h) >> "$BASE/streams/mem_buffer.txt"

  echo "[$TIMESTAMP] ✅ Ciclo concluído" >> "$LOG"
  sleep "$INTERVALO"
done
