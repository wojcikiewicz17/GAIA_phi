#include "../headers/omega_zipraf.h"
#include "../headers/omega_hash.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <errno.h>

// -----------------------------------------------------------------------------
// CRC32 simples
// -----------------------------------------------------------------------------
uint32_t calc_crc32(const unsigned char *buf, size_t len) {
    uint32_t crc = 0xFFFFFFFFu;
    for (size_t i = 0; i < len; i++) {
        crc ^= buf[i];
        for (int j = 0; j < 8; j++) {
            uint32_t mask = -(crc & 1u);
            crc = (crc >> 1) ^ (0xEDB88320u & mask);
        }
    }
    return ~crc;
}

// -----------------------------------------------------------------------------
// Utilitário: cópia binária segura (sem system("cp"))
// -----------------------------------------------------------------------------
static int copy_file_binary(const char* src, const char* dst) {
    FILE* in  = fopen(src, "rb");
    if (!in)  { perror("[copy] fopen src"); return -1; }
    FILE* out = fopen(dst, "wb");
    if (!out) { perror("[copy] fopen dst"); fclose(in); return -1; }

    unsigned char buf[8192];
    size_t n;
    while ((n = fread(buf, 1, sizeof(buf), in)) > 0) {
        if (fwrite(buf, 1, n, out) != n) {
            perror("[copy] fwrite");
            fclose(in); fclose(out);
            return -1;
        }
    }
    fclose(in);
    fclose(out);
    return 0;
}

// -----------------------------------------------------------------------------
// Inicializa os 8 arquivos .zrf, se não existirem
// -----------------------------------------------------------------------------
void zipraf_init_db(void) {
    for (int i = 0; i < 8; i++) {
        char path[128];
        snprintf(path, sizeof(path), "semantics/layer_%d.zrf", i);

        FILE* f = fopen(path, "rb");
        if (!f) {
            f = fopen(path, "wb");
            if (!f) {
                fprintf(stderr, "[ZIPRAF] ERRO ao criar %s: %s\n",
                        path, strerror(errno));
                continue;
            }
            ZipRafHeader h;
            memset(&h, 0, sizeof(h));
            h.magic       = ZIPRAF_MAGIC;
            h.version     = 1;
            h.layer_id    = (uint32_t)i;
            h.data_offset = sizeof(ZipRafHeader);
            fwrite(&h, sizeof(h), 1, f);
            printf("[ZIPRAF] Layer %d inicializado: %s\n", i, path);
        }
        if (f) fclose(f);
    }
}

// -----------------------------------------------------------------------------
// Atualiza CRC32 (recalcula sobre toda a área de dados de entradas)
// -----------------------------------------------------------------------------
static void zipraf_recalc_crc(FILE* zf, ZipRafHeader* h) {
    if (!zf || !h) return;
    if (fseek(zf, 0, SEEK_END) != 0) return;
    long end_pos = ftell(zf);
    if (end_pos <= 0) return;
    long data_len = end_pos - (long)h->data_offset;
    if (data_len <= 0) {
        h->crc32 = 0;
        return;
    }

    if (fseek(zf, (long)h->data_offset, SEEK_SET) != 0) return;

    unsigned char* buf = (unsigned char*)malloc((size_t)data_len);
    if (!buf) return;

    size_t r = fread(buf, 1, (size_t)data_len, zf);
    if (r != (size_t)data_len) {
        free(buf);
        return;
    }

    h->crc32 = calc_crc32(buf, (size_t)data_len);
    free(buf);
}

