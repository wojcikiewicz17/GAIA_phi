#include "gaia_zipraf.h"

GaiaStatus gaia_zipraf_open_layer(GaiaZipRafLayer *layer,
                                  GaiaZipRafLayerSpec spec,
                                  uint8_t *buffer,
                                  uint32_t capacity) {
    if (!layer || !buffer || capacity == 0) {
        return GAIA_ERR_NULL;
    }
    layer->spec = spec;
    layer->capacity = capacity;
    layer->count = 0;
    layer->buffer = buffer;
    return GAIA_OK;
}

GaiaStatus gaia_zipraf_append(GaiaZipRafLayer *layer, const void *record, uint32_t len) {
    uint32_t i = 0;
    const uint8_t *src = (const uint8_t *)record;
    if (!layer || !record || len == 0) {
        return GAIA_ERR_NULL;
    }
    if (layer->count + len > layer->capacity) {
        return GAIA_ERR_RANGE;
    }
    for (i = 0; i < len; i++) {
        layer->buffer[layer->count + i] = src[i];
    }
    layer->count += len;
    return GAIA_OK;
}

GaiaStatus gaia_zipraf_seal(GaiaZipRafLayer *layer) {
    if (!layer) {
        return GAIA_ERR_NULL;
    }
    return GAIA_OK;
}
