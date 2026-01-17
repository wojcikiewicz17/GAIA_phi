#include "rafaelia_image_ingest.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void set_err(char *err_buf, size_t err_len, const char *msg) {
    if (err_buf && err_len > 0) {
        snprintf(err_buf, err_len, "%s", msg);
    }
}

int rafaelia_image_vector(const char *path,
                          size_t vector_dim,
                          double *out_vec,
                          size_t out_len,
                          char *err_buf,
                          size_t err_len) {
    if (!path || !out_vec) {
        set_err(err_buf, err_len, "invalid_arguments");
        return 1;
    }
    if (vector_dim == 0 || out_len < vector_dim) {
        set_err(err_buf, err_len, "invalid_vector_dim");
        return 2;
    }

    FILE *fp = fopen(path, "rb");
    if (!fp) {
        char buffer[128];
        snprintf(buffer, sizeof(buffer), "open_failed:%s", strerror(errno));
        set_err(err_buf, err_len, buffer);
        return 3;
    }

    double *counts = calloc(vector_dim, sizeof(double));
    if (!counts) {
        fclose(fp);
        set_err(err_buf, err_len, "alloc_failed");
        return 4;
    }

    unsigned char buf[65536];
    size_t read_size = 0;
    unsigned long long total = 0;

    while ((read_size = fread(buf, 1, sizeof(buf), fp)) > 0) {
        for (size_t i = 0; i < read_size; i++) {
            size_t idx = (size_t)((buf[i] * vector_dim) / 256);
            if (idx >= vector_dim) {
                idx = vector_dim - 1;
            }
            counts[idx] += 1.0;
            total += 1;
        }
    }

    if (ferror(fp)) {
        fclose(fp);
        free(counts);
        set_err(err_buf, err_len, "read_failed");
        return 5;
    }

    if (total == 0) {
        total = 1;
    }

    for (size_t i = 0; i < vector_dim; i++) {
        out_vec[i] = counts[i] / (double)total;
    }

    free(counts);
    fclose(fp);
    return 0;
}
