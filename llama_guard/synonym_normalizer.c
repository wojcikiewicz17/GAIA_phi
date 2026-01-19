#include "synonym_normalizer.h"

#include <ctype.h>
#include <string.h>

typedef struct {
    const char *canonical;
    const char *aliases[12];
} SynonymEntry;

static const SynonymEntry kSynonymTable[] = {
    {
        "grapefruit",
        {"grapefruit", "toranja", "pomelo", "pomelo-grapefruit", "citrus paradisi", NULL}
    },
    {
        "criança",
        {"criança", "crianca", "bebê", "bebe", "infantil", "menor", "nenem", NULL}
    },
    {
        "alergia",
        {"alergia", "alergico", "alérgico", "hipersensibilidade", "intolerancia", NULL}
    },
    {
        "saneante",
        {"saneante", "desinfetante", "agua sanitaria", "água sanitária", "cloro", "bleach", NULL}
    },
    {
        "recipiente fechado",
        {"recipiente fechado", "frasco fechado", "pote fechado", "container fechado", NULL}
    },
    {
        "energia",
        {"energia", "aquecimento", "chama", "fogo", "microondas", "micro-ondas", NULL}
    }
};

static int is_word_char(int c) {
    return isalnum(c) || c == '-' || c == '_';
}

void synonym_normalizer_compact_lower(const char *input, char *out, size_t out_size) {
    if (!input || !out || out_size == 0) {
        return;
    }
    size_t o = 0;
    int prev_space = 1;
    for (size_t i = 0; input[i] != '\0' && o + 1 < out_size; ++i) {
        unsigned char ch = (unsigned char)input[i];
        if (is_word_char(ch) || ch >= 128) {
            out[o++] = (char)tolower(ch);
            prev_space = 0;
        } else {
            if (!prev_space && o + 1 < out_size) {
                out[o++] = ' ';
                prev_space = 1;
            }
        }
    }
    if (o > 0 && out[o - 1] == ' ') {
        o--;
    }
    out[o] = '\0';
}

static int contains_word(const char *haystack, const char *needle) {
    if (!haystack || !needle || !*needle) {
        return 0;
    }
    size_t needle_len = strlen(needle);
    const char *p = haystack;
    while ((p = strstr(p, needle)) != NULL) {
        int before_ok = (p == haystack) || !is_word_char((unsigned char)p[-1]);
        int after_ok = !is_word_char((unsigned char)p[needle_len]);
        if (before_ok && after_ok) {
            return 1;
        }
        p += needle_len;
    }
    return 0;
}

int synonym_normalizer_find(const char *input_text,
                            const char **out_canonical,
                            const char **out_alias) {
    char normalized[1024];
    synonym_normalizer_compact_lower(input_text, normalized, sizeof(normalized));

    for (size_t i = 0; i < sizeof(kSynonymTable) / sizeof(kSynonymTable[0]); ++i) {
        const SynonymEntry *entry = &kSynonymTable[i];
        for (size_t j = 0; entry->aliases[j]; ++j) {
            char alias_norm[128];
            synonym_normalizer_compact_lower(entry->aliases[j], alias_norm, sizeof(alias_norm));
            if (contains_word(normalized, alias_norm)) {
                if (out_canonical) {
                    *out_canonical = entry->canonical;
                }
                if (out_alias) {
                    *out_alias = entry->aliases[j];
                }
                return 1;
            }
        }
    }
    if (out_canonical) {
        *out_canonical = NULL;
    }
    if (out_alias) {
        *out_alias = NULL;
    }
    return 0;
}

int synonym_normalizer_contains_alias(const char *input_text,
                                      const char *canonical_term,
                                      const char **out_alias) {
    if (!canonical_term) {
        return 0;
    }
    char normalized[1024];
    synonym_normalizer_compact_lower(input_text, normalized, sizeof(normalized));

    for (size_t i = 0; i < sizeof(kSynonymTable) / sizeof(kSynonymTable[0]); ++i) {
        const SynonymEntry *entry = &kSynonymTable[i];
        if (strcmp(entry->canonical, canonical_term) != 0) {
            continue;
        }
        for (size_t j = 0; entry->aliases[j]; ++j) {
            char alias_norm[128];
            synonym_normalizer_compact_lower(entry->aliases[j], alias_norm, sizeof(alias_norm));
            if (contains_word(normalized, alias_norm)) {
                if (out_alias) {
                    *out_alias = entry->aliases[j];
                }
                return 1;
            }
        }
    }
    if (out_alias) {
        *out_alias = NULL;
    }
    return 0;
}
