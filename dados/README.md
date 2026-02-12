# dados/ — Laboratório expandido de código e artefatos

## Propósito
A pasta `dados/` funciona como um **laboratório operacional** com fontes C/Python, scripts de build, cabeçalhos de protocolo e artefatos de execução.

## Estrutura de arquivos (macrogrupos)
- **Core C e headers**: `omega_*.h`, `semantic_hash.c`, `mmap_nexus.c`, `infinite_attention.c`, `zipraf_db.c`, `vision_cortex.c`.
- **Build e automação**: `build_*.c`, `build_*.sh`, `RAFAELIA_*_RUN_ALL.sh`, snapshots e scripts de geração.
- **Pipelines Python RAFAELIA**: `RAFAELIA_*.py`, rotinas de análise, matriz, toroide, visualização e sementes.
- **Artefatos de dados**: `layer_*.zrf`, `gaia_semcore.vecdb`, imagens `.png/.svg`, checkpoints e arquivos auxiliares.
- **Binários experimentais**: executáveis gerados para validação prática local.

## Conceitos principais
1. **Sandbox de alta cadência**: área para prototipação e testes rápidos.
2. **Convergência código+dado**: scripts e artefatos convivem para ciclo curto de validação.
3. **Ponte com o core formal**: muitos componentes refletem ou antecipam módulos de `gaia_core_v2/`.

## Observação
Por conter artefatos e variantes históricas, `dados/` prioriza rastreabilidade experimental; para APIs estáveis, prefira `gaia_core_v2/`.
