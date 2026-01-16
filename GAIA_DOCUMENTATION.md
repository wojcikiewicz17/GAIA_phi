# GAIA-Ω (GAIA Phi) — Documentação Técnica Completa

## Resumo (Abstract)
O repositório **GAIA-Ω** organiza um conjunto de componentes experimentais que combinam: (1) vetorização semântica leve baseada em hashing, (2) memória persistente mapeada em disco, (3) pipelines de atenção e ingestão, (4) mecanismos de armazenamento compactado (VecDB/ZipRaf), (5) executáveis de demonstração e ferramentas de inspeção, e (6) experimentos matemáticos “Rafaelia” que simulam coexis­tência de núcleos algébricos. O núcleo gira em torno do tipo `VectorVerb` e de funções de hashing que projetam texto/bytes para vetores de baixa dimensão, permitindo desde interfaces IPC até busca aproximada via produto interno. Esta documentação faz um inventário exaustivo de arquivos e descreve arquitetura, lógica, algoritmos, modelos de dados, rotas, fluxos e artefatos binários presentes no repositório.

**Palavras‑chave:** hashing semântico, vector database, atenção infinita, memória mapeada, IPC Unix, ZipRaf, Newton–Raphson, processos simbólicos, arquitetura de dados.

---

## 1. Visão geral de arquitetura

### 1.1. Modelo conceitual
A arquitetura é centrada em **vetores compactos de 3 dimensões**, obtidos por hashing rápido (DJB2 ou variações FNV‑like), e armazenados em estruturas de dados persistentes. O objetivo prático é transformar texto/bytes em vetores pequenos que possam indexar memória, executar buscas por similaridade e alimentar pipelines de atenção e decisão. Há quatro pilares principais:

1. **Vetorização semântica (core)** — converte texto/bytes em vetores; fornece funções de hash e projeção para múltiplos componentes.
2. **Memória persistente (Nexus/MMAP)** — armazena vetores e metadados em disco e permite scan/consulta em memória mapeada.
3. **Armazenamento compacto** — VecDB (memória vetorial contínua) e ZipRaf (camadas semânticas em `.zrf`).
4. **Ferramentas e demos** — executáveis, CLI e servidores IPC para ingestão, consulta e visualização.

### 1.2. Diagrama macro (fluxo de dados)
```
[Input Texto/Binário]
        |
        v
[Hash Semântico] ---> [VectorVerb (3D)]
        |                     |
        |                     +--> [Nexus MMAP] --> [Atenção/Busca] --> [Outputs]
        |
        +--> [VecDB/ZipRaf] --> [Consulta Similaridade/Inspeção]
```

### 1.3. Convenções-chave
- **VectorVerb** é o tipo pivô: contém ponteiro para dados, dimensão e callback opcional (`kinetic_func`).
- **Dimensão padrão**: 3 floats (`omega_float`), usados em todos os módulos principais.
- **Hashing**: DJB2 e variações FNV‑like são usados para produzir vetores determinísticos.

---

## 2. Núcleo de tipos e protocolo (headers)

### 2.1. `dados/omega_protocol.h`
Define o tipo `omega_float` e a estrutura **VectorVerb**, que encapsula vetor, dimensão e callback opcional para processamento cinético.

### 2.2. `dados/omega_hash.h`
Declara funções de hashing semântico (`semantic_hash_djb2`, `omega_hash`) e projeção para vetor (`hash_to_vector`).

### 2.3. `dados/omega_vecdb.h`
Define o **layout binário** do VecDB com cabeçalho fixo de 64 bytes e registros compactos de 32 bytes. Estabelece dimensões, magic number, e estrutura do registro (hash, vetor quantizado, flags e referências).

### 2.4. `dados/omega_asm.h`
Define `SynapseNode` e funções do “córtex” simbólico. É o contrato mínimo para execução de padrões (sinapses) e despacho de ações.

### 2.5. `dados/omega_nexus.h`
Define o **Nexus** (memória persistente) com `NexusHeader` e `NexusCell`. Inclui protótipos para inicialização, append, scan e fechamento.

### 2.6. `dados/omega_attention.h`
Define a janela de contexto virtual (`VirtualContextWindow`) e as funções de **atenção**, que apontam para células de foco e calculam score.

### 2.7. `dados/omega_lexicon.h`
Define uma camada de **projeção lexical** de texto para vetor e a função de ressonância recursiva.

### 2.8. `dados/omega_vision.h`
Define hashing e projeção para vetores a partir de conteúdo visual em bytes.

