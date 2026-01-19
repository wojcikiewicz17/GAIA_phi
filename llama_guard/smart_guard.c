#include "smart_guard.h"
#include "synonym_normalizer.h"

#include <ctype.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    const char *token;
    SGReason reason;
} Trigger;

static const Trigger kVulnerableTriggers[] = {
    {"criança", SG_REASON_CHILD},
    {"crianca", SG_REASON_CHILD},
    {"bebê", SG_REASON_CHILD},
    {"bebe", SG_REASON_CHILD},
    {"menor", SG_REASON_CHILD},
    {"alergia", SG_REASON_ALLERGY},
    {"alergico", SG_REASON_ALLERGY},
    {"alérgico", SG_REASON_ALLERGY},
    {"asma", SG_REASON_HEALTH},
    {"saúde", SG_REASON_HEALTH},
    {"saude", SG_REASON_HEALTH},
    {"medicação", SG_REASON_HEALTH},
    {"medicacao", SG_REASON_HEALTH}
};

static const Trigger kRiskTriggers[] = {
    {"misturar", SG_REASON_CHEMICAL},
    {"mistura", SG_REASON_CHEMICAL},
    {"saneante", SG_REASON_CHEMICAL},
    {"desinfetante", SG_REASON_CHEMICAL},
    {"cloro", SG_REASON_CHEMICAL},
    {"quimico", SG_REASON_CHEMICAL},
    {"químico", SG_REASON_CHEMICAL},
    {"recipiente fechado", SG_REASON_PRESSURE},
    {"garrafa fechada", SG_REASON_PRESSURE},
    {"pressão", SG_REASON_PRESSURE},
    {"pressao", SG_REASON_PRESSURE},
    {"energia", SG_REASON_ENERGY},
    {"aquecimento", SG_REASON_ENERGY},
    {"chama", SG_REASON_ENERGY},
    {"fogo", SG_REASON_ENERGY}
};

static const char *kAmbiguousTokens[] = {
    "não sei",
    "nao sei",
    "acho que",
    "talvez",
    "genérico",
    "generico",
    "rótulo",
    "rotulo",
    "pode ser",
    "não lembro",
    "nao lembro"
};

static int contains_token(const char *haystack, const char *needle) {
    if (!haystack || !needle || !*needle) {
        return 0;
    }
    size_t len = strlen(needle);
    const char *p = haystack;
    while ((p = strstr(p, needle)) != NULL) {
        int before_ok = (p == haystack) || !isalnum((unsigned char)p[-1]);
        int after_ok = !isalnum((unsigned char)p[len]);
        if (before_ok && after_ok) {
            return 1;
        }
        p += len;
    }
    return 0;
}

static void compact_lower(const char *input, char *out, size_t out_size) {
    synonym_normalizer_compact_lower(input, out, out_size);
}

static uint32_t collect_reasons(const char *text, int *has_vulnerable, int *has_risk, int *has_ambiguous) {
    uint32_t reasons = SG_REASON_NONE;
    *has_vulnerable = 0;
    *has_risk = 0;
    *has_ambiguous = 0;

    char normalized[2048];
    compact_lower(text, normalized, sizeof(normalized));

    for (size_t i = 0; i < sizeof(kVulnerableTriggers) / sizeof(kVulnerableTriggers[0]); ++i) {
        if (contains_token(normalized, kVulnerableTriggers[i].token)) {
            reasons |= SG_REASON_VULNERABLE | kVulnerableTriggers[i].reason;
            *has_vulnerable = 1;
        }
    }

    for (size_t i = 0; i < sizeof(kRiskTriggers) / sizeof(kRiskTriggers[0]); ++i) {
        if (contains_token(normalized, kRiskTriggers[i].token)) {
            reasons |= kRiskTriggers[i].reason;
            *has_risk = 1;
        }
    }

    for (size_t i = 0; i < sizeof(kAmbiguousTokens) / sizeof(kAmbiguousTokens[0]); ++i) {
        if (contains_token(normalized, kAmbiguousTokens[i])) {
            reasons |= SG_REASON_AMBIGUOUS;
            *has_ambiguous = 1;
        }
    }

    const char *canonical = NULL;
    const char *alias = NULL;
    if (synonym_normalizer_find(normalized, &canonical, &alias)) {
        if (alias && canonical && strcmp(alias, canonical) != 0) {
            reasons |= SG_REASON_SYNONYM;
        }
        if (canonical && strcmp(canonical, "grapefruit") == 0) {
            reasons |= SG_REASON_ALLERGY;
            *has_vulnerable = 1;
        }
    }

    return reasons;
}

