# GAIA_phi como framework experimental — roteiro reproduzível e mensurável

## 1) Método (pipeline) em 6–10 passos

1. **Definir diretório raiz do experimento**: escolher o caminho de entrada para varredura (`--root`).【F:gaia_core.py†L242-L246】
2. **Definir filtros de extensão**: informar extensões incluídas (`--ext`) ou omitir para incluir todas.【F:gaia_core.py†L247-L250】
3. **Configurar exclusões de diretórios**: repetir `--exclude-dir` para excluir caminhos não relevantes.【F:gaia_core.py†L251-L256】
4. **Varredura determinística do diretório**: a lista de arquivos é ordenada antes do processamento, garantindo ordem estável entre execuções equivalentes.【F:gaia_core.py†L34-L42】【F:gaia_core.py†L78-L81】
5. **Cálculo de hash SHA3‑256**: o hash é calculado por OpenSSL quando disponível (`--openssl`) ou por fallback em `hashlib` quando necessário.【F:gaia_core.py†L45-L64】【F:gaia_core.py†L267-L271】
6. **Geração de métricas de resumo**: total de arquivos, total de bytes e total de erros são coletados no resumo do manifesto.【F:gaia_core.py†L93-L97】
7. **Emissão de saídas em múltiplos formatos**: JSON, JSONL e Markdown podem ser gerados (`--format`).【F:gaia_core.py†L150-L176】【F:gaia_core.py†L258-L261】
8. **Modo dry‑run (opcional)**: execução sem gravação de arquivos, retornando apenas o resumo e erros.【F:gaia_core.py†L204-L207】【F:gaia_core.py†L272-L276】
9. **Modo strict (opcional)**: falha se houver erros durante a varredura (retorno ≠ 0).【F:gaia_core.py†L277-L281】【F:gaia_core.py†L228】

---

## 2) Métricas definidas

- **Tempo total (s)**: medido externamente por comando de tempo do sistema (ex.: `/usr/bin/time -p`).
- **Bytes/s**: `bytes` do manifesto dividido pelo tempo total em segundos. O total de bytes está no resumo do manifesto.【F:gaia_core.py†L93-L97】【F:tests/expected/manifest.json†L9-L13】
- **Taxa de erro**: `errors / files` com base no resumo do manifesto.【F:gaia_core.py†L93-L97】【F:tests/expected/manifest.json†L9-L13】
- **Cobertura de extensões**: proporção de arquivos processados em relação ao total de arquivos no dataset (definido no protocolo). O filtro por extensão é configurado por `--ext`.【F:gaia_core.py†L24-L31】【F:gaia_core.py†L247-L250】
- **Determinismo do output**: verificado pela ordem estável dos arquivos (`sorted(...)`) e pela comparação de `manifest.jsonl` entre execuções equivalentes.【F:gaia_core.py†L78-L81】【F:gaia_core.py†L105-L114】

---

## 3) Protocolo de experimento

### 3.1 Dataset de teste (estrutura de diretórios)

Usar o dataset mínimo já presente no repositório:

```
/tests/fixtures/sample
├── a.txt
├── b.c
└── sub/
    └── ignore.bin
```

Esse dataset é consistente com os fixtures de teste existentes.【F:tests/fixtures/sample/a.txt†L1】【F:tests/fixtures/sample/b.c†L1】【F:tests/fixtures/sample/sub/ignore.bin†L1】

### 3.2 Comandos de execução

**Manifesto com filtro de extensões** (gera JSON/JSONL/MD):
```bash
python3 gaia_core.py manifest \
  --root tests/fixtures/sample \
  --ext .txt,.c \
  --out-dir tests/output \
  --format json,jsonl,md \
  --strict
```

**Dry‑run (sem gravação)**:
```bash
python3 gaia_core.py manifest \
  --root tests/fixtures/sample \
  --ext .txt,.c \
  --dry-run
```

**Execução com OpenSSL (quando disponível)**:
```bash
python3 gaia_core.py manifest \
  --root tests/fixtures/sample \
  --ext .txt,.c \
  --out-dir tests/output \
  --format json,jsonl,md \
  --openssl
```

