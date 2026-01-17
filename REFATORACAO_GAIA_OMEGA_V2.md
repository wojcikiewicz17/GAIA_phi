# Refatoração total GAIA-Ω / RAFAELIA (v2)

## 1. Nova arquitetura (texto + árvore)

### Objetivo
Separar de forma rígida: CORE determinístico (C-like), orquestração Python, e experimentos Rafaelia. Cada camada tem contratos explícitos e versões rastreáveis.

### Árvore proposta
```
/gaia-core
  /include
    gaia_vector.h
    gaia_hash.h
    gaia_metric.h
    gaia_projection.h
    gaia_nexus.h
    gaia_attention.h
    gaia_vecdb.h
    gaia_zipraf.h
    gaia_log.h
    gaia_error.h
  /src
    vector/
      vector_verb.c
      vector_ops.c
    hash/
      hash_djb2.c
      hash_fnv1a.c
      hash_aether.c
    metric/
      metric_dot.c
      metric_cosine.c
      metric_l1.c
    projection/
      projection_3d.c
      projection_nd.c
    storage/
      nexus_mmap.c
      vecdb.c
      zipraf.c
    attention/
      attention_linear.c
      attention_registry.c
    log/
      log_chain.c
    util/
      endian.c
      bytes.c
  /tests
    test_hash.c
    test_vector.c
    test_nexus.c
    test_vecdb.c

/gaia-engines
  /include
    raf_engine.h
  /src
    raf_newton.c
    raf_pipelines.c
    raf_metrics.c
  /plugins
    raf_coexist_v2.c
    raf_coexist_quintic.c
    raf_coexist_mixed.c
    raf_coexist_mixed_pipelines.c

/gaia-orchestrator
  /gaia
    __init__.py
    ingest.py
    memory.py
    query.py
    visualize.py
    registry.py
  /cli
    gaia_cli.py
  /ffi
    ffi_stub.py

/gaia-tools
  build/
    build.sh
    build_core.sh
    build_engines.sh
    build_python.sh
  data/
    dummy_data.txt
  scripts/
    prepare_zipraf_layers.sh
    bench_minimal.sh

/gaia-experiments
  /rafaelia
    notebooks/
    datasets/
    reports/

/docs
  architecture.md
  core_api.md
  migration_plan.md
```

### Dependências entre módulos
- gaia-core não depende de Python, nem de engines. Apenas C padrão e utilitários internos.
- gaia-engines depende de gaia-core (headers) para vetores, métricas, logging e contratos.
- gaia-orchestrator depende de gaia-core via FFI (futuro) e não depende de gaia-engines por padrão.
- gaia-tools depende de gaia-core e gaia-engines para build, diagnóstico e benchmarks.
- gaia-experiments depende de gaia-engines e gaia-orchestrator, nunca de gaia-core direto.

## 2. O que é removido, fundido ou renomeado

### Removido
- Scripts de build duplicados no root e em dados/.
- Binários compilados e artefatos de log versionados no root.

