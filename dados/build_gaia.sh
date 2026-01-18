#!/bin/bash
# =============================================================================
# GAIA-Ω: BUILD SYSTEM & ORCHESTRATOR
# Descrição: Reconstrói headers, núcleo e compila as ferramentas GAIA-Ω,
# incluindo o módulo de Atenção Infinita (Nexus-Attention sobre MMAP).
# =============================================================================

BASE_DIR=${BASE_DIR:-$(pwd)/gaia_omega_build}
mkdir -p "$BASE_DIR"
mkdir -p "$BASE_DIR/headers"
mkdir -p "$BASE_DIR/core"
mkdir -p "$BASE_DIR/neural"
mkdir -p "$BASE_DIR/cortex_memory"
cd "$BASE_DIR" || exit 1

echo "[INIT] Gerando Infraestrutura GAIA-Ω em $BASE_DIR..."

# =============================================================================
# 1. HEADERS (Definição de Tipos e Protocolos)
# =============================================================================

cat << 'EOF' > headers/omega_protocol.h
#ifndef OMEGA_PROTOCOL_H
#define OMEGA_PROTOCOL_H

#include <stdint.h>

typedef float omega_float;

typedef struct {
    omega_float* data;
    uint64_t dimension;
    void (*kinetic_func)(void*);
} VectorVerb;

#endif
EOF

cat << 'EOF' > headers/omega_nexus.h
#ifndef OMEGA_NEXUS_H
#define OMEGA_NEXUS_H

#include "omega_protocol.h"
#include <stdio.h>

typedef struct {
    char signature[8];
    uint64_t capacity;
    uint64_t count;
    uint64_t version;
} NexusHeader;

typedef struct {
    uint64_t id;
    omega_float vector[3];
    char action_tag[32];
    float confidence;
    uint32_t flags;
} NexusCell;

int nexus_init(const char* filepath, uint64_t capacity);
int nexus_append(VectorVerb* v, const char* action);
void nexus_scan_match(VectorVerb* input, void (*callback)(NexusCell*));
void nexus_close();

// Ponteiros globais mapeados via mmap_nexus.c
extern NexusHeader* header_ptr;
extern NexusCell*   cells_ptr;

#endif
EOF

cat << 'EOF' > headers/omega_asm.h
#ifndef OMEGA_ASM_H
#define OMEGA_ASM_H

#include "omega_protocol.h"

typedef void (*kinetic_handler_t)(VectorVerb*);

struct SynapseNode {
    omega_float* ref_vector;
    kinetic_handler_t handler;
    struct SynapseNode* next;
    const char* debug_name;
};

void collapse_and_execute(VectorVerb* intent, struct SynapseNode* memory_bank);
struct SynapseNode* build_genesis_cortex();
struct SynapseNode* load_cortex_from_disk();
void learn_new_pattern(VectorVerb* intent, const char* action_name);

#endif
EOF

cat << 'EOF' > headers/omega_hash.h
#ifndef OMEGA_HASH_H
#define OMEGA_HASH_H

#include <stdint.h>
#include "omega_protocol.h"

uint64_t semantic_hash_djb2(const char* str);
uint64_t omega_hash(const char* str); // Alias
void hash_to_vector(uint64_t hash, VectorVerb* v_out);

#endif
EOF

cat << 'EOF' > headers/omega_vision.h
#ifndef OMEGA_VISION_H
#define OMEGA_VISION_H

#include <stdint.h>
#include <stddef.h>   // size_t
#include "omega_protocol.h"

uint64_t visual_hash_raw(const uint8_t* data, size_t len);
void visual_to_vector(uint64_t hash, VectorVerb* v_out);

#endif
EOF

cat << 'EOF' > headers/omega_lexicon.h
#ifndef OMEGA_LEXICON_H
#define OMEGA_LEXICON_H

#include "omega_protocol.h"

void project_text_to_vector(const char* input, VectorVerb* v_out);
omega_float recursive_resonance(omega_float* input, omega_float* memory, int n);

#endif
EOF

cat << 'EOF' > headers/omega_gui.h
#ifndef OMEGA_GUI_H
#define OMEGA_GUI_H

#include "omega_protocol.h"
#include "omega_nexus.h"

#define SCREEN_W 80
#define SCREEN_H 24

