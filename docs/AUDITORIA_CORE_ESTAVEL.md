# Auditoria de Estabilidade — GAIA-Ω (GAIA Phi)

> Documento navegável (com sumário) que consolida a auditoria solicitada.

## Sumário
- [1) Mapa do projeto](#1-mapa-do-projeto)
- [2) Como rodar](#2-como-rodar)
  - [2.1 Scripts `.sh` (Linux/Termux)](#21-scripts-sh-linuxtermux)
  - [2.2 Compilar `.c` (comandos exatos encontrados nos scripts)](#22-compilar-c-comandos-exatos-encontrados-nos-scripts)
- [3) Dependências](#3-dependências)
- [4) O que já está bem feito](#4-o-que-já-está-bem-feito)
- [5) O que falta para virar core estável](#5-o-que-falta-para-virar-core-estável)
- [6) Pontos quebrados (riscos/erros prováveis)](#6-pontos-quebrados-riscoserros-prováveis)
- [7) Nível atual](#7-nível-atual)
  - [7.1 Avaliação formal (nível PhD/profissional)](#71-avaliação-formal-nível-phdprofissional)
  - [7.2 Avaliação técnica (objetiva)](#72-avaliação-técnica-objetiva)
- [8) Próximos 5 commits sugeridos](#8-próximos-5-commits-sugeridos)

---

## 1) Mapa do projeto

**Pastas principais e papel (evidência em documentação do próprio repositório):**

- `core/`: utilitários de indexação/snapshot do repositório, gerando `core/files_index.json` e um snapshot/manifest em `core/year_60/` por meio de scripts Python.【F:core/generate_core_index.py†L1-L54】【F:core/year_60/capture_repository.py†L1-L60】
- `dados/`: headers, implementações e artefatos duplicados (incluindo cópias de fontes e scripts).【F:GAIA_DOCUMENTATION.md†L250-L270】
- `docs/`: documentação e histórico (ex.: evolução em 59 ciclos).【F:docs/RELEASES_59X.md†L1-L120】
- `gaia_core_v2/`: headers e fontes do núcleo “v2”, com APIs como `gaia_hash_bytes` e `gaia_vecdb_*` que indicam uma organização mais formalizada do core.【F:gaia_core_v2/include/gaia_hash.h†L1-L14】【F:gaia_core_v2/include/gaia_vecdb.h†L1-L30】
- `gaia_engines_v2/`: engines RAFAELIA em C com a estrutura `RafEngine` e funções de registro/execução de engines.【F:gaia_engines_v2/include/raf_engine.h†L1-L18】

> Nota: a estrutura acima foi inferida **apenas** do inventário/descrição documental; se o repositório mudar, é necessário revalidar.

---

## 2) Como rodar

### 2.1 Scripts `.sh` (Linux/Termux)

**Regra operacional:** todos os scripts listados abaixo podem ser executados com `bash <script>`. Isso evita problemas de shebang específicos (ex.: caminhos do Termux) e é compatível com Linux/Termux.【F:bench_compare_hashes.sh†L1-L4】【F:build_gaia.sh†L1-L9】

**Scripts na raiz (comandos exatos):**

| Script | Comando recomendado | Observação |
|---|---|---|
| `FCEA_ABSENCE_INDEX.sh` | `bash FCEA_ABSENCE_INDEX.sh` | shebang `#!/bin/bash`.【F:FCEA_ABSENCE_INDEX.sh†L1】 |
| `FCEA_MOUC_VECTORS_BOOT.sh` | `bash FCEA_MOUC_VECTORS_BOOT.sh` | shebang `#!/bin/bash`.【F:FCEA_MOUC_VECTORS_BOOT.sh†L1】 |
| `QUANTIC_MOUC.sh` | `bash QUANTIC_MOUC.sh` | shebang `#!/bin/bash`.【F:QUANTIC_MOUC.sh†L1】 |
| `QUANTIC_MOUC_DAEMON.sh` | `bash QUANTIC_MOUC_DAEMON.sh` | shebang `#!/bin/bash`.【F:QUANTIC_MOUC_DAEMON.sh†L1】 |
| `QUANTIC_MOUC_GUI.sh` | `bash QUANTIC_MOUC_GUI.sh` | shebang `#!/bin/bash`.【F:QUANTIC_MOUC_GUI.sh†L1】 |
| `bench_compare_hashes.sh` | `bash bench_compare_hashes.sh` | shebang Termux (path fixo).【F:bench_compare_hashes.sh†L1】 |
| `bench_fiber_h.sh` | `bash bench_fiber_h.sh` | shebang Termux (path fixo).【F:bench_fiber_h.sh†L1】 |
| `bench_fiber_h_log.sh` | `bash bench_fiber_h_log.sh` | shebang Termux (path fixo).【F:bench_fiber_h_log.sh†L1】 |
| `build_commander_zipraf.sh` | `bash build_commander_zipraf.sh` | shebang `#!/bin/bash`.【F:build_commander_zipraf.sh†L1】 |
| `build_gaia.sh` | `bash build_gaia.sh` | shebang `#!/bin/bash`.【F:build_gaia.sh†L1】 |
| `build_raf_log.sh` | `bash build_raf_log.sh` | shebang `#!/bin/bash`.【F:build_raf_log.sh†L1】 |
| `build_rafaelia_image.sh` | `bash build_rafaelia_image.sh` | shebang `#!/usr/bin/env bash`.【F:build_rafaelia_image.sh†L1】 |
| `build_run_fiber_kernel.sh` | `bash build_run_fiber_kernel.sh` | shebang `#!/usr/bin/env bash`.【F:build_run_fiber_kernel.sh†L1】 |
| `build_vecdb.sh` | `bash build_vecdb.sh` | shebang `#!/bin/bash`.【F:build_vecdb.sh†L1】 |
| `fiber_console.sh` | `bash fiber_console.sh` | shebang Termux (path fixo).【F:fiber_console.sh†L1】 |
| `fiber_decide_and_bench.sh` | `bash fiber_decide_and_bench.sh` | shebang Termux (path fixo).【F:fiber_decide_and_bench.sh†L1】 |
| `fiber_lab_all.sh` | `bash fiber_lab_all.sh` | shebang Termux (path fixo).【F:fiber_lab_all.sh†L1】 |
| `fiber_speed_compare_cli.sh` | `bash fiber_speed_compare_cli.sh` | shebang `#!/usr/bin/env bash`.【F:fiber_speed_compare_cli.sh†L1】 |
| `fiber_suite.sh` | `bash fiber_suite.sh` | shebang Termux (path fixo).【F:fiber_suite.sh†L1】 |
| `fiber_suite_all.sh` | `bash fiber_suite_all.sh` | shebang Termux (path fixo).【F:fiber_suite_all.sh†L1】 |
| `fix_fiber_lab.sh` | `bash fix_fiber_lab.sh` | shebang Termux (path fixo).【F:fix_fiber_lab.sh†L1】 |
| `fix_fiber_printhex.sh` | `bash fix_fiber_printhex.sh` | shebang Termux (path fixo).【F:fix_fiber_printhex.sh†L1】 |
| `fix_fiber_tree_and_lab.sh` | `bash fix_fiber_tree_and_lab.sh` | shebang Termux (path fixo).【F:fix_fiber_tree_and_lab.sh†L1】 |
| `hash_speed_basic.sh` | `bash hash_speed_basic.sh` | shebang `#!/usr/bin/env bash`.【F:hash_speed_basic.sh†L1】 |

**Scripts em `dados/` (comandos exatos):**

| Script | Comando recomendado | Observação |
|---|---|---|
| `dados/RAFAELIA_BITRAF_RUN_ALL.sh` | `bash dados/RAFAELIA_BITRAF_RUN_ALL.sh` | shebang `#!/usr/bin/env bash`.【F:dados/RAFAELIA_BITRAF_RUN_ALL.sh†L1】 |
| `dados/RAFAELIA_BITRAF_SNAPSHOT.sh` | `bash dados/RAFAELIA_BITRAF_SNAPSHOT.sh` | shebang `#!/usr/bin/env bash`.【F:dados/RAFAELIA_BITRAF_SNAPSHOT.sh†L1】 |
| `dados/build_commander_zipraf.sh` | `bash dados/build_commander_zipraf.sh` | shebang `#!/bin/bash`.【F:dados/build_commander_zipraf.sh†L1】 |
| `dados/build_gaia.sh` | `bash dados/build_gaia.sh` | shebang `#!/bin/bash`.【F:dados/build_gaia.sh†L1】 |
| `dados/build_raf_log.sh` | `bash dados/build_raf_log.sh` | shebang `#!/bin/bash`.【F:dados/build_raf_log.sh†L1】 |
| `dados/build_vecdb.sh` | `bash dados/build_vecdb.sh` | shebang `#!/bin/bash`.【F:dados/build_vecdb.sh†L1】 |

---

### 2.2 Compilar `.c` (comandos exatos encontrados nos scripts)

**Build principal (`build_gaia.sh`):**

- `gcc -O3 boot_omega.c core/kinetic_math.c neural/synapse_registry.c -o gaia_boot -lm`【F:build_gaia.sh†L1033】
- `gcc -O3 interactive_mutant.c core/kinetic_math.c core/lexical_projector.c core/semantic_hash.c neural/synapse_registry.c -o gaia_mutant -lm`【F:build_gaia.sh†L1036】
- `gcc -O3 tools_ingest.c core/mmap_nexus.c core/semantic_hash.c -o gaia_ingest -lm`【F:build_gaia.sh†L1039】
- `gcc -O3 tools_absorb.c core/mmap_nexus.c core/semantic_hash.c core/vision_cortex.c -o gaia_absorb -lm`【F:build_gaia.sh†L1040】
- `gcc -O3 visual_shell.c core/mmap_nexus.c core/semantic_hash.c core/ansi_engine.c -o gaia_visual -lm`【F:build_gaia.sh†L1043】
- `gcc -O3 core/gaia_daemon.c core/mmap_nexus.c -o gaia_d -lm`【F:build_gaia.sh†L1046】
- `gcc -O3 visual_client.c core/semantic_hash.c -o gaia_client -lm`【F:build_gaia.sh†L1047】
- `gcc -O3 gaia_nanogpt.c core/infinite_attention.c core/mmap_nexus.c core/semantic_hash.c core/kinetic_math.c core/vision_cortex.c -o gaia_nanogpt -lm`【F:build_gaia.sh†L1050】

**VecDB (`build_vecdb.sh`):**

- `gcc -O3 gaia_vec_build.c core/semantic_hash.c -o gaia_vec_build -lm`【F:build_vecdb.sh†L508】
- `gcc -O3 gaia_vec_query.c core/semantic_hash.c -o gaia_vec_query -lm`【F:build_vecdb.sh†L511】

**ZipRaf Commander (`build_commander_zipraf.sh`):**

- `gcc -O3 tools_commander.c core/zipraf_db.c core/semantic_hash.c -o gaia_commander -lm`【F:build_commander_zipraf.sh†L558-L565】

**Log encadeado (`build_raf_log.sh`):**

- `gcc -O3 raf_event_append.c core/raf_event_log.c core/semantic_hash.c -o raf_event_append -lm`【F:build_raf_log.sh†L442】
- `gcc -O3 raf_event_verify.c core/raf_event_log.c core/semantic_hash.c -o raf_event_verify -lm`【F:build_raf_log.sh†L443】

**Imagem (Rafaelia) (`build_rafaelia_image.sh`):**

- `cc -O2 -fPIC -shared -o librafaelia_image.so rafaelia_image_ingest.c`【F:build_rafaelia_image.sh†L1-L4】

---

## 3) Dependências

**Explícitas no repositório:**

- **Bash**: scripts `.sh` usam `#!/bin/bash`, `#!/usr/bin/env bash` ou shebang Termux; executar via `bash` é compatível em Linux/Termux.【F:build_gaia.sh†L1-L9】【F:build_rafaelia_image.sh†L1】
- **Compilador C**: os scripts chamam `gcc` ou `cc` diretamente.【F:build_gaia.sh†L1033-L1050】【F:build_rafaelia_image.sh†L1-L4】
- **libm**: builds C linkam explicitamente `-lm`.【F:build_gaia.sh†L1033-L1050】
- **Python 3**: scripts Python com shebang `python3` (ex.: `aether_hybrid_web.py`).【F:aether_hybrid_web.py†L1-L12】
- **Flask**: importado pelo serviço web (`aether_hybrid_web.py`).【F:aether_hybrid_web.py†L16-L21】

**Versões específicas:** não há números de versão explícitos no repositório; portanto **não dá para afirmar** versões mínimas necessárias.

---

## 4) O que já está bem feito

- **Arquitetura conceitual bem documentada**: há uma descrição detalhada do fluxo hash → vetores → memória persistente → atenção/consulta, com inventário técnico dos módulos e artefatos. Isso facilita auditoria e onboarding técnico.【F:GAIA_DOCUMENTATION.md†L1-L214】
- **Núcleo C organizado por módulos** (hashing, Nexus/MMAP, atenção, ZipRaf, log encadeado, IPC) com headers e implementações descritos de forma clara na documentação interna.【F:GAIA_DOCUMENTATION.md†L80-L214】
- **Pipelines demonstrativos claros** (VecDB, ZipRaf, daemon IPC, NanoGPT simbólico), o que permite validar rapidamente a cadeia de hashing/consulta/armazenamento sem dependências externas pesadas.【F:GAIA_DOCUMENTATION.md†L120-L214】

---

## 5) O que falta para virar core estável

> Itens abaixo são lacunas **observáveis** pela ausência de evidência explícita no repositório/documentação. Quando algo não está documentado, é indicado como “não dá para afirmar”.

1. **Build reprodutível e portável (Linux/Termux)**
   - Há scripts com shebangs específicos de Termux (caminho fixo), o que quebra execução direta em Linux; padronizar para `#!/usr/bin/env bash` tornaria o core mais portátil.【F:bench_compare_hashes.sh†L1】【F:fix_fiber_lab.sh†L1】

2. **Padrão único de build**
   - Existem cópias de scripts e fontes em `dados/`, o que sugere risco de divergência entre versões do mesmo módulo/fluxo. Consolidar reduziria inconsistências.【F:GAIA_DOCUMENTATION.md†L250-L270】

3. **Documentação formal de dependências e versões**
   - O repositório não define versões mínimas (gcc, Python, Flask). Sem esse registro, a reprodução exata do ambiente fica frágil (não dá para afirmar compatibilidade cross-distro sem testes).【F:aether_hybrid_web.py†L1-L21】

4. **Testes automatizados/CI**
   - Não há evidência explícita de testes unitários/integração ou pipeline CI. Sem isso, a estabilidade operacional não é comprovada (não dá para afirmar cobertura de regressão).【F:GAIA_DOCUMENTATION.md†L1-L214】

---

## 6) Pontos quebrados (riscos/erros prováveis)

1. **Shebangs de Termux em scripts**
   - Scripts com `#!/data/data/com.termux/files/usr/bin/bash` falham quando executados diretamente em Linux, pois o path não existe. Exemplos: `bench_compare_hashes.sh`, `bench_fiber_h.sh`, `bench_fiber_h_log.sh`, `fiber_console.sh`, `fiber_decide_and_bench.sh`, `fiber_lab_all.sh`, `fiber_suite.sh`, `fiber_suite_all.sh`, `fix_fiber_lab.sh`, `fix_fiber_printhex.sh`, `fix_fiber_tree_and_lab.sh`.【F:bench_compare_hashes.sh†L1】【F:bench_fiber_h.sh†L1】【F:bench_fiber_h_log.sh†L1】【F:fiber_console.sh†L1】【F:fiber_decide_and_bench.sh†L1】【F:fiber_lab_all.sh†L1】【F:fiber_suite.sh†L1】【F:fiber_suite_all.sh†L1】【F:fix_fiber_lab.sh†L1】【F:fix_fiber_printhex.sh†L1】【F:fix_fiber_tree_and_lab.sh†L1】

2. **`build_vecdb.sh` e `build_raf_log.sh` assumem `~/gaia_omega_build` existente**
   - Eles fazem `cd "$BASE_DIR" || exit 1` antes de criar o diretório base, logo falham se o caminho não existir.【F:build_vecdb.sh†L9-L13】【F:build_raf_log.sh†L6-L14】

3. **Socket IPC com caminho relativo**
   - `GAIA_SOCKET_PATH` é definido como `gaia.sock` (sem caminho absoluto). Se servidor e cliente rodarem em diretórios diferentes, o socket pode não ser encontrado.【F:build_gaia.sh†L120-L145】

4. **Duplicação de fontes e scripts no diretório `dados/`**
   - O próprio inventário aponta duplicação de fontes/scripts; isso aumenta a chance de divergência e bugs por atualização parcial.【F:GAIA_DOCUMENTATION.md†L250-L270】

---

## 7) Nível atual

### 7.1 Avaliação formal (nível PhD/profissional)

**Classificação: _Pesquisa_**

**Justificativa formal:** a própria documentação descreve o repositório como um conjunto **experimental** de componentes e demos, com foco em investigação de hashing semântico, memória mapeada e mecanismos compactos (VecDB/ZipRaf). A ênfase em pipelines demonstrativos e experimentos matemáticos “Rafaelia” indica caráter de pesquisa, não produção estável.【F:GAIA_DOCUMENTATION.md†L1-L38】【F:GAIA_DOCUMENTATION.md†L120-L214】

### 7.2 Avaliação técnica (objetiva)

**Classificação técnica: _Protótipo avançado_ (com elementos de pesquisa)**

**Evidência técnica:** há binários e scripts de build que permitem executar fluxos completos (hash → memória → atenção → consulta), mas também há duplicações de fontes e scripts, dependências sem versionamento e ausência de testes/CI explícitos, o que impede afirmar estabilidade de produção.【F:GAIA_DOCUMENTATION.md†L120-L214】【F:GAIA_DOCUMENTATION.md†L250-L270】

---

## 8) Próximos 5 commits sugeridos

> Abaixo estão melhorias em ordem lógica, com **arquivos alvo e diffs sugeridos**. São sugestões baseadas no estado atual; não alteram o repo.

### Commit 1 — Garantir `BASE_DIR` (VecDB e log)
**Problema:** `build_vecdb.sh` e `build_raf_log.sh` usam `cd "$BASE_DIR"` sem criar o diretório base, causando falha se ele não existir.【F:build_vecdb.sh†L9-L13】【F:build_raf_log.sh†L6-L14】

**Diff sugerido (exemplo):**
```diff
-BASE_DIR=~/gaia_omega_build
-cd "$BASE_DIR" || exit 1
+BASE_DIR=${BASE_DIR:-~/gaia_omega_build}
+mkdir -p "$BASE_DIR"
+cd "$BASE_DIR" || exit 1
```

### Commit 2 — Portabilizar shebangs Termux
**Problema:** scripts com shebang Termux falham em Linux. Exemplos citados na seção de pontos quebrados.【F:bench_compare_hashes.sh†L1】【F:fiber_suite.sh†L1】

**Diff sugerido:**
```diff
-#!/data/data/com.termux/files/usr/bin/bash
+#!/usr/bin/env bash
```

### Commit 3 — Documentar dependências e versões mínimas
**Problema:** o repositório não documenta versões mínimas de gcc/cc, Python e Flask; isso reduz reprodutibilidade.【F:build_gaia.sh†L1033-L1050】【F:aether_hybrid_web.py†L1-L21】

**Diff sugerido (README.md):**
```diff
+## Dependências
+- bash
+- gcc/cc (toolchain C)
+- python3
+- flask (para aether_hybrid_web.py)
+Versões: não especificadas no repositório.
```

### Commit 4 — Adicionar `requirements.txt`
**Problema:** a dependência de Flask não está listada em arquivo de requirements, dificultando instalação automatizada.【F:aether_hybrid_web.py†L16-L21】

**Diff sugerido (novo arquivo `requirements.txt`):**
```text
flask
```

### Commit 5 — Reduzir duplicações em `dados/`
**Problema:** há duplicações de fontes e scripts no diretório `dados/`, reconhecidas no inventário; isso aumenta risco de divergência.【F:GAIA_DOCUMENTATION.md†L250-L270】

**Diff sugerido (exemplo de wrapper em `dados/build_gaia.sh`):**
```diff
-# (script grande duplicado)
+#!/usr/bin/env bash
+exec "$(dirname "$0")/../build_gaia.sh"
```

---

Se precisar, posso também gerar um checklist de estabilidade (build reprodutível, testes mínimos, CI, versionamento de formatos) **apenas** com base no que existe no repositório.