// -----------------------------------------------------------------------------
// Ingestão Otimizada:
// 1. Copia arquivo para support_knowledge/ (raw)
// 2. Calcula hash e vetor
// 3. Grava entrada compacta no layer_X.zrf correspondente
// -----------------------------------------------------------------------------
int zipraf_ingest(const char* filepath,
                  const char* filename,
                  SemanticLayer layer)
{
    if (!filepath || !filename) return -1;
    if (layer < 0 || layer > 7) layer = SEM_META_SELF;

    // 1) Copia RAW para support_knowledge/
    char dest_path[512];
    snprintf(dest_path, sizeof(dest_path),
             "support_knowledge/%s", filename);

    if (copy_file_binary(filepath, dest_path) != 0) {
        fprintf(stderr, "[ZIPRAF] Falha ao copiar '%s' -> '%s'\n",
                filepath, dest_path);
        return -2;
    }

    // 2) Amostra do conteúdo para hash semântico (até 4096 bytes)
    FILE* f = fopen(dest_path, "rb");
    if (!f) {
        fprintf(stderr, "[ZIPRAF] Não foi possível reabrir '%s'\n", dest_path);
        return -3;
    }
    if (fseek(f, 0, SEEK_END) != 0) {
        fclose(f);
        return -3;
    }
    long fsize = ftell(f);
    if (fsize < 0) {
        fclose(f);
        return -3;
    }
    if (fseek(f, 0, SEEK_SET) != 0) {
        fclose(f);
        return -3;
    }

    long sample_size = fsize > 4096 ? 4096 : fsize;
    if (sample_size <= 0) {
        fclose(f);
        fprintf(stderr, "[ZIPRAF] Arquivo vazio '%s'\n", dest_path);
        return -3;
    }

    char* buf = (char*)malloc((size_t)sample_size);
    if (!buf) {
        fclose(f);
        fprintf(stderr, "[ZIPRAF] Sem memória para hash\n");
        return -3;
    }
    size_t rb = fread(buf, 1, (size_t)sample_size, f);
    fclose(f);
    if (rb == 0) {
        free(buf);
        fprintf(stderr, "[ZIPRAF] Leitura vazia de '%s'\n", dest_path);
        return -3;
    }

    uint64_t doc_hash = semantic_hash_djb2(buf);
    free(buf);

    // 3) Vetorização via hash_to_vector
    omega_float vec_data[3];
    VectorVerb v;
    v.data         = vec_data;
    v.dimension    = 3;
    v.kinetic_func = NULL;
    hash_to_vector(doc_hash, &v);

    // 4) Append no layer_X.zrf
    char layer_path[128];
    snprintf(layer_path, sizeof(layer_path),
             "semantics/layer_%d.zrf", (int)layer);

    FILE* zf = fopen(layer_path, "r+b");
    if (!zf) {
        fprintf(stderr, "[ZIPRAF] Falha ao abrir layer '%s'\n", layer_path);
        return -4;
    }

    ZipRafHeader h;
    if (fread(&h, sizeof(h), 1, zf) != 1) {
        fclose(zf);
        fprintf(stderr, "[ZIPRAF] Falha ao ler header em '%s'\n", layer_path);
        return -4;
    }

    h.entry_count++;

    // Escreve entrada no fim
    if (fseek(zf, 0, SEEK_END) != 0) {
        fclose(zf);
        return -4;
    }

    ZipRafEntry entry;
    memset(&entry, 0, sizeof(entry));
    entry.semantic_hash = doc_hash;
    entry.vector[0]     = v.data[0];
    entry.vector[1]     = v.data[1];
    entry.vector[2]     = v.data[2];
    entry.doc_ref_id    = doc_hash; // ID lógico (para lookups futuros)

    if (fwrite(&entry, sizeof(entry), 1, zf) != 1) {
        fclose(zf);
        fprintf(stderr, "[ZIPRAF] Falha ao escrever entrada em '%s'\n", layer_path);
        return -4;
    }

    // Recalcula CRC32 da área de dados
    zipraf_recalc_crc(zf, &h);

    // Volta e grava header atualizado
    if (fseek(zf, 0, SEEK_SET) == 0) {
        fwrite(&h, sizeof(h), 1, zf);
    }
    fclose(zf);

    printf("[ZIPRAF] '%s' → layer %d | entries=%llu\n",
           filename, (int)layer, (unsigned long long)h.entry_count);

    return 0;
}
