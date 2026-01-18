#!/bin/bash
# =============================================================================
# RAFAELIA_EVENT_LOG: Log de Eventos Encadeado (Imutável + Auditável)
# =============================================================================

BASE_DIR=${BASE_DIR:-$(pwd)/gaia_omega_build}
mkdir -p "$BASE_DIR"
cd "$BASE_DIR" || exit 1

mkdir -p headers
mkdir -p core

echo "[INIT] Construindo RAFAELIA_EVENT_LOG em $BASE_DIR..."

# =============================================================================
# 1. HEADER: raf_event_log.h
# =============================================================================

cat << 'HDR' > headers/raf_event_log.h
#ifndef RAF_EVENT_LOG_H
#define RAF_EVENT_LOG_H

#include <stdint.h>

// Formato de linha no log (texto):
// seq|timestamp|actor|etype|prev_hash_hex|this_hash_hex|payload
//
// - seq           : uint64 (contador crescente, 0,1,2,...)
// - timestamp     : epoch (segundos)
// - actor         : id do agente (ex: 1 = sistema, 2 = Rafael, etc.)
// - etype         : tipo de evento (ex: 1 = SNAPSHOT, 2 = MUTACAO, etc.)
// - prev_hash_hex : this_hash_hex da linha anterior, ou 000...0 no primeiro
// - this_hash_hex : hash de todos os campos (exceto ele mesmo)
// - payload       : texto livre (sem '|'), resumo ou caminho do que aconteceu
//
// Se qualquer bit for alterado em qualquer lugar da cadeia,
// a verificação falha.

int raf_append_event(
    const char* log_path,
    uint32_t actor,
    uint32_t etype,
    const char* payload
);

int raf_verify_log(const char* log_path);

#endif
HDR

# =============================================================================
# 2. IMPLEMENTAÇÃO: core/raf_event_log.c
# =============================================================================

cat << 'SRC' > core/raf_event_log.c
#include "../headers/raf_event_log.h"
#include "../headers/omega_hash.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <errno.h>

#define RAF_MAX_LINE 4096

// Converte uint64 para string hex de 16 chars (sem 0x, sempre 16 dígitos)
static void u64_to_hex16(uint64_t x, char out[17]) {
    static const char* hexd = "0123456789abcdef";
    for (int i = 15; i >= 0; i--) {
        out[i] = hexd[x & 0xF];
        x >>= 4;
    }
    out[16] = '\0';
}

// Converte string hex de 16 chars para uint64
static int hex16_to_u64(const char* s, uint64_t* out) {
    uint64_t v = 0;
    for (int i = 0; i < 16; i++) {
        char c = s[i];
        uint8_t d;
        if (c >= '0' && c <= '9') d = (uint8_t)(c - '0');
        else if (c >= 'a' && c <= 'f') d = (uint8_t)(c - 'a' + 10);
        else if (c >= 'A' && c <= 'F') d = (uint8_t)(c - 'A' + 10);
        else return -1;
        v = (v << 4) | d;
    }
    *out = v;
    return 0;
}

// Lê a última linha do log (se existir) e retorna:
//  - last_seq, last_hash
// Se o arquivo não existir ou estiver vazio, retorna seq = -1, hash = 0.
static int raf_get_last(const char* log_path, int64_t* last_seq, uint64_t* last_hash) {
    *last_seq  = -1;
    *last_hash = 0;

    FILE* f = fopen(log_path, "r");
    if (!f) {
        // Se arquivo não existe ainda, isso não é erro
        if (errno == ENOENT) return 0;
        return -1;
    }

    char line[RAF_MAX_LINE];
    char last_line[RAF_MAX_LINE];
    last_line[0] = '\0';

    while (fgets(line, sizeof(line), f)) {
        if (line[0] == '\n' || line[0] == '\0') continue;
        strncpy(last_line, line, sizeof(last_line) - 1);
        last_line[sizeof(last_line) - 1] = '\0';
    }
    fclose(f);

    if (last_line[0] == '\0') {
        // arquivo vazio
        return 0;
    }

    // Espera formato:
    // seq|timestamp|actor|etype|prev_hash_hex|this_hash_hex|payload
    char* saveptr = NULL;
    char* tok = NULL;
    char* fields[7];
    int idx = 0;

    tok = strtok_r(last_line, "|\n", &saveptr);
    while (tok && idx < 7) {
        fields[idx++] = tok;
        tok = strtok_r(NULL, "|\n", &saveptr);
    }
    if (idx < 6) {
        // linha mal-formada
        return -1;
    }

    // seq
    *last_seq = strtoll(fields[0], NULL, 10);

    // this_hash_hex em fields[5]
    uint64_t h = 0;
    if (hex16_to_u64(fields[5], &h) != 0) {
        return -1;
    }
    *last_hash = h;
    return 0;
}