void gui_clear();
void gui_move(int x, int y);
void gui_draw_box(int x, int y, int w, int h, const char* title);
void gui_render_radar(VectorVerb* current_input, NexusHeader* header, NexusCell* cells);

#endif
EOF

cat << 'EOF' > headers/omega_plasticity.h
#ifndef OMEGA_PLASTICITY_H
#define OMEGA_PLASTICITY_H

#include "omega_protocol.h"
#include "omega_asm.h"

void learn_new_pattern(VectorVerb* intent, const char* action_name);
struct SynapseNode* load_cortex_from_disk();

#endif
EOF

cat << 'EOF' > headers/omega_ipc.h
#ifndef OMEGA_IPC_H
#define OMEGA_IPC_H

#include "omega_protocol.h"
#include "omega_nexus.h"

#define GAIA_SOCKET_PATH "gaia.sock"

#define OP_PING   0x01
#define OP_SEARCH 0x02
#define OP_INSERT 0x03

typedef struct {
    uint8_t opcode;
    omega_float vector[3]; // Flat array
    char payload[64];
} IPCRequest;

typedef struct {
    uint8_t status;
    uint64_t count;
    NexusCell best_match;
} IPCResponse;

#endif
EOF

# --- Atenção Infinita --------------------------------------------------------

cat << 'EOF' > headers/omega_attention.h
#ifndef OMEGA_ATTENTION_H
#define OMEGA_ATTENTION_H

#include "omega_protocol.h"
#include "omega_nexus.h"

// Janela Virtual de Contexto (não aloca dados, só aponta para o foco)
typedef struct {
    uint64_t    total_capacity; // Ex.: 1 Bilhão de slots no Nexus
    NexusCell*  focus_region;   // Célula atualmente em foco
    float       attention_score;
} VirtualContextWindow;

// Move a "cabeça" de leitura sobre o Nexus com base em um VectorVerb (Query)
void shift_attention(VectorVerb* query, VirtualContextWindow* win);

// Extrai o "token" simbólico associado à célula atual
char* resolve_memory_content(NexusCell* cell);

#endif
EOF

# =============================================================================
# 2. CORE IMPLEMENTATIONS (Núcleo Matemático, Nexus MMAP, etc.)
# =============================================================================

cat << 'EOF' > core/kinetic_math.c
#include "../headers/omega_protocol.h"

omega_float recursive_resonance(omega_float* input, omega_float* memory, int n) {
    return (n <= 0)
        ? 0.0f
        : (*input * *memory) + recursive_resonance(input + 1, memory + 1, n - 1);
}
EOF

cat << 'EOF' > core/semantic_hash.c
#include "../headers/omega_hash.h"

uint64_t semantic_hash_djb2(const char* str) {
    uint64_t hash = 5381;
    int c;
    while ((c = *str++)) hash = ((hash << 5) + hash) + (uint8_t)c;
    return hash;
}

uint64_t omega_hash(const char* str) {
    return semantic_hash_djb2(str);
}

void hash_to_vector(uint64_t hash, VectorVerb* v_out) {
    // v_out->data deve apontar para um buffer de pelo menos 3 floats
    v_out->data[0] = (omega_float)(hash & 0xFFFF) / 65535.0f;
    v_out->data[1] = (omega_float)((hash >> 16) & 0xFFFF) / 65535.0f;
    v_out->data[2] = (omega_float)((hash >> 32) & 0xFFFF) / 65535.0f;
}
EOF

cat << 'EOF' > core/lexical_projector.c
#include "../headers/omega_lexicon.h"
#include "../headers/omega_hash.h"

void project_text_to_vector(const char* input, VectorVerb* v_out) {
    uint64_t h = semantic_hash_djb2(input);
    hash_to_vector(h, v_out);
}
EOF

cat << 'EOF' > core/mmap_nexus.c
#include "../headers/omega_nexus.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/stat.h>

NexusHeader* header_ptr = NULL;
NexusCell*   cells_ptr  = NULL;
static int nexus_fd = -1;
static size_t file_size = 0;

