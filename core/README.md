# Core — Integração Multi‑Linguagem (C / ASM / Python / Rust)

Este diretório consolida a **metodologia de integração** do repositório para formar um núcleo (“core”) multi‑linguagem. O objetivo é garantir que **todos os arquivos** do projeto possam ser catalogados e organizados em uma visão única, respeitando as características de cada linguagem.

## Objetivo da refatoração
- **Centralizar** o mapa de arquivos existentes (C, ASM, Python, Rust e demais artefatos).
- **Padronizar** a visão de núcleo para uso em IA/automação.
- **Preservar** C/ASM **sem abstrações** ou dependências externas.
- **Manter a meta** de ~40KB por arquivo como referência para evolução futura do framework.

## Como gerar o índice do núcleo
O script abaixo varre o repositório inteiro (exceto `.git`) e gera `core/files_index.json`, que funciona como inventário da base.

```bash
python core/generate_core_index.py
```

## Estrutura produzida
- `core/files_index.json`: inventário completo, com contagem por linguagem/artefato.

## Convenções
- **C/ASM**: sem abstrações, sem dependências externas.
- **Python/Rust**: são tratados apenas como componentes de suporte e integração.
- **Fullstack enterprise**: o core é pensado como base para camada de serviços e automação.

> Este diretório é o ponto de convergência para a integração entre os arquivos já existentes no repositório.
