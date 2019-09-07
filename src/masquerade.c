#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char *setpath(void) {

    char *path = getenv("PATH");

    size_t path_size  = strlen(path) + strlen("PATH=") + sizeof(char *);
    char *pathenv = (char *)malloc(sizeof(path_size));

    char *ppath = pathenv;

    snprintf(pathenv, path_size, "PATH=%s", path);

    free(pathenv);

    return ppath;

}

void masquerade(char *username, char *data) {

    if(username == NULL) {
        username = getlogin();
    }

    char *program = "/usr/local/bin/notify-gtk";

    size_t buffer_size = strlen(program) + strlen(data) + sizeof(char *);
    char *command = (char *)malloc(sizeof(buffer_size));
    snprintf(command, buffer_size, "%s \"%s\"", program, data);

    char *envp[] = {setpath(), NULL};

    char *arguments[] = {
        "env", "DISPLAY=:0.0", "sudo", "-i", "su", username, "-c", command, (char *)NULL,
    };
    
    if(fork() == 0) {
        execvpe(arguments[0], arguments, envp);
    }

    free(command);

}
