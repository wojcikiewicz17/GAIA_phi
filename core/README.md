# core/ — Indexação e captura estrutural

## Propósito
A pasta `core/` concentra utilitários para **inventário determinístico** da árvore do repositório e captura histórica de estado.

## Estrutura de arquivos
- `generate_core_index.py`: gera índice de arquivos em `core/files_index.json`.
- `files_index.json`: índice serializado da árvore no momento da execução.
- `year_60/`: submódulo de captura/snapshot com scripts em C e Python.

## Conceitos principais
1. **Inventário determinístico**: mapear a árvore para auditoria e rastreabilidade.
2. **Snapshot de estado**: registrar o estado de uma janela temporal (`year_60`) para inspeção comparativa.
3. **Suporte à governança técnica**: fornecer base para documentos analíticos em `docs/`.
