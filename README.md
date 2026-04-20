# GAIA_phi — Arquitetura Unificada de Código, Dados e Pesquisa

## Abstract
O **GAIA_phi** é um repositório de pesquisa e engenharia que combina três eixos principais: (1) **núcleo determinístico em C** para hashing, vetorização, persistência e consulta; (2) **pipelines experimentais em Python** para indexação, análise e geração de manifestos; e (3) **documentação técnico‑científica** de evolução arquitetural, auditoria e método experimental.  

Este README consolida, em formato de dissertação analítica, os documentos que estavam distribuídos e estabelece uma navegação formal para entendimento de código-fonte, artefatos e conceitos por diretório.

---

## Resumo executivo
- O projeto adota uma estratégia de **determinismo operacional**: varredura ordenada, hashing reproduzível e saídas auditáveis.
- A base C concentra componentes de **baixo overhead** (hash, vecdb, mmap, zipraf, guardas de segurança).
- A base Python opera como **orquestração e metadocumentação** (manifestos, compilação de dataset, automações experimentais).
- A pasta `docs/` formaliza o estado da arte local: auditoria, oportunidades, roteiro experimental, manifesto técnico e árvore estrutural.

---

## Dissertação analítica (síntese unificada)

### 1) Problema estrutural original
Historicamente, o repositório acumulou documentos de alto valor técnico em paralelo à expansão rápida dos fontes. Isso gerou duas fricções:
1. **Conhecimento disperso**: conceitos importantes estavam em múltiplos `.md` sem ponto único de entrada.
2. **Assimetria entre documentação e árvore de código**: nem todo diretório tinha README próprio explicitando papel, arquivos e interfaces.

### 2) Estratégia de unificação aplicada
A unificação foi organizada por camadas:
- **Camada institucional (raiz)**: este README passa a ser o índice oficial, com resumo global e navegação.
- **Camada modular (cada diretório principal)**: cada pasta crítica recebe README com estrutura e conceitos.
- **Camada operacional (docs/)**: documentos analíticos continuam como base de profundidade, agora referenciados por um mapa único.

### 3) Resultado arquitetural
O projeto passa a ser lido como um sistema com fronteiras claras:
- `gaia_core_v2/` e `gaia_engines_v2/`: núcleo e motores formais em C.
- `llama_guard/`: política de contenção e normalização semântica.
- `core/`: indexação/snapshot do repositório.
- `tests/`: validação do CLI e fixtures determinísticas.
- `dados/`: laboratório expandido com fontes, scripts e artefatos operacionais.
- `docs/`: base de governança técnico-científica.

### 4) Implicação técnica
Com READMEs distribuídos por diretório, a manutenção passa a ser **navegável, auditável e escalável**:
- onboarding mais rápido;
- menor risco de divergência entre intenção e implementação;
- maior rastreabilidade em refatorações e estudos experimentais.

---

## Mapa profissional de navegação

## Diretórios principais
- [`core/`](core/README.md) — índice/snapshot determinístico do repositório.
- [`dados/`](dados/README.md) — sandbox técnico com fontes C/Python, scripts e artefatos.
- [`docs/`](docs/README.md) — corpus documental analítico e institucional.
- [`docs/ASM_NATIVE_PIPELINE.md`](docs/ASM_NATIVE_PIPELINE.md) — pipeline de assembly puro multi-arquitetura e CI.
- [`docs/LEVANTAMENTO_ESTRUTURAL_TOTAL.md`](docs/LEVANTAMENTO_ESTRUTURAL_TOTAL.md) — levantamento total, com mapa de 5 níveis e descrição arquivo a arquivo.
- [`gaia_core_v2/`](gaia_core_v2/README.md) — núcleo C modular (headers + implementações).
- [`gaia_engines_v2/`](gaia_engines_v2/README.md) — motores RAF de execução simbólica.
- [`llama_guard/`](llama_guard/README.md) — guard rails semânticos e integração de segurança.
- [`tests/`](tests/README.md) — suíte de testes e fixtures de validação.

## Submódulos com leitura guiada
- `gaia_core_v2/include/` → contratos públicos do core.
- `gaia_core_v2/src/` → implementação do core por responsabilidade.
- `gaia_engines_v2/include/` → API de engines.
- `gaia_engines_v2/src/` → implementação das engines.
- `core/year_60/` → captura/snapshot histórico.

---

## Resumo por diretório e funções

### `gaia_core_v2/`
Funções centrais: hashing, vetorização, projeção, métrica, memória/nexus, vecdb e zipraf.  
Objetivo: prover base C estável, com separação entre API e implementação.

### `gaia_engines_v2/`
Funções centrais: ciclo de vida de engine RAF (`init/run/close`) e cálculo de métricas de execução.  
Objetivo: padronizar execução de motores simbólicos no ecossistema.

### `llama_guard/`
Funções centrais: classificação de risco textual, normalização de sinônimos e integração pré-geração.  
Objetivo: reduzir exposição a conteúdo sensível por gate determinístico.

### `core/`
Funções centrais: geração de inventário (`files_index.json`) e captura versionada da árvore.  
Objetivo: rastreabilidade estrutural do repositório.

### `tests/`
Funções centrais: validar CLI de manifesto com saídas esperadas (`json/jsonl/md`).  
Objetivo: garantir determinismo e prevenir regressão funcional básica.

### `dados/`
Funções centrais: laboratório de expansão (prototipagem, scripts auxiliares, datasets e binários experimentais).  
Objetivo: acelerar experimentos sem bloquear evolução dos módulos formais.

### `docs/`
Funções centrais: consolidar método, auditoria, roadmap e estado da arte do projeto.  
Objetivo: governança técnica e leitura institucional de longo prazo.

---

## Fluxo recomendado de leitura (formal)
1. Leia este README (visão institucional).
2. Leia `docs/README.md` (mapa documental).
3. Leia `docs/LEVANTAMENTO_ESTRUTURAL_TOTAL.md` (mapa 5 níveis + arquivo a arquivo).
4. Entre em `gaia_core_v2/README.md` e `gaia_engines_v2/README.md` (núcleo executável).
5. Consulte `llama_guard/README.md` (camada de segurança).
6. Use `tests/README.md` para reproduzir validações.
7. Navegue `dados/README.md` para contexto de laboratório e artefatos.

---

## Execução rápida
```bash
make test
bash tests/run_tests.sh
python3 gaia_core.py manifest --root . --format json,jsonl,md --out-dir ./gaia_core_manifest
```

## Build unificado (host e Android/NDK)
```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build --parallel
ctest --test-dir build --output-on-failure

# Android (requer ANDROID_NDK_HOME)
make android-configure
cmake --build build-android --parallel

# Manifesto ASM (registradores/endereçamentos autoidentificados)
cmake --build build --target asm_manifest
```

---

## Licença
Consulte `LICENSE` e `LICENSE.md`.
