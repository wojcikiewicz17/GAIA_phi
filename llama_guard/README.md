# llama_guard/ — Guard rails semânticos e integração de segurança

## Propósito
A pasta `llama_guard/` implementa uma camada de proteção textual para classificação e mitigação de risco antes de geração/resposta.

## Estrutura de arquivos
- `smart_guard.{h,c}`: núcleo de decisão (ALLOW/WARN/BLOCK).
- `synonym_normalizer.{h,c}`: normalização lexical para robustez semântica.
- `llama_guard_integration.{h,c}`: integração com fluxo de inferência.
- `smart_guard_cli.c`: utilitário de linha de comando para validação.
- `bitstack_witness_q4.{h,c}`: wrapper de witness para blocos Q4.

## Conceitos principais
1. **Gate determinístico de risco**.
2. **Normalização prévia para reduzir variação lexical**.
3. **Integração modular com pipelines de inferência**.
