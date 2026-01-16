#ifndef OMEGA_NEXUS_H
#define OMEGA_NEXUS_H
#include "omega_protocol.h"
#include <stdio.h>

typedef struct {
    char signature[8];
    uint64_t capacity;
    uint64_t count;
    uint64_t version;
} NexusHeader;

typedef struct {
    uint64_t id;
    omega_float vector[3];
    char action_tag[32];
    float confidence;
    uint32_t flags;
} NexusCell;

int nexus_init(const char* filepath, uint64_t capacity);
int nexus_append(VectorVerb* v, const char* action);
void nexus_scan_match(VectorVerb* input, void (*callback)(NexusCell*));
void nexus_close();
#endif
