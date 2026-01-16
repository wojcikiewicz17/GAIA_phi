#include "headers/omega_protocol.h"
#include "headers/omega_asm.h"
#include <stdio.h>
static void run_simulation(const char* label, omega_float* data, uint64_t dim, struct SynapseNode* cortex) {
    printf("\n--- [EVENTO] %s ---\n", label);
    VectorVerb intent = { .data = data, .dimension = dim, .kinetic_func = NULL };
    collapse_and_execute(&intent, cortex);
}
int main(void) {
    printf("GAIA-OMEGA BOOT\n");
    struct SynapseNode* cortex = build_genesis_cortex();
    omega_float d1[] = {0.95f, 0.05f, 0.0f}; run_simulation("Save", d1, 3, cortex);
    omega_float d2[] = {0.10f, 0.85f, 0.05f}; run_simulation("Net", d2, 3, cortex);
    return 0;
}
