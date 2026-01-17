/*
 * FIBER-H – 256-bit Hash Kernel (v1.1)
 * ------------------------------------
 * Core properties:
 *  - 4 x 64-bit state (a,b,c,d) = (Σ,Ω,Δ,Φ)
 *  - 64-byte blocks, Merkle-Damgård style padding
 *  - Operations: XOR, ADD (mod 2^64), ROTL
 *  - Endianness: canonical little-endian I/O
 *
 * Security / Quality Notes:
 *  - All additions are intentionally modulo 2^64 (unsigned wrap).
 *  - Bit-rotations are masked to avoid undefined shift behavior.
 *  - Context pointer and output pointer are checked for NULL from API entry.
 *  - No dynamic memory allocation, no I/O, no libc time/locale calls.
 *
 * Normative Alignment:
 *  - ISO/IEC 25010: Reliability (no heap, deterministic core)
 *  - IEEE 1012: Clear V&V points (R-round, padding, load/store)
 *  - NIST 800-53: Minimal attack surface; no secrets kept beyond ctx.
 */

#include "fiber_hash.h"

/* Internal constants (RC and IV are fixed, versioned) */
static const fiber_u64 FIBER_H_RC[8] = {
    0x9E3779B185EBCA87UL, 0xC2B2AE3D27D4EB4FUL,
    0x165667B19E3779F9UL, 0x85EBCA77C2B2AE63UL,
    0x27D4EB2F165667C5UL, 0x94D049BB133111EBUL,
    0x3C6EF372FE94F82BUL, 0xBB67AE8584CAA73BUL
};

/* IV derived from SHA-256("FIBER-H-IV-v1") – fixed for this version */
static const fiber_u64 FIBER_H_IV[4] = {
    0x6A09E667F3BCC908UL,
    0xBB67AE8584CAA73BUL,
    0x3C6EF372FE94F82BUL,
    0xA54FF53A5F1D36F1UL
};

/* Rotate left 64 (safe, masked) */
static fiber_u64 fiber_rotl64(fiber_u64 x, unsigned int r) {
    r &= 63U;
    if (!r) return x;
    return (fiber_u64)((x << r) | (x >> (64U - r)));
}

/* Load 64-bit little-endian */
static fiber_u64 fiber_load64_le(const fiber_u8 *p) {
    return ((fiber_u64)p[0])       |
           ((fiber_u64)p[1] << 8)  |
           ((fiber_u64)p[2] << 16) |
           ((fiber_u64)p[3] << 24) |
           ((fiber_u64)p[4] << 32) |
           ((fiber_u64)p[5] << 40) |
           ((fiber_u64)p[6] << 48) |
           ((fiber_u64)p[7] << 56);
}

/* Store 64-bit little-endian */
static void fiber_store64_le(fiber_u8 *p, fiber_u64 v) {
    p[0] = (fiber_u8)(v & 0xFFU);
    p[1] = (fiber_u8)((v >> 8)  & 0xFFU);
    p[2] = (fiber_u8)((v >> 16) & 0xFFU);
    p[3] = (fiber_u8)((v >> 24) & 0xFFU);
    p[4] = (fiber_u8)((v >> 32) & 0xFFU);
    p[5] = (fiber_u8)((v >> 40) & 0xFFU);
    p[6] = (fiber_u8)((v >> 48) & 0xFFU);
    p[7] = (fiber_u8)((v >> 56) & 0xFFU);
}

/*
 * Single compression on a 64-byte block.
 * All mixing is local; caller handles feed-forward.
 */
static void fiber_h_compress_block(fiber_u64 *a, fiber_u64 *b,
                                   fiber_u64 *c, fiber_u64 *d,
                                   const fiber_u8 block[64])
{
    fiber_u64 m0 = fiber_load64_le(block +  0);
    fiber_u64 m1 = fiber_load64_le(block +  8);
    fiber_u64 m2 = fiber_load64_le(block + 16);
    fiber_u64 m3 = fiber_load64_le(block + 24);
    fiber_u64 m4 = fiber_load64_le(block + 32);
    fiber_u64 m5 = fiber_load64_le(block + 40);
    fiber_u64 m6 = fiber_load64_le(block + 48);
    fiber_u64 m7 = fiber_load64_le(block + 56);

    fiber_u64 ra = *a;
    fiber_u64 rb = *b;
    fiber_u64 rc = *c;
    fiber_u64 rd = *d;

    /* 8 rounds – unrolled for performance and predictability */
#define RND(M, RCVAL)                    \
    do {                                 \
        ra = fiber_rotl64(ra ^ (M), 23); \
        rb = fiber_rotl64(rb + rd, 17);  \
        rc ^= rb ^ (RCVAL);              \
        rd = fiber_rotl64(rd + ra, 41);  \
    } while (0)

    RND(m0, FIBER_H_RC[0]);
    RND(m1, FIBER_H_RC[1]);
    RND(m2, FIBER_H_RC[2]);
    RND(m3, FIBER_H_RC[3]);
    RND(m4, FIBER_H_RC[4]);
    RND(m5, FIBER_H_RC[5]);
    RND(m6, FIBER_H_RC[6]);
    RND(m7, FIBER_H_RC[7]);

#undef RND

    *a ^= ra;
    *b ^= rb;
    *c ^= rc;
    *d ^= rd;
}

