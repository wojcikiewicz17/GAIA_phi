#ifndef GAIA_VECTOR_H
#define GAIA_VECTOR_H

#include <stdint.h>
#include "gaia_error.h"

typedef struct {
    float *data;
    uint32_t dim;
    uint32_t cap;
    uint32_t flags;
} GaiaVector;

GaiaStatus gaia_vector_init(GaiaVector *v, float *buffer, uint32_t dim);
GaiaStatus gaia_vector_resize(GaiaVector *v, uint32_t dim);
GaiaStatus gaia_vector_zero(GaiaVector *v);
float gaia_vector_dot(const GaiaVector *a, const GaiaVector *b);
GaiaStatus gaia_vector_normalize(GaiaVector *v);

#endif
