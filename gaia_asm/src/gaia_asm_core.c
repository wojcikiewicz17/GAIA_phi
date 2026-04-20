#include "gaia_asm_core.h"

#if !defined(__x86_64__) && !defined(__aarch64__) && !defined(__arm__)
uint32_t gaia_asm_mix_u32(uint32_t a, uint32_t b, uint32_t c) {
    return gaia_asm_mix_u32_ref(a, b, c);
}
#endif

uint32_t gaia_asm_mix_u32_ref(uint32_t a, uint32_t b, uint32_t c) {
    uint32_t mixed = a ^ b;
    mixed = (mixed << 5U) | (mixed >> 27U);
    mixed += c;
    mixed ^= 0x9e3779b9U;
    return mixed;
}
