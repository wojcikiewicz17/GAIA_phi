#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
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

// ---- minimal SHA-256 ----
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

static void print_hex_bytes(const unsigned char *buf, size_t len, char *out, size_t out_len) {
    static const char* hexd = "0123456789abcdef";
    if (out_len < (len * 2 + 1)) return;
    for (size_t i = 0; i < len; i++) {
        out[i * 2] = hexd[(buf[i] >> 4) & 0xF];
        out[i * 2 + 1] = hexd[buf[i] & 0xF];
    }
    out[len * 2] = '\0';
}

static void json_escape(const char *src, char *dst, size_t dst_len) {
    size_t w = 0;
    for (size_t i = 0; src[i] && w + 2 < dst_len; i++) {
        char c = src[i];
        if (c == '"' || c == '\\') {
            dst[w++] = '\\';
        }
        dst[w++] = c;
    }
    dst[w] = '\0';
}

static void find_json_value(const char *body, const char *key, char *out, size_t out_len) {
    char pattern[64];
    snprintf(pattern, sizeof(pattern), "\"%s\"", key);
    const char *p = strstr(body, pattern);
    if (!p) {
        out[0] = '\0';
        return;
    }
    p = strchr(p, ':');
    if (!p) {
        out[0] = '\0';
        return;
    }
    p++;
    while (*p == ' ' || *p == '\t') p++;
    if (*p == '"') {
        p++;
        size_t i = 0;
        while (*p && *p != '"' && i + 1 < out_len) {
            out[i++] = *p++;
        }
        out[i] = '\0';
    } else {
        size_t i = 0;
        while (*p && *p != ',' && *p != '}' && i + 1 < out_len) {
            out[i++] = *p++;
        }
        out[i] = '\0';
    }
}

static void handle_api_hash(int client, const char *body) {
    char text[1024];
    char engine[32];
    char width_buf[32];
    find_json_value(body, "text", text, sizeof(text));
    find_json_value(body, "engine", engine, sizeof(engine));
    find_json_value(body, "width", width_buf, sizeof(width_buf));

    if (engine[0] == '\0') strcpy(engine, "aether");
    int width_bits = 256;
    if (width_buf[0] != '\0') width_bits = atoi(width_buf);

    if (text[0] == '\0') {
        const char *resp = "HTTP/1.1 400 Bad Request\r\nContent-Type: application/json\r\n\r\n{\"error\":\"missing text\"}";
        write(client, resp, strlen(resp));
        return;
    }

    char hex[512] = {0};
    int width_out = 256;
    if (strcmp(engine, "iron") == 0) {
        sha256_ctx ctx;
        sha256_init(&ctx);
        sha256_update(&ctx, (const unsigned char *)text, strlen(text));
        unsigned char hash[32];
        sha256_final(&ctx, hash);
        print_hex_bytes(hash, sizeof(hash), hex, sizeof(hex));
        width_out = 256;
    } else {
        int passes = width_bits / 64;
        if (passes < 1) passes = 1;
        if (passes > 16) passes = 16;
        uint64_t states[16];
        for (int i = 0; i < passes; i++) {
            uint64_t seed = (uint64_t)i * GOLDEN;
            states[i] = OFFSET ^ seed;
            states[i] = aether_update(states[i], (const unsigned char *)text, strlen(text));
        }
        char *p = hex;
        for (int i = 0; i < passes; i++) {
            char part[17];
            hex64(states[i], part);
            memcpy(p, part, 16);
            p += 16;
        }
        *p = '\0';
        width_out = passes * 64;
        strcpy(engine, "aether");
    }

    char escaped[2048];
    json_escape(text, escaped, sizeof(escaped));

    char body_out[4096];
    snprintf(body_out, sizeof(body_out),
             "{\"engine\":\"%s\",\"width_bits\":%d,\"hex\":\"%s\",\"label\":\"text\",\"text\":\"%s\"}",
             engine, width_out, hex, escaped);

    char header[256];
    snprintf(header, sizeof(header),
             "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: %zu\r\n\r\n",
             strlen(body_out));

    write(client, header, strlen(header));
    write(client, body_out, strlen(body_out));
}

static void handle_root(int client) {
    const char *html =
        "<html><head><title>AETHER-X HYBRID WEB (C)</title></head>"
        "<body><h1>AETHER-X HYBRID WEB (C)</h1>"
        "<p>Use POST /api/hash com JSON: {\"text\":\"hello\",\"engine\":\"aether\",\"width\":256}</p>"
        "</body></html>";
    char header[256];
    snprintf(header, sizeof(header),
             "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: %zu\r\n\r\n",
             strlen(html));
    write(client, header, strlen(header));
    write(client, html, strlen(html));
}

int main(void) {
    int port = 8000;
    const char *env = getenv("PORT");
    if (env) port = atoi(env);

    int server = socket(AF_INET, SOCK_STREAM, 0);
    if (server == -1) {
        perror("socket");
        return 1;
    }

    int opt = 1;
    setsockopt(server, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons((uint16_t)port);

    if (bind(server, (struct sockaddr *)&addr, sizeof(addr)) == -1) {
        perror("bind");
        close(server);
        return 1;
    }

    if (listen(server, 16) == -1) {
        perror("listen");
        close(server);
        return 1;
    }

    printf("[AETHER-X HYBRID WEB C] listening on 0.0.0.0:%d\n", port);

    for (;;) {
        int client = accept(server, NULL, NULL);
        if (client == -1) {
            continue;
        }
        char buf[8192];
        ssize_t n = read(client, buf, sizeof(buf) - 1);
        if (n <= 0) {
            close(client);
            continue;
        }
        buf[n] = '\0';

        char method[8] = {0};
        char path[256] = {0};
        sscanf(buf, "%7s %255s", method, path);

        char *body = strstr(buf, "\r\n\r\n");
        if (body) body += 4;
        else body = "";

        if (strcmp(method, "GET") == 0 && strcmp(path, "/") == 0) {
            handle_root(client);
        } else if (strcmp(method, "POST") == 0 && strcmp(path, "/api/hash") == 0) {
            handle_api_hash(client, body);
        } else {
            const char *resp = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nNot found";
            write(client, resp, strlen(resp));
        }

        close(client);
    }

    close(server);
    return 0;
}
