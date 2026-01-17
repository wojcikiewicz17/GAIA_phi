/* fiber_ecc.c – esqueleto conceitual */

#include "fiber_ecc.h"
#include "fiber_hash.h"  /* se quiser usar tipos auxiliares */

static uint8_t H1[10][16];     /* 10x16  bits => guardado como bytes */
static uint8_t H2_idx[10][32]; /* por ex.: cada linha usa 32 índices de bytes */
static uint8_t M[33][33];      /* 33x33 bits */

/* 1) inicializar as matrizes a partir da semente RAFAELIA */
static void fiber_ecc_init_once(void) {
    static int init_done = 0;
    if (init_done) return;
    init_done = 1;

    /* (aqui entra o PRNG baseado em RAFCODE-Φ + bitraf64)
       - gerar H1, H2_idx, M
       - forçar propriedades (não linha-zero, full rank, etc.)
    */
}

/* calcula XOR de todos bits/bytes de um sub-bloco de 64 bytes => 1 bit */
static uint8_t parity_block_64(const uint8_t *p) {
    uint8_t x = 0;
    for (size_t i = 0; i < 64; ++i) {
        x ^= p[i];                 /* XOR de bytes */
    }
    /* reduzir a 1 bit: XOR de todos os bits do byte final */
    x ^= x >> 4;
    x ^= x >> 2;
    x ^= x >> 1;
    return (uint8_t)(x & 1u);
}

void fiber_ecc_leaf_raf(const uint8_t *leaf,
                        size_t leaf_len,
                        fiber_ecc_raf_t *out)
{
    fiber_ecc_init_once();

    /* 1) dividir em 16 sub-blocos de 64 bytes (assumindo leaf_len = 1024) */
    uint8_t b[16] = {0};
    for (size_t k = 0; k < 16 && (k*64 + 64) <= leaf_len; ++k) {
        b[k] = parity_block_64(leaf + k*64); /* 1 bit por sub-bloco */
    }

    /* 2) aplicar H1: lane_parity (10 bits) */
    uint16_t p1 = 0;
    for (size_t r = 0; r < 10; ++r) {
        uint8_t acc = 0;
        for (size_t c = 0; c < 16; ++c) {
            if (H1[r][c]) acc ^= b[c];
        }
        if (acc & 1u) {
            p1 |= (uint16_t)(1u << r);
        }
    }

    /* 3) aplicar H2: block_parity (10 bits) */
    uint16_t p2 = 0;
    for (size_t r = 0; r < 10; ++r) {
        uint8_t acc = 0;
        /* H2_idx[r][j] = índice de byte em [0..leaf_len-1] */
        for (size_t j = 0; j < 32; ++j) {
            uint8_t idx = H2_idx[r][j];
            if (idx < leaf_len) {
                acc ^= leaf[idx];
            }
        }
        /* reduzir a 1 bit */
        acc ^= acc >> 4; acc ^= acc >> 2; acc ^= acc >> 1;
        if (acc & 1u) {
            p2 |= (uint16_t)(1u << r);
        }
    }

    /* 4) montar vetor v (33 bits): 16 (b) + 10 (p1) + 7 (p2 comprimido) */
    uint64_t v = 0;
    /* bits 0..15 -> b[k] */
    for (size_t i = 0; i < 16; ++i) {
        if (b[i] & 1u) v |= (uint64_t)1u << i;
    }
    /* bits 16..25 -> p1 (10 bits) */
    v |= ((uint64_t)p1 & 0x3FFu) << 16;
    /* bits 26..32 -> 7 bits do p2 (por ex. p2 ^ (p2>>3) & 0x7F) */
    uint16_t p2_mix = (uint16_t)((p2 ^ (p2 >> 3)) & 0x7Fu);
    v |= ((uint64_t)p2_mix) << 26;

    /* 5) aplicar M: u = M * v (mod 2) → 33 bits em raf_sig */
    uint64_t u = 0;
    for (size_t r = 0; r < 33; ++r) {
        uint8_t acc = 0;
        for (size_t c = 0; c < 33; ++c) {
            if (M[r][c]) {
                acc ^= (uint8_t)((v >> c) & 1u);
            }
        }
        if (acc & 1u) {
            u |= (uint64_t)1u << r;
        }
    }

    out->lane_parity = p1;
    out->block_parity = p2;
    out->raf_sig = u; /* 33 bits úteis aqui dentro */
}
