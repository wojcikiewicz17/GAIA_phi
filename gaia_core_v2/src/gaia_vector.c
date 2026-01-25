#include "gaia_vector.h"
#include "gaia_projection.h"
#include <string.h>

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
    if (!v || !v->data) {
        return GAIA_ERR_NULL;
    }
    memset(v->data, 0, (size_t)v->dim * sizeof(float));
    return GAIA_OK;
}

float gaia_vector_dot(const GaiaVector *a, const GaiaVector *b) {
    uint32_t i = 0;
    float sum = 0.0f;
    if (!a || !b || !a->data || !b->data || a->dim != b->dim) {
        return 0.0f;
    }
    const float *ap = a->data;
    const float *bp = b->data;
    uint32_t dim = a->dim;
    for (i = 0; i < dim; i++) {
        sum += ap[i] * bp[i];
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
    float *data = v->data;
    uint32_t dim = v->dim;
    for (i = 0; i < dim; i++) {
        float value = data[i];
        sum += value * value;
    }
    if (sum <= 0.0f) {
        return GAIA_ERR_RANGE;
    }
    inv = 1.0f;
    for (i = 0; i < 4; i++) {
        inv = inv * (1.5f - 0.5f * sum * inv * inv);
    }
    for (i = 0; i < dim; i++) {
        data[i] *= inv;
    }
    return GAIA_OK;
}

GaiaStatus gaia_vector_project_hash(GaiaVector *v, uint64_t hash) {
    if (!v || !v->data) {
        return GAIA_ERR_NULL;
    }
    if (v->dim == 3) {
        return gaia_project_3d(hash, v->data);
    }
    return gaia_project_nd(hash, v->data, v->dim);
}
