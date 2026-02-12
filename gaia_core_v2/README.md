# gaia_core_v2/ — Núcleo C modular do ecossistema GAIA

## Propósito
`gaia_core_v2/` representa a camada mais formal do core em C, separando contratos públicos (`include/`) e implementações (`src/`).

## Estrutura de arquivos
- `include/`: headers de módulos (`gaia_hash.h`, `gaia_vector.h`, `gaia_metric.h`, `gaia_nexus.h`, `gaia_vecdb.h`, `gaia_zipraf.h`, etc.).
- `src/`: implementações correspondentes por domínio funcional.

## Conceitos principais
1. **Separação API/implementação**: reduz acoplamento e facilita evolução controlada.
2. **Determinismo operacional**: foco em rotinas previsíveis e mensuráveis.
3. **Composição por módulos**: hash, vetor, métrica, persistência e consulta como blocos independentes.
