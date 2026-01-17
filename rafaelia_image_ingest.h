#ifndef RAFAELIA_IMAGE_INGEST_H
#define RAFAELIA_IMAGE_INGEST_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

int rafaelia_image_vector(const char *path,
                          size_t vector_dim,
                          double *out_vec,
                          size_t out_len,
                          char *err_buf,
                          size_t err_len);

#ifdef __cplusplus
}
#endif

#endif
