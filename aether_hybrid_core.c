#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define OFFSET 0xCBF29CE484222325ULL
#define PRIME  0x100000001B3ULL
#define GOLDEN 0x9E3779B97F4A7C15ULL
#define MASK64 0xFFFFFFFFFFFFFFFFULL

static uint64_t rotl64(uint64_t x, uint64_t r) {
    r &= 63u;
    return ((x << r) & MASK64) | (x >> (64u - r));
}

static uint64_t aether_update(uint64_t state, const unsigned char *data, size_t len) {
    uint64_t h = state;
    size_t n_blocks = len / 8;
    for (size_t i = 0; i < n_blocks; i++) {
        uint64_t k = 0;
        memcpy(&k, data + i * 8, 8);
        h ^= k;
        h = (h * PRIME) & MASK64;
        h = rotl64(h, 31);
        h ^= (h >> 33);
    }
    for (size_t i = n_blocks * 8; i < len; i++) {
        h ^= data[i];
        h = (h * PRIME) & MASK64;
    }
    return h;
}

static void hex64(uint64_t v, char out[17]) {
    static const char* hexd = "0123456789abcdef";
    for (int i = 15; i >= 0; i--) {
        out[i] = hexd[v & 0xF];
        v >>= 4;
    }
    out[16] = '\0';
}

// ---- minimal SHA-256 (public domain style) ----
typedef struct {
    uint32_t state[8];
    uint64_t bitlen;
    unsigned char data[64];
    size_t datalen;
} sha256_ctx;

static uint32_t rotr32(uint32_t x, uint32_t r) {
    return (x >> r) | (x << (32 - r));
}

static void sha256_transform(sha256_ctx *ctx, const unsigned char data[64]) {
    static const uint32_t k[64] = {
        0x428a2f98u, 0x71374491u, 0xb5c0fbcfu, 0xe9b5dba5u,
        0x3956c25bu, 0x59f111f1u, 0x923f82a4u, 0xab1c5ed5u,
        0xd807aa98u, 0x12835b01u, 0x243185beu, 0x550c7dc3u,
        0x72be5d74u, 0x80deb1feu, 0x9bdc06a7u, 0xc19bf174u,
        0xe49b69c1u, 0xefbe4786u, 0x0fc19dc6u, 0x240ca1ccu,
        0x2de92c6fu, 0x4a7484aau, 0x5cb0a9dcu, 0x76f988dau,
        0x983e5152u, 0xa831c66du, 0xb00327c8u, 0xbf597fc7u,
        0xc6e00bf3u, 0xd5a79147u, 0x06ca6351u, 0x14292967u,
        0x27b70a85u, 0x2e1b2138u, 0x4d2c6dfcu, 0x53380d13u,
        0x650a7354u, 0x766a0abbu, 0x81c2c92eu, 0x92722c85u,
        0xa2bfe8a1u, 0xa81a664bu, 0xc24b8b70u, 0xc76c51a3u,
        0xd192e819u, 0xd6990624u, 0xf40e3585u, 0x106aa070u,
        0x19a4c116u, 0x1e376c08u, 0x2748774cu, 0x34b0bcb5u,
        0x391c0cb3u, 0x4ed8aa4au, 0x5b9cca4fu, 0x682e6ff3u,
        0x748f82eeu, 0x78a5636fu, 0x84c87814u, 0x8cc70208u,
        0x90befffau, 0xa4506cebu, 0xbef9a3f7u, 0xc67178f2u
    };
    uint32_t w[64];
    for (int i = 0; i < 16; i++) {
        w[i] = ((uint32_t)data[i * 4] << 24) |
               ((uint32_t)data[i * 4 + 1] << 16) |
               ((uint32_t)data[i * 4 + 2] << 8) |
               ((uint32_t)data[i * 4 + 3]);
    }
    for (int i = 16; i < 64; i++) {
        uint32_t s0 = rotr32(w[i - 15], 7) ^ rotr32(w[i - 15], 18) ^ (w[i - 15] >> 3);
        uint32_t s1 = rotr32(w[i - 2], 17) ^ rotr32(w[i - 2], 19) ^ (w[i - 2] >> 10);
        w[i] = w[i - 16] + s0 + w[i - 7] + s1;
    }

    uint32_t a = ctx->state[0];
    uint32_t b = ctx->state[1];
    uint32_t c = ctx->state[2];
    uint32_t d = ctx->state[3];
    uint32_t e = ctx->state[4];
    uint32_t f = ctx->state[5];
    uint32_t g = ctx->state[6];
    uint32_t h = ctx->state[7];

    for (int i = 0; i < 64; i++) {
        uint32_t S1 = rotr32(e, 6) ^ rotr32(e, 11) ^ rotr32(e, 25);
        uint32_t ch = (e & f) ^ ((~e) & g);
        uint32_t temp1 = h + S1 + ch + k[i] + w[i];
        uint32_t S0 = rotr32(a, 2) ^ rotr32(a, 13) ^ rotr32(a, 22);
        uint32_t maj = (a & b) ^ (a & c) ^ (b & c);
        uint32_t temp2 = S0 + maj;

        h = g;
        g = f;
        f = e;
        e = d + temp1;
        d = c;
        c = b;
        b = a;
        a = temp1 + temp2;
    }

    ctx->state[0] += a;
    ctx->state[1] += b;
    ctx->state[2] += c;
    ctx->state[3] += d;
    ctx->state[4] += e;
    ctx->state[5] += f;
    ctx->state[6] += g;
    ctx->state[7] += h;
}