### 2.9. `dados/omega_gui.h`
Define funções de UI ASCII/ANSI para visualização simples no terminal (radar e caixas).

### 2.10. `dados/omega_ipc.h`
Define protocolo IPC via socket Unix (`gaia.sock`), com operações de ping, search e insert, e estruturas de request/response.

### 2.11. `dados/omega_plasticity.h`
Define interfaces de plasticidade (aprendizagem) e carregamento de córtex.

### 2.12. `dados/omega_zipraf.h`
Define o formato **ZipRaf** com 8 camadas semânticas, cabeçalho (`ZipRafHeader`) e entradas compactas (`ZipRafEntry`).

### 2.13. `dados/raf_event_log.h`
Define o protocolo para logs encadeados e auditáveis, com funções para append e verificação.

---

## 3. Implementações de núcleo (C)

### 3.1. Hashing semântico
- **`dados/semantic_hash.c`**: implementa DJB2 para hashing semântico, alias `omega_hash`, e a função `hash_to_vector` que mapeia bits para 3 floats normalizados.

### 3.2. Memória persistente (Nexus via MMAP)
- **`dados/mmap_nexus.c`**: implementa o mapeamento de `gaia.nexus` no disco, com append de células e scan simples por produto interno. A estrutura é mantida em memória mapeada e reaproveitada em vários módulos.

### 3.3. Atenção infinita
- **`dados/infinite_attention.c`**: implementa `shift_attention`, varrendo linearmente o Nexus para achar o melhor produto interno em 3D. Atualiza `VirtualContextWindow` com a célula mais relevante e score máximo.

### 3.4. Projeção lexical e ressonância
- **`dados/lexical_projector.c`**: converte texto para vetor usando hash semântico.
- **`dados/kinetic_math.c`**: define a função `recursive_resonance`, um produto interno recursivo em arrays de `omega_float`.

### 3.5. Cortex/“sinapses”
- **`dados/synapse_registry.c`**: define ações de exemplo (connect, write, panic) e constrói um córtex mínimo com um nó de sinapse. Funções de plasticidade são stubs para evitar erros de link.

### 3.6. Visão
- **`dados/vision_cortex.c`**: implementa `visual_hash_raw` (FNV‑like) e `visual_to_vector`, gerando vetor com viés no terceiro componente.

### 3.7. UI ANSI
- **`dados/ansi_engine.c`**: implementa UI de terminal, com limpeza de tela, posicionamento do cursor, desenho de caixas e radar de pontos (vetores).

### 3.8. ZipRaf (armazenamento por camadas)
- **`dados/zipraf_db.c`**: implementa CRC32, criação dos arquivos `layer_*.zrf`, ingestão de arquivos em `support_knowledge/`, hashing e gravação de entradas compactas; recalcula CRC no final.

### 3.9. Log encadeado de eventos
- **`dados/raf_event_log.c`**: implementa append de eventos com hash encadeado (prev/this), conversão hex, e verificação de consistência do log.

### 3.10. Daemon IPC
- **`dados/gaia_daemon.c`**: servidor Unix socket (`gaia.sock`) que responde a operações de busca/insert usando o Nexus. Integra `IPCRequest`/`IPCResponse`.

---

## 4. Ferramentas e demos (C no topo)

### 4.1. Boot simbólico
- **`boot_omega.c`**: executa o boot simbólico, cria o córtex e simula eventos de execução (`run_simulation`) com vetores 3D.

### 4.2. VecDB (builder e query)
- **`gaia_vec_build.c`**: constrói o banco vetorial (VecDB) via varredura recursiva de diretórios; mapeia o arquivo, quantiza vetores e escreve um índice `.index`.
- **`gaia_vec_query.c`**: consulta o VecDB via hashing da query, normalização de vetores e ordenação por produto interno; imprime os top‑k.

### 4.3. NanoGPT host simbólico
- **`gaia_nanogpt.c`**: simula uma janela de contexto gigante (1B vetores), usa o Nexus para atenção e “gera” respostas simbólicas dependendo do score e do conteúdo mapeado.

### 4.4. Motores “Rafaelia”
- **`raf_coexist_v2.c`**: define um universo de nós com quatro famílias matemáticas simbólicas (Fibo, Riemann, Navier‑Stokes, Yang‑Mills), hashes e ciclos de resolução linear com hints.
- **`raf_coexist_quintic.c`**: especializa em equações de 5º grau; usa Newton–Raphson e gera estatísticas de dificuldade por nó.
- **`raf_coexist_mixed.c`**: combina polinômios de grau 2‑6 e trigonometria; mede convergência e throughput.
- **`raf_coexist_mixed_pipelines.c`**: estende o modo mixed com pipelines secundários para nós difíceis (reprocessamento e reamostragem de coeficientes).