SGResult smart_guard_evaluate(const char *input_text) {
    SGResult result;
    result.risk_level = 0;
    result.action = SG_ACTION_ALLOW;
    result.reasons = SG_REASON_NONE;

    if (!input_text || input_text[0] == '\0') {
        return result;
    }

    int has_vulnerable = 0;
    int has_risk = 0;
    int has_ambiguous = 0;

    result.reasons = collect_reasons(input_text, &has_vulnerable, &has_risk, &has_ambiguous);

    if (has_vulnerable && has_ambiguous) {
        result.risk_level = 3;
        result.action = SG_ACTION_BLOCK;
    } else if (has_risk && has_vulnerable) {
        result.risk_level = 2;
        result.action = SG_ACTION_BLOCK;
    } else if (has_risk || has_ambiguous) {
        result.risk_level = 1;
        result.action = SG_ACTION_WARN;
    }

    return result;
}

const char *smart_guard_action_label(SGAction action) {
    switch (action) {
        case SG_ACTION_ALLOW:
            return "ALLOW";
        case SG_ACTION_WARN:
            return "WARN";
        case SG_ACTION_BLOCK:
            return "BLOCK";
        default:
            return "UNKNOWN";
    }
}

const char *smart_guard_reason_label(SGReason reason) {
    switch (reason) {
        case SG_REASON_VULNERABLE:
            return "vulneravel";
        case SG_REASON_AMBIGUOUS:
            return "ambiguo";
        case SG_REASON_CHILD:
            return "crianca";
        case SG_REASON_ALLERGY:
            return "alergia";
        case SG_REASON_HEALTH:
            return "saude";
        case SG_REASON_CHEMICAL:
            return "quimico";
        case SG_REASON_PRESSURE:
            return "pressao";
        case SG_REASON_ENERGY:
            return "energia";
        case SG_REASON_SYNONYM:
            return "sinonimo";
        default:
            return "desconhecido";
    }
}

size_t smart_guard_format_reasons(uint32_t reasons, char *out, size_t out_size) {
    if (!out || out_size == 0) {
        return 0;
    }
    size_t used = 0;
    out[0] = '\0';
    if (reasons == SG_REASON_NONE) {
        return 0;
    }

    for (uint32_t bit = 1u; bit <= SG_REASON_SYNONYM; bit <<= 1u) {
        if (reasons & bit) {
            const char *label = smart_guard_reason_label((SGReason)bit);
            int written = snprintf(out + used, out_size - used, "%s%s", used ? "," : "", label);
            if (written < 0 || (size_t)written >= out_size - used) {
                return used;
            }
            used += (size_t)written;
        }
    }
    return used;
}

void smart_guard_format_message(const SGResult *result, char *out, size_t out_size) {
    if (!out || out_size == 0) {
        return;
    }
    if (!result) {
        snprintf(out, out_size, "AVISA: entrada vazia");
        return;
    }
    char reasons_buf[256];
    smart_guard_format_reasons(result->reasons, reasons_buf, sizeof(reasons_buf));

    if (result->action == SG_ACTION_BLOCK) {
        snprintf(out, out_size, "AVISA: BLOQUEADO (nivel=%d, motivos=%s)", result->risk_level,
                 reasons_buf[0] ? reasons_buf : "indefinido");
    } else if (result->action == SG_ACTION_WARN) {
        snprintf(out, out_size, "AVISA: CAUTELA (nivel=%d, motivos=%s)", result->risk_level,
                 reasons_buf[0] ? reasons_buf : "indefinido");
    } else {
        snprintf(out, out_size, "OK (nivel=%d)", result->risk_level);
    }
}
