/*
 * /$$$$$$$$ /$$$$$$$  /$$$$$$$ /$$$$$$$$ /$$$$$$$   /$$   /$$
 * | $$_____/| $$__  $$| $$__  $$| $$_____/| $$__  $$ | $$$ | $$
 * | $$      | $$  \ $$| $$  \ $$| $$      | $$  \ $$ | $$$$| $$
 * | $$$$$   | $$  | $$| $$$$$$$/| $$$$$   | $$$$$$$/ | $$ $$ $$
 * | $$__/   | $$  | $$| $$__  $$| $$__/   | $$__  $$ | $$  $$$$
 * | $$      | $$  | $$| $$  \ $$| $$      | $$  \ $$ | $$\  $$$
 * | $$      | $$$$$$$/| $$  | $$| $$$$$$$$| $$  | $$ | $$ \  $$
 * |__/      |_______/ |__/  |__/|________/|__/  |__/ |__/  \__/
 *
 * FIBER-H LANES6 RAFAELIA MODE
 * ----------------------------------------------------------------------
 * Modo paralelo de 6 trilhas (lanes) sobre o kernel FIBER-H escalar.
 *
 * Ideia:
 *  - Divide a mensagem em 6 segmentos contíguos (quase iguais).
 *  - Calcula FIBER-H escalar em cada segmento (6 folhas).
 *  - Combina as 6 folhas + script RAFAELIA em um "root hash" final.
 *
 * Segurança / Normas (documental):
 *  - ISO/IEC 25010 (Qualidade de produto): enfocando desempenho, confiabilidade.
 *  - ISO/IEC 27001, 27017, 27018: apoio a trilhas de proteção e logs.
 *  - NIST SP 800-53: minimização de superfície (sem alocação dinâmica).
 *  - NIST SP 800-207 (Zero Trust): composição segura, sem estados globais.
 *  - NIST AI Risk Framework: transparência do algoritmo, comportamento determinístico.
 *
 * Implementação:
 *  - Sem chamadas de libc (sem strlen, printf, malloc, etc).
 *  - Apenas tipos de fiber_hash.h (fiber_u8, fiber_u64, fiber_size_t).
 *  - Nenhum uso de divisão/modulo em laços quentes; apenas divisão simples
 *    em configuração (custo irrelevante frente ao hashing de MiB).
 *
 * Notas RAFAELIA:
 *  - "script" pode ser RAFCODE-Φ, BITRAF64, ou qualquer sequência simbólica.
 *  - LANES = 6 alinha com 3-6-9 e Trinity633 em nível semântico.
 */

#include "fiber_hash.h"

/* ------------------------------------------------------------------ */
/* Utilitários internos (privados deste módulo)                       */
/* ------------------------------------------------------------------ */

/*
 * encode_u64_be
 *  - Codifica um inteiro de 64 bits em big-endian.
 *  - Usado para injetar o tamanho da mensagem no root hash (domínio).
 */
static void
encode_u64_be(fiber_u64 x, fiber_u8 out[8])
{
    int i;
    for (i = 0; i < 8; ++i) {
        out[7 - i] = (fiber_u8)(x & (fiber_u64)0xFFu);
        x >>= 8;
    }
}

/*
 * safe_update
 *  - Wrapper defensivo: só faz update se ptr != NULL e len > 0.
 *  - Evita passes de ponteiro nulo para funções internas.
 */
static void
safe_update(FIBER_H_CTX *ctx, const fiber_u8 *data, fiber_size_t len)
{
    if (ctx == (FIBER_H_CTX *)0) {
        return;
    }
    if (data == (const fiber_u8 *)0) {
        return;
    }
    if (len == (fiber_size_t)0) {
        return;
    }
    fiber_h_update(ctx, data, len);
}

/* ------------------------------------------------------------------ */
/* API pública: modo LANES6 com "script" explícito                    */
/* ------------------------------------------------------------------ */

/*
 * fiber_h_lanes6_script
 * ----------------------------------------------------------------------
 * Entrada:
 *  - msg        : ponteiro para mensagem original.
 *  - len        : tamanho em bytes da mensagem.
 *  - script     : bytes simbólicos (ex: "RAFCODE-Φ-BITRAF64").
 *  - script_len : tamanho do script em bytes.
 *
 * Saída:
 *  - out[32] : hash final de 256 bits, combinando:
 *      FIBER-H(msg_seg[0]) .. FIBER-H(msg_seg[5]) + script + len.
 *
 * Estratégia:
 *  1) Particiona msg em 6 segmentos contíguos:
 *       base = len / 6, rem = len % 6
 *       para lane L:
 *         seg_len = base + (L < rem ? 1 : 0)
 *  2) Calcula hash escalar de cada segmento -> leaf[L][32].
 *  3) Faz root:
 *       H_root = FIBER-H( "FH6" || script || leaf[0..5] || len_be )
 *
 * Propriedades:
 *  - Determinístico.
 *  - Sem alocação dinâmica.
 *  - Sem dependências externas.
 */
