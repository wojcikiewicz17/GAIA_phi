#ifndef GAIA_QUANT_H
#define GAIA_QUANT_H

#include <stdint.h>
#include "gaia_vector.h"
#include "gaia_error.h"

GaiaStatus gaia_quant_minmax(const GaiaVector *v, float *out_min, float *out_max);
GaiaStatus gaia_quantize_u8(const GaiaVector *v, uint8_t *out, float min, float max);
GaiaStatus gaia_dequantize_u8(const uint8_t *in, uint32_t dim, float *out, float min, float max);

#endif
