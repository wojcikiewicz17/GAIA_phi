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