int nexus_init(const char* filepath, uint64_t capacity) {
    nexus_fd = open(filepath, O_RDWR | O_CREAT, 0644);
    if (nexus_fd == -1) return -1;

    size_t total_sz = sizeof(NexusHeader) + (capacity * sizeof(NexusCell));
    struct stat st;
    if (fstat(nexus_fd, &st) == -1) return -1;

    if (st.st_size == 0) {
        if (ftruncate(nexus_fd, total_sz) == -1) return -1;
    }
    file_size = total_sz;

    void* map = mmap(NULL, total_sz, PROT_READ | PROT_WRITE, MAP_SHARED, nexus_fd, 0);
    if (map == MAP_FAILED) return -1;

    header_ptr = (NexusHeader*)map;
    cells_ptr  = (NexusCell*)((char*)map + sizeof(NexusHeader));

    if (st.st_size == 0) {
        memset(header_ptr, 0, sizeof(NexusHeader));
        header_ptr->capacity = capacity;
        header_ptr->count    = 0;
        header_ptr->version  = 1;
        memcpy(header_ptr->signature, "GAIANEX", 7);
    }

    return 0;
}

int nexus_append(VectorVerb* v, const char* action) {
    if (!header_ptr || header_ptr->count >= header_ptr->capacity) return -1;

    NexusCell* c = &cells_ptr[header_ptr->count];
    memset(c, 0, sizeof(NexusCell));

    c->id = header_ptr->count;
    c->vector[0] = v->data[0];
    c->vector[1] = v->data[1];
    c->vector[2] = v->data[2];
    strncpy(c->action_tag, action, 31);
    c->action_tag[31] = '\0';
    c->confidence = 1.0f;
    c->flags = 0;

    header_ptr->count++;
    return 0;
}

void nexus_scan_match(VectorVerb* input, void (*callback)(NexusCell*)) {
    if (!header_ptr || !cells_ptr || !callback) return;

    for (uint64_t i = 0; i < header_ptr->count; i++) {
        NexusCell* c = &cells_ptr[i];
        float dot = (float)(
            input->data[0] * c->vector[0] +
            input->data[1] * c->vector[1] +
            input->data[2] * c->vector[2]
        );
        if (dot > 0.85f) callback(c);
    }
}

void nexus_close() {
    if (header_ptr) {
        munmap(header_ptr, file_size);
        header_ptr = NULL;
        cells_ptr  = NULL;
    }
    if (nexus_fd != -1) {
        close(nexus_fd);
        nexus_fd = -1;
    }
}
EOF

cat << 'EOF' > core/vision_cortex.c
#include "../headers/omega_vision.h"

uint64_t visual_hash_raw(const uint8_t* data, size_t len) {
    uint64_t h = 0xcbf29ce484222325ULL;
    size_t step = (len > 4096) ? len / 1024 : 1;
    for (size_t i = 0; i < len; i += step) {
        h ^= data[i];
        h *= 0x100000001b3ULL;
    }
    return h;
}

void visual_to_vector(uint64_t hash, VectorVerb* v_out) {
    v_out->data[0] = (omega_float)(hash & 0xFFFF) / 65535.0f;
    v_out->data[1] = (omega_float)((hash >> 16) & 0xFFFF) / 65535.0f;
    v_out->data[2] = 0.6f + ((omega_float)((hash >> 32) & 0xFFFF) / 163840.0f);
}
EOF

cat << 'EOF' > core/ansi_engine.c
#include "../headers/omega_gui.h"
#include <stdio.h>

void gui_clear() {
    printf("\033[2J\033[H");
}

void gui_move(int x, int y) {
    printf("\033[%d;%dH", y, x);
}

void gui_draw_box(int x, int y, int w, int h, const char* title) {
    gui_move(x, y); printf("┌");
    for(int i=0;i<w-2;i++) printf("─");
    printf("┐");
    for(int i=1;i<h-1;i++) {
        gui_move(x,y+i); printf("│");
        gui_move(x+w-1,y+i); printf("│");
    }
    gui_move(x,y+h-1); printf("└");
    for(int i=0;i<w-2;i++) printf("─");
    printf("┘");
    if(title) { gui_move(x+2,y); printf(" %s ", title); }
}