Os comandos acima seguem o CLI definido no próprio `gaia_core.py`.【F:gaia_core.py†L238-L281】

### 3.3 Formato de logs

O formato de log recomendado é o JSONL gerado por `manifest.jsonl`, que contém um objeto por linha com `path`, `size` e `sha3_256`.【F:gaia_core.py†L105-L114】【F:tests/expected/manifest.jsonl†L1-L2】

---

## 4) Baseline e delta (comparação entre execuções)

**Baseline**: executar o manifesto e preservar `manifest.jsonl` como referência.

**Delta**: executar novamente com os mesmos parâmetros e comparar os JSONL.

Exemplo de comparação:
```bash
python3 gaia_core.py manifest --root tests/fixtures/sample --ext .txt,.c --out-dir tests/baseline --format jsonl --strict
python3 gaia_core.py manifest --root tests/fixtures/sample --ext .txt,.c --out-dir tests/delta --format jsonl --strict

diff -u tests/baseline/manifest.jsonl tests/delta/manifest.jsonl
```

A comparação utiliza o JSONL emitido pelo próprio CLI e garante determinismo quando não há mudança de conteúdo.【F:gaia_core.py†L105-L114】【F:gaia_core.py†L163-L171】

---

## 5) Experimentos comparativos sugeridos (2)

1. **OpenSSL vs. fallback em hashlib**
   - **Hipótese testável**: comparar tempo total e bytes/s usando `--openssl` vs. sem `--openssl`.
   - **Comandos**: executar duas vezes o protocolo 3.2, uma com `--openssl` e outra sem.
   - **Evidência no código**: caminho preferencial via OpenSSL e fallback em `hashlib` estão implementados no CLI.【F:gaia_core.py†L45-L64】【F:gaia_core.py†L267-L271】

2. **Cobertura de extensões**
   - **Hipótese testável**: comparar o número de arquivos processados com `--ext .txt,.c` vs. sem `--ext`.
   - **Comandos**: rodar uma vez com filtro e outra sem filtro.
   - **Evidência no código**: o filtro de extensões é aplicado no pipeline com `--ext`.【F:gaia_core.py†L24-L31】【F:gaia_core.py†L78-L81】

---

## 6) Template de seção de paper

### Introdução
- Contextualizar o objetivo de um pipeline determinístico de manifesto e hash para auditoria de datasets e reprodutibilidade.
- Referenciar o CLI `gaia_core.py` como ponto de entrada experimental e os formatos de saída (JSON/JSONL/MD).【F:gaia_core.py†L231-L281】【F:README.md†L11-L86】

### Método
- Descrever o pipeline em etapas (seção 1), incluindo varredura determinística, filtro de extensões e cálculo SHA3‑256 (OpenSSL/fallback).【F:gaia_core.py†L34-L64】【F:gaia_core.py†L78-L81】
- Definir o dataset usado (seção 3.1).【F:tests/fixtures/sample/a.txt†L1】【F:tests/fixtures/sample/b.c†L1】
- Explicar o formato de logs JSONL e as métricas derivadas do resumo do manifesto.【F:gaia_core.py†L93-L114】【F:tests/expected/manifest.json†L9-L13】

### Resultados
- Relatar métricas de tempo, bytes/s, taxa de erro e determinismo a partir do manifesto e do tempo total medido externamente.
- Usar o diff entre JSONL de baseline e delta para demonstrar determinismo quando o dataset não muda.【F:gaia_core.py†L105-L114】【F:gaia_core.py†L163-L171】

### Limitações
- O CLI não registra tempo interno; métricas de tempo dependem de medição externa.
- O dataset de teste atual é mínimo (fixtures), exigindo ampliação para cenários maiores.【F:tests/fixtures/sample/a.txt†L1】【F:tests/fixtures/sample/b.c†L1】

### Próximos passos
- Incluir conjuntos de dados maiores e estratificados por extensão para medir cobertura e escalabilidade.
- Automatizar coleta de tempo e bytes/s em logs padronizados, mantendo compatibilidade com o manifesto atual.【F:gaia_core.py†L93-L114】【F:gaia_core.py†L105-L114】
