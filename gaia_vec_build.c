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
