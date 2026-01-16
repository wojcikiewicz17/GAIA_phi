#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "headers/omega_protocol.h"
#include "headers/omega_nexus.h"
#include "headers/omega_hash.h"
#include "headers/omega_attention.h"

// Protótipos esperados do módulo de hash/tokenização vetorial
// Devem existir em core/semantic_hash.c ou equivalente.
uint64_t semantic_hash_djb2(const char* text);
void     hash_to_vector(uint64_t h, VectorVerb* v);

// Simulação da geração de tokens do NanoGPT
// Em um cenário real, aqui entraria a multiplicação de matrizes
// do seu modelo treinado. Nesta demo, misturamos:
//  - prompt textual
//  - memória em foco (via Nexus)
//  - score de atenção
static void nanogpt_generate(const char* prompt, VirtualContextWindow* win) {
    (void)prompt;

    printf("\n\033[1;35m[NanoGPT 1B]\033[0m Gerando resposta baseada no Foco de Atenção...\n");

    if (win->focus_region) {
        char* memory_token = resolve_memory_content(win->focus_region);

        printf("Contexto Ativo (via MMAP): \033[32m%s\033[0m\n",
               memory_token ? memory_token : "(null)");
        printf("Confiança da Atenção: %.4f\n", win->attention_score);

        printf(">> \033[1;37m");
        if (win->attention_score > 0.9f) {
            printf("Baseado nos meus registros absolutos de '%s', confirmo a operação.",
                   memory_token ? memory_token : "(desconhecido)");
        } else if (win->attention_score > 0.7f) {
            printf("Acesso parcial aos dados de '%s'. Requer validação.",
                   memory_token ? memory_token : "(desconhecido)");
        } else if (memory_token) {
            printf("Minha janela de 1 bilhão de vetores não contém referência clara, "
                   "mas '%s' parece relacionado.", memory_token);
        } else {
            printf("Não encontrei memória relevante para este prompt.");
        }
        printf("\033[0m\n");

        // Se o token parecer um caminho de arquivo, tenta ler as primeiras linhas
        if (memory_token) {
            FILE* f = fopen(memory_token, "r");
            if (f) {
                printf("\033[90m[Lendo bytes do contexto '%s'...]\033[0m\n", memory_token);
                char buf[128];
                int  lines = 0;
                while (fgets(buf, sizeof(buf), f) && lines < 3) {
                    printf("   %s", buf);
                    lines++;
                }
                fclose(f);
            }
        }
    } else {
        printf(">> [Vazio] A vastidão de 1Bi vetores está silenciosa para este prompt.\n");
    }
}

int main(void) {
    char input_buf[1024];

    // 1. Boot: mapeia o universo (ex.: 1M de slots; em produção, 1B)
    if (nexus_init("gaia.nexus", 1000000) != 0) {
        fprintf(stderr, "[ERR] Falha ao inicializar gaia.nexus\n");
        return 1;
    }

    VirtualContextWindow v_ctx;
    v_ctx.total_capacity  = 0;
    v_ctx.focus_region    = NULL;
    v_ctx.attention_score = 0.0f;

    omega_float qbuf[3] = {0.0f, 0.0f, 0.0f};
    VectorVerb query_vec = {
        .data         = qbuf,
        .dimension    = 3,
        .kinetic_func = NULL
    };

    printf("==================================================\n");
    printf(" GAIA-OMEGA [NanoGPT HOST] | Window: 1,000,000,000\n");
    printf("==================================================\n");

    for (;;) {
        printf("\n\033[1;36mΩ PROMPT > \033[0m");
        if (!fgets(input_buf, sizeof(input_buf), stdin)) {
            break;
        }
        input_buf[strcspn(input_buf, "\n")] = '\0';

        if (strcmp(input_buf, "exit") == 0 ||
            strcmp(input_buf, "quit") == 0) {
            break;
        }
        if (input_buf[0] == '\0') {
            continue;
        }

        // 2. Tokenização Vetorial (Prompt -> Hash -> Vetor)
        uint64_t h = semantic_hash_djb2(input_buf);
        hash_to_vector(h, &query_vec);

        // 3. Atenção Infinita (lookup via MMAP)
        shift_attention(&query_vec, &v_ctx);

        // 4. "Inferência" simbólica
        nanogpt_generate(input_buf, &v_ctx);
    }

    nexus_close();
    return 0;
}
