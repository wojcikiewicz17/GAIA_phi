#ifndef LLAMA_GUARD_INTEGRATION_H
#define LLAMA_GUARD_INTEGRATION_H

#include <stddef.h>

#include "smart_guard.h"

#ifdef __cplusplus
extern "C" {
#endif

SGAction llama_guard_gate_prompt(const char *prompt,
                                 char *out_message,
                                 size_t out_message_size);

#ifdef __cplusplus
}
#endif

#endif
