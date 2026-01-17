/*
 * bench_fiber_h.c
 * ----------------
 * Combined self-test + benchmark runner for FIBER-H.
 *
 * Features:
 *  - Self-test using multiple KATs ("" , "a", "abc", 64B, 1000B, 1MiB zeros)
 *  - Benchmark with configurable:
 *      total size in MiB  (1 .. 1024)
 *      block size in bytes (64 .. 65536, multiple of 64)
 *  - Uses CLOCK_MONOTONIC for stable timing
 *
 * Usage:
 *   ./bench_fiber_h selftest
 *   ./bench_fiber_h [total_mib] [block_size_bytes]
 *
 * Example:
 *   ./bench_fiber_h           # defaults: 256 MiB, 1024-byte blocks
 *   ./bench_fiber_h 128 4096  # 128 MiB, 4 KiB blocks
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "fiber_hash.h"

#ifndef FIBER_CPU_FREQ_MHZ
#define FIBER_CPU_FREQ_MHZ 2800.0
#endif

static double now_seconds(void) {
    struct timespec ts;
    if (clock_gettime(CLOCK_MONOTONIC, &ts) != 0) {
        /* Fallback: very coarse, but we avoid aborting */
        return (double)time(NULL);
    }
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

/* Hex encoder (for KAT display) */
static void hex_encode(const unsigned char *in, size_t len, char *out) {
    static const char *hex = "0123456789abcdef";
    for (size_t i = 0; i < len; ++i) {
        unsigned char v = in[i];
        out[2*i + 0] = hex[v >> 4];
        out[2*i + 1] = hex[v & 0x0F];
    }
    out[2*len] = '\0';
}

static int run_selftest(void) {
    printf("[*] FIBER-H self-test (KATs)\n");

    struct {
        const char *label;
        const unsigned char *data;
        size_t len;
    } cases[6];

    static const unsigned char zeros64[64] = {0};
    static const unsigned char As64[64] = {
        [0 ... 63] = 0x41
    };
    static unsigned char zeros1MiB[1024 * 1024];

    cases[0].label = "\"\"";
    cases[0].data  = (const unsigned char *)"";
    cases[0].len   = 0;

    cases[1].label = "\"a\"";
    cases[1].data  = (const unsigned char *)"a";
    cases[1].len   = 1;

    cases[2].label = "\"abc\"";
    cases[2].data  = (const unsigned char *)"abc";
    cases[2].len   = 3;

    cases[3].label = "64x00";
    cases[3].data  = zeros64;
    cases[3].len   = sizeof(zeros64);

    cases[4].label = "64x41";
    cases[4].data  = As64;
    cases[4].len   = sizeof(As64);

    cases[5].label = "1MiB_zeros";
    cases[5].data  = zeros1MiB;
    cases[5].len   = sizeof(zeros1MiB);

    unsigned char out[32];
    char hex[65];

    for (int i = 0; i < 6; ++i) {
        fiber_h(cases[i].data, (fiber_size_t)cases[i].len, out);
        hex_encode(out, 32, hex);
        printf("  FIBER-H(%s) = %s\n", cases[i].label, hex);
    }

    printf("[*] Self-test completed (compare above vs expected KATs in your docs).\n");
    return 0;
}

static int run_bench(size_t total_mib, size_t block_size) {
    /* Clamp and sanitize parameters */
    if (total_mib < 1)   total_mib = 1;
    if (total_mib > 1024) total_mib = 1024;

    if (block_size < 64)      block_size = 64;
    if (block_size > 65536)   block_size = 65536;
    /* enforce multiple of 64 (block aligned to FIBER-H block size) */
    block_size = (block_size / 64) * 64;
    if (block_size == 0) block_size = 64;

    const double cpu_mhz = FIBER_CPU_FREQ_MHZ;

    size_t total_bytes = total_mib * 1024ULL * 1024ULL;
    size_t loops       = total_bytes / block_size;

    printf("FIBER-H benchmark\n");
    printf("  Target bytes   : %zu (%.2f MiB)\n",
           total_bytes, (double)total_bytes / (1024.0 * 1024.0));
    printf("  Block size     : %zu bytes\n", block_size);
    printf("  CPU_FREQ_MHZ   : %.2f MHz\n\n", cpu_mhz);

    unsigned char *buf = (unsigned char *)malloc(block_size);
    if (!buf) {
        fprintf(stderr, "[ERR] malloc(%zu) failed\n", block_size);
        return 1;
    }

    /* Fill buffer with simple pattern (data dependency minimal) */
    for (size_t i = 0; i < block_size; ++i) {
        buf[i] = (unsigned char)(i * 1315423911U);
    }

    unsigned char out[32];
    unsigned char checksum = 0;

    double t1 = now_seconds();
    for (size_t i = 0; i < loops; ++i) {
        fiber_h(buf, (fiber_size_t)block_size, out);
        checksum ^= out[0]; /* Prevent dead-code elimination */
    }
    double t2 = now_seconds();

    double dt   = t2 - t1;
    double mibs = (double)total_bytes / (1024.0 * 1024.0) / dt;
    double cpb  = (cpu_mhz * 1e6 * dt) / (double)total_bytes;

    printf("--- Results ---\n");
    printf("  Time elapsed   : %.6f s\n", dt);
    printf("  Processed      : %.2f MiB\n",
           (double)total_bytes / (1024.0 * 1024.0));
    printf("  Throughput     : %.2f MiB/s\n", mibs);
    printf("  Cycles per byte: %.3f (approx.)\n", cpb);
    printf("  Checksum       : 0x%02X\n", (unsigned int)checksum);

    free(buf);
    return 0;
}

int main(int argc, char **argv) {
    if (argc >= 2 && strcmp(argv[1], "selftest") == 0) {
        return run_selftest();
    }

    size_t total_mib  = 256;
    size_t block_size = 1024;

    if (argc >= 2) {
        total_mib = (size_t)strtoul(argv[1], NULL, 10);
    }
    if (argc >= 3) {
        block_size = (size_t)strtoul(argv[2], NULL, 10);
    }

    return run_bench(total_mib, block_size);
}
