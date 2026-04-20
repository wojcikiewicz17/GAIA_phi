#include <stdio.h>
#include <string.h>

#include "gaia_hash.h"
#include "gaia_asm_core.h"
#include "gaia_projection.h"
#include "gaia_vector.h"
#include "raf_engine.h"
#include "smart_guard.h"

static GaiaStatus pass_engine(const void *input, void *output) {
    const float *in = (const float *)input;
    float *out = (float *)output;
    if (!in || !out) {
        return GAIA_ERR_NULL;
    }
    out[0] = in[0] + in[1];
    return GAIA_OK;
}

static GaiaStatus pass_metrics(void *out_metrics) {
    uint32_t *m = (uint32_t *)out_metrics;
    if (!m) {
        return GAIA_ERR_NULL;
    }
    *m = 42u;
    return GAIA_OK;
}

int main(void) {
    const uint8_t msg[] = "gaia";
    uint64_t h = gaia_hash_bytes(GAIA_HASH_FNV1A, msg, sizeof(msg) - 1u);
    if (h == 0u) {
        fprintf(stderr, "hash failure\n");
        return 1;
    }

    float buf[3] = {0};
    GaiaVector vec;
    if (gaia_vector_init(&vec, buf, 3u) != GAIA_OK) {
        fprintf(stderr, "vector init failure\n");
        return 1;
    }
    if (gaia_vector_project_hash(&vec, h) != GAIA_OK) {
        fprintf(stderr, "vector projection failure\n");
        return 1;
    }

    {
        uint32_t mixed_asm = gaia_asm_mix_u32(0x12345678u, 0x0badf00du, 0x11111111u);
        uint32_t mixed_ref = gaia_asm_mix_u32_ref(0x12345678u, 0x0badf00du, 0x11111111u);
        if (mixed_asm != mixed_ref) {
            fprintf(stderr, "asm core mismatch (%u != %u)\n", mixed_asm, mixed_ref);
            return 1;
        }
    }

    {
        float proj[3] = {0};
        if (gaia_project_3d(h, proj) != GAIA_OK) {
            fprintf(stderr, "projection failure\n");
            return 1;
        }
    }

    {
        RafEngine engine = {"sum", pass_engine, pass_metrics};
        float in[2] = {2.0f, 3.0f};
        float out[1] = {0};
        uint32_t metrics = 0u;
        raf_engine_reset();
        if (raf_engine_register(&engine) != GAIA_OK) {
            fprintf(stderr, "engine register failure\n");
            return 1;
        }
        if (raf_engine_execute("sum", in, out) != GAIA_OK || out[0] != 5.0f) {
            fprintf(stderr, "engine execute failure\n");
            return 1;
        }
        if (raf_engine_metrics("sum", &metrics) != GAIA_OK || metrics != 42u) {
            fprintf(stderr, "engine metrics failure\n");
            return 1;
        }
    }

    {
        SGResult r = smart_guard_evaluate("misturar cloro para crianca");
        if (r.action != SG_ACTION_BLOCK) {
            fprintf(stderr, "smart guard failure\n");
            return 1;
        }
    }

    printf("structural selftest: OK\n");
    return 0;
}
