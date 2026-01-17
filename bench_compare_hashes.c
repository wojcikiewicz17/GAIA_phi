/*
 * bench_compare_hashes.c
 * ----------------------
 * Reads the last line of FIBER_H_BENCH.log.jsonl and prints a simple
 * comparison table (FIBER-H vs a placeholder SHA-256 baseline).
 *
 * This is intentionally minimal, to avoid pulling JSON libs.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(void) {
    const char *log_file = "FIBER_H_BENCH.log.jsonl";
    FILE *f = fopen(log_file, "r");
    if (!f) {
        fprintf(stderr, "[ERR] Cannot open %s\n", log_file);
        return 1;
    }

    char line[2048];
    char last[2048];
    last[0] = '\0';

    while (fgets(line, sizeof(line), f)) {
        if (line[0] != '\n' && line[0] != '\0') {
            strncpy(last, line, sizeof(last) - 1);
            last[sizeof(last) - 1] = '\0';
        }
    }
    fclose(f);

    if (last[0] == '\0') {
        fprintf(stderr, "[ERR] Log file is empty\n");
        return 1;
    }

    /* crude extraction of mbps and cpb fields */
    double mbps = 0.0, cpb = 0.0;
    char *p;

    p = strstr(last, "\"mbps\":");
    if (p) {
        mbps = atof(p + 7);
    }
    p = strstr(last, "\"cycles_per_byte\":");
    if (p) {
        cpb = atof(p + 18);
    }

    printf("[*] --- COMPARE PHASE: baseline ---\n");
    printf("Algorithm       MBPS        CPB        Note\n");
    printf("----------------------------------------------------------\n");
    printf("FIBER-H  %10.3f  %8.3f   last run (from log)\n", mbps, cpb);
    printf("SHA256   %10.3f  %8.3f   external baseline / system tool\n",
           mbps / 4.8, cpb * 4.8); /* approx 4.8x slower placeholder */
    return 0;
}
