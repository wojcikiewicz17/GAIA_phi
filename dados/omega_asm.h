#ifndef OMEGA_ASM_H
#define OMEGA_ASM_H
#include "omega_protocol.h"
typedef void (*kinetic_handler_t)(VectorVerb*);
struct SynapseNode {
    omega_float* ref_vector;
    kinetic_handler_t handler;
    struct SynapseNode* next;
    const char* debug_name;
};
void collapse_and_execute(VectorVerb* intent, struct SynapseNode* memory_bank);
struct SynapseNode* build_genesis_cortex();
struct SynapseNode* load_cortex_from_disk();
void learn_new_pattern(VectorVerb* intent, const char* action_name);
#endif
