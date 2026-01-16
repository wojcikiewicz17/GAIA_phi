#!/bin/bash
# =============================================================================
# GAIA-Ω: SEMCORE VETORIZADO (32MB) — Banco de Vetores para "Vetor, Verbo"
# Cria:
#   - headers/omega_vecdb.h
#   - gaia_vec_build  : constrói o banco vetorizado a partir de arquivos
#   - gaia_vec_query  : consulta por similaridade
# =============================================================================

BASE_DIR=~/gaia_omega_build
cd "$BASE_DIR" || exit 1

mkdir -p headers
mkdir -p core
mkdir -p vecdb_data

echo "[INIT] Instalando núcleo de banco vetorizado (SemCore 32MB)..."

# =============================================================================
# 1. HEADER: Estrutura do VecDB (SemCore)
# =============================================================================

cat << 'HDR' > headers/omega_vecdb.h
#ifndef OMEGA_VECDB_H
#define OMEGA_VECDB_H

#include <stdint.h>

// Banco Vetorial compacto, alinhado para ~32MB total.
// Layout:
//   [Header: 64 bytes]
//   [MaxEntries * RecordSize]
// Com MaxEntries=1_000_000 e RecordSize=32 => ~32.000.064 bytes

#define VECD_MAGIC 0x56454344u  // 'VECD'
#define VECD_VERSION 1
#define VECD_DIM 3              // 3 dimensões (compatível com hash_to_vector)
#define VECD_RECORD_SIZE 32     // sizeof(VecDBRecord)

typedef struct __attribute__((packed)) {
    uint32_t magic;         // "VECD"
    uint32_t version;       // versão do formato
    uint32_t dim;           // número de componentes no vetor (3)
    uint32_t record_size;   // tamanho fixo da struct VecDBRecord
    uint64_t max_entries;   // capacidade máxima
    uint64_t used_entries;  // quantos registros preenchidos
    uint8_t  reserved[32];  // padding / futuro (total header = 64 bytes)
} VecDBHeader;

// Record exatamente 32 bytes
typedef struct __attribute__((packed)) {
    uint64_t semantic_hash;     // hash semântico do conteúdo
    uint16_t qvec[4];           // vetor quantizado (0..65535) em até 4D (usamos 3 + 1 reserva)
    uint16_t layer_and_ports;   // bits: 0-2=layer, 3-10=ports, 11-15=flags
    uint32_t extra_flags;       // reservado pra RAFAELIA (mutado, zipraf, etc.)
    uint64_t doc_ref;           // ID lógico / hash de arquivo / índice externo
    uint16_t reserved_pad;      // padding -> total 32 bytes
} VecDBRecord;

#endif
HDR

# =============================================================================
# 2. BUILDER: gaia_vec_build
# Constrói o banco vetorial a partir de um diretório de arquivos (ex: support_knowledge/)
# =============================================================================

cat << 'SRC' > gaia_vec_build.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <errno.h>

#include "headers/omega_protocol.h"
#include "headers/omega_hash.h"
#include "headers/omega_vecdb.h"

// -----------------------------------------------------------------------------
// Utilitário de erro
// -----------------------------------------------------------------------------
static void die(const char* msg) {
    perror(msg);
    exit(1);
}

// -----------------------------------------------------------------------------
// Hash rápido de arquivo (amostra até 4096 bytes)
// -----------------------------------------------------------------------------
static uint64_t hash_file_quick(const char* path) {
    FILE* f = fopen(path, "rb");
    if (!f) {
        // Se não conseguir abrir, usa apenas o path como hash
        return omega_hash(path);
    }
    const size_t MAX_SAMPLE = 4096;
    unsigned char buf[MAX_SAMPLE];
    size_t n = fread(buf, 1, MAX_SAMPLE, f);
    fclose(f);

    // djb2-like em 64 bits
    uint64_t h = 5381u;
    for (size_t i = 0; i < n; i++) {
        h = ((h << 5) + h) + buf[i];
    }

    // Combina com hash do caminho
    uint64_t hp = omega_hash(path);
    return h ^ (hp << 1);
}