---

## 5. Ferramentas Python

### 5.1. `aether_hybrid_core.py`
CLI que fornece hashing híbrido: AETHER (FNV+rotate), IRON (SHA‑256) e BLAKE2b. Usa heurística de tamanho para escolher o caminho rápido (AETHER) ou turbo (BLAKE2b).

### 5.2. `aether_hybrid_web.py`
Serviço Flask com UI simples e API `/api/hash`, oferecendo AETHER e IRON via web. Inclui renderização HTML e tratamento de uploads/JSON.

### 5.3. `gaia_chat.py`
Cliente IPC em Python que envia queries para `gaia.sock`, converte texto em vetor via hashing local e interpreta a resposta (match/sem memória).

---

## 6. Scripts de build e geração

### 6.1. `build_gaia.sh`
Script de build “tudo‑em‑um” que gera headers, implementações em C, e compila binários principais (boot, ingest, visual, daemon, nanogpt, etc.). Também descreve uma sequência de comandos para uso pós‑instalação.

### 6.2. `build_vecdb.sh`
Gera `omega_vecdb.h` e compila `gaia_vec_build`/`gaia_vec_query`, responsáveis pelo VecDB. Inclui a lógica de ingestão recursiva.

### 6.3. `build_commander_zipraf.sh`
Gera `omega_zipraf.h`, implementa `zipraf_db.c` e monta o ambiente de camadas semânticas; é a base do mecanismo ZipRaf e do “Commander”.

### 6.4. `build_raf_log.sh`
Gera `raf_event_log.h` e `raf_event_log.c`, provendo um log encadeado verificável e imutável.

---

## 7. Artefatos e dados

### 7.1. Artefatos de dados e exemplo
- **`dummy_data.txt`**: amostra textual usada para ingestão em Nexus.
- **`checkpoint2.zip`**: artefato zipado, possivelmente checkpoint ou dataset de exemplo.

### 7.2. Dados Vetoriais e ZipRaf
- **`dados/gaia_semcore.vecdb`** e **`dados/gaia_semcore.vecdb.index`**: exemplos de VecDB e índice.
- **`dados/layer_0.zrf`**…`dados/layer_7.zrf`: camadas ZipRaf pré‑geradas.

### 7.3. Binários/executáveis pré‑compilados
Existem executáveis sem extensão (ex.: `gaia_boot`, `gaia_vec_build`, `gaia_vec_query`, `gaia_nanogpt`, `gaia_d`, `gaia_visual`, `gaia_client`, `gaia_zipraf_inspect`, etc.) tanto na raiz quanto dentro de `dados/`. Estes binários refletem o resultado de builds anteriores e devem ser tratados como artefatos prontos para execução ou inspeção.

---

## 8. Inventário por arquivo (root)

### 8.1. C (fontes principais)
- **`boot_omega.c`** — boot simbólico do córtex, executa padrões de teste.
- **`gaia_vec_build.c`** — builder do VecDB com mmap e indexação.
- **`gaia_vec_query.c`** — consulta por similaridade no VecDB.
- **`gaia_nanogpt.c`** — host simbólico de NanoGPT (atenção + Nexus).
- **`raf_coexist_v2.c`** — engine RAFAELIA v2 (famílias matemáticas simbólicas).
- **`raf_coexist_quintic.c`** — engine RAFAELIA quíntica (Newton–Raphson).
- **`raf_coexist_mixed.c`** — engine mista (polinômios + trigonometria).
- **`raf_coexist_mixed_pipelines.c`** — engine mista com pipelines de reprocessamento.

### 8.2. Python
- **`aether_hybrid_core.py`** — CLI de hashing híbrido (AETHER/IRON/BLAKE).
- **`aether_hybrid_web.py`** — serviço web (Flask) para hashing.
- **`gaia_chat.py`** — cliente IPC via socket Unix.

### 8.3. Shell
- **`build_gaia.sh`** — gerador e compilador completo da plataforma.
- **`build_vecdb.sh`** — gerador de VecDB e ferramentas.
- **`build_commander_zipraf.sh`** — gerador do ZipRaf e ambiente “Commander”.
- **`build_raf_log.sh`** — gerador do log encadeado.

### 8.4. Dados e artefatos
- **`dummy_data.txt`** — exemplo de dados para ingestão.
- **`checkpoint2.zip`** — arquivo zipado de referência.
- **`LICENSE`** — licença do repositório.

