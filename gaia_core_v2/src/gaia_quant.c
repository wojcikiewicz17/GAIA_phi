#include "gaia_quant.h"

GaiaStatus gaia_quant_minmax(const GaiaVector *v, float *out_min, float *out_max) {
    uint32_t i = 0;
    float min_val = 0.0f;
    float max_val = 0.0f;
    const float *data = 0;
    uint32_t dim = 0;
    if (!v || !v->data || !out_min || !out_max) {
        return GAIA_ERR_NULL;
    }
    if (v->dim == 0) {
        return GAIA_ERR_RANGE;
    }
    data = v->data;
    dim = v->dim;
    min_val = data[0];
    max_val = data[0];
    for (i = 1; i < dim; i++) {
        float val = data[i];
        if (val < min_val) {
            min_val = val;
        }
        if (val > max_val) {
            max_val = val;
        }
    }
    *out_min = min_val;
    *out_max = max_val;
    return GAIA_OK;
}

GaiaStatus gaia_quantize_u8(const GaiaVector *v, uint8_t *out, float min, float max) {
    uint32_t i = 0;
    float scale = 0.0f;
    const float *data = 0;
    uint32_t dim = 0;
    if (!v || !v->data || !out) {
        return GAIA_ERR_NULL;
    }
    if (max <= min) {
        return GAIA_ERR_RANGE;
    }
    data = v->data;
    dim = v->dim;
    scale = 255.0f / (max - min);
    for (i = 0; i < dim; i++) {
        float val = (data[i] - min) * scale;
        if (val < 0.0f) {
            val = 0.0f;
        } else if (val > 255.0f) {
            val = 255.0f;
        }
        out[i] = (uint8_t)(val + 0.5f);
    }
    return GAIA_OK;
}

GaiaStatus gaia_dequantize_u8(const uint8_t *in, uint32_t dim, float *out, float min, float max) {
    uint32_t i = 0;
    float scale = 0.0f;
    const uint8_t *src = 0;
    if (!in || !out || dim == 0) {
        return GAIA_ERR_NULL;
    }
    if (max <= min) {
        return GAIA_ERR_RANGE;
    }
    src = in;
    scale = (max - min) / 255.0f;
    for (i = 0; i < dim; i++) {
        out[i] = min + ((float)src[i] * scale);
    }
    return GAIA_OK;
}
