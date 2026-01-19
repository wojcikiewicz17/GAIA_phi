# GAIA-Ω (GAIA Phi)

## Resumo acadêmico
O projeto **GAIA-Ω** organiza um ecossistema experimental em C e Python voltado a vetorização semântica ultra‑compacta (3D), memória persistente mapeada em disco, busca aproximada por produto interno, protocolos IPC, e mecanismos de armazenamento compacto (VecDB/ZipRaf). O repositório também inclui motores matemáticos simbólicos “Rafaelia”, com foco em simulação de coexistência entre famílias algébricas e análise de convergência numérica. O objetivo é fornecer um laboratório reprodutível para investigar o acoplamento entre hashing semântico leve, estruturas de armazenamento persistente e pipelines de atenção/consulta em ambientes de baixa dimensão. 【F:GAIA_DOCUMENTATION.md†L1-L167】

## Auditoria de estabilidade
- [Auditoria de Estabilidade — GAIA-Ω (documento navegável)](docs/AUDITORIA_CORE_ESTAVEL.md)
- [GAIA_phi como framework experimental — roteiro reproduzível](docs/ROTEIRO_EXPERIMENTAL_GAIA_CORE.md)
- [Árvore estrutural de arquivos (inventário completo)](docs/ARVORE_ESTRUTURAL.md)
- [Análise de oportunidades, operações e inovações](docs/ANALISE_OPORTUNIDADES_OPERACOES.md)

---

## GAIA_CORE CLI (ponto de entrada)

O ponto de entrada padronizado para consolidar o core é o **CLI `gaia_core.py`**. Ele oferece o comando `manifest` para gerar um manifesto determinístico (JSON/JSONL/MD) com SHA3‑256, filtros por extensão, dry‑run e modo strict.

---

## Instalação (Linux/Termux)

Dependências mínimas:
- `python3` (obrigatório)
- `openssl` (opcional, usado para SHA3‑256 quando disponível)
- `gcc/cc` e `make` (para compilar os binários C quando necessário)

### Linux (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install -y python3 gcc make openssl
```

### Termux
```bash
pkg update
pkg install -y python clang make openssl
```

---

## Como rodar (CLI + build)

### Manifesto determinístico (Linux/Termux)
```bash
python3 gaia_core.py manifest --root . --ext .c,.h,.py --format json,jsonl,md --out-dir ./gaia_core_manifest --openssl
```

### Modo dry-run (não grava arquivos)
```bash
python3 gaia_core.py manifest --root . --ext .c,.h --dry-run
```

### Modo strict (falha se houver erro)
```bash
python3 gaia_core.py manifest --root . --ext .c,.h --strict
```

### Build C (Linux/Termux)
```bash
BASE_DIR="$PWD/gaia_omega_build" bash build_gaia.sh
BASE_DIR="$PWD/gaia_omega_build" bash build_vecdb.sh
BASE_DIR="$PWD/gaia_omega_build" bash build_commander_zipraf.sh
BASE_DIR="$PWD/gaia_omega_build" bash build_raf_log.sh
```

---

## Flags principais (CLI)

```text
manifest
  --root        Diretório raiz para varredura (default: diretório atual)
  --ext         Extensões filtradas (ex.: .c,.h,.py). Se omitido, inclui tudo
  --exclude-dir Diretórios excluídos (pode repetir)
  --format      json,jsonl,md (default: todos)
  --out-dir     Diretório de saída (default: ./gaia_core_manifest)
  --openssl     Preferir OpenSSL para SHA3-256 (fallback em hashlib)
  --dry-run     Não grava arquivos; apenas imprime resumo
  --strict      Falha se ocorrer erro durante a varredura
```

---

## Outputs gerados (manifest)

- `manifest.json` — estrutura completa com filtros, resumo e entradas.
- `manifest.jsonl` — um JSON por linha (path/size/sha3_256).
- `manifest.md` — relatório em Markdown com tabela e erros.

---

## Testes mínimos

```bash
bash tests/run_tests.sh
```

---

## Especificações Rafaelia/BitStack (novo núcleo)

- [SPEC_BITSTACK_WORLD_MODEL_V1.md](SPEC_BITSTACK_WORLD_MODEL_V1.md)
- [SPEC_SMART_GUARD_V1.md](SPEC_SMART_GUARD_V1.md)

---

## Smart Guard + Synonym Normalizer (C)

### Build rápido (Linux/Termux)
```bash
gcc -O2 -Wall -Wextra -I./llama_guard \
  llama_guard/smart_guard.c \
  llama_guard/synonym_normalizer.c \
  llama_guard/llama_guard_integration.c \
  llama_guard/smart_guard_cli.c \
  -o smart_guard_cli
