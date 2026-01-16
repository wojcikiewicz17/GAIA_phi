#include "../headers/omega_asm.h"
#include <stdio.h>
#include <stdlib.h>
void action_net_connect(VectorVerb* v) { printf("[ACT] NET_CONNECT\n"); }
void action_io_write(VectorVerb* v) { printf("[ACT] IO_WRITE\n"); }
void action_kernel_panic(VectorVerb* v) { printf("[ACT] KERNEL_PANIC\n"); exit(0); }
struct SynapseNode* build_genesis_cortex() {
    static struct SynapseNode n1;
    static omega_float v1[] = {0.1, 0.9, 0.1};
    n1.ref_vector = v1; n1.handler = action_net_connect; n1.debug_name = "NET"; n1.next = NULL;
    return &n1;
}
// Stub para evitar erro de linkagem se plasticity não for usado
struct SynapseNode* load_cortex_from_disk() { return NULL; }
void learn_new_pattern(VectorVerb* intent, const char* action_name) {}
void collapse_and_execute(VectorVerb* intent, struct SynapseNode* bank) {
    if(bank && bank->handler) bank->handler(intent);
}
