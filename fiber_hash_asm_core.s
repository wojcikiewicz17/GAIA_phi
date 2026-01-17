.text
// fiber_hash_asm_core.s (AArch64)
// FIBER-H – 256-bit hash kernel (v1.1) - ASM compress core
// Target: Android 15 (Termux, aarch64)
// ABI: AArch64 ELF, AAPCS64
//
// void fiber_h_compress_asm_real(uint64_t *state, const uint8_t *block);
//   x0 = state (ptr to 4x u64: a,b,c,d)
//   x1 = block (ptr to 64-byte block)

.global fiber_h_compress_asm_real
.type   fiber_h_compress_asm_real, %function

fiber_h_compress_asm_real:
    // Load state: a,b,c,d -> x2,x3,x4,x5
    LDP     x2, x3, [x0]         // a = state[0], b = state[1]
    LDP     x4, x5, [x0, #16]    // c = state[2], d = state[3]

    // Load message: m0..m7 -> x6..x13 (little-endian na plataforma)
    LDP     x6,  x7,  [x1]       // m0, m1
    LDP     x8,  x9,  [x1, #16]  // m2, m3
    LDP     x10, x11, [x1, #32]  // m4, m5
    LDP     x12, x13, [x1, #48]  // m6, m7

    // ------------------------------------------------------------------
    // Round 0
    //   G(a,b,m0, rotl32, rotl24)
    //   G(c,d,m1, rotl16, rotl63)
    //   G(a,c,m2, rotl32, rotl24)
    //   G(b,d,m3, rotl16, rotl63)
    // ------------------------------------------------------------------

    // G(a,b,m0, rotl32, rotl24)
    ADD     x2, x2, x6           // a += m0
    EOR     x3, x3, x2           // b ^= a
    ROR     x3, x3, #32          // b = rotl32(b)  (rol32 == ror32)
    ADD     x2, x2, x3           // a += b
    ROR     x2, x2, #40          // a = rotl24(a)  (rol24 == ror40)

    // G(c,d,m1, rotl16, rotl63)
    ADD     x4, x4, x7           // c += m1
    EOR     x5, x5, x4           // d ^= c
    ROR     x5, x5, #48          // d = rotl16(d)  (rol16 == ror48)
    ADD     x4, x4, x5           // c += d
    ROR     x4, x4, #1           // c = rotl63(c)  (rol63 == ror1)

    // G(a,c,m2, rotl32, rotl24)
    ADD     x2, x2, x8           // a += m2
    EOR     x4, x4, x2           // c ^= a
    ROR     x4, x4, #32          // c = rotl32(c)
    ADD     x2, x2, x4           // a += c
    ROR     x2, x2, #40          // a = rotl24(a)

    // G(b,d,m3, rotl16, rotl63)
    ADD     x3, x3, x9           // b += m3
    EOR     x5, x5, x3           // d ^= b
    ROR     x5, x5, #48          // d = rotl16(d)
    ADD     x3, x3, x5           // b += d
    ROR     x3, x3, #1           // b = rotl63(b)

    // ------------------------------------------------------------------
    // Round 1
    //   G(a,b,m4, rotl32, rotl24)
    //   G(c,d,m5, rotl16, rotl63)
    //   G(a,c,m6, rotl32, rotl24)
    //   G(b,d,m7, rotl16, rotl63)
    // ------------------------------------------------------------------

    // G(a,b,m4, rotl32, rotl24)
    ADD     x2, x2, x10          // a += m4
    EOR     x3, x3, x2           // b ^= a
    ROR     x3, x3, #32          // b = rotl32(b)
    ADD     x2, x2, x3           // a += b
    ROR     x2, x2, #40          // a = rotl24(a)

    // G(c,d,m5, rotl16, rotl63)
    ADD     x4, x4, x11          // c += m5
    EOR     x5, x5, x4           // d ^= c
    ROR     x5, x5, #48          // d = rotl16(d)
    ADD     x4, x4, x5           // c += d
    ROR     x4, x4, #1           // c = rotl63(c)

    // G(a,c,m6, rotl32, rotl24)
    ADD     x2, x2, x12          // a += m6
    EOR     x4, x4, x2           // c ^= a
    ROR     x4, x4, #32          // c = rotl32(c)
    ADD     x2, x2, x4           // a += c
    ROR     x2, x2, #40          // a = rotl24(a)

    // G(b,d,m7, rotl16, rotl63)
    ADD     x3, x3, x13          // b += m7
    EOR     x5, x5, x3           // d ^= b
    ROR     x5, x5, #48          // d = rotl16(d)
    ADD     x3, x3, x5           // b += d
    ROR     x3, x3, #1           // b = rotl63(b)

    // ------------------------------------------------------------------
    // Feedforward: state[i] ^= new_state[i]
    // ------------------------------------------------------------------
    LDP     x14, x15, [x0]       // load original a,b
    LDP     x16, x17, [x0, #16]  // load original c,d

    EOR     x2, x2, x14          // a_new ^= a_old
    EOR     x3, x3, x15          // b_new ^= b_old
    EOR     x4, x4, x16          // c_new ^= c_old
    EOR     x5, x5, x17          // d_new ^= d_old

    // Store back
    STP     x2, x3, [x0]
    STP     x4, x5, [x0, #16]

    RET

.size fiber_h_compress_asm_real, .-fiber_h_compress_asm_real