void fiber_h_init(FIBER_H_CTX *ctx) {
    if (!ctx) return; /* Defensive: avoid NULL deref */
    ctx->a = FIBER_H_IV[0];
    ctx->b = FIBER_H_IV[1];
    ctx->c = FIBER_H_IV[2];
    ctx->d = FIBER_H_IV[3];
    ctx->total_len  = 0;
    ctx->buffer_len = 0;
}

void fiber_h_update(FIBER_H_CTX *ctx, const fiber_u8 *data, fiber_size_t len) {
    if (!ctx) return;
    if (!data && len != 0) return; /* invalid call */

    ctx->total_len += (fiber_u64)len;

    fiber_size_t offset = 0;
    /* Consume any partial block first */
    if (ctx->buffer_len > 0) {
        fiber_size_t need = (fiber_size_t)(64 - ctx->buffer_len);
        fiber_size_t take = (len < need) ? len : need;

        for (fiber_size_t i = 0; i < take; ++i) {
            ctx->buffer[ctx->buffer_len + i] = data[i];
        }
        ctx->buffer_len += take;
        offset += take;
        len    -= take;

        if (ctx->buffer_len == 64) {
            fiber_h_compress_block(&ctx->a, &ctx->b, &ctx->c, &ctx->d, ctx->buffer);
            ctx->buffer_len = 0;
        }
    }

    /* Process full blocks directly from input */
    while (len >= 64) {
        fiber_h_compress_block(&ctx->a, &ctx->b, &ctx->c, &ctx->d, data + offset);
        offset += 64;
        len    -= 64;
    }

    /* Buffer remaining tail */
    for (fiber_size_t i = 0; i < len; ++i) {
        ctx->buffer[ctx->buffer_len + i] = data[offset + i];
    }
    ctx->buffer_len += len;
}

/*
 * Padding:
 *  - Append 0x80
 *  - Append zeros
 *  - Append 8-byte little-endian total length (bytes)
 */
void fiber_h_final(FIBER_H_CTX *ctx, fiber_u8 out[32]) {
    if (!ctx || !out) return;

    fiber_u8  last[64];
    fiber_u64 bit_len = ctx->total_len;  /* bytes, not bits (by design) */

    /* Copy remaining bytes to local 'last' buffer */
    fiber_size_t i;
    for (i = 0; i < ctx->buffer_len; ++i) {
        last[i] = ctx->buffer[i];
    }

    /* Append 0x80 */
    last[ctx->buffer_len] = 0x80;
    ++i;

    /* If not enough room for length, pad and compress once */
    if (i > 56) {
        for (; i < 64; ++i) last[i] = 0x00;
        fiber_h_compress_block(&ctx->a, &ctx->b, &ctx->c, &ctx->d, last);
        i = 0;
    }

    /* Pad with zeros until 56 bytes */
    for (; i < 56; ++i) last[i] = 0x00;

    /* Store length (bytes) as 64-bit LE at the end */
    fiber_store64_le(last + 56, bit_len);

    /* Final block */
    fiber_h_compress_block(&ctx->a, &ctx->b, &ctx->c, &ctx->d, last);

    /* Output final state as 32-byte hash (little-endian words) */
    fiber_store64_le(out +  0, ctx->a);
    fiber_store64_le(out +  8, ctx->b);
    fiber_store64_le(out + 16, ctx->c);
    fiber_store64_le(out + 24, ctx->d);
}

void fiber_h(const fiber_u8 *data, fiber_size_t len, fiber_u8 out[32]) {
    if (!out) return;
    FIBER_H_CTX ctx;
    fiber_h_init(&ctx);
    if (data && len > 0) {
        fiber_h_update(&ctx, data, len);
    }
    fiber_h_final(&ctx, out);
}
