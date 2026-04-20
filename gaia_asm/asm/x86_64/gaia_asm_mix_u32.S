.text
.global gaia_asm_mix_u32
.type gaia_asm_mix_u32, @function
gaia_asm_mix_u32:
    movl %edi, %eax
    xorl %esi, %eax
    roll $5, %eax
    addl %edx, %eax
    xorl $0x9e3779b9, %eax
    ret
.size gaia_asm_mix_u32, .-gaia_asm_mix_u32
.section .note.GNU-stack,"",@progbits