static void sha256_init(sha256_ctx *ctx) {
    ctx->datalen = 0;
    ctx->bitlen = 0;
    ctx->state[0] = 0x6a09e667u;
    ctx->state[1] = 0xbb67ae85u;
    ctx->state[2] = 0x3c6ef372u;
    ctx->state[3] = 0xa54ff53au;
    ctx->state[4] = 0x510e527fu;
    ctx->state[5] = 0x9b05688cu;
    ctx->state[6] = 0x1f83d9abu;
    ctx->state[7] = 0x5be0cd19u;
}

static void sha256_update(sha256_ctx *ctx, const unsigned char *data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        ctx->data[ctx->datalen++] = data[i];
        if (ctx->datalen == 64) {
            sha256_transform(ctx, ctx->data);
            ctx->bitlen += 512;
            ctx->datalen = 0;
        }
    }
}

static void sha256_final(sha256_ctx *ctx, unsigned char hash[32]) {
    size_t i = ctx->datalen;

    if (ctx->datalen < 56) {
        ctx->data[i++] = 0x80;
        while (i < 56) ctx->data[i++] = 0x00;
    } else {
        ctx->data[i++] = 0x80;
        while (i < 64) ctx->data[i++] = 0x00;
        sha256_transform(ctx, ctx->data);
        memset(ctx->data, 0, 56);
    }

    ctx->bitlen += ctx->datalen * 8;
    ctx->data[63] = (unsigned char)(ctx->bitlen);
    ctx->data[62] = (unsigned char)(ctx->bitlen >> 8);
    ctx->data[61] = (unsigned char)(ctx->bitlen >> 16);
    ctx->data[60] = (unsigned char)(ctx->bitlen >> 24);
    ctx->data[59] = (unsigned char)(ctx->bitlen >> 32);
    ctx->data[58] = (unsigned char)(ctx->bitlen >> 40);
    ctx->data[57] = (unsigned char)(ctx->bitlen >> 48);
    ctx->data[56] = (unsigned char)(ctx->bitlen >> 56);
    sha256_transform(ctx, ctx->data);

    for (i = 0; i < 4; i++) {
        hash[i]      = (unsigned char)((ctx->state[0] >> (24 - i * 8)) & 0xFF);
        hash[i + 4]  = (unsigned char)((ctx->state[1] >> (24 - i * 8)) & 0xFF);
        hash[i + 8]  = (unsigned char)((ctx->state[2] >> (24 - i * 8)) & 0xFF);
        hash[i + 12] = (unsigned char)((ctx->state[3] >> (24 - i * 8)) & 0xFF);
        hash[i + 16] = (unsigned char)((ctx->state[4] >> (24 - i * 8)) & 0xFF);
        hash[i + 20] = (unsigned char)((ctx->state[5] >> (24 - i * 8)) & 0xFF);
        hash[i + 24] = (unsigned char)((ctx->state[6] >> (24 - i * 8)) & 0xFF);
        hash[i + 28] = (unsigned char)((ctx->state[7] >> (24 - i * 8)) & 0xFF);
    }
}

static void print_hex_bytes(const unsigned char *buf, size_t len) {
    for (size_t i = 0; i < len; i++) {
        printf("%02x", buf[i]);
    }
}

