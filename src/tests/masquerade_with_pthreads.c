#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <pthread.h>
#include <inttypes.h>

typedef struct Arguments {
    char *data;
    char *username;
    char *program;
} arguments;

int write_to_shared_memory(char *data) {

    // ftok to generate unique key
    key_t key = ftok("shmfile",65);

    int shmid = shmget(key,1024,0666|IPC_CREAT);

    // shmat to attach to shared memory
    char *shared_data = (char*)shmat(shmid,(void*)0,0);
    const void *message = data;

    memcpy(shared_data, message, (sizeof(message) + sizeof(size_t)));

    //detach from shared memory
    shmdt(shared_data);

    return 0;
}

void *masquerade(void *pargs) {

    arguments **targs = (arguments **)pargs;

    size_t buffer_size = strlen((*targs)->program) + sizeof(int);

    char command_array[buffer_size];

    snprintf(command_array, buffer_size, "%s", (*targs)->program);

    char *path = getenv("PATH");
    size_t psize = strlen(path) + sizeof("PATH=");

    char pathenv[psize];
    snprintf(pathenv, psize, "PATH=%s", path);
    
    char *envp[] = {pathenv, NULL};
    char *arguments[] = {"env", "DISPLAY=:0.0", "sudo", "-i", "su", (*targs)->username, "-c", command_array, (char *)NULL};

    write_to_shared_memory((*targs)->data);

    execvpe(arguments[0], arguments, envp);

}

void main(int argc, char **argv) {

    pthread_t tid;
    arguments *margs;

    margs = (arguments *)malloc((3 * sizeof(char *)) + sizeof(arguments));

    margs->data     = argv[2];
    margs->username = argv[1];
    margs->program  = "/usr/local/bin/notify-gtk2";

    pthread_create(&tid, NULL, masquerade, (void *)&margs);
    pthread_join(tid, NULL); 

    free(margs);

}