void gui_render_radar(VectorVerb* cur, NexusHeader* h, NexusCell* c) {
    if (!h || !c || !cur) return;
    uint64_t limit = (h->count > 500) ? 500 : h->count;
    for(uint64_t i=0;i<limit;i++) {
        int sx = 2 + (int)(c[i].vector[0] * (SCREEN_W-4));
        int sy = 2 + (int)(c[i].vector[1] * (SCREEN_H-4));
        gui_move(sx, sy); printf(".");
    }
    int cx = 2 + (int)(cur->data[0] * (SCREEN_W-4));
    int cy = 2 + (int)(cur->data[1] * (SCREEN_H-4));
    gui_move(cx, cy); printf("+");
}
EOF

cat << 'EOF' > neural/synapse_registry.c
#include "../headers/omega_asm.h"
#include <stdio.h>
#include <stdlib.h>

void action_net_connect(VectorVerb* v)  { (void)v; printf("[ACT] NET_CONNECT\n"); }
void action_io_write(VectorVerb* v)     { (void)v; printf("[ACT] IO_WRITE\n"); }
void action_kernel_panic(VectorVerb* v) { (void)v; printf("[ACT] KERNEL_PANIC\n"); exit(0); }

struct SynapseNode* build_genesis_cortex() {
    static struct SynapseNode n1;
    static omega_float v1[] = {0.1f, 0.9f, 0.1f};
    n1.ref_vector = v1;
    n1.handler    = action_net_connect;
    n1.debug_name = "NET";
    n1.next       = NULL;
    return &n1;
}

struct SynapseNode* load_cortex_from_disk() { return NULL; }
void learn_new_pattern(VectorVerb* intent, const char* action_name) {
    (void)intent; (void)action_name;
}

void collapse_and_execute(VectorVerb* intent, struct SynapseNode* bank) {
    (void)intent;
    if(bank && bank->handler) bank->handler(intent);
}
EOF

cat << 'EOF' > core/gaia_daemon.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>

#include "../headers/omega_ipc.h"
#include "../headers/omega_nexus.h"

extern void nexus_scan_match(VectorVerb*, void (*)(NexusCell*));

static IPCResponse temp_resp;
static int found = 0;

static void _daemon_cb(NexusCell* c) {
    memcpy(&temp_resp.best_match, c, sizeof(NexusCell));
    found = 1;
}

int main() {
    printf("[DAEMON] Iniciando Kernel IPC...\n");
    if (nexus_init("gaia.nexus", 1000000) != 0) return 1;

    int s_fd, c_fd;
    struct sockaddr_un addr;
    s_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (s_fd == -1) return 1;

    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, GAIA_SOCKET_PATH, sizeof(addr.sun_path)-1);
    unlink(GAIA_SOCKET_PATH);
    if(bind(s_fd, (struct sockaddr*)&addr, sizeof(addr)) == -1) return 1;

    listen(s_fd, 5);

    while(1) {
        c_fd = accept(s_fd, NULL, NULL);
        if(c_fd == -1) continue;
        IPCRequest req;
        IPCResponse resp;
        memset(&resp, 0, sizeof(resp));

        if(read(c_fd, &req, sizeof(req)) > 0) {
            VectorVerb v_tmp = { .data = req.vector, .dimension = 3, .kinetic_func = NULL };

            if(req.opcode == OP_SEARCH) {
                found = 0;
                memset(&temp_resp, 0, sizeof(temp_resp));
                nexus_scan_match(&v_tmp, _daemon_cb);
                resp = temp_resp;
                resp.status = found ? 1 : 0;
            } else if (req.opcode == OP_INSERT) {
                nexus_append(&v_tmp, req.payload);
                resp.status = 1;
            } else if (req.opcode == OP_PING) {
                resp.status = 1;
            }

            if (header_ptr) resp.count = header_ptr->count;
        }
        write(c_fd, &resp, sizeof(resp));
        close(c_fd);
    }
    return 0;
}
EOF

# --- Atenção Infinita: implementação sobre Nexus MMAP ------------------------

cat << 'EOF' > core/infinite_attention.c
#include "../headers/omega_attention.h"
#include <string.h>

NexusHeader* header_ptr;
NexusCell*   cells_ptr;

// Dot product simples em 3 dimensões (demo)
static inline float dot3(const omega_float* a, const omega_float* b) {
    return (float)(a[0] * b[0] +
                   a[1] * b[1] +
                   a[2] * b[2]);
}

