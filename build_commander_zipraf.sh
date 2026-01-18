#!/bin/bash
# =============================================================================
# GAIA-OMEGA: COMMANDER UPDATE (ZIPRAF ENGINE + DOS SHELL UI) — v2
# Compatível com o núcleo já existente (omega_protocol, omega_hash, etc.)
# =============================================================================

BASE_DIR=${BASE_DIR:-$(pwd)/gaia_omega_build}
mkdir -p "$BASE_DIR"
mkdir -p "$BASE_DIR/headers"
mkdir -p "$BASE_DIR/core"
mkdir -p "$BASE_DIR/nexus_zipraf"      # opcional, reservado
mkdir -p "$BASE_DIR/semantics"        # 8 camadas
mkdir -p "$BASE_DIR/support_knowledge"
cd "$BASE_DIR" || exit 1

echo "[INIT] Instalando / atualizando Protocolo ZipRaf e GAIA COMMANDER..."

# =============================================================================
# 1. PROTOCOLO ZIPRAF (Storage Otimizado em 8 Camadas Semânticas)
# =============================================================================

cat << 'HDR' > headers/omega_zipraf.h
#ifndef OMEGA_ZIPRAF_H
#define OMEGA_ZIPRAF_H

#include <stdint.h>
#include "omega_protocol.h"

// Assinatura Mágica: 0x5A 0x52 0x41 0x46 (ZRAF)
#define ZIPRAF_MAGIC 0x4641525A

// As 8 Camadas Semânticas
typedef enum {
    SEM_CORE_LOGIC   = 0, // Código, Matemática, Algoritmos
    SEM_SYS_ADMIN    = 1, // Scripts, Configs, Logs
    SEM_NET_SEC      = 2, // Network, Crypto, Segurança
    SEM_HUMAN_CHAT   = 3, // Diálogo natural (JSON, txt)
    SEM_VISUAL_MEM   = 4, // Imagens, ASCII Art
    SEM_AUDIO_WAVE   = 5, // Som / Voz (futuro)
    SEM_TEMPORAL     = 6, // Séries temporais / histórico
    SEM_META_SELF    = 7  // Estado interno, metadados
} SemanticLayer;

// Cabeçalho de Arquivo ZipRaf (32 bytes)
typedef struct {
    uint32_t magic;         // "ZRAF"
    uint32_t version;       // v1
    uint32_t layer_id;      // 0-7
    uint32_t crc32;         // Checksum dos dados
    uint64_t entry_count;   // Quantos vetores
    uint64_t data_offset;   // Offset do primeiro ZipRafEntry
} ZipRafHeader;

// Entrada Compacta
// float[3] (12B) + semantic_hash(8B) + doc_ref_id(8B) = 28 bytes
typedef struct {
    uint64_t    semantic_hash; // "DNA" do conteúdo
    omega_float vector[3];     // Coordenadas
    uint64_t    doc_ref_id;    // ID lógico para /support_knowledge
} ZipRafEntry;

// API do ZipRaf
void        zipraf_init_db(void);
int         zipraf_ingest(const char* filepath,
                          const char* filename,
                          SemanticLayer layer);
uint32_t    calc_crc32(const unsigned char *buf, size_t len);

#endif
HDR

# =============================================================================
# 2. CORE ZIPRAF (Implementação do Storage)
# =============================================================================

cat << 'SRC' > core/zipraf_db.c
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
SRC

# =============================================================================
# 3. GAIA COMMANDER (TUI estilo DOS / Norton Commander)
# =============================================================================

cat << 'SRC' > tools_commander.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>
#include <unistd.h>
#include <termios.h>
#include <sys/stat.h>
#include <errno.h>

#include "headers/omega_zipraf.h"
#include "headers/omega_hash.h"

// Cores estilo DOS
#define BG_BLUE   "\033[44m"
#define FG_WHITE  "\033[37m"
#define FG_CYAN   "\033[36m"
#define FG_YELLOW "\033[33m"
#define RESET     "\033[0m"

static struct termios orig_termios;

