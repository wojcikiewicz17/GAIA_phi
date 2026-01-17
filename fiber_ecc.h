/* fiber_ecc.h */

#ifndef FIBER_ECC_H
#define FIBER_ECC_H

#include <stddef.h>
#include <stdint.h>

typedef struct {
    uint16_t lane_parity;   /* p^(1)  - 10 bits (H1)  */
    uint16_t block_parity;  /* p^(2)  - 10 bits (H2)  */
    uint64_t raf_sig;       /* u (33 bits úteis)      */
} fiber_ecc_raf_t;

/* calcula ECC RAFAELIA para 1 folha (leaf) */
void fiber_ecc_leaf_raf(const uint8_t *leaf,
                        size_t leaf_len,
                        fiber_ecc_raf_t *out);

#endif
