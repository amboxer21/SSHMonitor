#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <inttypes.h>

typedef struct Arguments {
    char *data;
    char *username;
    char *program;
} Arguments;
    
void *masquerade(void *thread_args) {

    Arguments *targs = (Arguments *)thread_args;

    ssize_t buffer_size = strlen(targs->program) + strlen(targs->data) + sizeof(int);

    char command_array[buffer_size];

    snprintf(command_array, buffer_size, "%s \"%s\"", targs->program, targs->data);

    char *path = getenv("PATH");
    ssize_t psize = strlen(path) + sizeof("PATH=");

    char pathenv[psize];
    snprintf(pathenv, psize, "PATH=%s", path);
    
    char *envp[] = {pathenv, NULL};
    char *arguments[] = {"env", "DISPLAY=:0.0", "sudo", "-i", "su", (char *)targs->username, "-c", command_array, NULL};
    
    execvpe(arguments[0], arguments, envp);

}

int main(int argc, char *argv[]) {

    Arguments args;

    args.data     = argv[2];
    args.username = argv[1];
    args.program  = "/home/anthony/Documents/Python/sshmonitor/src/notify-gtk";

    pthread_t thread_id;

    pthread_create(&thread_id, NULL, masquerade, (void *)&args);
    pthread_join(thread_id, NULL);

    return 0;
}
