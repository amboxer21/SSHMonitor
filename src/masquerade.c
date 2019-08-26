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
    
//void *masquerade(void *thread_args) {
void masquerade(Arguments *targs) {

    //Arguments *targs = (Arguments *)thread_args;

    size_t buffer_size = strlen(targs->program) + strlen(targs->data) + sizeof(int);

    char command_array[buffer_size];

    snprintf(command_array, buffer_size, "%s \"%s\"", targs->program, targs->data);

    char *path = getenv("PATH");
    size_t psize = strlen(path) + sizeof("PATH=");

    char pathenv[psize];
    snprintf(pathenv, psize, "PATH=%s", path);
    
    char *envp[] = {pathenv, NULL};
    char *arguments[] = {"env", "DISPLAY=:0.0", "sudo", "-i", "su", (char *)targs->username, "-c", command_array, NULL};
    
    execvpe(arguments[0], arguments, envp);

}

int main(int argc, char *argv[]) {

    Arguments args;

    args.data = malloc(sizeof(args.data));
    args.program = malloc(sizeof(args.program));
    args.username = malloc(sizeof(args.username));

    args.data     = argv[2];
    args.username = argv[1];
    args.program  = "/usr/local/bin/notify-gtk";

    masquerade(&args);

    /*pthread_t thread_id;

    pthread_create(&thread_id, NULL, masquerade, (void *)&args);
    pthread_join(thread_id, NULL);*/

    free(args.data);
    free(args.program);
    free(args.username);

    return 0;
}
