#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <inttypes.h>

int masquerade(char *username, char *data) {

    char *program = "/home/anthony/Documents/Python/sshmonitor/src/notify-gtk";

    ssize_t buffer_size = strlen(program) + strlen(data) + sizeof(int);

    char command_array[buffer_size];

    snprintf(command_array, buffer_size, "%s \"%s\"", program, data);

    char *path = getenv("PATH");
    ssize_t psize = strlen(path) + sizeof("PATH=");

    char pathenv[psize];
    snprintf(pathenv, psize, "PATH=%s", path);
    
    char *envp[] = {pathenv, NULL};
    char *arguments[] = {"env", "DISPLAY=:0.0", "sudo", "-i", "su", (char *)username, "-c", command_array, NULL};
    
    return execvpe(arguments[0], arguments, envp);

}

int main(int argc, char *argv[]) {

    masquerade(argv[1], argv[2]);

    return 0;
}
