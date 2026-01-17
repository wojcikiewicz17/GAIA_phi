#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "fiber_hash.h"

/*
 * FIBER-H brute-force test (2-byte messages)
 *
 * - Gera todas as mensagens de 2 bytes (0..65535)
 * - Calcula FIBER-H(msg, 2)
 * - Ordena por hash e procura colisões exatas (256 bits)
 *
 * Este código é apenas um TESTE DE MESA AUTOMATIZADO,
 * não faz nenhum tipo de ataque de senha.
 */

/* Estrutura para guardar (mensagem, hash) */
typedef struct {
    unsigned char msg[2];
    unsigned char hash[32];
} fiber_entry_t;

/* Impressão em hex para debug opcional */
static void fiber_print_hex(const unsigned char *buf, size_t len) {
    for (size_t i = 0; i < len; ++i) {
        printf("%02x", (unsigned int)buf[i]);
    }
}

/* Comparador para qsort (ordena pelo hash de 32 bytes) */
static int fiber_cmp_entry(const void *a, const void *b) {
    const fiber_entry_t *ea = (const fiber_entry_t *)a;
    const fiber_entry_t *eb = (const fiber_entry_t *)b;
    return memcmp(ea->hash, eb->hash, 32);
}

int main(void) {
    const unsigned int N = 65536U; /* 2^16 mensagens de 2 bytes */
    fiber_entry_t *table = NULL;
    unsigned int i;
    unsigned int collisions = 0;

    printf("[*] FIBER-H brute-force test over 2-byte messages (0x0000..0xFFFF)\n");

    table = (fiber_entry_t *)malloc((size_t)N * sizeof(fiber_entry_t));
    if (!table) {
        fprintf(stderr, "[ERROR] malloc() failed allocating %u entries\n", N);
        return 1;
    }

    /* 1) Gerar mensagens e hashes */
    printf("[*] Generating messages and computing hashes...\n");
    for (i = 0; i < N; ++i) {
        unsigned char msg[2];
        unsigned char out[32];

        msg[0] = (unsigned char)(i & 0xFFu);
        msg[1] = (unsigned char)((i >> 8) & 0xFFu);

        fiber_h(msg, 2, out);

        table[i].msg[0] = msg[0];
        table[i].msg[1] = msg[1];
        memcpy(table[i].hash, out, 32);
    }

    /* 2) Ordenar por hash para detectar colisões */
    printf("[*] Sorting %u entries by 256-bit hash...\n", N);
    qsort(table, (size_t)N, sizeof(fiber_entry_t), fiber_cmp_entry);

    /* 3) Scan linear procurando colisões exatas */
    printf("[*] Scanning for exact 256-bit collisions...\n");
    for (i = 1; i < N; ++i) {
        if (memcmp(table[i - 1].hash, table[i].hash, 32) == 0) {
            /* Encontramos duas mensagens diferentes com mesmo hash 256-bit */
            if (table[i - 1].msg[0] != table[i].msg[0] ||
                table[i - 1].msg[1] != table[i].msg[1]) {
                printf("[COLLISION] found between messages:\n");
                printf("  m1 = %02x%02x\n",
                       (unsigned int)table[i - 1].msg[0],
                       (unsigned int)table[i - 1].msg[1]);
                printf("  m2 = %02x%02x\n",
                       (unsigned int)table[i].msg[0],
                       (unsigned int)table[i].msg[1]);
                printf("  hash = ");
                fiber_print_hex(table[i].hash, 32);
                printf("\n");
                collisions++;
            }
        }
    }

    printf("[*] Brute-force scan finished.\n");
    printf("[*] Total messages checked : %u\n", N);
    printf("[*] Total exact collisions  : %u\n", collisions);

    free(table);
    return 0;
}
