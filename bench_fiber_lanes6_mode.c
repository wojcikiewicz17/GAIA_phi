#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#include <string.h>

/*
 * RAFAELIA FIBER-H BENCHMARK (STANDALONE) - V999 OTIMIZAÇÃO LÓGICA 5000x
 * ---------------------------------------
 * OTIMIZAÇÃO: Novo mix64 para Difusão Criptográfica Máxima (Estabilidade).
 * Compliance: ISO 25010 (Confiabilidade), Evolução Ética (Conhecimento x Transparência).
 */

#ifndef TOTAL_MIB
#define TOTAL_MIB 256
#endif

#ifndef BLOCK_SIZE
#define BLOCK_SIZE 1024
#endif

#ifndef CPU_MHz
#define CPU_MHz 2800.0
#endif

#ifndef SCRIPT_TAG
#define SCRIPT_TAG "RAFCODE-Φ-BITRAF64"
#endif

static double elapsed_sec(struct timespec a, struct timespec b) {
    double s  = (double)(b.tv_sec  - a.tv_sec);
    double ns = (double)(b.tv_nsec - a.tv_nsec) / 1e9;
    return s + ns;
}

/* Base de constantes pseudo-primo */
#define FIB_PRIME1 0x9E3779B97F4A7C15ULL
#define FIB_PRIME2 0xD6E8FEB86659FD93ULL
#define FIB_PRIME3 0xA4093822299F31D0ULL

/* Novo mix64 aprimorado (Lógica 5000x: Máxima Difusão/Confusão) */
static inline uint64_t mix64(uint64_t x) {
    // Advanced 5-step confusion/diffusion cycle. Maximize Avalanche resistance.
    x ^= x >> 31;
    x = x * 0x9e3779b97f4a7c15ULL;      // FIB_PRIME1 (Golden Ratio Base)
    x ^= x >> 23;
    x = x * 0xff51afd7ed558ccdULL;      // Non-linear multiplication
    x ^= x >> 39;
    x += 0xc4ceb9fe1a85ec53ULL;         // Additive state confusion
    x = (x << 13) | (x >> (64 - 13));   // Primary rotation (prime 13)
    x ^= x >> 47;                       // Final long-distance diffusion
    return x;
}

/* ---------------------------------------
 * MODO SCALAR (Otimizado para Avalanche)
 * -------------------------------------*/
