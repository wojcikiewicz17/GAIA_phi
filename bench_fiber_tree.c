#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "fiber_hash.h"

/* Medição simples com CLOCK_MONOTONIC */
static double now_sec(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}

static void fill_pattern(fiber_u8 *buf, fiber_size_t len) {
    fiber_size_t i;
    fiber_u8 seed = 0x5a;
    for (i = 0u; i < len; ++i) {
        seed ^= (fiber_u8)(i * 131u);
        buf[i] = (fiber_u8)(seed + (fiber_u8)i);
    }
}

int main(int argc, char **argv) {
    fiber_size_t total_mib  = 256u;
    fiber_size_t leaf_size  = 1024u;
    double cpu_mhz          = 2800.0; /* ajuste se quiser */

    if (argc >= 2) {
        total_mib = (fiber_size_t)strtoul(argv[1], NULL, 10);
        if (total_mib == 0u) total_mib = 256u;
    }
    if (argc >= 3) {
        leaf_size = (fiber_size_t)strtoul(argv[2], NULL, 10);
        if (leaf_size == 0u) leaf_size = 1024u;
    }
    if (argc >= 4) {
        cpu_mhz = atof(argv[3]);
        if (cpu_mhz <= 0.0) cpu_mhz = 2800.0;
    }

    fiber_size_t total_bytes = total_mib * 1024u * 1024u;
    fiber_u8 *buf = (fiber_u8 *)malloc((size_t)total_bytes);
    if (!buf) {
        fprintf(stderr, "[-] malloc failed for %u MiB\n",
                (unsigned)total_mib);
        return 1;
    }

    fill_pattern(buf, total_bytes);

    fiber_u8 out[32];
    double t0 = now_sec();
    fiber_h_tree(buf, total_bytes, out, leaf_size);
    double t1 = now_sec();

    free(buf);

    double elapsed = t1 - t0;
    double mib = (double)total_bytes / (1024.0 * 1024.0);
    double mbps = (elapsed > 0.0) ? (mib / elapsed) : 0.0;
    double cpb  = 0.0;
    if (elapsed > 0.0) {
        double cycles = cpu_mhz * 1e6 * elapsed;
        cpb = cycles / (double)total_bytes;
    }

    printf("FIBER-H tree benchmark\n");
    printf("  Total size   : %.2f MiB\n", mib);
    printf("  Leaf size    : %u bytes\n", (unsigned)leaf_size);
    printf("  CPU_FREQ_MHz : %.2f MHz\n\n", cpu_mhz);
    printf("--- Results ---\n");
    printf("  Time elapsed : %.6f s\n", elapsed);
    printf("  Throughput   : %.2f MiB/s\n", mbps);
    printf("  Cycles/byte  : %.3f\n", cpb);
    printf("  Root hash    : ");
    {
        fiber_size_t i;
        for (i = 0u; i < (fiber_size_t)32u; ++i) {
            printf("%02x", (unsigned)out[i]);
        }
        printf("\n");
    }

    return 0;
}
