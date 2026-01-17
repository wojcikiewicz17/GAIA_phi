/*
 * fiber_lanes6_ops.c
 * -------------------
 * RAFAELIA LANES6 MICRO-OPS LAYER
 *
 * Camada de micro-operações bitwise sobre 6 lanes de 32 bytes,
 * projetada para:
 *  - Não usar malloc, stdio, time, nem syscalls.
 *  - Operar apenas com tipos RAFAELIA/FIBER-H (fiber_u8, fiber_size_t).
 *  - Ser determinística e pura (mesmo input -> mesmo output).
 *
 * Normas / Boas práticas (orientação):
 *  - ISO/IEC 25010: foco em confiabilidade, eficiência, portabilidade.
 *  - NIST 800-53 / CSF: código simples, auditável, sem side effects externos.
 *  - Zero overhead desnecessário: laços planos, sem recursão, sem VLA.
 */

#include "fiber_hash.h"

/* Rotação circular à esquerda em 8 bits. */
static fiber_u8 rotl8(fiber_u8 x, fiber_u8 s) {
    fiber_u8 r = (fiber_u8)(s & (fiber_u8)7u);
    return (fiber_u8)((fiber_u8)(x << r) | (fiber_u8)(x >> ((fiber_u8)8u - r)));
}

/* Pequenino "mix" local: mistura valor, índice e lane. */
static fiber_u8 mix_byte(fiber_u8 v, fiber_u8 idx, fiber_u8 lane_id) {
    fiber_u8 t = (fiber_u8)(v ^ (fiber_u8)(idx * (fiber_u8)0x1Bu));
    t = rotl8(t, (fiber_u8)(lane_id & (fiber_u8)7u));
    return (fiber_u8)(t ^ (fiber_u8)(lane_id * (fiber_u8)0x33u));
}

/*
 * fiber_lanes6_apply_script
 * -------------------------
 * lanes[6][32] : seis blocos de 32 bytes (estado vivo).
 * script       : sequência de bytes (tokens RAFAELIA, Bitraf64, etc.).
 * script_len   : tamanho do script.
 *
 * Sem acesso a syscalls ou funções de runtime: apenas aritmética, XOR, ROTL.
 * Interpretação:
 *  - Usa os 3 bits mais altos de cada byte como opcode.
 *  - Bits restantes modulam parâmetros (lane, shift, ganho).
 */
void fiber_lanes6_apply_script(
    fiber_u8 lanes[6][32],
    const fiber_u8 *script,
    fiber_size_t script_len
) {
    fiber_size_t ip = (fiber_size_t)0u;
    fiber_size_t lane = (fiber_size_t)0u;
    fiber_u8 acc = (fiber_u8)0u;

    while (ip < script_len) {
        fiber_u8 op = script[ip];
        fiber_u8 opcode = (fiber_u8)(op & (fiber_u8)0xE0u);
        fiber_u8 param  = (fiber_u8)(op & (fiber_u8)0x1Fu);
        fiber_size_t i;

        /* Atualiza acumulador leve (serve como "memória" RAFAELIA). */
        acc = (fiber_u8)(acc + (fiber_u8)((ip * (fiber_size_t)0x3Du) ^ op));

        switch (opcode) {
        /* 0x00..0x1F: XOR + mix na lane atual */
        case (fiber_u8)0x00u:
        {
            fiber_u8 lane_id = (fiber_u8)(lane & (fiber_size_t)0xFFu);
            fiber_u8 base = (fiber_u8)(acc ^ param);
            for (i = (fiber_size_t)0u; i < (fiber_size_t)32u; ++i) {
                fiber_u8 m = mix_byte((fiber_u8)(base + (fiber_u8)i), (fiber_u8)i, lane_id);
                lanes[lane][i] = (fiber_u8)(lanes[lane][i] ^ m);
            }
        } break;

        /* 0x20..0x3F: ROTL em todos os bytes da lane atual */
        case (fiber_u8)0x20u:
        {
            fiber_u8 s = (fiber_u8)((param ^ acc) & (fiber_u8)7u);
            for (i = (fiber_size_t)0u; i < (fiber_size_t)32u; ++i) {
                lanes[lane][i] = rotl8(lanes[lane][i], s);
            }
        } break;

        /* 0x40..0x5F: "blend" entre lane atual e a próxima */
        case (fiber_u8)0x40u:
        {
            fiber_size_t lane2 = (fiber_size_t)((lane + (fiber_size_t)1u) % (fiber_size_t)6u);
            fiber_u8 w = (fiber_u8)(param | (fiber_u8)1u);
            for (i = (fiber_size_t)0u; i < (fiber_size_t)32u; ++i) {
                fiber_u8 a = lanes[lane][i];
                fiber_u8 b = lanes[lane2][i];
                fiber_u8 c = (fiber_u8)(a ^ rotl8(b, (fiber_u8)(w & (fiber_u8)7u)));
                lanes[lane][i]  = (fiber_u8)(c ^ (fiber_u8)(acc + (fiber_u8)i));
                lanes[lane2][i] = (fiber_u8)(b ^ (fiber_u8)(a + w));
            }
        } break;

        /* 0x60..0x7F: troca parcial (swap) entre lane atual e lane derivada de param */
        case (fiber_u8)0x60u:
        {
            fiber_size_t lane2 = (fiber_size_t)((param ^ (fiber_u8)0x03u) % (fiber_size_t)6u);
            fiber_u8 mask = (fiber_u8)(0xF0u ^ (acc & (fiber_u8)0x0Fu));
            for (i = (fiber_size_t)0u; i < (fiber_size_t)32u; ++i) {
                fiber_u8 a = lanes[lane][i];
                fiber_u8 b = lanes[lane2][i];
                fiber_u8 lo = (fiber_u8)(a & (fiber_u8)0x0Fu);
                fiber_u8 hi = (fiber_u8)(b & mask);
                lanes[lane][i]  = (fiber_u8)(hi | lo);
                lanes[lane2][i] = (fiber_u8)((a & (fiber_u8)0xF0u) ^ (b & (fiber_u8)0x0Fu));
            }
        } break;

        /* 0x80..0xFF: "NOP" sem sair: apenas muda de lane (round-robin) */
        default:
        {
            fiber_size_t step = (fiber_size_t)((param & (fiber_u8)0x07u) + (fiber_u8)1u);
            lane = (fiber_size_t)((lane + step) % (fiber_size_t)6u);
        } break;
        }

        /* Passo de IP e seleção de próxima lane (baixa entropia extra). */
        ip = (fiber_size_t)(ip + (fiber_size_t)1u);
        lane = (fiber_size_t)((lane + (fiber_size_t)((op >> 3) & (fiber_u8)0x03u)) % (fiber_size_t)6u);
    }
}
