# gaia_core_v2/include/ — Contratos públicos do core

## Conteúdo
Headers que definem interfaces do núcleo:
- hashing (`gaia_hash.h`),
- vetores e projeção (`gaia_vector.h`, `gaia_projection.h`),
- métricas (`gaia_metric.h`),
- memória/nexus (`gaia_nexus.h`),
- persistência (`gaia_vecdb.h`, `gaia_zipraf.h`),
- utilidades (`gaia_error.h`, `gaia_log.h`, `gaia_quant.h`, `gaia_attention.h`).

## Conceitos
- **Contrato estável** para consumidores C.
- **Tipagem e semântica explícita** por domínio.
