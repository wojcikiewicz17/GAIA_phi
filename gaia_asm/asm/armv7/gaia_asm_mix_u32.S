.syntax unified
.text
.global gaia_asm_mix_u32
.type gaia_asm_mix_u32, %function
gaia_asm_mix_u32:
    eor r0, r0, r1
    ror r0, r0, #27
    add r0, r0, r2
    ldr r3, =0x9e3779b9
    eor r0, r0, r3
    bx lr
.size gaia_asm_mix_u32, .-gaia_asm_mix_u32
