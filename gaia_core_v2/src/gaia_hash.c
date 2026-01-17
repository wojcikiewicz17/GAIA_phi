#include "gaia_hash.h"

static uint64_t gaia_hash_djb2(const uint8_t *buf, size_t len) {
    uint64_t hash = 5381u;
    size_t i = 0;
    for (i = 0; i < len; i++) {
        hash = ((hash << 5) + hash) + (uint64_t)buf[i];
    }
    return hash;
}

static uint64_t gaia_hash_fnv1a(const uint8_t *buf, size_t len) {
    uint64_t hash = 1469598103934665603ull;
    size_t i = 0;
    for (i = 0; i < len; i++) {
        hash ^= (uint64_t)buf[i];
        hash *= 1099511628211ull;
    }
    return hash;
}

static uint64_t gaia_hash_aether(const uint8_t *buf, size_t len) {
    uint64_t hash = 0xA3B195354A39B70Dull;
    size_t i = 0;
    for (i = 0; i < len; i++) {
        hash ^= (hash << 7) ^ (hash >> 3) ^ (uint64_t)(buf[i] * 131u);
        hash *= 0x9E3779B97F4A7C15ull;
    }
    return hash ^ (hash >> 32);
}

uint64_t gaia_hash_bytes(GaiaHashKind kind, const uint8_t *buf, size_t len) {
    if (!buf || len == 0) {
        return 0;
    }
    switch (kind) {
        case GAIA_HASH_DJB2:
            return gaia_hash_djb2(buf, len);
        case GAIA_HASH_FNV1A:
            return gaia_hash_fnv1a(buf, len);
        case GAIA_HASH_AETHER:
            return gaia_hash_aether(buf, len);
        default:
            return 0;
    }
}
