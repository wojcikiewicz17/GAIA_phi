#include "fiber_hash_lanes6.h"

/* 
 * Small helper: fill memory with a constant byte (no stdlib).
 */
static void fiber_memset(fiber_u8 *dst, fiber_u8 v, fiber_size_t n) {
    fiber_size_t i;
    for (i = 0; i < n; ++i) {
        dst[i] = v;
    }
}

/* 
 * Small helper: XOR in-place: dst[i] ^= src[i]
 */
static void fiber_memxor(fiber_u8 *dst, const fiber_u8 *src, fiber_size_t n) {
    fiber_size_t i;
    for (i = 0; i < n; ++i) {
        dst[i] ^= src[i];
    }
}

/*
 * Derive per-lane IV using base FIBER-H:
 *   cv[i] = FIBER-H("FIBER-H-LANE6-IV-" || i_byte)
 * where i_byte is lane index in [0..5].
 */
static void fiber_h_lanes6_derive_iv(FIBER_H_LANES6_CTX *ctx) {
    fiber_u8 seed[32];
    fiber_size_t base_len = 0u;
    fiber_size_t i;

    /* Base seed: ASCII "FIBER-H-LANE6-IV-" (18 bytes) + zero padding */
    {
        const char *s = "FIBER-H-LANE6-IV-";
        /* manual copy to avoid strlen/stdlib */
        base_len = 0u;
        while (s[base_len] != '\0' && base_len < 31u) {
            seed[base_len] = (fiber_u8)s[base_len];
            base_len++;
        }
        /* zero pad remainder */
        while (base_len < 32u) {
            seed[base_len] = 0u;
            base_len++;
        }
    }

    for (i = 0u; i < 6u; ++i) {
        fiber_u8 tmp[33];
        fiber_size_t j;

        /* copy base seed into tmp[0..31] */
        for (j = 0u; j < 32u; ++j) {
            tmp[j] = seed[j];
        }
        /* lane index in last byte */
        tmp[32] = (fiber_u8)i;

        /* cv[i] = FIBER-H(tmp, 33) */
        fiber_h(tmp, (fiber_size_t)33u, ctx->cv[i]);
    }
}

/*
 * Process one "superblock" of 384 bytes:
 *   - Split into 6 chunks of 64 bytes.
 *   - For each lane i:
 *       cv[i] = FIBER-H( cv[i] || chunk_i );
 *
 * No subtraction is used; only concatenation + base hash.
 */
static void fiber_h_lanes6_process_superblock(FIBER_H_LANES6_CTX *ctx,
                                              const fiber_u8 block[384]) {
    fiber_size_t lane;
    fiber_size_t j;

    for (lane = 0u; lane < 6u; ++lane) {
        fiber_u8 in[32u + 64u]; /* cv (32) + chunk (64) */
        fiber_size_t chunk_offset = lane * 64u;

        /* copy current cv into in[0..31] */
        for (j = 0u; j < 32u; ++j) {
            in[j] = ctx->cv[lane][j];
        }
        /* copy chunk into in[32..95] */
        for (j = 0u; j < 64u; ++j) {
            in[32u + j] = block[chunk_offset + j];
        }

        /* new cv[i] = FIBER-H(in, 96) */
        fiber_h(in, (fiber_size_t)96u, ctx->cv[lane]);
    }

    /* update total length (mod 2^64 via natural overflow) */
    ctx->total_len += (fiber_u64)384u;
}

/*
 * Collapse 6 lanes into a single 256-bit value:
 *   tmp = cv[0] XOR cv[1] XOR ... XOR cv[5]
 *   out = FIBER-H(tmp, 32)
 */
static void fiber_h_lanes6_collapse(const FIBER_H_LANES6_CTX *ctx,
                                    fiber_u8 out[32]) {
    fiber_u8 tmp[32];
    fiber_size_t i, lane;

    /* start from lane 0 */
    for (i = 0u; i < 32u; ++i) {
        tmp[i] = ctx->cv[0][i];
    }

    /* XOR remaining lanes */
    for (lane = 1u; lane < 6u; ++lane) {
        fiber_memxor(tmp, ctx->cv[lane], (fiber_size_t)32u);
    }

    /* final root = FIBER-H(tmp, 32) */
    fiber_h(tmp, (fiber_size_t)32u, out);
}

/* --- Public API --- */

void fiber_h_lanes6_init(FIBER_H_LANES6_CTX *ctx) {
    fiber_size_t i, lane;

    /* Clear chaining values */
    for (lane = 0u; lane < 6u; ++lane) {
        for (i = 0u; i < 32u; ++i) {
            ctx->cv[lane][i] = 0u;
        }
    }
    ctx->total_len = 0u;
    ctx->buf_len   = 0u;
    fiber_memset(ctx->buffer, 0u, (fiber_size_t)384u);

    /* Derive per-lane IVs using base FIBER-H */
    fiber_h_lanes6_derive_iv(ctx);
}

void fiber_h_lanes6_update(FIBER_H_LANES6_CTX *ctx,
                           const fiber_u8 *data,
                           fiber_size_t len) {
    fiber_size_t offset = 0u;

    if (len == 0u) {
        return;
    }

    /* First, fill buffer to 384 if there is partial data */
    if (ctx->buf_len > 0u) {
        fiber_size_t space = (fiber_size_t)384u - ctx->buf_len;
        fiber_size_t take = (len < space) ? len : space;

        fiber_size_t i;
        for (i = 0u; i < take; ++i) {
            ctx->buffer[ctx->buf_len + i] = data[i];
        }

        ctx->buf_len += take;
        offset       += take;

        if (ctx->buf_len == 384u) {
            fiber_h_lanes6_process_superblock(ctx, ctx->buffer);
            ctx->buf_len = 0u;
        }
    }

    /* Process as many whole 384-byte superblocks as possible directly */
    while ((len - offset) >= 384u) {
        fiber_h_lanes6_process_superblock(ctx, &data[offset]);
        offset += 384u;
    }

    /* Store any remaining tail into buffer */
    if (offset < len) {
        fiber_size_t rem = len - offset;
        fiber_size_t i;
        for (i = 0u; i < rem; ++i) {
            ctx->buffer[i] = data[offset + i];
        }
        ctx->buf_len = rem;
    }
}

void fiber_h_lanes6_final(FIBER_H_LANES6_CTX *ctx,
                          fiber_u8 out[32]) {
    /* If there is remaining data in buffer, pad with zeros and process */
    if (ctx->buf_len > 0u) {
        fiber_size_t i;
        /* zero pad from buf_len to 384 */
        for (i = ctx->buf_len; i < 384u; ++i) {
            ctx->buffer[i] = 0u;
        }
        fiber_h_lanes6_process_superblock(ctx, ctx->buffer);
        ctx->buf_len = 0u;
    }

    /* Collapse 6 lanes into final 256-bit root */
    fiber_h_lanes6_collapse(ctx, out);
}

void fiber_h_lanes6(const fiber_u8 *data,
                    fiber_size_t len,
                    fiber_u8 out[32]) {
    FIBER_H_LANES6_CTX ctx;
    fiber_h_lanes6_init(&ctx);
    fiber_h_lanes6_update(&ctx, data, len);
    fiber_h_lanes6_final(&ctx, out);
}
