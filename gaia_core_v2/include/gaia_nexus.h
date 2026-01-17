#ifndef GAIA_NEXUS_H
#define GAIA_NEXUS_H

#include <stdint.h>
#include "gaia_vector.h"
#include "gaia_metric.h"
#include "gaia_error.h"

typedef struct {
    GaiaVector *vectors;
    uint64_t *ids;
    uint32_t capacity;
    uint32_t count;
} GaiaNexus;

GaiaStatus gaia_nexus_init(GaiaNexus *nx,
                           GaiaVector *vectors,
                           uint64_t *ids,
                           uint32_t capacity);
GaiaStatus gaia_nexus_insert(GaiaNexus *nx, const GaiaVector *v, uint64_t id);
GaiaStatus gaia_nexus_scan(GaiaNexus *nx, const GaiaVector *query,
                           uint64_t *out_ids, float *out_scores, uint32_t limit);
void gaia_nexus_close(GaiaNexus *nx);

#endif