static void disableRawMode(void) {
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &orig_termios);
    printf("\033[?25h"); // mostra cursor
}

static void enableRawMode(void) {
    tcgetattr(STDIN_FILENO, &orig_termios);
    atexit(disableRawMode);
    struct termios raw = orig_termios;
    raw.c_lflag &= ~(ECHO | ICANON);
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw);
    printf("\033[?25l"); // oculta cursor
}

static void cls(void) {
    printf("\033[2J\033[H");
}

static void draw_bar(int y, const char* text) {
    printf("\033[%d;1H%s%s%-80s%s", y, BG_BLUE, FG_WHITE, text, RESET);
}

// -----------------------------------------------------------------------------
// Heurística para camada semântica por extensão
// -----------------------------------------------------------------------------
static SemanticLayer guess_layer(const char* filename) {
    if (!filename) return SEM_META_SELF;

    if (strstr(filename, ".c")   ||
        strstr(filename, ".h")   ||
        strstr(filename, ".py")  ||
        strstr(filename, ".rs"))   return SEM_CORE_LOGIC;

    if (strstr(filename, ".sh")  ||
        strstr(filename, ".conf")||
        strstr(filename, ".log"))  return SEM_SYS_ADMIN;

    if (strstr(filename, ".pem") ||
        strstr(filename, ".crt") ||
        strstr(filename, ".key"))  return SEM_NET_SEC;

    if (strstr(filename, ".json") ||
        strstr(filename, ".jsonl")||
        strstr(filename, ".txt")  ||
        strstr(filename, ".md"))   return SEM_HUMAN_CHAT;

    if (strstr(filename, ".png")  ||
        strstr(filename, ".jpg")  ||
        strstr(filename, ".jpeg") ||
        strstr(filename, ".webp")) return SEM_VISUAL_MEM;

    return SEM_META_SELF;
}

// Resolve tipo de entrada: arquivo ou diretório (fallback se d_type for 0)
static int is_directory(const char* base, const struct dirent* ent) {
    if (ent->d_type == DT_DIR) return 1;
    if (ent->d_type == DT_REG) return 0;

    // fallback via stat
    char path[1024];
    snprintf(path, sizeof(path), "%s/%s", base, ent->d_name);
    struct stat st;
    if (stat(path, &st) == 0) {
        return S_ISDIR(st.st_mode) ? 1 : 0;
    }
    return 0;
}

