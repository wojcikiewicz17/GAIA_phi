#ifndef FIBER_HASH_H
#define FIBER_HASH_H

/*
 *  FIBER-H – 256-bit hash kernel (v1.1)
 *
 *  Características:
 *  - Small footprint: 256-bit state (4 x 64-bit words)
 *  - Zero malloc / zero stdint em todo o núcleo
 *  - Endianness-agnostic via helpers locais LE
 *  - C API estável e mínima para FFI
 *
 *  NOTE:
 *  Este header é intencionalmente auto-contido:
 *  não depende de <stdint.h> ou <stddef.h>, usando
 *  typedefs básicos para máxima portabilidade.
 */

/* ---------------------------------------------------------
 * Basic fixed-width aliases (assumes LP64 / 64-bit long)
 * --------------------------------------------------------- */

typedef unsigned char  fiber_u8;
typedef unsigned long  fiber_u64;   /* assumindo 64 bits (LP64) */
typedef fiber_u64      fiber_size_t;
typedef long           fiber_s32;

#ifdef __cplusplus
extern "C" {
#endif

/* ---------------------------------------------------------
 * Core state context
 * --------------------------------------------------------- */

typedef struct {
    fiber_u64   a;           /* Σ: word 0 of internal state   */
    fiber_u64   b;           /* Ω: word 1 of internal state   */
    fiber_u64   c;           /* Δ: word 2 of internal state   */
    fiber_u64   d;           /* Φ: word 3 of internal state   */
    fiber_u64   total_len;   /* total message length in bytes (mod 2^64) */
    fiber_u8    buffer[64];  /* partial block buffer (one 512-bit block) */
    fiber_size_t buffer_len; /* number of bytes currently stored in buffer */
} FIBER_H_CTX;

/* ---------------------------------------------------------
 * Core one-shot and streaming API
 * --------------------------------------------------------- */

/*
 * fiber_h_init
 *  Initialize a FIBER-H context with fixed IV.
 *  The caller must provide a valid pointer to ctx.
 */
void fiber_h_init(FIBER_H_CTX *ctx);

/*
 * fiber_h_update
 *  Absorb 'len' bytes from 'data' into the running hash.
 *  Streaming-safe: can be called multiple times.
 */
void fiber_h_update(FIBER_H_CTX *ctx,
                    const fiber_u8 *data,
                    fiber_size_t len);

/*
 * fiber_h_final
 *  Finalize the hash:
 *    - apply padding
 *    - write 32-byte digest to 'out'
 *  After this call, ctx contents are no longer stable.
 */
void fiber_h_final(FIBER_H_CTX *ctx, fiber_u8 out[32]);

/*
 * fiber_h
 *  One-shot convenience wrapper:
 *    - init
 *    - update
 *    - final
 */
void fiber_h(const fiber_u8 *data,
             fiber_size_t len,
             fiber_u8 out[32]);

/* ---------------------------------------------------------
 * Optional lanes / micro-ops layer (LANES6, etc.)
 * --------------------------------------------------------- */
/* Esta camada é opcional; pode ficar vazia se não usar lanes6. */
#include "fiber_ops.h"

/* ---------------------------------------------------------
 * Tree / parallel mode API (Merkle-style)
 * --------------------------------------------------------- */
/*
 * fiber_h_tree
 *  Compute a 256-bit FIBER-H digest in tree mode.
 *
 *  Parameters:
 *    - data      : pointer to input message
 *    - len       : length in bytes
 *    - out[32]   : output buffer (256-bit digest)
 *    - leaf_size : per-leaf chunk in bytes (e.g. 1024, 4096).
 *
 *  Behavior:
 *    - If len == 0      : hashes empty string (same as fiber_h("",0)).
 *    - If leaf_size== 0 : a sane default (1024) is used.
 *    - Leaves are hashed with fiber_h; internal nodes hash the
 *      concatenation of two child digests (64 bytes).
 *
 *  NOTE:
 *  Tree mode é implementado em fiber_hash_tree.c e pode
 *  usar malloc internamente, mas o kernel (fiber_hash.c)
 *  permanece malloc-free.
 */
void fiber_h_tree(const fiber_u8 *data,
                  fiber_size_t len,
                  fiber_u8 out[32],
                  fiber_size_t leaf_size);

#ifdef __cplusplus
} /* extern "C" */
#endif

#endif /* FIBER_HASH_H */