// Atenção sobre disco (Zero-Copy Attention)
void shift_attention(VectorVerb* query, VirtualContextWindow* win) {
    if (!header_ptr || !cells_ptr || !win || !query || !query->data) {
        return;
    }

    if (query->dimension < 3) {
        return;
    }

    NexusCell* best_cell = NULL;
    float      max_score = -1.0f;

    for (uint64_t i = 0; i < header_ptr->count; i++) {
        NexusCell* candidate = &cells_ptr[i];
        float score = dot3(query->data, candidate->vector);
        if (score > max_score) {
            max_score = score;
            best_cell = candidate;
        }
    }

    win->focus_region    = best_cell;
    win->attention_score = max_score;
    win->total_capacity  = header_ptr->capacity;
}

char* resolve_memory_content(NexusCell* cell) {
    if (!cell) return NULL;

    if (strncmp(cell->action_tag, "IMG:", 4) == 0) {
        return "[DADOS VISUAIS BINÁRIOS]";
    }
    return cell->action_tag;
}
EOF

# =============================================================================
# 3. PROGRAMAS DE USUÁRIO / TOOLS / SHELLS
# =============================================================================

# BOOT OMEGA
cat << 'EOF' > boot_omega.c
#include "headers/omega_protocol.h"
#include "headers/omega_asm.h"
#include <stdio.h>

static void run_simulation(const char* label, omega_float* data, uint64_t dim, struct SynapseNode* cortex) {
    printf("\n--- [EVENTO] %s ---\n", label);
    VectorVerb intent = { .data = data, .dimension = dim, .kinetic_func = NULL };
    collapse_and_execute(&intent, cortex);
}

int main(void) {
    printf("GAIA-OMEGA BOOT\n");
    struct SynapseNode* cortex = build_genesis_cortex();

    omega_float d1[] = {0.95f, 0.05f, 0.0f};
    run_simulation("Save", d1, 3, cortex);

    omega_float d2[] = {0.10f, 0.85f, 0.05f};
    run_simulation("Net", d2, 3, cortex);

    return 0;
}
EOF

# INTERACTIVE MUTANT (simplificado, REPL recursivo)
cat << 'EOF' > interactive_mutant.c
#include "headers/omega_protocol.h"
#include "headers/omega_asm.h"
#include "headers/omega_lexicon.h"
#include "headers/omega_plasticity.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void execute_by_id(int id, VectorVerb* v) {
    (void)v;
    printf("Exec ID: %d\n", id);
}

void recursive_read(char* buffer, int idx) {
    int c = getchar();
    if (c == '\n' || c == EOF) { buffer[idx] = '\0'; return; }
    buffer[idx] = (char)c;
    recursive_read(buffer, idx + 1);
}

void mutant_repl(struct SynapseNode* cortex) {
    (void)cortex;
    char buf[256];
    printf("\nΩ [MUTANT] > ");
    fflush(stdout);
    recursive_read(buf, 0);
    if(buf[0]=='q') return;
    printf("CMD: %s\n", buf);
    mutant_repl(cortex);
}

int main() {
    printf("GAIA MUTANT\n");
    struct SynapseNode* c = build_genesis_cortex();
    mutant_repl(c);
    return 0;
}
EOF

# TOOLS INGEST
cat << 'EOF' > tools_ingest.c
#include "headers/omega_protocol.h"
#include "headers/omega_nexus.h"
#include "headers/omega_hash.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 4096

int main(int argc, char** argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <nexus_file> < <data_stream>\\n", argv[0]);
        return 1;
    }

    if (nexus_init(argv[1], 1000000) != 0) {
        fprintf(stderr, "[ERR] nexus_init falhou.\\n");
        return 1;
    }

    char line[MAX_LINE];
    unsigned long count = 0;

    while (fgets(line, MAX_LINE, stdin)) {
        line[strcspn(line, "\\n")] = 0;
        if(strlen(line) < 2 || line[0] == '#') continue;

        uint64_t h = omega_hash(line);
        omega_float vec[3];
        vec[0] = (omega_float)(h & 0xFFFF) / 65535.0f;
        vec[1] = (omega_float)((h >> 16) & 0xFFFF) / 65535.0f;
        vec[2] = (omega_float)((h >> 32) & 0xFFFF) / 65535.0f;

        VectorVerb v = { .data = vec, .dimension = 3, .kinetic_func = NULL };
        nexus_append(&v, line);
        count++;
    }

    printf("Total: %lu\\n", count);
    nexus_close();
    return 0;
}
EOF