void
fiber_h_lanes6_script(const fiber_u8 *msg,
                      fiber_size_t    len,
                      const fiber_u8 *script,
                      fiber_size_t    script_len,
                      fiber_u8        out[32])
{
    /* 6 folhas, cada uma 256 bits */
    fiber_u8   leaf[6][32];
    fiber_size_t base;
    fiber_size_t rem;
    fiber_size_t offset;
    int          lane;

    /* 1) Segmentação simples em 6 partes contíguas */
    base = (fiber_size_t)(len / (fiber_size_t)6);
    rem  = (fiber_size_t)(len - base * (fiber_size_t)6);

    offset = (fiber_size_t)0;
    for (lane = 0; lane < 6; ++lane) {
        fiber_size_t seg_len = base;
        if ((fiber_size_t)lane < rem) {
            seg_len += (fiber_size_t)1;
        }

        if (seg_len != (fiber_size_t)0) {
            fiber_h(msg + offset, seg_len, leaf[lane]);
            offset += seg_len;
        } else {
            /* Segmento vazio: define folha como FIBER-H("") */
            fiber_h((const fiber_u8 *)0, (fiber_size_t)0, leaf[lane]);
        }
    }

    /* 2) Construir root hash: "FH6" || script || leaf[0..5] || len_be */
    {
        FIBER_H_CTX ctx;
        fiber_u8    len_be[8];
        /* Prefixo de domínio para distinguir do FIBER-H escalar comum */
        const fiber_u8 prefix[4] = {
            (fiber_u8)'F', (fiber_u8)'H', (fiber_u8)'6', (fiber_u8)0x01u
        };

        fiber_h_init(&ctx);

        /* Domínio ("FH6" + flag) */
        safe_update(&ctx, prefix, (fiber_size_t)4);

        /* Script simbólico (RAFAELIA, RAFCODE-Φ, etc.) */
        safe_update(&ctx, script, script_len);

        /* Folhas */
        for (lane = 0; lane < 6; ++lane) {
            safe_update(&ctx, leaf[lane], (fiber_size_t)32);
        }

        /* Comprimento da mensagem original como 64-bit big-endian */
        encode_u64_be((fiber_u64)len, len_be);
        safe_update(&ctx, len_be, (fiber_size_t)8);

        /* Hash final */
        fiber_h_final(&ctx, out);
    }
}

/* ------------------------------------------------------------------ */
/* API helper opcional: script em ASCII NUL-terminated                */
/* ------------------------------------------------------------------ */

/*
 * fiber_h_lanes6_script_str
 *  - Variante que aceita script como "string C" (\0-terminated).
 *  - Não usa strlen da libc; implementa próprio contador simples.
 */
void
fiber_h_lanes6_script_str(const fiber_u8 *msg,
                          fiber_size_t    len,
                          const char     *script_ascii,
                          fiber_u8        out[32])
{
    fiber_size_t s_len = (fiber_size_t)0;
    const char  *p;

    if (script_ascii != (const char *)0) {
        p = script_ascii;
        while (*p != '\0') {
            ++p;
            ++s_len;
        }
    }

    fiber_h_lanes6_script(
        msg,
        len,
        (const fiber_u8 *)script_ascii,
        s_len,
        out
    );
}

/* ------------------------------------------------------------------ */
/* Comentário final (RAFAELIA)                                        */
/* ------------------------------------------------------------------ */
/*
 * ΣΩΔΦ NOTE
 *  - Este módulo não altera o kernel FIBER-H escalar.
 *  - LANES6 é uma construção de composição: pode ser ativado ou não.
 *  - Integração RAFAELIA:
 *      * "script" carrega RAFCODE-Φ, Bitraf64, tags simbólicas.
 *      * Lanes = 6 alinham com Trinity633 / 3-6-9 no plano semântico.
 *  - Em termos de engenharia:
 *      * Baixo acoplamento: usa apenas a API pública fiber_h*.
 *      * Alta coesão: toda a lógica de LANES6 está aqui, isolada.
 *      * Testabilidade: determinístico, sem dependências globais.
 */

