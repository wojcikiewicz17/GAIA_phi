#ifndef FIBER_OPS_H
#define FIBER_OPS_H
/*
 * FIBER-H MICRO-OPS LAYER
 * ------------------------
 * Camada de micro-operações sobre lanes[6][32].
 *
 * Objetivos:
 *  - Nenhuma dependência de libc (sem strlen, time, rand, etc.).
 *  - Execução determinística, estável e reproduzível.
 *  - Preparar terreno para “linguagem de hiperforma” (ASCII -> operações).
 *
 * Normas (síntese conceitual):
 *  - ISO/IEC 25010: confiabilidade e manutenibilidade (código modular).
 *  - IEEE 830: interface clara (struct + função bem definidas).
 *  - NIST 800-53: comportamento previsível / auditável (LUT fixa).
 */

#include "fiber_hash.h"

/* Micro-op: interpretação de um byte (símbolo) como operação sobre lanes. */
typedef struct {
    fiber_u8 axis;   /* 0 = por lane; 1 = por coluna; 2/3 reservados p/ hiperformas */
    fiber_u8 op;     /* 0 = NOP; 1 = XOR; 2 = ROL; 3 = NOT; 4 = SWAP; 5 = reservado */
    fiber_u8 span;   /* tamanho da janela em bytes (0 => linha/coluna inteira) */
    fiber_u8 flags;  /* bit0=espelho, bit1=reverse, bits6-2 = seleção lane/coluna */
} fiber_op_t;

/* LUT de 256 entradas: cada byte vira um fiber_op_t. */
extern const fiber_op_t FIBER_OP_LUT[256];

/*
 * Aplica uma sequência de micro-ops (script) sobre lanes[6][32].
 *
 * - lanes      : matriz de estado [6 lanes][32 bytes].
 * - script     : bytes que definem as operações (ex.: texto, chave, token).
 * - script_len : tamanho do script em bytes.
 *
 * Não aloca memória, não chama libc, apenas mexe na matriz existente.
 */
void fiber_lanes6_apply_script(
    fiber_u8 lanes[6][32],
    const fiber_u8 *script,
    fiber_size_t script_len
);

#endif /* FIBER_OPS_H */