```

### Uso (exemplo rápido)
```bash
./smart_guard_cli
```

### Integração em llama-cli / llama-server

1. **Antes da geração**: chame `llama_guard_gate_prompt(prompt, ...)`.
2. **BLOCK**: retornar `AVISA` e interromper geração.
3. **WARN**: retornar `AVISA` e gerar resposta cautelosa.
4. **ALLOW**: gerar normalmente.

O wrapper de witness para blocos Q4 está disponível em `llama_guard/bitstack_witness_q4.{h,c}`.

---

## RAFAELIA_CYCLE (tool extra em C)

Ferramenta adicional para indexação determinística com SHA3‑256 e relatórios JSON/JSONL/MD/CSV.

### Build (Linux)
```bash
sudo apt-get install -y gcc libssl-dev
gcc -O2 -Wall -Wextra rafaelia_cycle.c -o rafaelia_cycle -lssl -lcrypto
```

### Build (Termux)
```bash
pkg install -y clang openssl
clang -O2 -Wall -Wextra rafaelia_cycle.c -o rafaelia_cycle -lssl -lcrypto
```

### Execução
```bash
./rafaelia_cycle --base . --out-dir out --ext .c,.h,.py
```

---

## Motivação e escopo
1. **Vetorização mínima e determinística**: reduzir dimensionalidade a um vetor 3D preservando sinal semântico aproximado e custo constante de hashing. 【F:GAIA_DOCUMENTATION.md†L16-L43】
2. **Memória persistente e atenção**: testar busca linear por produto interno sobre memória mapeada (Nexus/MMAP), com janela de contexto virtual. 【F:GAIA_DOCUMENTATION.md†L74-L115】
3. **Armazenamento compacto multi‑camadas**: comparar VecDB (registros fixos e quantizados) e ZipRaf (camadas semânticas com CRC). 【F:GAIA_DOCUMENTATION.md†L33-L37】
4. **Engines simbólicas “Rafaelia”**: quantificar convergência e “dificuldade” de nós matemáticos em pipelines numericamente intensivos. 【F:GAIA_DOCUMENTATION.md†L130-L167】

---

## Arquitetura conceitual

```
[Texto/Binário] → [Hash Semântico] → [VectorVerb 3D]
                           │
                           ├──> [Nexus/MMAP] → [Atenção/Busca] → [Resposta]
                           │
                           └──> [VecDB/ZipRaf] → [Consulta Similaridade]