# TOOLS ABSORB (corrigido: checagem de argc e mode)
cat << 'EOF' > tools_absorb.c
#include "headers/omega_protocol.h"
#include "headers/omega_nexus.h"
#include "headers/omega_hash.h"
#include "headers/omega_vision.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void ingest_json(FILE* f) {
    (void)f;
    printf("JSON Ingested.\\n");
}

void ingest_img(const char* p) {
    printf("IMG Ingested: %s\\n", p);
}

int main(int argc, char** argv) {
    if(argc < 3) {
        fprintf(stderr, "Usage: %s <nexus_file> <data_file> [mode]\\n", argv[0]);
        fprintf(stderr, "Mode: 'img' para imagem, outro para JSON/texto.\\n");
        return 1;
    }

    const char* nexus_path = argv[1];
    const char* data_path  = argv[2];
    const char* mode       = (argc >= 4) ? argv[3] : "json";

    if (nexus_init(nexus_path, 1000000) != 0) {
        fprintf(stderr, "[ERR] nexus_init falhou.\\n");
        return 1;
    }

    if(strstr(mode, "img")) {
        ingest_img(data_path);
    } else {
        FILE* f = fopen(data_path, "r");
        if (f) {
            ingest_json(f);
            fclose(f);
        } else {
            fprintf(stderr, "[ERR] Não foi possível abrir '%s'\\n", data_path);
        }
    }

    nexus_close();
    return 0;
}
EOF

# VISUAL SHELL
cat << 'EOF' > visual_shell.c
#include "headers/omega_protocol.h"
#include "headers/omega_nexus.h"
#include "headers/omega_hash.h"
#include "headers/omega_gui.h"
#include <stdio.h>
#include <string.h>

extern NexusHeader* header_ptr;
extern NexusCell*   cells_ptr;

static int found = 0;
static void on_match(NexusCell* c) { (void)c; found = 1; }

int main() {
    if (nexus_init("gaia.nexus", 1000000) != 0) {
        fprintf(stderr, "[ERR] nexus_init falhou.\\n");
        return 1;
    }

    VectorVerb v;
    omega_float buf[3] = {0.0f, 0.0f, 0.0f};
    v.data = buf;
    v.dimension = 3;
    v.kinetic_func = NULL;

    while(1) {
        gui_clear();
        gui_draw_box(1,1,60,10,"GAIA VISUAL");
        if(header_ptr && cells_ptr) gui_render_radar(&v, header_ptr, cells_ptr);

        printf("\\nCMD> ");
        char inbuf[64];
        if(!fgets(inbuf,60,stdin)) break;
        inbuf[strcspn(inbuf, "\\n")] = 0;
        if(inbuf[0]=='q') break;

        uint64_t h = semantic_hash_djb2(inbuf);
        hash_to_vector(h, &v);
        found=0;
        nexus_scan_match(&v, on_match);
    }

    nexus_close();
    return 0;
}
EOF

# VISUAL CLIENT (IPC)
cat << 'EOF' > visual_client.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>

#include "headers/omega_ipc.h"
#include "headers/omega_hash.h"

static int transaction(IPCRequest* req, IPCResponse* resp) {
    int fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (fd == -1) return 0;

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, GAIA_SOCKET_PATH, sizeof(addr.sun_path)-1);

    if(connect(fd, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
        close(fd);
        return 0;
    }

    if (write(fd, req, sizeof(IPCRequest)) <= 0) {
        close(fd);
        return 0;
    }
    if (read(fd, resp, sizeof(IPCResponse)) <= 0) {
        close(fd);
        return 0;
    }

    close(fd);
    return 1;
}

