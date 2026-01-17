#ifndef GAIA_LOG_H
#define GAIA_LOG_H

#include <stddef.h>
#include <stdint.h>
#include "gaia_error.h"

typedef struct {
    uint64_t prev_hash;
    uint64_t hash;
    uint32_t len;
} GaiaLogEntry;

typedef struct {
    GaiaLogEntry *entries;
    uint8_t *payload;
    uint32_t entry_cap;
    uint32_t payload_cap;
    uint32_t entry_count;
    uint32_t payload_count;
} GaiaLogChain;

GaiaStatus gaia_log_init(GaiaLogChain *log,
                         GaiaLogEntry *entries,
                         uint8_t *payload,
                         uint32_t entry_cap,
                         uint32_t payload_cap);
GaiaStatus gaia_log_append(GaiaLogChain *log,
                           const void *data,
                           uint32_t len,
                           uint64_t *out_hash);
GaiaStatus gaia_log_verify(const GaiaLogChain *log, uint32_t index);
void gaia_log_close(GaiaLogChain *log);

#endif
