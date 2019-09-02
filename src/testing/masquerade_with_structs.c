#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <inttypes.h>

typedef struct Arguments {
    char *data;
    char *username;
    char *program;
} arguments;
    
void masquerade(arguments **targs) {

    size_t buffer_size = strlen((*targs)->program) + strlen((*targs)->data) + sizeof(int);

    char command_array[buffer_size];

    snprintf(command_array, buffer_size, "%s \"%s\"", (*targs)->program, (*targs)->data);

    char *path = getenv("PATH");
    size_t psize = strlen(path) + sizeof("PATH=");

    char pathenv[psize];
    snprintf(pathenv, psize, "PATH=%s", path);
    
    char *envp[] = {pathenv, NULL};
    char *arguments[] = {"env", "DISPLAY=:0.0", "sudo", "-i", "su", (*targs)->username, "-c", command_array, (char *)NULL};
    
    execvpe(arguments[0], arguments, envp);

}

int main(int argc, char *argv[]) {

    arguments *args;

    args = (arguments *)malloc((3 * sizeof(char *)) + sizeof(arguments));

    args->data     = argv[2];
    args->username = argv[1];
    args->program  = "/usr/local/bin/notify-gtk";

    masquerade(&args);

    free(args);

    return 0;
}
