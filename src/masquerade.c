#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <inttypes.h>

char *setpath() {

    char *path = getenv("PATH");

    size_t psize  = strlen(path) + strlen("PATH=") + sizeof(int);
    char *pathenv = (char *)malloc(sizeof(psize));

    char *ppath = pathenv;

    snprintf(pathenv, psize, "PATH=%s", path);

    free(pathenv);

    return ppath;

}

void masquerade(char *username, char *data) {

    char *program  = "/usr/local/bin/notify-gtk";

    size_t buffer_size = strlen(program) + strlen(data) + sizeof(int);
    char *command = (char *)malloc(sizeof(buffer_size));

    snprintf(command, buffer_size, "%s \"%s\"", program, data);

    char *envp[] = {setpath(), NULL};
    char *arguments[] = {"env", "DISPLAY=:0.0", "sudo", "-i", "su", username, "-c", command, (char *)NULL};
    
    if(fork() == 0) {
        execvpe(arguments[0], arguments, envp);
    }

    free(command);

}
