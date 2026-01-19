#ifndef LLAMA_GUARD_SYNONYM_NORMALIZER_H
#define LLAMA_GUARD_SYNONYM_NORMALIZER_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

int synonym_normalizer_find(const char *input_text,
                            const char **out_canonical,
                            const char **out_alias);

int synonym_normalizer_contains_alias(const char *input_text,
                                      const char *canonical_term,
                                      const char **out_alias);

void synonym_normalizer_compact_lower(const char *input, char *out, size_t out_size);

#ifdef __cplusplus
}
#endif

#endif
