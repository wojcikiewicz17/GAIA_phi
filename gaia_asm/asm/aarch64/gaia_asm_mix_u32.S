.text
.global gaia_asm_mix_u32
.type gaia_asm_mix_u32, %function
gaia_asm_mix_u32:
    eor w0, w0, w1
    ror w0, w0, #27
    add w0, w0, w2
    mov w3, #0x79b9
    movk w3, #0x9e37, lsl #16
    eor w0, w0, w3
    ret
.size gaia_asm_mix_u32, .-gaia_asm_mix_u32
