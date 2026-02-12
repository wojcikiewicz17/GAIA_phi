# gaia_core_v2/src/ — Implementações do core

## Conteúdo
Implementações C dos contratos definidos em `../include/`:
`gaia_hash.c`, `gaia_vector.c`, `gaia_metric.c`, `gaia_nexus.c`, `gaia_vecdb.c`, `gaia_zipraf.c`, entre outros.

## Conceitos
1. **Correspondência 1:1 com headers** para manutenção previsível.
2. **Especialização por responsabilidade** (hash, memória, consulta, logging, quantização).
