#ifndef GAIA_ASM_CORE_H
#define GAIA_ASM_CORE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

uint32_t gaia_asm_mix_u32(uint32_t a, uint32_t b, uint32_t c);
uint32_t gaia_asm_mix_u32_ref(uint32_t a, uint32_t b, uint32_t c);

#ifdef __cplusplus
}
#endif

#endif
