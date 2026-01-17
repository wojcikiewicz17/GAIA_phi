#include "gaia_nexus.h"

GaiaStatus gaia_nexus_init(GaiaNexus *nx,
                           GaiaVector *vectors,
                           uint64_t *ids,
                           uint32_t capacity) {
    if (!nx || !vectors || !ids || capacity == 0) {
        return GAIA_ERR_NULL;
    }
    nx->vectors = vectors;
    nx->ids = ids;
    nx->capacity = capacity;
    nx->count = 0;
    return GAIA_OK;
}

GaiaStatus gaia_nexus_insert(GaiaNexus *nx, const GaiaVector *v, uint64_t id) {
    uint32_t idx = 0;
    if (!nx || !v || !v->data) {
        return GAIA_ERR_NULL;
    }
    if (nx->count >= nx->capacity) {
        return GAIA_ERR_RANGE;
    }
    idx = nx->count;
    nx->vectors[idx] = *v;
    nx->ids[idx] = id;
    nx->count++;
    return GAIA_OK;
}

GaiaStatus gaia_nexus_scan(GaiaNexus *nx, const GaiaVector *query,
                           uint64_t *out_ids, float *out_scores, uint32_t limit) {
    uint32_t i = 0;
    uint32_t j = 0;
    if (!nx || !query || !out_ids || !out_scores) {
        return GAIA_ERR_NULL;
    }
    if (limit == 0) {
        return GAIA_ERR_RANGE;
    }
    for (i = 0; i < limit; i++) {
        out_ids[i] = 0;
        out_scores[i] = -1.0f;
    }
    for (i = 0; i < nx->count; i++) {
        float score = gaia_metric_cosine(query, &nx->vectors[i]);
        for (j = 0; j < limit; j++) {
            if (score > out_scores[j]) {
                uint32_t k = 0;
                for (k = limit - 1; k > j; k--) {
                    out_scores[k] = out_scores[k - 1];
                    out_ids[k] = out_ids[k - 1];
                }
                out_scores[j] = score;
                out_ids[j] = nx->ids[i];
                break;
            }
        }
    }
    return GAIA_OK;
}

void gaia_nexus_close(GaiaNexus *nx) {
    if (!nx) {
        return;
    }
    nx->vectors = 0;
    nx->ids = 0;
    nx->capacity = 0;
    nx->count = 0;
}
