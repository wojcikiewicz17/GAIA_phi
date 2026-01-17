#!/usr/bin/env bash
set -euo pipefail

cc -O2 -fPIC -shared -o librafaelia_image.so rafaelia_image_ingest.c

echo "[OK] librafaelia_image.so built"
