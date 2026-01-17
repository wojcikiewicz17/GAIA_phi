// ============================================================================
// RAFAELIA FIBER-H HASH TREE LIB (v999)
//  - Implementa APENAS fiber_h_tree (256-bit), sem main()
//  - Para uso em: fiber_stress_lab, test suites, etc.
// ============================================================================

#include "fiber_hash.h"   // fiber_u8, fiber_size_t, fiber_h
#include <stdio.h>
#include <stdlib.h>       // malloc, free
#include <string.h>       // memcpy

// Constantes de digest / nó interno (Merkle 256-bit)
#define FIBER_DIGEST_SIZE 32u
#define NODE_COMBINED_SIZE (FIBER_DIGEST_SIZE * 2u) // 64 bytes

// --------------------------------------------------------------------------
// fiber_h_tree
//  - data/len      : mensagem original
//  - out[32]       : digest 256-bit (raiz)
//  - leaf_size     : tamanho da folha em bytes (ex.: 1024)
// --------------------------------------------------------------------------
void fiber_h_tree(const fiber_u8 *data,
                  fiber_size_t len,
                  fiber_u8 out[FIBER_DIGEST_SIZE],
                  fiber_size_t leaf_size)
{
    // Casos degenerados: usa direto o kernel base
    if (!data || len == 0 || leaf_size == 0 || leaf_size >= len) {
        fiber_h(data, len, out);
        return;
    }

    // 1) Número de folhas
    fiber_size_t n_leaves = (len + leaf_size - 1u) / leaf_size;

    // 2) Vetor de hashes de folhas (n_leaves * 32 bytes)
    fiber_u8 *hashes = (fiber_u8 *)malloc((size_t)n_leaves * FIBER_DIGEST_SIZE);
    if (!hashes) {
        // Sem memória -> fallback linear (proteção)
        fiber_h(data, len, out);
        return;
    }

    // 3) Hash de cada folha
    for (fiber_size_t i = 0; i < n_leaves; ++i) {
        fiber_size_t offset    = i * leaf_size;
        fiber_size_t chunk_len = (offset + leaf_size > len)
                               ? (len - offset)
                               : leaf_size;

        fiber_h(data + offset, chunk_len, hashes + (size_t)i * FIBER_DIGEST_SIZE);
    }

    // 4) Sobe a árvore até sobrar 1 nó (raiz)
    fiber_size_t cur_nodes = n_leaves;
    fiber_u8 buf[NODE_COMBINED_SIZE]; // 64 bytes

    while (cur_nodes > 1u) {
        fiber_size_t next_nodes = (cur_nodes + 1u) / 2u;

        for (fiber_size_t i = 0; i < next_nodes; ++i) {
            const fiber_u8 *left  = hashes + (size_t)(2u * i) * FIBER_DIGEST_SIZE;
            const fiber_u8 *right = NULL;

            // Copia o filho esquerdo
            memcpy(buf, left, FIBER_DIGEST_SIZE);

            if ((2u * i + 1u) < cur_nodes) {
                // Filho direito existe
                right = hashes + (size_t)(2u * i + 1u) * FIBER_DIGEST_SIZE;
                memcpy(buf + FIBER_DIGEST_SIZE, right, FIBER_DIGEST_SIZE);
            } else {
                // Nó ímpar: espelhamento + salt para difusão extra
                fiber_u8 salt_byte = (fiber_u8)(cur_nodes ^ (len & 0xFFu));
                for (size_t j = 0; j < FIBER_DIGEST_SIZE; ++j) {
                    buf[FIBER_DIGEST_SIZE + j] = left[j] ^ salt_byte;
                }
            }

            // Pai = H(left || right_mod)
            fiber_h(buf, (fiber_size_t)NODE_COMBINED_SIZE,
                    hashes + (size_t)i * FIBER_DIGEST_SIZE);
        }

        cur_nodes = next_nodes;
    }

    // 5) Raiz = primeiro hash
    memcpy(out, hashes, FIBER_DIGEST_SIZE);
    free(hashes);
}
