#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <sys/ipc.h>
#include <sys/shm.h>

int main(int argc, char **argv) {

    // ftok to generate unique key
    key_t key = ftok("shmfile",65);

    int shmid = shmget(key,1024,0666|IPC_CREAT);

    // shmat to attach to shared memory
    char *str = (char*) shmat(shmid,(void*)0,0);
    const void *message = "Secret message";

    memcpy(str, message, (sizeof(message) + sizeof(size_t)));

    printf("Data written in memory: %s\n",str);

    //detach from shared memory
    shmdt(str);

    return 0;
}

