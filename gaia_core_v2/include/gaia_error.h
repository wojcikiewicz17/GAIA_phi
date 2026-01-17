#ifndef GAIA_ERROR_H
#define GAIA_ERROR_H

#include <stdint.h>

typedef enum {
    GAIA_OK = 0,
    GAIA_ERR_NULL = -1,
    GAIA_ERR_RANGE = -2,
    GAIA_ERR_NOMEM = -3,
    GAIA_ERR_BAD_DIM = -4,
    GAIA_ERR_UNSUPPORTED = -5,
    GAIA_ERR_IO = -6
} GaiaStatus;

#endif