### Fundido
- Headers duplicados de omega_* no root e em dados/ viram gaia-core/include/*.
- Implementações paralelas de hashing e vetorização passam para gaia-core/src/hash e gaia-core/src/vector.

### Renomeado
- omega_* -> gaia_* (padronização semântica, sem perda de conceito).
- VectorVerb -> GaiaVector (mantendo compatibilidade por typedef).
- Nexus -> gaia_nexus (API explícita com init/insert/scan/close).
- ZipRaf -> gaia_zipraf_layer (camadas semanticamente versionadas).

## 3. Especificação clara do CORE GAIA-Ω v2

### Princípios
- Determinístico, sem dependências externas pesadas.
- Hashing e vetores são primários.
- APIs pequenas, estáveis, auditáveis e com contratos explícitos.

### Componentes do core
- gaia_vector: tipo de vetor, dimensão, capacidade, operações básicas.
- gaia_hash: hashing semântico base (DJB2, FNV1a, AETHER).
- gaia_projection: projeção 3D e N-dimensional.
- gaia_metric: métricas (dot, cosine, L1).
- gaia_nexus: memória persistente (MMAP) com interface mínima.
- gaia_attention: estratégias registráveis (linear por default).
- gaia_vecdb: armazenamento compacto com layout fixo e quantização.
- gaia_zipraf: camadas semanticamente versionadas com CRC.
- gaia_log: log encadeado com integridade.

## 4. Interfaces-chave (pseudocódigo/headers)

### gaia_vector.h
```
typedef struct {
    float *data;
    uint32_t dim;
    uint32_t cap;
    uint32_t flags;
} GaiaVector;

GaiaVector gaia_vector_make(uint32_t dim);
void gaia_vector_free(GaiaVector *v);
int gaia_vector_resize(GaiaVector *v, uint32_t dim);
float gaia_vector_dot(const GaiaVector *a, const GaiaVector *b);
int gaia_vector_normalize(GaiaVector *v);
```

### gaia_hash.h
```
typedef enum {
    GAIA_HASH_DJB2,
    GAIA_HASH_FNV1A,
    GAIA_HASH_AETHER
} GaiaHashKind;

uint64_t gaia_hash_bytes(GaiaHashKind kind, const uint8_t *buf, size_t len);
```

### gaia_projection.h
```
int gaia_project_3d(uint64_t hash, float out[3]);
int gaia_project_nd(uint64_t hash, float *out, uint32_t dim);
```

### gaia_metric.h
```
float gaia_metric_dot(const GaiaVector *a, const GaiaVector *b);
float gaia_metric_cosine(const GaiaVector *a, const GaiaVector *b);
float gaia_metric_l1(const GaiaVector *a, const GaiaVector *b);
```

### gaia_nexus.h
```
typedef struct GaiaNexus GaiaNexus;

int gaia_nexus_init(GaiaNexus **out, const char *path, size_t capacity);
int gaia_nexus_insert(GaiaNexus *nx, const GaiaVector *v, uint64_t id);
int gaia_nexus_scan(GaiaNexus *nx, const GaiaVector *query,
                    uint64_t *out_ids, float *out_scores, size_t limit);
void gaia_nexus_close(GaiaNexus *nx);
```

### gaia_attention.h
```
typedef struct {
    const char *name;
    int (*score)(const GaiaVector *query, const GaiaVector *vec, float *out_score);
} GaiaAttentionStrategy;

int gaia_attention_register(const GaiaAttentionStrategy *strategy);
int gaia_attention_apply(const char *name, const GaiaVector *query,
                         const GaiaVector *vec, float *out_score);
```

### gaia_vecdb.h
```
typedef struct GaiaVecDB GaiaVecDB;

int gaia_vecdb_open(GaiaVecDB **out, const char *path);
int gaia_vecdb_insert(GaiaVecDB *db, const GaiaVector *v, uint64_t id);
int gaia_vecdb_query(GaiaVecDB *db, const GaiaVector *query,
                     uint64_t *out_ids, float *out_scores, size_t limit);
void gaia_vecdb_close(GaiaVecDB *db);
```

### gaia_zipraf.h
```
typedef struct {
    uint32_t version;
    uint32_t layer_id;
} GaiaZipRafLayerSpec;

int gaia_zipraf_open_layer(const char *path, GaiaZipRafLayerSpec spec);
int gaia_zipraf_append(const char *path, const void *record, size_t len);
```

### raf_engine.h
```
typedef struct {
    const char *name;
    int (*run)(const void *input, void *output);
    int (*metrics)(void *out_metrics);
} RafEngine;

int raf_engine_register(const RafEngine *engine);
int raf_engine_execute(const char *name, const void *input, void *output);
```

## 5. Plano de migração incremental

1. Congelar o estado atual e criar branch de refatoração.
2. Extrair headers omega_* para gaia-core/include com typedefs de compatibilidade.
3. Criar gaia_core build mínimo com hash + vector + projection.
4. Migrar Nexus/MMAP para gaia_nexus com init/insert/scan/close.
5. Migrar VecDB e ZipRaf para gaia_core/storage com APIs claras.
6. Isolar engines Rafaelia em gaia-engines com registro de plugins.
7. Migrar scripts Python para gaia-orchestrator com módulos ingest/memory/query/visualize.
8. Unificar build em gaia-tools/build com targets reprodutíveis.
9. Remover duplicações antigas e manter um mapa de compatibilidade por 1 versão.

## 6. Como supera LLaMA conceitualmente

- Prioriza determinismo e auditabilidade, não opacidade estatística.
- Vetores são gerados por hashing semântico controlável, sem dependência de treino massivo.
- Memória persistente e atenção linear são explícitas e rastreáveis.
- Permite integração com motores simbólicos (Rafaelia) sem acoplamento frágil.
- Escala para múltiplos backends (CPU, WASM, Rust, Python) sem dependências pesadas.

## 7. Diretrizes de build e DevEx

- build.sh orquestra compilações do core, engines e ferramentas.
- build_core.sh compila apenas gaia-core e testes de sanidade.
- build_engines.sh compila plugins Rafaelia.
- build_python.sh valida lint e empacotamento básico do orquestrador.

### Testes mínimos sugeridos
- test_hash: valida hashes determinísticos.
- test_vector: valida operações vetoriais básicas.
- test_nexus: valida init/insert/scan/close.
- test_vecdb: valida layout e consulta simples.

## 8. Contratos de logs e métricas

- gaia_log expõe API de log encadeado (hash de eventos + checksum).
- engines Rafaelia reportam métricas padronizadas (tempo, iterações, convergência).
- orquestrador Python registra execução e artifacts em diretório de experimento.
