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
