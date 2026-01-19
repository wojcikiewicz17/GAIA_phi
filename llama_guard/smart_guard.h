#ifndef LLAMA_GUARD_SMART_GUARD_H
#define LLAMA_GUARD_SMART_GUARD_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    SG_ACTION_ALLOW = 0,
    SG_ACTION_WARN = 1,
    SG_ACTION_BLOCK = 2
} SGAction;

typedef enum {
    SG_REASON_NONE = 0u,
    SG_REASON_VULNERABLE = 1u << 0,
    SG_REASON_AMBIGUOUS = 1u << 1,
    SG_REASON_CHILD = 1u << 2,
    SG_REASON_ALLERGY = 1u << 3,
    SG_REASON_HEALTH = 1u << 4,
    SG_REASON_CHEMICAL = 1u << 5,
    SG_REASON_PRESSURE = 1u << 6,
    SG_REASON_ENERGY = 1u << 7,
    SG_REASON_SYNONYM = 1u << 8
} SGReason;

typedef struct {
    int risk_level;
    SGAction action;
    uint32_t reasons;
} SGResult;

SGResult smart_guard_evaluate(const char *input_text);

const char *smart_guard_action_label(SGAction action);
const char *smart_guard_reason_label(SGReason reason);

size_t smart_guard_format_reasons(uint32_t reasons, char *out, size_t out_size);

void smart_guard_format_message(const SGResult *result, char *out, size_t out_size);

#ifdef __cplusplus
}
#endif

#endif