```

- **VectorVerb** é o tipo pivô: ponteiro para dados, dimensão e callback opcional de processamento cinético. 【F:GAIA_DOCUMENTATION.md†L45-L74】
- **Hashing DJB2/FNV‑like**: gera vetor 3D normalizado e determinístico. 【F:GAIA_DOCUMENTATION.md†L74-L115】
- **Nexus/MMAP**: memória persistente para varredura por produto interno. 【F:GAIA_DOCUMENTATION.md†L74-L115】
- **VecDB**: registros de 32 bytes, quantização e índice auxiliar. 【F:GAIA_DOCUMENTATION.md†L100-L111】
- **ZipRaf**: camadas semânticas (`layer_0.zrf`…`layer_7.zrf`) com CRC32. 【F:GAIA_DOCUMENTATION.md†L118-L125】

---

## Organização do repositório (mapa de componentes)

### Núcleo C (root)
- **Boot simbólico e simulação**: `boot_omega.c`. 【F:GAIA_DOCUMENTATION.md†L132-L137】
- **VecDB**: `gaia_vec_build.c` (builder), `gaia_vec_query.c` (consulta). 【F:GAIA_DOCUMENTATION.md†L138-L143】
- **NanoGPT simbólico**: `gaia_nanogpt.c`. 【F:GAIA_DOCUMENTATION.md†L144-L147】
- **Engines “Rafaelia”**: `raf_coexist_v2.c`, `raf_coexist_quintic.c`, `raf_coexist_mixed.c`, `raf_coexist_mixed_pipelines.c`. 【F:GAIA_DOCUMENTATION.md†L148-L167】

### Núcleo C (diretório `dados/`)
Inclui headers e implementações que formalizam o protocolo de vetorização, memória e IPC: `omega_protocol.h`, `omega_hash.h`, `omega_nexus.h`, `omega_attention.h`, `omega_vecdb.h`, `omega_zipraf.h`, `raf_event_log.h`, e implementações correspondentes (`semantic_hash.c`, `mmap_nexus.c`, `infinite_attention.c`, `zipraf_db.c`, etc.). 【F:GAIA_DOCUMENTATION.md†L45-L127】【F:GAIA_DOCUMENTATION.md†L200-L222】

### Ferramentas Python
- `aether_hybrid_core.py` (CLI de hashing AETHER/IRON/BLAKE2b). 【F:GAIA_DOCUMENTATION.md†L171-L179】
- `aether_hybrid_web.py` (serviço Flask com API `/api/hash`). 【F:GAIA_DOCUMENTATION.md†L179-L184】
- `gaia_chat.py` (cliente IPC). 【F:GAIA_DOCUMENTATION.md†L184-L186】

### Scripts de build
- `build_gaia.sh`, `build_vecdb.sh`, `build_commander_zipraf.sh`, `build_raf_log.sh`. 【F:GAIA_DOCUMENTATION.md†L190-L214】

### Dados e artefatos
- `dummy_data.txt`, `checkpoint2.zip`, camadas `layer_*.zrf`, `gaia_semcore.vecdb`. 【F:GAIA_DOCUMENTATION.md†L216-L243】

---

## Fluxos operacionais (uso acadêmico)

> **Observação**: esta seção descreve o fluxo previsto pelos scripts e binários do projeto; a execução depende de ambiente C padrão com `gcc` e utilitários POSIX.

1. **Build principal** (núcleo C e binários):
   - `build_gaia.sh` gera cabeçalhos e compila ferramentas básicas (boot, ingestão, daemon, etc.). 【F:GAIA_DOCUMENTATION.md†L190-L214】
2. **VecDB** (indexação vetorial):
   - `build_vecdb.sh` compila o builder e o query de VecDB. 【F:GAIA_DOCUMENTATION.md†L205-L210】
3. **ZipRaf** (camadas semânticas):
   - `build_commander_zipraf.sh` inicializa as camadas `layer_*.zrf` e estrutura o repositório de conhecimento. 【F:GAIA_DOCUMENTATION.md†L210-L214】
4. **Log encadeado**:
   - `build_raf_log.sh` prepara a infraestrutura de logging auditável. 【F:GAIA_DOCUMENTATION.md†L213-L214】

---

## Lógica e princípios de design

### 1) Vetorização compacta e determinística
A decisão por **3 dimensões** reduz custo de processamento e torna viável a exploração de atenção linear em memória mapeada, sem depender de GPUs ou bibliotecas pesadas de ML. 【F:GAIA_DOCUMENTATION.md†L16-L43】【F:GAIA_DOCUMENTATION.md†L74-L115】

### 2) Persistência e varredura controlada
A memória mapeada (Nexus) permite **scan linear** para produto interno; essa estratégia é deliberadamente simples, usada como baseline experimental para estudos de trade‑offs entre custo e precisão. 【F:GAIA_DOCUMENTATION.md†L74-L115】

### 3) Dualidade de armazenamento
VecDB trabalha com **registros fixos e quantizados**; ZipRaf oferece **camadas semânticas** com CRC, buscando complementaridade entre eficiência e integridade. 【F:GAIA_DOCUMENTATION.md†L100-L125】

### 4) Engines matemáticas “Rafaelia”
As engines simulam universos com padrões matemáticos diversos e usam Newton–Raphson e pipelines para analisar convergência e dificuldade computacional. 【F:GAIA_DOCUMENTATION.md†L148-L167】

---

## Pontos de extensão (além do que já se vê no código)

1. **Refatoração estrutural**
   - Consolidar duplicações entre root e `dados/`, reduzindo divergências de versões e simplificando a manutenção de headers e implementações. 【F:GAIA_DOCUMENTATION.md†L262-L268】

2. **Camada de API formal (FFI/SDK)**
   - Expor o pipeline central (hash → vector → Nexus → atenção) via uma API estável (C ABI, Python bindings, gRPC) para integração com sistemas externos.

3. **Indexação híbrida**
   - Complementar o scan linear com índices aproximados (HNSW/IVF) e comparar custos de atualização vs. precisão para vetores 3D.

4. **Métricas e benchmarking**
   - Adicionar suite padronizada (tempo, memória, recall) para comparar: (a) scan linear, (b) VecDB quantizado, (c) ZipRaf por camadas.

5. **Segurança e auditoria**
   - Evoluir o log encadeado com assinaturas digitais e checkpoints para garantir não‑repúdio e rastreabilidade acadêmica.

6. **Camada visual e inspeção semântica**
   - Extender o terminal UI com gráficos históricos, heatmaps e distribuição estatística de vetores para depuração científica.

---

## Referência rápida de executáveis
- `gaia_boot`, `gaia_ingest`, `gaia_absorb`, `gaia_visual`, `gaia_d`, `gaia_client`
- `gaia_vec_build`, `gaia_vec_query`
- `gaia_nanogpt`
- `gaia_zipraf_inspect`
- `raf_coexist_v2`, `raf_coexist_quintic`, `raf_coexist_mixed`, `raf_coexist_mixed_pipelines`

Os binários acima estão presentes como artefatos de build e auxiliam a exploração prática dos fluxos descritos. 【F:GAIA_DOCUMENTATION.md†L216-L236】

---

## Licença
Consulte o arquivo `LICENSE` para termos completos de uso e redistribuição. 【F:GAIA_DOCUMENTATION.md†L212-L218】
