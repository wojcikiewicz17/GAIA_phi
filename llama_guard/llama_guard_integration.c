#include "llama_guard_integration.h"

#include <string.h>

SGAction llama_guard_gate_prompt(const char *prompt,
                                 char *out_message,
                                 size_t out_message_size) {
    SGResult result = smart_guard_evaluate(prompt);
    if (out_message && out_message_size > 0) {
        smart_guard_format_message(&result, out_message, out_message_size);
    }
    return result.action;
}
