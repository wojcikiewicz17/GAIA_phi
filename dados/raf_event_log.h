#ifndef RAF_EVENT_LOG_H
#define RAF_EVENT_LOG_H

#include <stdint.h>

// Formato de linha no log (texto):
// seq|timestamp|actor|etype|prev_hash_hex|this_hash_hex|payload
//
// - seq           : uint64 (contador crescente, 0,1,2,...)
// - timestamp     : epoch (segundos)
// - actor         : id do agente (ex: 1 = sistema, 2 = Rafael, etc.)
// - etype         : tipo de evento (ex: 1 = SNAPSHOT, 2 = MUTACAO, etc.)
// - prev_hash_hex : this_hash_hex da linha anterior, ou 000...0 no primeiro
// - this_hash_hex : hash de todos os campos (exceto ele mesmo)
// - payload       : texto livre (sem '|'), resumo ou caminho do que aconteceu
//
// Se qualquer bit for alterado em qualquer lugar da cadeia,
// a verificação falha.

int raf_append_event(
    const char* log_path,
    uint32_t actor,
    uint32_t etype,
    const char* payload
);

int raf_verify_log(const char* log_path);

#endif