int main() {
    char buf[128];
    IPCRequest req;
    IPCResponse resp;

    while(1) {
        printf("\\nCLIENT> ");
        if(!fgets(buf, 120, stdin)) break;
        buf[strcspn(buf, "\\n")] = 0;
        if(strcmp(buf,"exit")==0) break;

        memset(&req, 0, sizeof(req));
        req.opcode = OP_SEARCH;

        uint64_t h = semantic_hash_djb2(buf);
        req.vector[0] = (float)(h & 0xFFFF)        / 65535.0f;
        req.vector[1] = (float)((h >> 16) & 0xFFFF)/ 65535.0f;
        req.vector[2] = (float)((h >> 32) & 0xFFFF)/ 65535.0f;

        if(transaction(&req, &resp)) {
            printf("STATUS: %d | COUNT: %llu | MATCH: %s\\n",
                   resp.status,
                   (unsigned long long)resp.count,
                   resp.best_match.action_tag);
        } else {
            printf("DAEMON OFFLINE.\\n");
        }
    }
    return 0;
}
EOF

# PYTHON CHAT (simples, alinhado ao IPCRequest)
cat << 'EOF' > gaia_chat.py
import socket, struct

SOCKET_PATH = "gaia.sock"

def hash_djb2(text: str) -> int:
    h = 5381
    for ch in text:
        h = ((h << 5) + h) + ord(ch)
    return h & 0xFFFFFFFFFFFFFFFF

def talk(text: str):
    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(SOCKET_PATH)

        h = hash_djb2(text)
        v0 = (h & 0xFFFF) / 65535.0
        v1 = ((h >> 16) & 0xFFFF) / 65535.0
        v2 = ((h >> 32) & 0xFFFF) / 65535.0

        payload = text.encode("utf-8")[:64]
        payload = payload.ljust(64, b"\\x00")

        # Struct C: uint8_t opcode; float v[3]; char payload[64];
        req = struct.pack("=B3f64s", 2, v0, v1, v2, payload)
        s.sendall(req)
        resp_data = s.recv(1024)
        s.close()

        if not resp_data:
            print("Resposta vazia.")
            return

        # status (B), count(Q), best_match...
        status = resp_data[0]
        if status == 1:
            print("MATCH ENCONTRADO!")
        else:
            print("SEM MEMÓRIA.")
    except Exception as e:
        print(f"ERR: {e}")

if __name__ == "__main__":
    while True:
        t = input("PY> ")
        if t == "q":
            break
        talk(t)
EOF

# DUMMY DATA
cat << 'EOF' > dummy_data.txt
user_id: 101 action: login status: success
user_id: 102 action: purchase item: gpu
system_log: error memory overflow
neural_net: activation layer 4
EOF

# --- NanoGPT Host com Atenção Infinita ---------------------------------------

cat << 'EOF' > gaia_nanogpt.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "headers/omega_protocol.h"
#include "headers/omega_nexus.h"
#include "headers/omega_hash.h"
#include "headers/omega_attention.h"

// Protótipos esperados
uint64_t semantic_hash_djb2(const char* text);
void     hash_to_vector(uint64_t h, VectorVerb* v);

// Simulação de geração tipo NanoGPT usando Nexus-Attention
static void nanogpt_generate(const char* prompt, VirtualContextWindow* win) {
    printf("\\n\\033[1;35m[NanoGPT 1B]\\033[0m Gerando resposta baseada no Foco de Atenção...\\n");

    if (win->focus_region) {
        char* memory_token = resolve_memory_content(win->focus_region);

        printf("Contexto Ativo (via MMAP): \\033[32m%s\\033[0m\\n",
               memory_token ? memory_token : "(null)");
        printf("Confiança da Atenção: %.4f\\n", win->attention_score);

        printf(">> \\033[1;37m");
        if (win->attention_score > 0.9f) {
            printf("Baseado nos meus registros absolutos de '%s', confirmo a operação.",
                   memory_token ? memory_token : "(desconhecido)");
        } else if (win->attention_score > 0.7f) {
            printf("Acesso parcial aos dados de '%s'. Requer validação.",
                   memory_token ? memory_token : "(desconhecido)");
        } else if (memory_token) {
            printf("Minha janela de 1 bilhão de vetores não contém referência clara, "
                   "mas '%s' parece relacionado.", memory_token);
        } else {
            printf("Não encontrei memória relevante para este prompt.");
        }
        printf("\\033[0m\\n");

        if (memory_token) {
            FILE* f = fopen(memory_token, "r");
            if (f) {
                printf("\\033[90m[Lendo bytes do contexto '%s'...]\\033[0m\\n", memory_token);
                char buf[128];
                int  lines = 0;
                while (fgets(buf, sizeof(buf), f) && lines < 3) {
                    printf("   %s", buf);
                    lines++;
                }
                fclose(f);
            }
        }
    } else {
        printf(">> [Vazio] A vastidão de 1Bi vetores está silenciosa para este prompt.\\n");
    }
}

