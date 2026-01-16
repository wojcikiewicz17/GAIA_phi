#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>
#include "../headers/omega_ipc.h"
#include "../headers/omega_nexus.h"

extern NexusHeader* header_ptr;
extern void nexus_scan_match(VectorVerb*, void (*)(NexusCell*));

static IPCResponse temp_resp;
static int found = 0;
void _daemon_cb(NexusCell* c) {
    memcpy(&temp_resp.best_match, c, sizeof(NexusCell));
    found = 1;
}

int main() {
    printf("[DAEMON] Iniciando Kernel IPC...\n");
    if (nexus_init("gaia.nexus", 1000000) != 0) return 1;
    
    int s_fd, c_fd; struct sockaddr_un addr;
    s_fd = socket(AF_UNIX, SOCK_STREAM, 0);
    memset(&addr, 0, sizeof(addr)); addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, GAIA_SOCKET_PATH, sizeof(addr.sun_path)-1);
    unlink(GAIA_SOCKET_PATH);
    if(bind(s_fd, (struct sockaddr*)&addr, sizeof(addr)) == -1) return 1;
    listen(s_fd, 5);

    while(1) {
        c_fd = accept(s_fd, NULL, NULL);
        if(c_fd == -1) continue;
        IPCRequest req; IPCResponse resp; memset(&resp, 0, sizeof(resp));
        if(read(c_fd, &req, sizeof(req)) > 0) {
            VectorVerb v_tmp = { .data = req.vector, .dimension = 3 };
            if(req.opcode == OP_SEARCH) {
                found = 0; nexus_scan_match(&v_tmp, _daemon_cb);
                resp.status = found;
            } else if (req.opcode == OP_INSERT) {
                nexus_append(&v_tmp, req.payload); resp.status = 1;
            }
            resp.count = header_ptr->count;
        }
        write(c_fd, &resp, sizeof(resp));
        close(c_fd);
    }
    return 0;
}
