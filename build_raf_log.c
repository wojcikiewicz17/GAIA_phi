#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

static int run_script(const char *script) {
    pid_t pid = fork();
    if (pid == 0) {
        execl("/bin/bash", "bash", script, (char *)NULL);
        _exit(127);
    }
    if (pid < 0) {
        perror("fork");
        return 1;
    }
    int status = 0;
    if (waitpid(pid, &status, 0) < 0) {
        perror("waitpid");
        return 1;
    }
    if (WIFEXITED(status)) {
        return WEXITSTATUS(status);
    }
    return 1;
}

int main(void) {
    printf("[build_raf_log.c] delegando para build_raf_log.sh\n");
    return run_script("./build_raf_log.sh");
}