int main(void) {
    char input_buf[1024];

    if (nexus_init("gaia.nexus", 1000000) != 0) {
        fprintf(stderr, "[ERR] Falha ao inicializar gaia.nexus\\n");
        return 1;
    }

    VirtualContextWindow v_ctx;
    v_ctx.total_capacity  = 0;
    v_ctx.focus_region    = NULL;
    v_ctx.attention_score = 0.0f;

    omega_float qbuf[3] = {0.0f, 0.0f, 0.0f};
    VectorVerb query_vec = {
        .data         = qbuf,
        .dimension    = 3,
        .kinetic_func = NULL
    };

    printf("==================================================\\n");
    printf(" GAIA-OMEGA [NanoGPT HOST] | Window: 1,000,000,000\\n");
    printf("==================================================\\n");

    for (;;) {
        printf("\\n\\033[1;36mΩ PROMPT > \\033[0m");
        if (!fgets(input_buf, sizeof(input_buf), stdin)) {
            break;
        }
        input_buf[strcspn(input_buf, "\\n")] = '\\0';

        if (strcmp(input_buf, "exit") == 0 ||
            strcmp(input_buf, "quit") == 0) {
            break;
        }
        if (input_buf[0] == '\\0') {
            continue;
        }

        uint64_t h = semantic_hash_djb2(input_buf);
        hash_to_vector(h, &query_vec);
        shift_attention(&query_vec, &v_ctx);
        nanogpt_generate(input_buf, &v_ctx);
    }

    nexus_close();
    return 0;
}
EOF

# =============================================================================
# 4. COMPILAÇÃO
# =============================================================================

echo "[BUILD] Compilando Boot..."
gcc -O3 boot_omega.c core/kinetic_math.c neural/synapse_registry.c -o gaia_boot -lm

echo "[BUILD] Compilando Mutant..."
gcc -O3 interactive_mutant.c core/kinetic_math.c core/lexical_projector.c core/semantic_hash.c neural/synapse_registry.c -o gaia_mutant -lm

echo "[BUILD] Compilando Ingest Tools..."
gcc -O3 tools_ingest.c core/mmap_nexus.c core/semantic_hash.c -o gaia_ingest -lm
gcc -O3 tools_absorb.c core/mmap_nexus.c core/semantic_hash.c core/vision_cortex.c -o gaia_absorb -lm

echo "[BUILD] Compilando Visual Shell..."
gcc -O3 visual_shell.c core/mmap_nexus.c core/semantic_hash.c core/ansi_engine.c -o gaia_visual -lm

echo "[BUILD] Compilando Daemon & Client..."
gcc -O3 core/gaia_daemon.c core/mmap_nexus.c -o gaia_d -lm
gcc -O3 visual_client.c core/semantic_hash.c -o gaia_client -lm

echo "[BUILD] Compilando NanoGPT Host (Infinite Attention)..."
gcc -O3 gaia_nanogpt.c core/infinite_attention.c core/mmap_nexus.c core/semantic_hash.c core/kinetic_math.c core/vision_cortex.c -o gaia_nanogpt -lm

chmod +x gaia_*

echo "=========================================================="
echo " GAIA-Ω INSTALADO COM SUCESSO EM: $BASE_DIR"
echo "=========================================================="
echo "COMANDOS DISPONÍVEIS:"
echo "1.  ./gaia_ingest gaia.nexus < dummy_data.txt     (Alimentar Nexus)"
echo "2.  ./gaia_visual                                (Radar Visual)"
echo "3.  ./gaia_d &                                   (Rodar Servidor IPC)"
echo "4.  ./gaia_client                                (Cliente IPC)"
echo "5.  python3 gaia_chat.py                         (Chat Python ↔ Nexus)"
echo "6.  ./gaia_nanogpt                               (Host NanoGPT 1B Context)"
echo "7.  ./gaia_boot                                  (Boot simbólico do Cortex)"
echo "=========================================================="
