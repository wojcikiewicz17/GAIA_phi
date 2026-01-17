#ifndef GAIA_PROJECTION_H
#define GAIA_PROJECTION_H

#include <stdint.h>
#include "gaia_error.h"

GaiaStatus gaia_project_3d(uint64_t hash, float out[3]);
GaiaStatus gaia_project_nd(uint64_t hash, float *out, uint32_t dim);

#endif
