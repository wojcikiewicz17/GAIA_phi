#ifndef OMEGA_IPC_H
#define OMEGA_IPC_H
#include "omega_protocol.h"
#include "omega_nexus.h"
#define GAIA_SOCKET_PATH "gaia.sock"
#define OP_PING   0x01
#define OP_SEARCH 0x02
#define OP_INSERT 0x03
typedef struct {
    uint8_t opcode;
    omega_float vector[3]; // Flat array
    char payload[64];
} IPCRequest;
typedef struct {
    uint8_t status;
    uint64_t count;
    NexusCell best_match;
} IPCResponse;
#endif
