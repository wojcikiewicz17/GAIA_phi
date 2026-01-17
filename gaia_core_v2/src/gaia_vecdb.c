#include "gaia_vecdb.h"
#include "gaia_metric.h"

GaiaStatus gaia_vecdb_init(GaiaVecDB *db,
                           float *storage,
                           uint64_t *ids,
                           uint32_t capacity,
                           uint32_t dim,
                           uint32_t quant_bits) {
    if (!db || !storage || !ids || capacity == 0 || dim == 0) {
        return GAIA_ERR_NULL;
    }
    db->header.dim = dim;
    db->header.quant_bits = quant_bits;
    db->header.capacity = capacity;
    db->header.count = 0;
    db->storage = storage;
    db->ids = ids;
    return GAIA_OK;
}

GaiaStatus gaia_vecdb_insert(GaiaVecDB *db, const GaiaVector *v, uint64_t id) {
    uint32_t idx = 0;
    uint32_t i = 0;
    float *dst = 0;
    if (!db || !v || !v->data) {
        return GAIA_ERR_NULL;
    }
    if (v->dim != db->header.dim) {
        return GAIA_ERR_BAD_DIM;
    }
    if (db->header.count >= db->header.capacity) {
        return GAIA_ERR_RANGE;
    }
    idx = db->header.count;
    dst = db->storage + (idx * db->header.dim);
    for (i = 0; i < db->header.dim; i++) {
        dst[i] = v->data[i];
    }
    db->ids[idx] = id;
    db->header.count++;
    return GAIA_OK;
}

GaiaStatus gaia_vecdb_query(GaiaVecDB *db, const GaiaVector *query,
                            uint64_t *out_ids, float *out_scores, uint32_t limit) {
    uint32_t i = 0;
    uint32_t j = 0;
    if (!db || !query || !out_ids || !out_scores) {
        return GAIA_ERR_NULL;
    }
    if (query->dim != db->header.dim || limit == 0) {
        return GAIA_ERR_BAD_DIM;
    }
    for (i = 0; i < limit; i++) {
        out_ids[i] = 0;
        out_scores[i] = -1.0f;
    }
    for (i = 0; i < db->header.count; i++) {
        GaiaVector vec;
        vec.data = db->storage + (i * db->header.dim);
        vec.dim = db->header.dim;
        vec.cap = db->header.dim;
        vec.flags = 0;
        {
            float score = gaia_metric_cosine(query, &vec);
            for (j = 0; j < limit; j++) {
                if (score > out_scores[j]) {
                    uint32_t k = 0;
                    for (k = limit - 1; k > j; k--) {
                        out_scores[k] = out_scores[k - 1];
                        out_ids[k] = out_ids[k - 1];
                    }
                    out_scores[j] = score;
                    out_ids[j] = db->ids[i];
                    break;
                }
            }
        }
    }
    return GAIA_OK;
}

void gaia_vecdb_close(GaiaVecDB *db) {
    if (!db) {
        return;
    }
    db->storage = 0;
    db->ids = 0;
    db->header.capacity = 0;
    db->header.count = 0;
}
