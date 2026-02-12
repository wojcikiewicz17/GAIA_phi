# tests/ — Validação determinística do CLI e fixtures

## Propósito
A pasta `tests/` valida comportamento esperado de componentes principais, com foco no gerador de manifesto (`gaia_core.py`).

## Estrutura de arquivos
- `run_tests.sh`: script principal de execução.
- `fixtures/`: conjunto de entrada controlada para testes.
- `expected/`: saídas esperadas (`manifest.json`, `manifest.jsonl`, `manifest.md`).
- `smart_guard_cases.md`: casos de referência para camada de guard.

## Conceitos principais
1. **Reprodutibilidade**: mesmas entradas, mesmas saídas.
2. **Detecção de regressão**: comparação com baseline esperado.