// -----------------------------------------------------------------------------
// Navegador de Arquivos / Absorção em ZipRaf
// -----------------------------------------------------------------------------
static void file_browser(const char* start_path) {
    struct dirent **namelist = NULL;
    int n;
    int selected      = 0;
    int scroll_offset = 0;
    char cwd[1024];

    strncpy(cwd, start_path, sizeof(cwd)-1);
    cwd[sizeof(cwd)-1] = '\0';

    for (;;) {
        cls();
        draw_bar(1, " GAIA-OMEGA COMMANDER [ZIPRAF ENGINE] ");
        printf("\033[2;1H%sPATH:%s %s%s", FG_YELLOW, RESET, cwd, RESET);

        n = scandir(cwd, &namelist, NULL, alphasort);
        if (n < 0) {
            perror("scandir");
            return;
        }

        int max_rows = 16;
        if (selected >= n) selected = (n > 0 ? n-1 : 0);
        if (selected < 0) selected = 0;

        for (int i = 0; i < max_rows; i++) {
            int idx = i + scroll_offset;
            printf("\033[%d;1H", 4 + i);
            if (idx >= n) {
                printf("                                                                                ");
                continue;
            }

            struct dirent* ent = namelist[idx];
            int is_dir = is_directory(cwd, ent);

            if (idx == selected) {
                printf("%s%s> %-40s%s", BG_BLUE, FG_WHITE, ent->d_name, RESET);
            } else {
                printf("  %-40s", ent->d_name);
            }

            if (is_dir) {
                printf(" [DIR]");
            } else {
                SemanticLayer l = guess_layer(ent->d_name);
                printf(" [LAYER %d]", l);
            }
        }

        draw_bar(22, " [UP/DWN] Navegar | [ENTER] Entrar/Absorver | [Q] Sair ");

        int c = getchar();
        if (c == 'q' || c == 'Q') {
            for (int i=0; i<n; i++) free(namelist[i]);
            free(namelist);
            break;
        }

        if (c == '\033') { // escape sequence
            int c1 = getchar();
            int c2 = getchar();
            if (c1 == '[') {
                if (c2 == 'A') { // up
                    if (selected > 0) selected--;
                    if (selected < scroll_offset) scroll_offset--;
                } else if (c2 == 'B') { // down
                    if (selected < n-1) selected++;
                    if (selected >= scroll_offset + max_rows) scroll_offset++;
                }
            }
        } else if (c == '\n' || c == '\r') {
            if (n == 0) continue;
            struct dirent* ent = namelist[selected];
            int is_dir = is_directory(cwd, ent);

            if (is_dir) {
                if (strcmp(ent->d_name, ".") == 0) {
                    // nada
                } else if (strcmp(ent->d_name, "..") == 0) {
                    // subir
                    char* slash = strrchr(cwd, '/');
                    if (slash && slash != cwd) {
                        *slash = '\0';
                    } else {
                        // volta para / ou mantém
                        strcpy(cwd, "/");
                    }
                } else {
                    size_t len = strlen(cwd);
                    if (len + 1 + strlen(ent->d_name) < sizeof(cwd)) {
                        if (strcmp(cwd, "/") != 0)
                            strcat(cwd, "/");
                        strcat(cwd, ent->d_name);
                    }
                }
                selected      = 0;
                scroll_offset = 0;
            } else {
                // Arquivo → Absorver para ZipRaf
                char fullpath[2048];
                snprintf(fullpath, sizeof(fullpath), "%s/%s", cwd, ent->d_name);

                SemanticLayer l = guess_layer(ent->d_name);

                draw_bar(23, " ABSORVENDO ARQUIVO PARA ZIPRAF... ");
                printf("\033[24;1H%s[INFO]%s %s → camada %d\n",
                       FG_CYAN, RESET, ent->d_name, (int)l);

                int res = zipraf_ingest(fullpath, ent->d_name, l);
                if (res == 0) {
                    printf("\033[25;1H%s[SUCCESS]%s '%s' indexado em layer_%d.zrf\n",
                           FG_CYAN, RESET, ent->d_name, (int)l);
                } else {
                    printf("\033[25;1H[ERROR] falha ao absorver '%s' (code=%d)\n",
                           ent->d_name, res);
                }
                fflush(stdout);
                usleep(600000); // ~0.6s
            }
        }

        for (int i=0; i<n; i++) free(namelist[i]);
        free(namelist);
    }
}

int main(void) {
    zipraf_init_db();
    enableRawMode();

    char cwd[1024];
    if (!getcwd(cwd, sizeof(cwd))) {
        strcpy(cwd, ".");
    }

    file_browser(cwd);

    disableRawMode();
    cls();
    printf("GAIA COMMANDER ENCERRADO.\n");
    return 0;
}
SRC

# =============================================================================
# 4. COMPILAÇÃO
# =============================================================================

echo "[BUILD] Compilando GAIA COMMANDER..."
gcc -O3 tools_commander.c \
    core/zipraf_db.c \
    core/semantic_hash.c \
    -o gaia_commander -lm

if [ $? -eq 0 ]; then
    chmod +x gaia_commander
    echo "=================================================="
    echo " GAIA COMMANDER [ZIPRAF ENGINE] PRONTO "
    echo "=================================================="
    echo "1. Execute:  ./gaia_commander"
    echo "2. Navegue com SETAS."
    echo "3. ENTER em diretório: entra."
    echo "4. ENTER em arquivo: absorve para ZipRaf + copia para support_knowledge/"
    echo "5. Camadas salvas em: $BASE_DIR/semantics/layer_*.zrf"
    echo "=================================================="
else
    echo "[FAIL] Erro na compilação."
fi
