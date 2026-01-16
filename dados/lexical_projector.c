#include "../headers/omega_lexicon.h"
#include "../headers/omega_hash.h"
void project_text_to_vector(const char* input, VectorVerb* v_out) {
    uint64_t h = semantic_hash_djb2(input);
    hash_to_vector(h, v_out);
}
