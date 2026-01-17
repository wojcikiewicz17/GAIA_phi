#include "raf_engine.h"

#define RAF_ENGINE_MAX 8u

static RafEngine raf_registry[RAF_ENGINE_MAX];
static uint32_t raf_count = 0;

static int raf_name_equal(const char *a, const char *b) {
    if (!a || !b) {
        return 0;
    }
    while (*a && *b && *a == *b) {
        a++;
        b++;
    }
    return (*a == '\0' && *b == '\0');
}

GaiaStatus raf_engine_register(const RafEngine *engine) {
    if (!engine || !engine->name || !engine->run) {
        return GAIA_ERR_NULL;
    }
    if (raf_count >= RAF_ENGINE_MAX) {
        return GAIA_ERR_RANGE;
    }
    raf_registry[raf_count] = *engine;
    raf_count++;
    return GAIA_OK;
}

GaiaStatus raf_engine_execute(const char *name, const void *input, void *output) {
    uint32_t i = 0;
    if (!name) {
        return GAIA_ERR_NULL;
    }
    for (i = 0; i < raf_count; i++) {
        if (raf_name_equal(raf_registry[i].name, name)) {
            return raf_registry[i].run(input, output);
        }
    }
    return GAIA_ERR_RANGE;
}

GaiaStatus raf_engine_metrics(const char *name, void *out_metrics) {
    uint32_t i = 0;
    if (!name) {
        return GAIA_ERR_NULL;
    }
    for (i = 0; i < raf_count; i++) {
        if (raf_name_equal(raf_registry[i].name, name)) {
            if (!raf_registry[i].metrics) {
                return GAIA_ERR_UNSUPPORTED;
            }
            return raf_registry[i].metrics(out_metrics);
        }
    }
    return GAIA_ERR_RANGE;
}

void raf_engine_reset(void) {
    raf_count = 0;
}
