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
    for (i = 0; i < a->dim; i++) {
        float diff = a->data[i] - b->data[i];
        sum += (diff < 0.0f) ? -diff : diff;
    }
    return sum;
}

float gaia_metric_cosine(const GaiaVector *a, const GaiaVector *b) {
    float dot = gaia_metric_dot(a, b);
    float aa = gaia_metric_dot(a, a);
    float bb = gaia_metric_dot(b, b);
    float prod = 0.0f;
    float inv = 0.0f;
    uint32_t i = 0;
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