// Computa o hash do evento: usa omega_hash() em uma string canônica
// Formato canônico:
// "seq|timestamp|actor|etype|prev_hash_hex|payload"
static uint64_t raf_compute_hash(
    uint64_t seq,
    uint64_t ts,
    uint32_t actor,
    uint32_t etype,
    const char* prev_hash_hex,
    const char* payload
) {
    char buf[RAF_MAX_LINE * 2];
    snprintf(
        buf,
        sizeof(buf),
        "%llu|%llu|%u|%u|%s|%s",
        (unsigned long long)seq,
        (unsigned long long)ts,
        actor,
        etype,
        prev_hash_hex,
        payload ? payload : ""
    );
    return omega_hash(buf);
}

// Append de evento encadeado no log
int raf_append_event(
    const char* log_path,
    uint32_t actor,
    uint32_t etype,
    const char* payload
) {
    if (!log_path) return -1;

    int64_t last_seq = -1;
    uint64_t last_hash = 0;

    if (raf_get_last(log_path, &last_seq, &last_hash) != 0) {
        fprintf(stderr, "[RAF_LOG] Erro ao ler último evento de '%s'\n", log_path);
        return -1;
    }

    uint64_t seq = (last_seq < 0) ? 0u : (uint64_t)(last_seq + 1);

    time_t now = time(NULL);
    uint64_t ts = (uint64_t)now;

    char prev_hex[17];
    if (last_seq < 0) {
        // Primeiro evento usa 0 como prev_hash
        memset(prev_hex, '0', 16);
        prev_hex[16] = '\0';
    } else {
        u64_to_hex16(last_hash, prev_hex);
    }

    if (!payload) payload = "";

    uint64_t this_hash = raf_compute_hash(seq, ts, actor, etype, prev_hex, payload);

    char this_hex[17];
    u64_to_hex16(this_hash, this_hex);

    FILE* f = fopen(log_path, "a");
    if (!f) {
        fprintf(stderr, "[RAF_LOG] Não foi possível abrir '%s' para append.\n", log_path);
        return -1;
    }

    fprintf(
        f,
        "%llu|%llu|%u|%u|%s|%s|%s\n",
        (unsigned long long)seq,
        (unsigned long long)ts,
        actor,
        etype,
        prev_hex,
        this_hex,
        payload
    );
    fclose(f);

    return 0;
}

// Verifica TODO o log:
//  - seq incremental
//  - prev_hash bate com this_hash anterior
//  - this_hash bate com recálculo
int raf_verify_log(const char* log_path) {
    if (!log_path) return -1;

    FILE* f = fopen(log_path, "r");
    if (!f) {
        if (errno == ENOENT) {
            printf("[RAF_LOG] Arquivo '%s' não existe. Nada a verificar.\n", log_path);
            return 0;
        }
        fprintf(stderr, "[RAF_LOG] Erro ao abrir '%s' para leitura.\n", log_path);
        return -1;
    }

    char line[RAF_MAX_LINE];
    uint64_t expected_seq = 0;
    uint64_t last_hash = 0;
    int line_num = 0;
    int has_any = 0;

    while (fgets(line, sizeof(line), f)) {
        line_num++;
        if (line[0] == '\n' || line[0] == '\0') continue;

        has_any = 1;

        char backup[RAF_MAX_LINE];
        strncpy(backup, line, sizeof(backup) - 1);
        backup[sizeof(backup) - 1] = '\0';

        char* saveptr = NULL;
        char* fields[7];
        int idx = 0;
        char* tok = strtok_r(backup, "|\n", &saveptr);
        while (tok && idx < 7) {
            fields[idx++] = tok;
            tok = strtok_r(NULL, "|\n", &saveptr);
        }
        if (idx < 6) {
            fprintf(stderr, "[RAF_LOG] Linha %d mal-formada.\n", line_num);
            fclose(f);
            return -1;
        }

        uint64_t seq = strtoull(fields[0], NULL, 10);
        uint64_t ts  = strtoull(fields[1], NULL, 10);
        uint32_t actor = (uint32_t)strtoul(fields[2], NULL, 10);
        uint32_t etype = (uint32_t)strtoul(fields[3], NULL, 10);
        const char* prev_hex = fields[4];
        const char* this_hex = fields[5];
        const char* payload  = (idx >= 7) ? fields[6] : "";

        // seq deve ser incremental
        if (seq != expected_seq) {
            fprintf(stderr,
                "[RAF_LOG] Quebra na sequência na linha %d: esperado seq=%llu, encontrado=%llu.\n",
                line_num,
                (unsigned long long)expected_seq,
                (unsigned long long)seq
            );
            fclose(f);
            return -1;
        }

        // prev_hash deve bater com last_hash
        uint64_t prev_h = 0;
        if (hex16_to_u64(prev_hex, &prev_h) != 0) {
            fprintf(stderr, "[RAF_LOG] prev_hash inválido na linha %d.\n", line_num);
            fclose(f);
            return -1;
        }

        if (expected_seq == 0) {
            // primeiro evento: prev_hash deve ser 0
            if (prev_h != 0) {
                fprintf(stderr, "[RAF_LOG] prev_hash do primeiro evento não é 0 na linha %d.\n", line_num);
                fclose(f);
                return -1;
            }
        } else {
            if (prev_h != last_hash) {
                fprintf(stderr,
                    "[RAF_LOG] Encadeamento quebrado na linha %d: prev_hash != this_hash anterior.\n",
                    line_num
                );
                fclose(f);
                return -1;
            }
        }

        // this_hash deve bater com recálculo
        uint64_t this_h_stored = 0;
        if (hex16_to_u64(this_hex, &this_h_stored) != 0) {
            fprintf(stderr, "[RAF_LOG] this_hash inválido na linha %d.\n", line_num);
            fclose(f);
            return -1;
        }

        uint64_t this_h_calc = raf_compute_hash(seq, ts, actor, etype, prev_hex, payload);
        if (this_h_calc != this_h_stored) {
            fprintf(stderr,
                "[RAF_LOG] Hash inválido na linha %d: esperado=%016llx, encontrado=%016llx.\n",
                line_num,
                (unsigned long long)this_h_calc,
                (unsigned long long)this_h_stored
            );
            fclose(f);
            return -1;
        }

        last_hash = this_h_stored;
        expected_seq++;
    }

    fclose(f);

    if (!has_any) {
        printf("[RAF_LOG] '%s' está vazio, mas consistente.\n", log_path);
        return 0;
    }

    printf("[RAF_LOG] Verificação OK. Eventos totais: %llu\n",
           (unsigned long long)expected_seq);
    return 0;
}
SRC

