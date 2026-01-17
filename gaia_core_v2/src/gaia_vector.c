#include "gaia_vector.h"

GaiaStatus gaia_vector_init(GaiaVector *v, float *buffer, uint32_t dim) {
    if (!v || !buffer || dim == 0) {
        return GAIA_ERR_NULL;
    }
    v->data = buffer;
    v->dim = dim;
    v->cap = dim;
    v->flags = 0;
    return gaia_vector_zero(v);
}

GaiaStatus gaia_vector_resize(GaiaVector *v, uint32_t dim) {
    if (!v || !v->data) {
        return GAIA_ERR_NULL;
    }
    if (dim == 0 || dim > v->cap) {
        return GAIA_ERR_RANGE;
    }
    v->dim = dim;
    return GAIA_OK;
}

GaiaStatus gaia_vector_zero(GaiaVector *v) {
    uint32_t i = 0;
    if (!v || !v->data) {
        return GAIA_ERR_NULL;
    }
    for (i = 0; i < v->dim; i++) {
        v->data[i] = 0.0f;
    }
    return GAIA_OK;
}

float gaia_vector_dot(const GaiaVector *a, const GaiaVector *b) {
    uint32_t i = 0;
    float sum = 0.0f;
    if (!a || !b || !a->data || !b->data || a->dim != b->dim) {
        return 0.0f;
    }
    for (i = 0; i < a->dim; i++) {
        sum += a->data[i] * b->data[i];
    }
    return sum;
}

GaiaStatus gaia_vector_normalize(GaiaVector *v) {
    uint32_t i = 0;
    float sum = 0.0f;
    float inv = 0.0f;
    if (!v || !v->data) {
        return GAIA_ERR_NULL;
    }
    for (i = 0; i < v->dim; i++) {
        sum += v->data[i] * v->data[i];
    }
    if (sum <= 0.0f) {
        return GAIA_ERR_RANGE;
    }
    inv = 1.0f;
    for (i = 0; i < 4; i++) {
        inv = inv * (1.5f - 0.5f * sum * inv * inv);
    }
    for (i = 0; i < v->dim; i++) {
        v->data[i] *= inv;
    }
    return GAIA_OK;
}
