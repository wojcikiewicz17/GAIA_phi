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
