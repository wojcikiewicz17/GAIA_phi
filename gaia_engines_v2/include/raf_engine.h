#ifndef RAF_ENGINE_H
#define RAF_ENGINE_H

#include <stdint.h>
#include "gaia_error.h"

typedef struct {
    const char *name;
    GaiaStatus (*run)(const void *input, void *output);
    GaiaStatus (*metrics)(void *out_metrics);
} RafEngine;

GaiaStatus raf_engine_register(const RafEngine *engine);
GaiaStatus raf_engine_execute(const char *name, const void *input, void *output);
GaiaStatus raf_engine_metrics(const char *name, void *out_metrics);
void raf_engine_reset(void);

#endif
