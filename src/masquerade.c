#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <inttypes.h>

#define NOTIFY "/home/anthony/Documents/Python/sshmonitor/src/notify-gtk TEST"

int masquerade(char *username, char *data) {

    char *path = getenv("PATH");
    ssize_t psize = strlen(path) + sizeof("PATH=");

    char pathenv[psize];
    snprintf(pathenv, psize, "PATH=%s", path);
    
    char *envp[] = {pathenv, NULL};
    char *arguments[] = {"env", "DISPLAY=:0", "sudo", "-i", "su", "anthony", "-c", NOTIFY, NULL};
    
    return execvpe(arguments[0], arguments, envp);

}

int main(int argc, char *argv[]) {

    masquerade(argv[1], argv[2]);

    return 0;
}
