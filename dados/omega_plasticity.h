#ifndef OMEGA_PLASTICITY_H
#define OMEGA_PLASTICITY_H
#include "omega_protocol.h"
#include "omega_asm.h"
void learn_new_pattern(VectorVerb* intent, const char* action_name);
struct SynapseNode* load_cortex_from_disk();
#endif
