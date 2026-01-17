#ifndef GAIA_HASH_H
#define GAIA_HASH_H

#include <stddef.h>
#include <stdint.h>
#include "gaia_error.h"

typedef enum {
    GAIA_HASH_DJB2 = 0,
    GAIA_HASH_FNV1A = 1,
    GAIA_HASH_AETHER = 2
} GaiaHashKind;

uint64_t gaia_hash_bytes(GaiaHashKind kind, const uint8_t *buf, size_t len);

#endif