### 8.5. Executáveis e binários
- **`gaia_boot`, `gaia_ingest`, `gaia_absorb`, `gaia_visual`, `gaia_d`, `gaia_client`, `gaia_vec_build`, `gaia_vec_query`, `gaia_nanogpt`, `gaia_zipraf_inspect`, `raf_coexist_v2`, `raf_coexist_quintic`, `raf_coexist_mixed`, `raf_coexist_mixed_pipelines`** — binários pré‑compilados.

---

## 9. Inventário por arquivo (diretório `dados/`)

### 9.1. Headers
- `omega_protocol.h`, `omega_hash.h`, `omega_vecdb.h`, `omega_asm.h`, `omega_nexus.h`, `omega_attention.h`, `omega_lexicon.h`, `omega_vision.h`, `omega_gui.h`, `omega_ipc.h`, `omega_plasticity.h`, `omega_zipraf.h`, `raf_event_log.h`.

### 9.2. Implementações C
- `semantic_hash.c`, `mmap_nexus.c`, `infinite_attention.c`, `lexical_projector.c`, `kinetic_math.c`, `synapse_registry.c`, `vision_cortex.c`, `ansi_engine.c`, `zipraf_db.c`, `raf_event_log.c`, `gaia_daemon.c`.

### 9.3. Ferramentas e fontes duplicadas
- `boot_omega.c`, `gaia_vec_build.c`, `gaia_vec_query.c`, `gaia_nanogpt.c`, `gaia_chat.py`, além de cópias dos scripts de build.

### 9.4. Artefatos de dados
- `gaia_semcore.vecdb`, `gaia_semcore.vecdb.index`, `layer_0.zrf`…`layer_7.zrf`, `checkpoint2.zip`, `dummy_data.txt`.

### 9.5. Executáveis
- `gaia_boot`, `gaia_vec_build`, `gaia_vec_query`, `gaia_nanogpt`, `gaia_d`, `gaia_client`, `gaia_commander`, `gaia_zipraf_inspect`, `gaia_visual`, `gaia_ingest`, `gaia_absorb`, `gaia_mutant` e outros binários presentes no diretório.

---

## 10. Algoritmos e dinâmicas (nível avançado)

### 10.1. Hashing e projeção vetorial
- **DJB2** é usado como núcleo determinístico para gerar hash de texto; os bits são decompostos para formar 3 componentes de vetor entre 0 e 1. Isso permite representar texto com um vetor compacto e eficiente.
- **AETHER (FNV+rotate)**: variantes do hash FNV são combinadas com rotação para aumentar dispersão. No modo “turbo”, BLAKE2b é usado como fallback para grandes cargas.

### 10.2. Atenção infinita (Nexus)
- A atenção varre o Nexus via produto interno de 3 dimensões, escolhendo a célula com maior score. A escolha de 3D reduz custo de cálculo e torna a busca linear um baseline de simplicidade.

### 10.3. VecDB
- O VecDB usa registros fixos de 32 bytes, quantizando vetores em `uint16_t` para compactar. A consulta calcula produto interno normalizado e ordena por score (top‑k).

### 10.4. ZipRaf
- ZipRaf organiza dados em 8 camadas semânticas. Cada ingestão cria uma entrada compacta que registra hash semântico, vetor e referência, com CRC32 para integridade.

### 10.5. Motores “Rafaelia”
- Os motores “coexist” simulam universos de nós com diferentes tipos de problemas matemáticos. O uso de Newton–Raphson permite medir convergência e “dificuldade” por nó. O modo pipelines avalia nós difíceis com reprocessamento e reamostragem para fins de benchmark e estabilidade.

---

## 11. Bibliografia e referências (sugeridas)

1. Knuth, D. E. *The Art of Computer Programming* — hashing e estruturas de dados.
2. Rivest, R. L. *MD5* e padrões de hashing histórico.
3. FNV Hash Specification — fundamentos do FNV.
4. National Institute of Standards and Technology (NIST) — SHA‑256.
5. RFC 7693 — BLAKE2.
6. Press, W. H. et al. *Numerical Recipes* — Newton–Raphson, estabilidade numérica.
7. Silberschatz, A. et al. *Operating System Concepts* — memória mapeada e IPC.
8. Szeliski, R. *Computer Vision: Algorithms and Applications* — hashing e representação visual.

---

## 12. Observações finais
Esta documentação é intencionalmente extensa e exaustiva para atender o requisito de inventariar e descrever cada arquivo do repositório. Ela oferece uma base sólida para futuras refatorações, migrações de arquitetura (C/ASM) ou consolidação de módulos em um núcleo mais conciso.
