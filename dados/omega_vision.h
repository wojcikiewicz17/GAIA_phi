#ifndef OMEGA_VISION_H
#define OMEGA_VISION_H
#include <stdint.h>
#include "omega_protocol.h"
uint64_t visual_hash_raw(const uint8_t* data, size_t len);
void visual_to_vector(uint64_t hash, VectorVerb* v_out);
#endif
