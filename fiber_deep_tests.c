#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include "fiber_hash.h"

/*
 * FIBER-H deep tests:
 *
 * 1) Avalanche test (flip each input bit, measure Hamming distance of hash).
 * 2) Monte Carlo randomness test (bit balance over many random messages).
 *
 * These tests are IMPLEMENTATION CHECKS only.
 * They DO NOT perform password cracking or any hostile operation.
 */

/* ----------------- Small PRNG (xorshift32) ----------------- */

static uint32_t prng_state = 0x12345678u;

static uint32_t prng_next(void) {
    /* xorshift32: small, fast, deterministic, no libc dependency */
    uint32_t x = prng_state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    prng_state = x;
    return x;
}

static void prng_seed(uint32_t seed) {
    if (seed == 0) seed = 0x12345678u;
    prng_state = seed;
}

/* ----------------- Helpers ----------------- */

static void print_hex(const unsigned char *buf, size_t len) {
    for (size_t i = 0; i < len; ++i) {
        printf("%02x", (unsigned int)buf[i]);
    }
}

static unsigned int hamming_distance_256(const unsigned char h1[32],
                                         const unsigned char h2[32]) {
    unsigned int diff_bits = 0;
    for (size_t i = 0; i < 32; ++i) {
        unsigned char x = (unsigned char)(h1[i] ^ h2[i]);
        /* Count bits set in x (Brian Kernighan’s method) */
        while (x) {
            x &= (unsigned char)(x - 1);
            diff_bits++;
        }
    }
    return diff_bits;
}

/* ----------------- 1) Avalanche Test ----------------- */

static void run_avalanche_test(void) {
    const size_t MSG_LEN = 32; /* 256 bits of input */
    unsigned char base_msg[32];
    unsigned char base_hash[32];
    unsigned char mutated[32];
    unsigned char mutated_hash[32];

    const unsigned int TOTAL_BITS = (unsigned int)(MSG_LEN * 8);
    unsigned long long sum_dist = 0;
    unsigned int min_dist = 256;
    unsigned int max_dist = 0;

    printf("[*] AVALANCHE TEST\n");
    printf("[*] Base message length: %zu bytes (%u bits)\n",
           MSG_LEN, TOTAL_BITS);

    /* Choose a deterministic base message: 0x00, 0x01, 0x02, ... */
    for (size_t i = 0; i < MSG_LEN; ++i) {
        base_msg[i] = (unsigned char)i;
    }

    fiber_h(base_msg, MSG_LEN, base_hash);

    printf("    Base message: ");
    print_hex(base_msg, MSG_LEN);
    printf("\n");
    printf("    Base hash   : ");
    print_hex(base_hash, 32);
    printf("\n");

    /* For each bit of the input, flip and measure hash difference */
    for (unsigned int bit = 0; bit < TOTAL_BITS; ++bit) {
        memcpy(mutated, base_msg, MSG_LEN);

        /* bit index → byte + bit-in-byte */
        unsigned int byte_idx = bit / 8;
        unsigned int bit_idx  = bit % 8;
        unsigned char mask    = (unsigned char)(1u << bit_idx);

        mutated[byte_idx] ^= mask;

        fiber_h(mutated, MSG_LEN, mutated_hash);

        unsigned int dist = hamming_distance_256(base_hash, mutated_hash);
        sum_dist += (unsigned long long)dist;
        if (dist < min_dist) min_dist = dist;
        if (dist > max_dist) max_dist = dist;
    }

    double avg_dist = (double)sum_dist / (double)TOTAL_BITS;
    double avg_ratio = avg_dist / 256.0 * 100.0;

    printf("[*] Avalanche results over %u bit flips:\n", TOTAL_BITS);
    printf("    Min distance  : %u bits\n", min_dist);
    printf("    Max distance  : %u bits\n", max_dist);
    printf("    Avg distance  : %.2f bits (%.2f%% of 256)\n",
           avg_dist, avg_ratio);
    printf("[*] Ideal ≈ 128 bits (50%%) changed per flip.\n\n");
}

/* ----------------- 2) Monte Carlo Bit Randomness ----------------- */

static void run_monte_carlo_randomness(unsigned int samples) {
    const size_t MSG_LEN = 32;
    unsigned char msg[32];
    unsigned char hash[32];

    /* Count how many times each bit (0..255) is 1 */
    unsigned long long bit_ones[256];
    memset(bit_ones, 0, sizeof(bit_ones));

    printf("[*] MONTE CARLO RANDOMNESS TEST\n");
    printf("[*] Samples: %u messages of %zu bytes each\n",
           samples, MSG_LEN);

    /* Initialize message from PRNG */
    prng_seed(0xCAFEBABEu);

    for (unsigned int s = 0; s < samples; ++s) {
        /* Fill message with PRNG bytes */
        for (size_t i = 0; i < MSG_LEN; ++i) {
            msg[i] = (unsigned char)(prng_next() & 0xFFu);
        }

        fiber_h(msg, MSG_LEN, hash);

        /* Count bits */
        for (size_t byte = 0; byte < 32; ++byte) {
            unsigned char b = hash[byte];
            for (unsigned int bit = 0; bit < 8; ++bit) {
                unsigned int bit_index = (unsigned int)(byte * 8 + bit);
                if (b & (unsigned char)(1u << bit)) {
                    bit_ones[bit_index]++;
                }
            }
        }
    }

    printf("[*] Bit-level statistics (first 16 bits for preview):\n");
    for (unsigned int i = 0; i < 16; ++i) {
        double p = (double)bit_ones[i] / (double)samples * 100.0;
        printf("    bit[%3u]: ones=%llu  p=%.2f%%\n",
               i, bit_ones[i], p);
    }

    /* Summarize min/max over all 256 bits */
    double min_p = 100.0, max_p = 0.0;
    for (unsigned int i = 0; i < 256; ++i) {
        double p = (double)bit_ones[i] / (double)samples * 100.0;
        if (p < min_p) min_p = p;
        if (p > max_p) max_p = p;
    }
    printf("[*] Global bit balance over 256 bits:\n");
    printf("    min p(1) = %.2f%%\n", min_p);
    printf("    max p(1) = %.2f%%\n", max_p);
    printf("    Ideal is around 50%% for each bit.\n\n");
}

/* ----------------- Entry Point ----------------- */

static void print_usage(const char *prog) {
    printf("Usage:\n");
    printf("  %s avalanche          # run avalanche test\n", prog);
    printf("  %s montecarlo N       # run randomness test with N samples\n", prog);
    printf("\nExamples:\n");
    printf("  %s avalanche\n", prog);
    printf("  %s montecarlo 10000\n", prog);
}

int main(int argc, char **argv) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "avalanche") == 0) {
        run_avalanche_test();
        return 0;
    }

    if (strcmp(argv[1], "montecarlo") == 0) {
        if (argc < 3) {
            fprintf(stderr, "[ERROR] montecarlo requires N samples.\n");
            print_usage(argv[0]);
            return 1;
        }
        unsigned int samples = (unsigned int)strtoul(argv[2], NULL, 10);
        if (samples == 0) {
            fprintf(stderr, "[ERROR] invalid N (must be > 0).\n");
            return 1;
        }
        run_monte_carlo_randomness(samples);
        return 0;
    }

    fprintf(stderr, "[ERROR] unknown mode: %s\n", argv[1]);
    print_usage(argv[0]);
    return 1;
}
