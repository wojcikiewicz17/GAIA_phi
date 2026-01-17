#ifndef GAIA_METRIC_H
#define GAIA_METRIC_H

#include "gaia_vector.h"

float gaia_metric_dot(const GaiaVector *a, const GaiaVector *b);
float gaia_metric_l1(const GaiaVector *a, const GaiaVector *b);
float gaia_metric_cosine(const GaiaVector *a, const GaiaVector *b);

#endif
