#include "gaia_projection.h"

static float gaia_hash_to_unit(uint32_t x) {
    return ((float)(x & 0xFFFFu) / 65535.0f) * 2.0f - 1.0f;
}

GaiaStatus gaia_project_3d(uint64_t hash, float out[3]) {
    if (!out) {
        return GAIA_ERR_NULL;
    }
    out[0] = gaia_hash_to_unit((uint32_t)(hash));
    out[1] = gaia_hash_to_unit((uint32_t)(hash >> 21));
    out[2] = gaia_hash_to_unit((uint32_t)(hash >> 42));
    return GAIA_OK;
}

GaiaStatus gaia_project_nd(uint64_t hash, float *out, uint32_t dim) {
    uint32_t i = 0;
    if (!out || dim == 0) {
        return GAIA_ERR_NULL;
    }
    for (i = 0; i < dim; i++) {
        uint32_t shift = (i * 11u) % 53u;
        out[i] = gaia_hash_to_unit((uint32_t)(hash >> shift));
    }
    return GAIA_OK;
}
