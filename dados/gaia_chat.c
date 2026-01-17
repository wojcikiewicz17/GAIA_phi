#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>

#include "headers/omega_ipc.h"

static uint64_t djb2_hash(const char *text) {
    uint64_t h = 5381u;
    for (const unsigned char *p = (const unsigned char *)text; *p; p++) {
        h = ((h << 5) + h) + *p;
    }
    return h;
}

static void hash_to_vec(uint64_t h, float out[3]) {
    out[0] = (float)(h & 0xFFFFu) / 65535.0f;
    out[1] = (float)((h >> 16) & 0xFFFFu) / 65535.0f;
    out[2] = (float)((h >> 32) & 0xFFFFu) / 65535.0f;
}

static int talk(const char *text) {
    int fd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (fd == -1) {
        perror("socket");
        return 1;
    }

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, GAIA_SOCKET_PATH, sizeof(addr.sun_path) - 1);

    if (connect(fd, (struct sockaddr *)&addr, sizeof(addr)) == -1) {
        perror("connect");
        close(fd);
        return 1;
    }

    IPCRequest req;
    memset(&req, 0, sizeof(req));
    req.opcode = OP_SEARCH;
    uint64_t h = djb2_hash(text);
    hash_to_vec(h, req.vector);

    if (write(fd, &req, sizeof(req)) != (ssize_t)sizeof(req)) {
        perror("write");
        close(fd);
        return 1;
    }

    IPCResponse resp;
    ssize_t n = read(fd, &resp, sizeof(resp));
    if (n <= 0) {
        perror("read");
        close(fd);
        return 1;
    }

    if (resp.status) {
        printf("MATCH ENCONTRADO!\n");
    } else {
        printf("SEM MEMORIA.\n");
    }

    close(fd);
    return 0;
}

int main(void) {
    char buf[1024];
    for (;;) {
        printf("C> ");
        if (!fgets(buf, sizeof(buf), stdin)) {
            break;
        }
        buf[strcspn(buf, "\n")] = '\0';
        if (strcmp(buf, "q") == 0) {
            break;
        }
        if (buf[0] == '\0') {
            continue;
        }
        talk(buf);
    }
    return 0;
}
