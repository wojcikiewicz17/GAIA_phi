#!/bin/bash
LOGFILE="$HOME/FCEA_QUANTIC_MOUC/logs/daemon_status.txt"
touch "$LOGFILE"
tail -n 20 "$HOME/FCEA_QUANTIC_MOUC/logs/"*.log | tail -n 50 > "$LOGFILE"
dialog --title "♾️ QUANTIC MOUC STATUS" --textbox "$LOGFILE" 25 80