// -----------------------------------------------------------------------------
// Cria e inicializa o VecDB
// -----------------------------------------------------------------------------
static int create_vecdb(const char* db_path, uint64_t max_entries, VecDBHeader** out_hdr, VecDBRecord** out_recs) {
    int fd = open(db_path, O_RDWR | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) return -1;

    uint64_t total_size = sizeof(VecDBHeader) + max_entries * VECD_RECORD_SIZE;
    if (ftruncate(fd, (off_t)total_size) != 0) {
        close(fd);
        return -1;
    }

    void* map = mmap(NULL, total_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (map == MAP_FAILED) {
        close(fd);
        return -1;
    }

    close(fd);

    VecDBHeader* hdr = (VecDBHeader*)map;
    VecDBRecord*  recs = (VecDBRecord*)((uint8_t*)map + sizeof(VecDBHeader));

    memset(hdr, 0, sizeof(*hdr));
    hdr->magic       = VECD_MAGIC;
    hdr->version     = VECD_VERSION;
    hdr->dim         = VECD_DIM;
    hdr->record_size = VECD_RECORD_SIZE;
    hdr->max_entries = max_entries;
    hdr->used_entries= 0;

    *out_hdr  = hdr;
    *out_recs = recs;
    return 0;
}

// -----------------------------------------------------------------------------
// Append de um registro
// -----------------------------------------------------------------------------
static int vecdb_append(VecDBHeader* hdr, VecDBRecord* recs,
                        uint64_t semantic_hash, const omega_float* vec,
                        uint16_t layer, uint16_t ports_mask,
                        uint32_t extra_flags, uint64_t doc_ref) {
    if (hdr->used_entries >= hdr->max_entries) return -1;
    uint64_t idx = hdr->used_entries;
    VecDBRecord* r = &recs[idx];

    r->semantic_hash = semantic_hash;

    // Quantização (0..1) -> 0..65535
    uint16_t q0 = (uint16_t)(vec[0] * 65535.0f + 0.5f);
    uint16_t q1 = (uint16_t)(vec[1] * 65535.0f + 0.5f);
    uint16_t q2 = (uint16_t)(vec[2] * 65535.0f + 0.5f);
    r->qvec[0] = q0;
    r->qvec[1] = q1;
    r->qvec[2] = q2;
    r->qvec[3] = 0;

    uint16_t lp = 0;
    lp |= (layer & 0x7u);           // bits 0-2
    lp |= ((ports_mask & 0xFFu) << 3); // bits 3-10
    // bits 11-15 reservados a flags internos
    r->layer_and_ports = lp;

    r->extra_flags = extra_flags;
    r->doc_ref     = doc_ref;
    r->reserved_pad= 0;

    hdr->used_entries++;
    return 0;
}

// -----------------------------------------------------------------------------
// Caminhamento recursivo de diretório
// -----------------------------------------------------------------------------
static void walk_and_ingest(const char* root,
                            VecDBHeader* hdr,
                            VecDBRecord* recs,
                            FILE* index_out,
                            uint16_t default_layer,
                            uint16_t default_ports)
{
    DIR* d = opendir(root);
    if (!d) {
        fprintf(stderr, "[WARN] Não foi possível abrir %s\n", root);
        return;
    }

    struct dirent* ent;
    char path[2048];

    while ((ent = readdir(d)) != NULL) {
        if (strcmp(ent->d_name, ".")  == 0) continue;
        if (strcmp(ent->d_name, "..") == 0) continue;

        snprintf(path, sizeof(path), "%s/%s", root, ent->d_name);

        struct stat st;
        if (stat(path, &st) != 0) continue;

        if (S_ISDIR(st.st_mode)) {
            // Recursão
            walk_and_ingest(path, hdr, recs, index_out, default_layer, default_ports);
        } else if (S_ISREG(st.st_mode)) {
            if (hdr->used_entries >= hdr->max_entries) {
                fprintf(stderr, "[INFO] Capacidade máxima do VecDB atingida (%llu).\n",
                        (unsigned long long)hdr->max_entries);
                closedir(d);
                return;
            }

            uint64_t h = hash_file_quick(path);

            omega_float vdata[3];
            VectorVerb v;
            v.data      = vdata;
            v.dimension = 3;
            v.kinetic_func = NULL;

            // Usa hash_to_vector do seu núcleo omega_hash
            hash_to_vector(h, &v);

            uint64_t doc_ref = h; // Aqui podemos usar o próprio hash como doc_ref

            if (vecdb_append(hdr, recs, h, v.data,
                             default_layer, default_ports,
                             0u, doc_ref) != 0)
            {
                fprintf(stderr, "[WARN] Falha ao inserir no VecDB.\n");
                continue;
            }

            uint64_t idx = hdr->used_entries - 1;
            fprintf(index_out, "%llu|%llu|%llu|%s\n",
                    (unsigned long long)idx,
                    (unsigned long long)h,
                    (unsigned long long)doc_ref,
                    path);
        }
    }

    closedir(d);
}

int main(int argc, char** argv) {
    if (argc < 3) {
        fprintf(stderr,
            "Uso: %s <saida_vecdb> <diretorio_raiz> [max_entries]\n"
            "Exemplo: %s vecdb_data/gaia_semcore.vecdb support_knowledge 1000000\n",
            argv[0], argv[0]);
        return 1;
    }

    const char* db_path   = argv[1];
    const char* root_dir  = argv[2];
    uint64_t max_entries  = 1000000ull;

    if (argc >= 4) {
        max_entries = strtoull(argv[3], NULL, 10);
        if (max_entries == 0) max_entries = 1000000ull;
    }

    VecDBHeader* hdr = NULL;
    VecDBRecord* recs= NULL;

    if (create_vecdb(db_path, max_entries, &hdr, &recs) != 0) {
        die("create_vecdb");
    }

    // Arquivo de índice (mapeia idx -> path)
    char index_path[2048];
    snprintf(index_path, sizeof(index_path), "%s.index", db_path);
    FILE* index_out = fopen(index_path, "w");
    if (!index_out) {
        die("fopen index");
    }

    // Layer padrão: 3 (HUMAN_CHAT), ports=0x00 (depois você especializa)
    uint16_t default_layer = 3;
    uint16_t default_ports = 0x00u;

    printf("[VECBUILD] Construindo VecDB em '%s' a partir de '%s'...\n",
           db_path, root_dir);
    walk_and_ingest(root_dir, hdr, recs, index_out, default_layer, default_ports);
    fclose(index_out);

    printf("[VECBUILD] Feito. used_entries=%llu / max_entries=%llu\n",
           (unsigned long long)hdr->used_entries,
           (unsigned long long)hdr->max_entries);

    // sync & unmap
    uint64_t total_size = sizeof(VecDBHeader) + hdr->max_entries * VECD_RECORD_SIZE;
    msync(hdr, total_size, MS_SYNC);
    munmap(hdr, total_size);

    return 0;
}
SRC

# =============================================================================
# 3. QUERY: gaia_vec_query
# Consulta o VecDB em memória e retorna os top-K mais similares
# =============================================================================

cat << 'SRC' > gaia_vec_query.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <math.h>

#include "headers/omega_protocol.h"
#include "headers/omega_hash.h"
#include "headers/omega_vecdb.h"

typedef struct {
    uint64_t idx;
    float score;
    VecDBRecord rec;
} VecHit;

// -----------------------------------------------------------------------------
// Utilitário de comparação para ordenar hits (maior score primeiro)
// -----------------------------------------------------------------------------
static int cmp_hits(const void* a, const void* b) {
    const VecHit* ha = (const VecHit*)a;
    const VecHit* hb = (const VecHit*)b;
    if (ha->score < hb->score) return 1;
    if (ha->score > hb->score) return -1;
    return 0;
}

// -----------------------------------------------------------------------------
// Carrega VecDB read-only em memória
// -----------------------------------------------------------------------------
static int open_vecdb(const char* path, VecDBHeader** out_hdr, VecDBRecord** out_recs, uint64_t* out_total_size) {
    int fd = open(path, O_RDONLY);
    if (fd == -1) return -1;

    off_t sz = lseek(fd, 0, SEEK_END);
    if (sz <= 0) {
        close(fd);
        return -1;
    }
    lseek(fd, 0, SEEK_SET);

    void* map = mmap(NULL, (size_t)sz, PROT_READ, MAP_SHARED, fd, 0);
    if (map == MAP_FAILED) {
        close(fd);
        return -1;
    }

    close(fd);

    VecDBHeader* hdr = (VecDBHeader*)map;
    VecDBRecord* recs = (VecDBRecord*)((uint8_t*)map + sizeof(VecDBHeader));

    if (hdr->magic != VECD_MAGIC) {
        fprintf(stderr, "[ERR] VecDB magic inválido.\n");
        munmap(map, (size_t)sz);
        return -1;
    }

    *out_hdr  = hdr;
    *out_recs = recs;
    *out_total_size = (uint64_t)sz;
    return 0;
}

int main(int argc, char** argv) {
    if (argc < 3) {
        fprintf(stderr,
                "Uso: %s <vecdb_path> <texto_busca> [top_k]\n"
                "Exemplo: %s vecdb_data/gaia_semcore.vecdb \"oráculo zipraf\" 5\n",
                argv[0], argv[0]);
        return 1;
    }

    const char* db_path = argv[1];
    const char* query   = argv[2];
    int top_k = 5;
    if (argc >= 4) {
        top_k = atoi(argv[3]);
        if (top_k <= 0) top_k = 5;
        if (top_k > 100) top_k = 100;
    }

    VecDBHeader* hdr = NULL;
    VecDBRecord* recs= NULL;
    uint64_t total_size = 0;

    if (open_vecdb(db_path, &hdr, &recs, &total_size) != 0) {
        fprintf(stderr, "[ERR] Falha ao abrir VecDB.\n");
        return 1;
    }

    printf("[VECQUERY] VecDB: used=%llu / max=%llu / dim=%u\n",
           (unsigned long long)hdr->used_entries,
           (unsigned long long)hdr->max_entries,
           hdr->dim);

    // Projeta a query para vetor
    uint64_t hq = omega_hash(query);
    omega_float qv_data[3];
    VectorVerb qv;
    qv.data      = qv_data;
    qv.dimension = 3;
    qv.kinetic_func = NULL;
    hash_to_vector(hq, &qv);

    // Normaliza o vetor da query
    float qnorm = sqrtf(qv.data[0]*qv.data[0] +
                        qv.data[1]*qv.data[1] +
                        qv.data[2]*qv.data[2] + 1e-12f);
    float q0 = qv.data[0] / qnorm;
    float q1 = qv.data[1] / qnorm;
    float q2 = qv.data[2] / qnorm;

    uint64_t n = hdr->used_entries;
    if (n == 0) {
        fprintf(stderr, "[VECQUERY] Banco vazio.\n");
        munmap(hdr, (size_t)total_size);
        return 0;
    }

    if (top_k > (int)n) top_k = (int)n;

    VecHit* hits = (VecHit*)calloc((size_t)n, sizeof(VecHit));
    if (!hits) {
        fprintf(stderr, "[ERR] Sem memória para hits.\n");
        munmap(hdr, (size_t)total_size);
        return 1;
    }

    // Varre todos os registros em memória (32MB → super rápido)
    for (uint64_t i = 0; i < n; i++) {
        VecDBRecord* r = &recs[i];

        // reconstrói vetor float aproximado a partir dos quantizados
        float v0 = (float)r->qvec[0] / 65535.0f;
        float v1 = (float)r->qvec[1] / 65535.0f;
        float v2 = (float)r->qvec[2] / 65535.0f;

        float vnorm = sqrtf(v0*v0 + v1*v1 + v2*v2 + 1e-12f);
        v0 /= vnorm;
        v1 /= vnorm;
        v2 /= vnorm;

        float score = q0*v0 + q1*v1 + q2*v2;

        hits[i].idx   = i;
        hits[i].score = score;
        hits[i].rec   = *r;
    }

    // Ordena por score (descendente)
    qsort(hits, (size_t)n, sizeof(VecHit), cmp_hits);

    printf("[VECQUERY] Top %d resultados para \"%s\":\n", top_k, query);
    for (int k = 0; k < top_k; k++) {
        VecHit* h = &hits[k];

        uint16_t lp = h->rec.layer_and_ports;
        uint16_t layer = lp & 0x7u;
        uint16_t ports = (lp >> 3) & 0xFFu;

        printf("  #%d  idx=%llu  score=%.4f  hash=%llu  layer=%u  ports=0x%02X  doc_ref=%llu\n",
               k,
               (unsigned long long)h->idx,
               h->score,
               (unsigned long long)h->rec.semantic_hash,
               (unsigned)layer,
               (unsigned)ports,
               (unsigned long long)h->rec.doc_ref);
    }

    free(hits);
    munmap(hdr, (size_t)total_size);
    return 0;
}
SRC

# =============================================================================
# 4. COMPILAÇÃO
# =============================================================================

echo "[BUILD] Compilando gaia_vec_build..."
gcc -O3 gaia_vec_build.c core/semantic_hash.c -o gaia_vec_build -lm

echo "[BUILD] Compilando gaia_vec_query..."
gcc -O3 gaia_vec_query.c core/semantic_hash.c -o gaia_vec_query -lm

chmod +x gaia_vec_build gaia_vec_query

echo "=================================================="
echo " SEMCORE VETORIZADO INSTALADO "
echo "=================================================="
echo "1. Construa o banco (exemplo):"
echo "   ./gaia_vec_build vecdb_data/gaia_semcore.vecdb support_knowledge 1000000"
echo ""
echo "   -> Isso cria:"
echo "      - vecdb_data/gaia_semcore.vecdb       (≈32MB, 1M vetores max)"
echo "      - vecdb_data/gaia_semcore.vecdb.index (idx|hash|doc_ref|path)"
echo ""
echo "2. Consulte o banco:"
echo "   ./gaia_vec_query vecdb_data/gaia_semcore.vecdb \"texto da busca\" 5"
echo ""
echo "   -> Resultado: Top-K vetores mais próximos em memória,"
echo "      pronto pra Nano-GPT estilo 'vetor, vetor, verbo'."
echo "=================================================="

