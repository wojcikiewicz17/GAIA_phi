#include <stdio.h>   /* Apenas para printf no self-test */
#include <string.h>  /* Apenas para strlen no self-test */
#include "fiber_hash.h"

/* Dump hex em linha contínua: baixo overhead, sem malloc */
static void fiber_dump_hex(const fiber_u8 *h, fiber_size_t n) {
    fiber_size_t i;
    for (i = 0; i < n; ++i) {
        unsigned int v = (unsigned int)h[i];
        static const char hex[] = "0123456789abcdef";
        char hi = hex[(v >> 4) & 0xF];
        char lo = hex[v & 0xF];
        putchar(hi);
        putchar(lo);
    }
}

int main(void) {
    struct {
        const char *label;
        const char *msg;
    } tests[] = {
        { "\"\"",  ""   },
        { "\"a\"", "a"  },
        { "\"abc\"", "abc" }
    };

    fiber_u8 out[32];
    int i;

    for (i = 0; i < (int)(sizeof(tests) / sizeof(tests[0])); ++i) {
        const char *m = tests[i].msg;
        fiber_size_t len = (fiber_size_t)strlen(m);

        fiber_h((const fiber_u8 *)m, len, out);

        printf("FIBER-H(%s) = ", tests[i].label);
        fiber_dump_hex(out, (fiber_size_t)32);
        putchar('\n');
    }

    return 0;
}
