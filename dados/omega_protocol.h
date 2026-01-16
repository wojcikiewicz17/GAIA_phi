#ifndef OMEGA_PROTOCOL_H
#define OMEGA_PROTOCOL_H
#include <stdint.h>
typedef float omega_float;
typedef struct {
    omega_float* data;
    uint64_t dimension;
    void (*kinetic_func)(void*);
} VectorVerb;
#endif
