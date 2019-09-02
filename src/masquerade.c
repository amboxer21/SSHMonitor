#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <inttypes.h>

void masquerade(char *username, char *data) {

    char *program  = "/usr/local/bin/notify-gtk";

    size_t buffer_size = strlen(program) + strlen(data) + sizeof(int);

    char command_array[buffer_size];

    snprintf(command_array, buffer_size, "%s \"%s\"", program, data);

    char *path = getenv("PATH");
    size_t psize = strlen(path) + sizeof("PATH=");

    char pathenv[psize];
    snprintf(pathenv, psize, "PATH=%s", path);
    
    char *envp[] = {pathenv, NULL};
    char *arguments[] = {"env", "DISPLAY=:0.0", "sudo", "-i", "su", username, "-c", command_array, NULL};
    
    execvpe(arguments[0], arguments, envp);

}
