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
