#include <stdio.h>
#include <string.h>

#include "smart_guard.h"

int main(void) {
    char line[1024];
    puts("Smart Guard CLI (digite 'q' para sair)");
    for (;;) {
        printf("> ");
        if (!fgets(line, sizeof(line), stdin)) {
            break;
        }
        line[strcspn(line, "\n")] = '\0';
        if (strcmp(line, "q") == 0) {
            break;
        }
        SGResult result = smart_guard_evaluate(line);
        char message[256];
        smart_guard_format_message(&result, message, sizeof(message));
        printf("%s\n", message);
    }
    return 0;
}
