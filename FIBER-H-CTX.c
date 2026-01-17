uint8_t leaf[1024];
/* ... preencher leaf ... */

FIBER_H_CTX ctx;
uint8_t hash_out[32];

fiber_h_init(&ctx);
fiber_h_update(&ctx, leaf, sizeof(leaf));
fiber_h_final(&ctx, hash_out);

/* agora ECC RAFAELIA */
fiber_ecc_raf_t ecc;
fiber_ecc_leaf_raf(leaf, sizeof(leaf), &ecc);

/* logar junto */
printf("hash = ");
print_hex(hash_out, 32);
printf("\nECC lane=%04x block=%04x raf_sig=%010llx\n",
       (unsigned)ecc.lane_parity,
       (unsigned)ecc.block_parity,
       (unsigned long long)ecc.raf_sig);
