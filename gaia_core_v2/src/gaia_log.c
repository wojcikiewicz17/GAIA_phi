#include "gaia_log.h"
#include "gaia_hash.h"

static uint64_t gaia_log_hash_block(uint64_t prev_hash, const uint8_t *data, uint32_t len) {
    uint64_t acc = prev_hash;
    uint64_t h = gaia_hash_bytes(GAIA_HASH_AETHER, data, len);
    acc ^= h + 0x9E3779B97F4A7C15ull + (acc << 6) + (acc >> 2);
    return acc;
}

GaiaStatus gaia_log_init(GaiaLogChain *log,
                         GaiaLogEntry *entries,
                         uint8_t *payload,
                         uint32_t entry_cap,
                         uint32_t payload_cap) {
    if (!log || !entries || !payload || entry_cap == 0 || payload_cap == 0) {
        return GAIA_ERR_NULL;
    }
    log->entries = entries;
    log->payload = payload;
    log->entry_cap = entry_cap;
    log->payload_cap = payload_cap;
    log->entry_count = 0;
    log->payload_count = 0;
    return GAIA_OK;
}

GaiaStatus gaia_log_append(GaiaLogChain *log,
                           const void *data,
                           uint32_t len,
                           uint64_t *out_hash) {
    uint32_t i = 0;
    uint8_t *dst = 0;
    uint64_t prev = 0;
    uint64_t hash = 0;
    if (!log || !data || len == 0) {
        return GAIA_ERR_NULL;
    }
    if (log->entry_count >= log->entry_cap || log->payload_count + len > log->payload_cap) {
        return GAIA_ERR_RANGE;
    }
    dst = log->payload + log->payload_count;
    for (i = 0; i < len; i++) {
        dst[i] = ((const uint8_t *)data)[i];
    }
    if (log->entry_count > 0) {
        prev = log->entries[log->entry_count - 1].hash;
    }
    hash = gaia_log_hash_block(prev, dst, len);
    log->entries[log->entry_count].prev_hash = prev;
    log->entries[log->entry_count].hash = hash;
    log->entries[log->entry_count].len = len;
    log->entry_count++;
    log->payload_count += len;
    if (out_hash) {
        *out_hash = hash;
    }
    return GAIA_OK;
}

GaiaStatus gaia_log_verify(const GaiaLogChain *log, uint32_t index) {
    uint32_t i = 0;
    uint32_t offset = 0;
    uint64_t prev = 0;
    if (!log || index >= log->entry_count) {
        return GAIA_ERR_RANGE;
    }
    for (i = 0; i < index; i++) {
        offset += log->entries[i].len;
    }
    prev = (index == 0) ? 0 : log->entries[index - 1].hash;
    {
        const GaiaLogEntry *entry = &log->entries[index];
        const uint8_t *data = log->payload + offset;
        uint64_t calc = gaia_log_hash_block(prev, data, entry->len);
        return (calc == entry->hash) ? GAIA_OK : GAIA_ERR_RANGE;
    }
}

void gaia_log_close(GaiaLogChain *log) {
    if (!log) {
        return;
    }
    log->entries = 0;
    log->payload = 0;
    log->entry_cap = 0;
    log->payload_cap = 0;
    log->entry_count = 0;
    log->payload_count = 0;
}
