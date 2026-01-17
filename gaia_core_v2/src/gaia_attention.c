#include "gaia_attention.h"
#include "gaia_metric.h"

#define GAIA_ATTENTION_MAX 8u

static GaiaAttentionStrategy gaia_attention_registry[GAIA_ATTENTION_MAX];
static uint32_t gaia_attention_count = 0;

static GaiaStatus gaia_attention_linear(const GaiaVector *query,
                                        const GaiaVector *vec,
                                        float *out_score) {
    if (!query || !vec || !out_score) {
        return GAIA_ERR_NULL;
    }
    *out_score = gaia_metric_cosine(query, vec);
    return GAIA_OK;
}

GaiaStatus gaia_attention_register(const GaiaAttentionStrategy *strategy) {
    if (!strategy || !strategy->name || !strategy->score) {
        return GAIA_ERR_NULL;
    }
    if (gaia_attention_count >= GAIA_ATTENTION_MAX) {
        return GAIA_ERR_RANGE;
    }
    gaia_attention_registry[gaia_attention_count] = *strategy;
    gaia_attention_count++;
    return GAIA_OK;
}

GaiaStatus gaia_attention_apply(const char *name, const GaiaVector *query,
                                const GaiaVector *vec, float *out_score) {
    uint32_t i = 0;
    if (!name || !query || !vec || !out_score) {
        return GAIA_ERR_NULL;
    }
    for (i = 0; i < gaia_attention_count; i++) {
        const GaiaAttentionStrategy *entry = &gaia_attention_registry[i];
        const char *s = entry->name;
        const char *t = name;
        while (*s && *t && *s == *t) {
            s++;
            t++;
        }
        if (*s == '\0' && *t == '\0') {
            return entry->score(query, vec, out_score);
        }
    }
    return gaia_attention_linear(query, vec, out_score);
}

void gaia_attention_reset(void) {
    gaia_attention_count = 0;
}
