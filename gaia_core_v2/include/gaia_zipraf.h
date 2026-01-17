#ifndef GAIA_ZIPRAF_H
#define GAIA_ZIPRAF_H

#include <stdint.h>
#include "gaia_error.h"

typedef struct {
    uint32_t version;
    uint32_t layer_id;
} GaiaZipRafLayerSpec;

typedef struct {
    GaiaZipRafLayerSpec spec;
    uint32_t capacity;
    uint32_t count;
    uint8_t *buffer;
} GaiaZipRafLayer;

GaiaStatus gaia_zipraf_open_layer(GaiaZipRafLayer *layer,
                                  GaiaZipRafLayerSpec spec,
                                  uint8_t *buffer,
                                  uint32_t capacity);
GaiaStatus gaia_zipraf_append(GaiaZipRafLayer *layer, const void *record, uint32_t len);
GaiaStatus gaia_zipraf_seal(GaiaZipRafLayer *layer);

#endif
