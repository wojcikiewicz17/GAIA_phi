#!/bin/bash
BASE="$HOME/FCEA_QUANTIC_MOUC"
LOG="$BASE/logs/$(date +%s)_log.txt"
echo "♾️ Iniciando análise ultraestrutural segura" >> "$LOG"

ping -c 3 1.1.1.1 | tee "$BASE/echo/ping.log" | awk '/time=/{print $0 >> "'"$BASE"'/streams/latency_values.txt"}'
(termux-wifi-connectioninfo 2>/dev/null || echo "sem termux-api") >> "$BASE/streams/net_stats.txt"
(ip route 2>/dev/null || echo "ip route indisponível") >> "$BASE/streams/net_stats.txt"
(logcat -d 2>/dev/null | grep -Ei 'fail|overflow|error|irq|fault' || echo "logcat indisponível") >> "$BASE/irq/irq_faults.txt"
(procrank 2>/dev/null || echo "procrank indisponível") >> "$BASE/streams/mem_buffer.txt"
(toybox free 2>/dev/null || free -h) >> "$BASE/streams/mem_buffer.txt"

echo "✅ Análise QUANTIC_MOUC concluída: $(date)" >> "$LOG"
