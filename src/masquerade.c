#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <inttypes.h>

struct Arguments {
    char *data;
    char *username;
};
    
int masquerade(struct Arguments *args) {

    char *program = "/home/anthony/Documents/Python/sshmonitor/src/notify-gtk";

    ssize_t buffer_size = strlen(program) + strlen(args->data) + sizeof(int);

    char command_array[buffer_size];

    snprintf(command_array, buffer_size, "%s \"%s\"", program, args->data);

    char *path = getenv("PATH");
    ssize_t psize = strlen(path) + sizeof("PATH=");

    char pathenv[psize];
    snprintf(pathenv, psize, "PATH=%s", path);
    
    char *envp[] = {pathenv, NULL};
    char *arguments[] = {"env", "DISPLAY=:0.0", "sudo", "-i", "su", (char *)args->username, "-c", command_array, NULL};
    
    return execvpe(arguments[0], arguments, envp);

}

int main(int argc, char *argv[]) {

    pthread_t thread_id;

    struct Arguments args;

    args.data = argv[2];
    args.username = argv[1];

    pthread_create(&thread_id, NULL, (void *)masquerade, (void *)&args);
    pthread_join(thread_id, NULL);

    return 0;
}
