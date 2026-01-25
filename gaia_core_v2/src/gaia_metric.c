#include "gaia_metric.h"

float gaia_metric_dot(const GaiaVector *a, const GaiaVector *b) {
    return gaia_vector_dot(a, b);
}

float gaia_metric_l1(const GaiaVector *a, const GaiaVector *b) {
    uint32_t i = 0;
    float sum = 0.0f;
    if (!a || !b || !a->data || !b->data || a->dim != b->dim) {
        return 0.0f;
    }
    const float *ap = a->data;
    const float *bp = b->data;
    uint32_t dim = a->dim;
    for (i = 0; i < dim; i++) {
        float diff = ap[i] - bp[i];
        sum += (diff < 0.0f) ? -diff : diff;
    }
    return sum;
}

float gaia_metric_cosine(const GaiaVector *a, const GaiaVector *b) {
    uint32_t i = 0;
    float dot = 0.0f;
    float aa = 0.0f;
    float bb = 0.0f;
    float prod = 0.0f;
    float inv = 0.0f;
    const float *ap = 0;
    const float *bp = 0;
    if (!a || !b || !a->data || !b->data || a->dim != b->dim) {
        return 0.0f;
    }
    ap = a->data;
    bp = b->data;
    uint32_t dim = a->dim;
    for (i = 0; i < dim; i++) {
        float av = ap[i];
        float bv = bp[i];
        dot += av * bv;
        aa += av * av;
        bb += bv * bv;
    }
    if (aa <= 0.0f || bb <= 0.0f) {
        return 0.0f;
    }
    prod = aa * bb;
    inv = 1.0f;
    for (i = 0; i < 4; i++) {
        inv = inv * (1.5f - 0.5f * prod * inv * inv);
    }
    return dot * inv;
}
