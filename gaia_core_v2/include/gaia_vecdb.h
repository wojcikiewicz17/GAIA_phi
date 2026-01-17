#ifndef GAIA_VECDB_H
#define GAIA_VECDB_H

#include <stdint.h>
#include "gaia_vector.h"
#include "gaia_error.h"

typedef struct {
    uint32_t dim;
    uint32_t quant_bits;
    uint32_t capacity;
    uint32_t count;
} GaiaVecDBHeader;

typedef struct {
    GaiaVecDBHeader header;
    float *storage;
    uint64_t *ids;
} GaiaVecDB;

GaiaStatus gaia_vecdb_init(GaiaVecDB *db,
                           float *storage,
                           uint64_t *ids,
                           uint32_t capacity,
                           uint32_t dim,
                           uint32_t quant_bits);
GaiaStatus gaia_vecdb_insert(GaiaVecDB *db, const GaiaVector *v, uint64_t id);
GaiaStatus gaia_vecdb_query(GaiaVecDB *db, const GaiaVector *query,
                            uint64_t *out_ids, float *out_scores, uint32_t limit);
void gaia_vecdb_close(GaiaVecDB *db);

#endif
