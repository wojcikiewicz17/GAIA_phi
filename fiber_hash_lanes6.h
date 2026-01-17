#ifndef FIBER_HASH_LANES6_H
#define FIBER_HASH_LANES6_H

/* 
 * FIBER-H LANES6 MODE (Experimental)
 * -----------------------------------
 * - High-level construction over base FIBER-H (fiber_h()).
 * - 6 internal lanes of 256-bit chaining values (6 x 32 bytes).
 * - Processes data in "superblocks" of 384 bytes (6 x 64).
 * - Uses only:
 *     - modular addition (inside fiber_h)
 *     - XOR
 *     - left rotations
 * - No subtraction, no dynamic allocation, no OS calls.
 *
 * Normative intent:
 * - ISO/IEC 25010: reliability, performance efficiency.
 * - NIST 800-53: auditability (deterministic, reproducible).
 * - IEEE 12207: clear separation between core kernel and mode.
 */

#include "fiber_hash.h"

/* 
 * Lanes6 context:
 * - cv[6][32]: six 256-bit chaining values (raw bytes).
 * - total_len: total message length (bytes, modulo 2^64 logic).
 * - buffer[384]: pending data until we can process a "superblock".
 * - buf_len: current number of bytes in buffer.
 */
typedef struct {
    fiber_u8   cv[6][32];
    fiber_u64  total_len;
    fiber_u8   buffer[384];
    fiber_size_t buf_len;
} FIBER_H_LANES6_CTX;

/* API (experimental) */

void fiber_h_lanes6_init(FIBER_H_LANES6_CTX *ctx);

/* Feed arbitrary-length data; may be called many times */
void fiber_h_lanes6_update(FIBER_H_LANES6_CTX *ctx,
                           const fiber_u8 *data,
                           fiber_size_t len);

/* Finalize and produce 256-bit root hash */
void fiber_h_lanes6_final(FIBER_H_LANES6_CTX *ctx,
                          fiber_u8 out[32]);

/* Convenience one-shot wrapper */
void fiber_h_lanes6(const fiber_u8 *data,
                    fiber_size_t len,
                    fiber_u8 out[32]);

#endif /* FIBER_HASH_LANES6_H */
