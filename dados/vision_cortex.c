#include "../headers/omega_vision.h"
uint64_t visual_hash_raw(const uint8_t* data, size_t len) {
    uint64_t h = 0xcbf29ce484222325;
    size_t step = (len > 4096) ? len / 1024 : 1;
    for (size_t i = 0; i < len; i += step) { h ^= data[i]; h *= 0x100000001b3; }
    return h;
}
void visual_to_vector(uint64_t hash, VectorVerb* v_out) {
    v_out->data[0] = (omega_float)(hash & 0xFFFF) / 65535.0f;
    v_out->data[1] = (omega_float)((hash >> 16) & 0xFFFF) / 65535.0f;
    v_out->data[2] = 0.6f + ((omega_float)((hash >> 32) & 0xFFFF) / 163840.0f);
}
