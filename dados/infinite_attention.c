#include "../headers/omega_attention.h"
#include <string.h>

// Ponteiros globais definidos em core/mmap_nexus.c
extern NexusHeader* header_ptr;
extern NexusCell*   cells_ptr;

// Dot product simples em 3 dimensões (demo)
static inline float dot3(const omega_float* a, const omega_float* b) {
    return (float)(a[0] * b[0] +
                   a[1] * b[1] +
                   a[2] * b[2]);
}

// Atenção sobre disco (Zero-Copy Attention)
// Em vez de calcular matrizes gigantes em RAM, usamos a geometria do vetor
// para "saltar" até a região relevante do Nexus (MMAP).
void shift_attention(VectorVerb* query, VirtualContextWindow* win) {
    if (!header_ptr || !cells_ptr || !win || !query || !query->data) {
        return;
    }

    if (query->dimension < 3) {
        // Dimensão insuficiente para dot3 – em uma versão futura,
        // você pode generalizar para N dimensões.
        return;
    }

    NexusCell* best_cell = NULL;
    float      max_score = -1.0f;

    // Scan linear (demo). Para 1B real, plugue HNSW / DiskANN aqui.
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

// Recupera o dado simbólico associado à célula
char* resolve_memory_content(NexusCell* cell) {
    if (!cell) return NULL;

    // Exemplo: prefixo IMG indica conteúdo visual binário
    if (strncmp(cell->action_tag, "IMG:", 4) == 0) {
        return "[DADOS VISUAIS BINÁRIOS]";
    }

    // Em muitos casos, action_tag será:
    // - um identificador semântico
    // - ou um caminho de arquivo (ex.: "large_data.json")
    return cell->action_tag;
}