static int hash_stream_aether(FILE *f, int width_bits, int formatted) {
    int passes = width_bits / 64;
    if (passes < 1) passes = 1;
    if (passes > 16) passes = 16;

    uint64_t states[16];
    for (int i = 0; i < passes; i++) {
        uint64_t seed = (uint64_t)i * GOLDEN;
        states[i] = OFFSET ^ seed;
    }

    unsigned char buf[4 * 1024 * 1024];
    size_t total = 0;
    clock_t t0 = clock();
    size_t nread;
    while ((nread = fread(buf, 1, sizeof(buf), f)) > 0) {
        total += nread;
        for (int i = 0; i < passes; i++) {
            states[i] = aether_update(states[i], buf, nread);
        }
    }
    clock_t t1 = clock();
    double elapsed = (double)(t1 - t0) / (double)CLOCKS_PER_SEC;
    if (elapsed <= 0.0) elapsed = 1e-9;

    if (formatted) {
        printf("Engine     : AETHER_C\n");
        printf("Width      : %d bits\n", passes * 64);
        printf("Bytes      : %zu\n", total);
        printf("Time (s)   : %.6f\n", elapsed);
        printf("Speed      : %.2f MB/s\n", (total / (1024.0 * 1024.0)) / elapsed);
        printf("Hex digest : ");
    }

    for (int i = 0; i < passes; i++) {
        char hex[17];
        hex64(states[i], hex);
        printf("%s", hex);
    }
    printf("\n");

    return 0;
}

static int hash_stream_sha256(FILE *f, int formatted) {
    unsigned char buf[4 * 1024 * 1024];
    size_t total = 0;
    clock_t t0 = clock();
    sha256_ctx ctx;
    sha256_init(&ctx);
    size_t nread;
    while ((nread = fread(buf, 1, sizeof(buf), f)) > 0) {
        total += nread;
        sha256_update(&ctx, buf, nread);
    }
    unsigned char hash[32];
    sha256_final(&ctx, hash);
    clock_t t1 = clock();
    double elapsed = (double)(t1 - t0) / (double)CLOCKS_PER_SEC;
    if (elapsed <= 0.0) elapsed = 1e-9;

    if (formatted) {
        printf("Engine     : IRON_SHA256\n");
        printf("Width      : 256 bits\n");
        printf("Bytes      : %zu\n", total);
        printf("Time (s)   : %.6f\n", elapsed);
        printf("Speed      : %.2f MB/s\n", (total / (1024.0 * 1024.0)) / elapsed);
        printf("Hex digest : ");
    }

    print_hex_bytes(hash, sizeof(hash));
    printf("\n");
    return 0;
}

static void usage(const char *prog) {
    fprintf(stderr, "Uso: %s <arquivo|texto> [-e aether|iron] [-w WIDTH] [-f]\n", prog);
}

int main(int argc, char **argv) {
    if (argc < 2) {
        usage(argv[0]);
        return 1;
    }

    const char *target = argv[1];
    const char *engine = "aether";
    int width_bits = 256;
    int formatted = 0;

    for (int i = 2; i < argc; i++) {
        if (strcmp(argv[i], "-e") == 0 || strcmp(argv[i], "--engine") == 0) {
            if (i + 1 < argc) engine = argv[++i];
        } else if (strcmp(argv[i], "-w") == 0 || strcmp(argv[i], "--width") == 0) {
            if (i + 1 < argc) width_bits = atoi(argv[++i]);
        } else if (strcmp(argv[i], "-f") == 0 || strcmp(argv[i], "--formatted") == 0) {
            formatted = 1;
        }
    }

    FILE *f = fopen(target, "rb");
    if (f) {
        if (strcmp(engine, "iron") == 0) {
            int rc = hash_stream_sha256(f, formatted);
            fclose(f);
            return rc;
        }
        if (strcmp(engine, "aether") == 0) {
            int rc = hash_stream_aether(f, width_bits, formatted);
            fclose(f);
            return rc;
        }
        fclose(f);
        fprintf(stderr, "Engine inválido: %s\n", engine);
        return 1;
    }

    // tratar como texto literal
    if (strcmp(engine, "iron") == 0) {
        sha256_ctx ctx;
        sha256_init(&ctx);
        sha256_update(&ctx, (const unsigned char *)target, strlen(target));
        unsigned char hash[32];
        sha256_final(&ctx, hash);
        if (formatted) {
            printf("Engine     : IRON_SHA256\n");
            printf("Width      : 256 bits\n");
            printf("Bytes      : %zu\n", strlen(target));
            printf("Hex digest : ");
        }
        print_hex_bytes(hash, sizeof(hash));
        printf("\n");
        return 0;
    }

    if (strcmp(engine, "aether") == 0) {
        int passes = width_bits / 64;
        if (passes < 1) passes = 1;
        if (passes > 16) passes = 16;
        uint64_t states[16];
        for (int i = 0; i < passes; i++) {
            uint64_t seed = (uint64_t)i * GOLDEN;
            states[i] = OFFSET ^ seed;
            states[i] = aether_update(states[i], (const unsigned char *)target, strlen(target));
        }
        for (int i = 0; i < passes; i++) {
            char hex[17];
            hex64(states[i], hex);
            printf("%s", hex);
        }
        printf("\n");
        return 0;
    }

    fprintf(stderr, "Engine inválido: %s\n", engine);
    return 1;
}
