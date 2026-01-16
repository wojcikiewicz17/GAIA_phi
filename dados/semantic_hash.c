#include "../headers/omega_hash.h"
uint64_t semantic_hash_djb2(const char* str) {
    uint64_t hash = 5381;
    int c;
    while ((c = *str++)) hash = ((hash << 5) + hash) + c;
    return hash;
}
uint64_t omega_hash(const char* str) { return semantic_hash_djb2(str); }
void hash_to_vector(uint64_t hash, VectorVerb* v_out) {
    v_out->data[0] = (omega_float)(hash & 0xFFFF) / 65535.0f;
    v_out->data[1] = (omega_float)((hash >> 16) & 0xFFFF) / 65535.0f;
    v_out->data[2] = (omega_float)((hash >> 32) & 0xFFFF) / 65535.0f;
}
