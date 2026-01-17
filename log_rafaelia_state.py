#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAFAELIA STATE LOGGER v1.0
--------------------------
Registra um estado RAFAELIA (A..E + ψχρΔΣΩ) em JSONL.

NORMS: ISO 25010 (confiabilidade), NIST 800-53 (audit), IEEE 12207.
SEAL : RAFCODE-Φ-BITRAF64  | Autor: ∆RafaelVerboΩ

Uso direto:

  RAFAELIA_A_LEVEL=7 \\
  RAFAELIA_B_SEED=53 \\
  RAFAELIA_C_ZIPRAF=multi_91 \\
  RAFAELIA_D_CONTEXT=Malta \\
  RAFAELIA_E_NCA=NCA-046 \\
  RAFAELIA_PSI="Benchmark FiberH" \\
  RAFAELIA_CHI="CPU 2800MHz, lanes6" \\
  RAFAELIA_DELTA="ajuste de blocos e lanes" \\
  RAFAELIA_SIGMA="MBps estáveis" \\
  RAFAELIA_OMEGA="bench_fiber_lanes6_mode.log" \\
  ./log_rafaelia_state.py "FIBER-H LANES6 256MiB BLOCK=1024"

O log é gravado em:
  - RAFAELIA_LOG_PATH (se definido), ou
  - ~/RAFAELIA_REALIZACOES.log.jsonl (padrão).
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def build_event(message: str) -> Dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()

    cwd = os.getcwd()
    script_name = os.path.basename(sys.argv[0]) or "log_rafaelia_state.py"
    cmdline = " ".join(sys.argv)

    # Vetores A..E (níveis e perfis)
    A_ethica_level = int(_env("RAFAELIA_A_LEVEL", "0"))
    B_seed_family = _env("RAFAELIA_B_SEED", "")
    C_zipraf_profile = _env("RAFAELIA_C_ZIPRAF", "")
    D_context_tag = _env("RAFAELIA_D_CONTEXT", "")
    E_nca_code = _env("RAFAELIA_E_NCA", "")

    # ψχρΔΣΩ (cognitivo)
    psi_intent = _env("RAFAELIA_PSI", "")
    chi_context = _env("RAFAELIA_CHI", "")
    rho_noise_str = _env("RAFAELIA_RHO", "")
    try:
        rho_noise = float(rho_noise_str) if rho_noise_str else None
    except ValueError:
        rho_noise = None

    delta_transmutation = _env("RAFAELIA_DELTA", "")
    sigma_synthesis = _env("RAFAELIA_SIGMA", "")
    omega_output_raw = _env("RAFAELIA_OMEGA", "")

    if omega_output_raw:
        omega_output: List[str] = [
            item.strip() for item in omega_output_raw.split(",") if item.strip()
        ]
    else:
        omega_output = []

    rafcode = _env("RAFAELIA_CODE", "RAFCODE-Φ-BITRAF64")

    core_material = "|".join(
        [
            now,
            message,
            str(A_ethica_level),
            B_seed_family,
            C_zipraf_profile,
            D_context_tag,
            E_nca_code,
            psi_intent,
            chi_context,
            str(rho_noise) if rho_noise is not None else "",
            delta_transmutation,
            sigma_synthesis,
            ",".join(omega_output),
            rafcode,
            cwd,
            cmdline,
        ]
    ).encode("utf-8", errors="ignore")

    core_hash_full = hashlib.sha3_256(core_material).hexdigest()
    run_id = core_hash_full[:16]

    event: Dict[str, Any] = {
        "timestamp_utc": now,
        "run_id": run_id,
        "script_name": script_name,
        "cwd": cwd,
        "cmdline": cmdline,
        "message": message,
        "A_ethica_level": A_ethica_level,
        "B_seed_family": B_seed_family,
        "C_zipraf_profile": C_zipraf_profile,
        "D_context_tag": D_context_tag,
        "E_nca_code": E_nca_code,
        "psi_intent": psi_intent,
        "chi_context": chi_context,
        "rho_noise": rho_noise,
        "delta_transmutation": delta_transmutation,
        "sigma_synthesis": sigma_synthesis,
        "omega_output": omega_output,
        "core_hash": core_hash_full,
        "rafcode": rafcode,
    }

    return event


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Uso: RAFAELIA_*=... log_rafaelia_state.py \"mensagem curta do evento\"",
            file=sys.stderr,
        )
        sys.exit(1)

    message = sys.argv[1]
    event = build_event(message)

    log_path = _env(
        "RAFAELIA_LOG_PATH",
        os.path.expanduser("~/RAFAELIA_REALIZACOES.log.jsonl"),
    )

    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"[RAFAELIA] Evento registrado em: {log_path}")
    print(f"[RAFAELIA] run_id={event['run_id']} core_hash={event['core_hash'][:24]}...")


if __name__ == "__main__":
    main()