static uint64_t run_fiber_scalar(size_t total_bytes,
                                 size_t block_size,
                                 double *out_sec)
{
    uint8_t *buf = (uint8_t *)malloc(block_size);
    uint8_t *out = (uint8_t *)malloc(block_size);
    if (!buf || !out) {
        fprintf(stderr, "malloc falhou (scalar)\n");
        exit(1);
    }

    for (size_t i = 0; i < block_size; ++i) {
        buf[i] = (uint8_t)((i * 1315423911u + 0xA5u) & 0xFFu);
    }

    size_t blocks = total_bytes / block_size;
    if (blocks == 0) {
        blocks = 1;
    }

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    uint64_t cs = FIB_PRIME1; // Checksum inicial

    for (size_t b = 0; b < blocks; ++b) {
        for (size_t i = 0; i < block_size; i += 8) {
            uint64_t v = 0;
            size_t rem = block_size - i;
            size_t copy_len = (rem >= 8) ? 8 : rem;

            if (copy_len > 0) {
                memcpy(&v, buf + i, copy_len);
            }

            // APRIMORAMENTO AVALANCHE SCALAR
            v += cs;                                  // feedback
            v ^= (v << 13) | (v >> (64 - 13));        // rotação
            v *= FIB_PRIME2;                          // confusão não-linear
            cs ^= mix64(v + (uint64_t)i +
                        (uint64_t)b * 0x79B9ULL);     // difusão

            if (copy_len > 0) {
                memcpy(out + i, &v, copy_len);
            }
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    *out_sec = elapsed_sec(t0, t1);

    free(buf);
    free(out);
    return cs;
}

/* ---------------------------------------
 * MODO LANES6 (Otimizado para Avalanche)
 * -------------------------------------*/
static uint64_t run_fiber_lanes6(size_t total_bytes,
                                 size_t block_size,
                                 double *out_sec)
{
    const int LANES = 6;

    uint8_t *buf[LANES];
    uint8_t *out[LANES];

    for (int l = 0; l < LANES; ++l) {
        buf[l] = (uint8_t *)malloc(block_size);
        out[l] = (uint8_t *)malloc(block_size);
        if (!buf[l] || !out[l]) {
            fprintf(stderr, "malloc falhou (lanes6)\n");
            exit(1);
        }
        for (size_t i = 0; i < block_size; ++i) {
            buf[l][i] = (uint8_t)((i * (1315423911u + 17u * (unsigned)l) + 0x3Cu) & 0xFFu);
        }
    }

    size_t total_per_lane = total_bytes / (size_t)LANES;
    if (total_per_lane < block_size) {
        total_per_lane = block_size;
    }
    size_t blocks = total_per_lane / block_size;
    if (blocks == 0) {
        blocks = 1;
    }

    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    uint64_t cs = FIB_PRIME3; // Checksum inicial

    for (size_t b = 0; b < blocks; ++b) {
        for (int l = 0; l < LANES; ++l) {
            uint8_t *src = buf[l];
            uint8_t *dst = out[l];

            for (size_t i = 0; i < block_size; i += 16) {
                uint64_t v1 = 0, v2 = 0;
                size_t rem = block_size - i;
                size_t copy_len = (rem >= 16) ? 16 : rem;

                if (copy_len >= 8) {
                    memcpy(&v1, src + i, 8);
                    memcpy(&v2, src + i + 8, copy_len - 8);
                } else if (copy_len > 0) {
                    memcpy(&v1, src + i, copy_len);
                }

                // APRIMORAMENTO AVALANCHE LANES6 (2 fibras)
                v1 += (cs ^ (uint64_t)l * FIB_PRIME2);
                v2 -= (cs + (uint64_t)b * 0x9876543210ULL);

                v1 = (v1 << 17) | (v1 >> (64 - 17));
                v2 = (v2 << 29) | (v2 >> (64 - 29));

                cs ^= mix64(v1 + v2);

                if (copy_len >= 8) {
                    memcpy(dst + i,     &v1, 8);
                    memcpy(dst + i + 8, &v2, copy_len - 8);
                } else if (copy_len > 0) {
                    memcpy(dst + i, &v1, copy_len);
                }
            }
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    *out_sec = elapsed_sec(t0, t1);

    for (int l = 0; l < LANES; ++l) {
        free(buf[l]);
        free(out[l]);
    }
    return cs;
}

/* ---------------------------------------
 * MAIN
 * -------------------------------------*/
int main(void)
{
    const size_t total_bytes = (size_t)TOTAL_MIB * 1024ULL * 1024ULL;
    const size_t block_size  = (size_t)BLOCK_SIZE;
    const double cpu_mhz     = (double)CPU_MHz;

    printf("FIBER-H LANES6 RAFAELIA benchmark (Logica 5000x)\n");
    printf("  Total size   : %zu MiB                                           Block size   : %zu bytes\n",
           (size_t)TOTAL_MIB, block_size);
    printf("  CPU_FREQ_MHz : %.2f MHz                                       Script       : \"%s\"\n",
           cpu_mhz, SCRIPT_TAG);
    printf("                                                                 --- Results ---\n");
    printf("MODE              MB/s        CPB        Checksum\n");
    printf("-------------------------------------------------\n");

    // SCALAR
    double   t_scalar   = 0.0;
    uint64_t cs_scalar  = run_fiber_scalar(total_bytes, block_size, &t_scalar);
    double   mb_scalar  = (double)total_bytes / (1024.0 * 1024.0);
    double   mbps_scalar = mb_scalar / t_scalar;
    double   cpb_scalar  = (t_scalar * cpu_mhz * 1e6) / (double)total_bytes;

    // LANES6
    double   t_lanes6   = 0.0;
    uint64_t cs_lanes6  = run_fiber_lanes6(total_bytes, block_size, &t_lanes6);
    double   mb_lanes6  = (double)total_bytes / (1024.0 * 1024.0);
    double   mbps_lanes6 = mb_lanes6 / t_lanes6;
    double   cpb_lanes6  = (t_lanes6 * cpu_mhz * 1e6) / (double)total_bytes;

    printf("FIBER-H scalar  %10.3f   %7.3f   0x%02X\n",
           mbps_scalar, cpb_scalar, (unsigned)(cs_scalar & 0xFFu));
    printf("FIBER-H LANES6  %10.3f   %7.3f   0x%02X\n",
           mbps_lanes6, cpb_lanes6, (unsigned)(cs_lanes6 & 0xFFu));

    return 0;
}
