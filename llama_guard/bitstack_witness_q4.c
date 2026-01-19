#include "bitstack_witness_q4.h"

#include <string.h>

static uint32_t crc32c_table[256];
static int crc32c_ready = 0;

static void crc32c_init(void) {
    if (crc32c_ready) {
        return;
    }
    uint32_t poly = 0x1EDC6F41u;
    for (uint32_t i = 0; i < 256; ++i) {
        uint32_t crc = i;
        for (int j = 0; j < 8; ++j) {
            if (crc & 1u) {
                crc = (crc >> 1u) ^ poly;
            } else {
                crc >>= 1u;
            }
        }
        crc32c_table[i] = crc;
    }
    crc32c_ready = 1;
}

static uint32_t crc32c_compute(const uint8_t *data, size_t len) {
    crc32c_init();
    uint32_t crc = 0xFFFFFFFFu;
    for (size_t i = 0; i < len; ++i) {
        uint8_t idx = (uint8_t)((crc ^ data[i]) & 0xFFu);
        crc = (crc >> 8u) ^ crc32c_table[idx];
    }
    return ~crc;
}

void bitstack_q4_pack_planar(const uint8_t *packed, size_t packed_bytes,
                             uint8_t *plane_hi, uint8_t *plane_lo) {
    if (!packed || !plane_hi || !plane_lo) {
        return;
    }
    memset(plane_hi, 0, packed_bytes);
    memset(plane_lo, 0, packed_bytes);
    for (size_t i = 0; i < packed_bytes; ++i) {
        uint8_t byte = packed[i];
        plane_hi[i] = (byte >> 4) & 0x0Fu;
        plane_lo[i] = byte & 0x0Fu;
    }
}

static uint32_t xor_fold(const uint8_t *data, size_t len) {
    uint32_t acc = 0;
    for (size_t i = 0; i < len; ++i) {
        acc ^= (uint32_t)data[i];
        acc = (acc << 1u) | (acc >> 31u);
    }
    return acc;
}

uint32_t bitstack_q4_compute_witness(const BitstackQ4Block *block) {
    if (!block || !block->plane_hi || !block->plane_lo) {
        return 0;
    }
    if (block->mode == BITSTACK_WITNESS_CRC32C) {
        uint32_t hi_crc = crc32c_compute(block->plane_hi, block->bytes_per_plane);
        uint32_t lo_crc = crc32c_compute(block->plane_lo, block->bytes_per_plane);
        return hi_crc ^ lo_crc;
    }
    uint32_t hi_xor = xor_fold(block->plane_hi, block->bytes_per_plane);
    uint32_t lo_xor = xor_fold(block->plane_lo, block->bytes_per_plane);
    return hi_xor ^ lo_xor;
}

int bitstack_q4_verify_block(const BitstackQ4Block *block) {
    if (!block) {
        return 0;
    }
    uint32_t expected = bitstack_q4_compute_witness(block);
    return expected == block->witness;
}

void bitstack_q4_apply_fallback(uint8_t *plane_hi, uint8_t *plane_lo,
                                size_t bytes_per_plane) {
    if (!plane_hi || !plane_lo) {
        return;
    }
    memset(plane_hi, 0, bytes_per_plane);
    memset(plane_lo, 0, bytes_per_plane);
}

void bitstack_q4_warmup(void *base, size_t bytes) {
    if (!base || bytes == 0) {
        return;
    }
    volatile uint8_t *ptr = (volatile uint8_t *)base;
    size_t page = 4096;
    for (size_t i = 0; i < bytes; i += page) {
        ptr[i] = ptr[i];
    }
}
