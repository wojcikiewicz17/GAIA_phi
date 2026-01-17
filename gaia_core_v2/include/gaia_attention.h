#ifndef GAIA_ATTENTION_H
#define GAIA_ATTENTION_H

#include "gaia_vector.h"
#include "gaia_error.h"

typedef struct {
    const char *name;
    GaiaStatus (*score)(const GaiaVector *query, const GaiaVector *vec, float *out_score);
} GaiaAttentionStrategy;

GaiaStatus gaia_attention_register(const GaiaAttentionStrategy *strategy);
GaiaStatus gaia_attention_apply(const char *name, const GaiaVector *query,
                                const GaiaVector *vec, float *out_score);

#endif
