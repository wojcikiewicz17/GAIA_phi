#ifndef LLAMA_GUARD_BITSTACK_WITNESS_Q4_H
#define LLAMA_GUARD_BITSTACK_WITNESS_Q4_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    BITSTACK_WITNESS_XOR = 0,
    BITSTACK_WITNESS_CRC32C = 1
} BitstackWitnessMode;

typedef struct {
    const uint8_t *plane_hi;
    const uint8_t *plane_lo;
    size_t bytes_per_plane;
    uint32_t witness;
    BitstackWitnessMode mode;
} BitstackQ4Block;

void bitstack_q4_pack_planar(const uint8_t *packed, size_t packed_bytes,
                             uint8_t *plane_hi, uint8_t *plane_lo);

uint32_t bitstack_q4_compute_witness(const BitstackQ4Block *block);

int bitstack_q4_verify_block(const BitstackQ4Block *block);

void bitstack_q4_apply_fallback(uint8_t *plane_hi, uint8_t *plane_lo,
                                size_t bytes_per_plane);

void bitstack_q4_warmup(void *base, size_t bytes);

#ifdef __cplusplus
}
#endif

#endif
