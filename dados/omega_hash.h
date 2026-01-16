#ifndef OMEGA_HASH_H
#define OMEGA_HASH_H
#include <stdint.h>
#include "omega_protocol.h"
uint64_t semantic_hash_djb2(const char* str);
uint64_t omega_hash(const char* str); // Alias
void hash_to_vector(uint64_t hash, VectorVerb* v_out);
#endif