# =============================================================================
# 3. BINÁRIOS: raf_event_append.c e raf_event_verify.c
# =============================================================================

cat << 'SRC' > raf_event_append.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "headers/raf_event_log.h"

// Uso:
//   ./raf_event_append <log_path> <actor_id> <etype> "payload"
int main(int argc, char** argv) {
    if (argc < 5) {
        fprintf(stderr,
            "Uso: %s <log_path> <actor_id> <etype> \"payload\"\n"
            "Exemplo: %s raf_events.log 1 100 \"SNAPSHOT RAFAELIA_DB_FINAL_33.zipraf\"\n",
            argv[0], argv[0]);
        return 1;
    }

    const char* log_path = argv[1];
    uint32_t actor = (uint32_t)strtoul(argv[2], NULL, 10);
    uint32_t etype = (uint32_t)strtoul(argv[3], NULL, 10);
    const char* payload = argv[4];

    if (strchr(payload, '|') != NULL) {
        fprintf(stderr, "[RAF_LOG] Payload não pode conter '|'.\n");
        return 1;
    }

    int r = raf_append_event(log_path, actor, etype, payload);
    if (r != 0) {
        fprintf(stderr, "[RAF_LOG] Falha ao append de evento.\n");
        return 1;
    }

    printf("[RAF_LOG] Evento anexado em '%s'.\n", log_path);
    return 0;
}
SRC

cat << 'SRC' > raf_event_verify.c
#include <stdio.h>
#include <stdlib.h>
#include "headers/raf_event_log.h"

// Uso:
//   ./raf_event_verify <log_path>
int main(int argc, char** argv) {
    if (argc < 2) {
        fprintf(stderr,
            "Uso: %s <log_path>\n"
            "Exemplo: %s raf_events.log\n",
            argv[0], argv[0]);
        return 1;
    }

    const char* log_path = argv[1];
    int r = raf_verify_log(log_path);
    if (r != 0) {
        fprintf(stderr, "[RAF_LOG] Verificação FALHOU.\n");
        return 1;
    }
    return 0;
}
SRC

# =============================================================================
# 4. COMPILAÇÃO
# =============================================================================

echo "[BUILD] Compilando RAFAELIA_EVENT_LOG..."

gcc -O3 raf_event_append.c core/raf_event_log.c core/semantic_hash.c -o raf_event_append -lm
gcc -O3 raf_event_verify.c core/raf_event_log.c core/semantic_hash.c -o raf_event_verify -lm

chmod +x raf_event_append raf_event_verify

echo "=================================================="
echo " RAFAELIA_EVENT_LOG INSTALADO "
echo "=================================================="
echo "1. Anexar evento:"
echo "   ./raf_event_append raf_events.log 1 100 \"SNAPSHOT RAFAELIA_DB_FINAL_33.zipraf\""
echo ""
echo "2. Verificar integridade total do log:"
echo "   ./raf_event_verify raf_events.log"
echo ""
echo "Mexeu 1 bit -> cadeia quebra -> verificação acusa."
echo "=================================================="
