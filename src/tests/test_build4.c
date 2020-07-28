#define _GNU_SOURCE

#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/wait.h>

#include "build.h"

pthread_t tid[2];
pthread_mutex_t lock;

static const time_t t_time;

void *compile_libmasquerade(void *arg) {

    pthread_mutex_lock(&lock);

    //printf("void *compile_libmasquerade ENTRY\n");

    char *cwd = get_current_dir_name();
    char *program = "/masquerade.c";
    char *shared_object = "/libmasquerade.so";

    ssize_t so_buffer = strlen(cwd) + strlen(shared_object) + (sizeof(char *) * 2);
    char *library = (char *)malloc(so_buffer * sizeof(char *));
    snprintf(library, so_buffer, "%s%s", cwd, shared_object);

    ssize_t exe_buffer = strlen(cwd) + strlen(program) + (sizeof(char *) * 2);
    char *executable = (char *)malloc(exe_buffer * sizeof(char *));
    snprintf(executable, exe_buffer, "%s%s", cwd, program);

    char *envp[] = {"PATH=/usr/bin", NULL};

    char *arguments[] = {
        "/usr/bin/gcc", "-w", "-shared", "-o", library, "-fPIC", executable, (char *)NULL 
    };

    if(fork() == 0) {
        //printf("(INFO) %s - SSHMonitor - Compiling masquerade shared object.\n",chomp(ctime(&t_time)));
        //printf("(INFO) %s - SSHMonitor - Copying libmasquerade.so -> src/lib/shared/\n",chomp(ctime(&t_time)));
        execvpe(arguments[0], arguments, envp);
    }

    free(library);
    free(executable);

    //printf("void *compile_libmasquerade EXIT\n");

    pthread_mutex_unlock(&lock);

    return 0;

}

void *compile_gtk(void *pkg_config) {

    pthread_mutex_lock(&lock);

    //printf("void *compile_gtk ENTRY\n");

    Argument **args = (Argument **)pkg_config;

    char *cwd = get_current_dir_name();
    char *program = "/notify-gtk.c";

    size_t buffer_size = strlen(cwd) + strlen(program) + (sizeof(char *) * 2);
    char *command = (char *)malloc(buffer_size * sizeof(char *));
    snprintf(command, buffer_size, "%s%s", cwd, program);

    char *exe = "/notify-gtk";

    buffer_size = strlen(cwd) + strlen(exe) + (sizeof(char *) * 2);
    char *executable = (char *)malloc(buffer_size * sizeof(char *));
    snprintf(executable, buffer_size, "%s%s", cwd, exe);

    char *envp[] = {setpath(), NULL};

    char *arguments[] = { "/usr/bin/gcc", "-w", command, "-o", executable, chomp((*args)->output), (char *)NULL };
    
    if(fork() == 0) {
        if(execvpe(arguments[0], arguments, envp) == -1) {
            perror("PERROR - execvpe error occured in compile_gtk: ");
        }
    }

    free(command);
    free(executable);

    //printf("void *compile_gtk EXIT\n");

    pthread_mutex_unlock(&lock);

    return 0;

}

void *pkg_config(void *package) {

    pthread_mutex_lock(&lock);

    //printf("void *pkg_config ENTRY\n");

    Argument **args = (Argument **)package;

    pid_t pid;

    char *envp[] = {setpath(), NULL};

    char *arguments[] = {
        "/usr/bin/pkg-config", "--cflags", "--libs", (*args)->pkgconfig, (char *)NULL 
    };

    if(pipe((*args)->fd) == -1) {
        perror("Error occured with pipe call: ");
    }

    if((pid = fork()) < 0) {
        perror("fork() error: ");
    }
    else if(pid == 0) {
        close((*args)->fd[0]);
        dup2((*args)->fd[1], 1);
        close((*args)->fd[1]);
        execvpe(arguments[0], arguments, envp);
    }
    else {
        close((*args)->fd[1]);
        while (read((*args)->fd[0], (*args)->output, BUFFER) != 0) { } 
    }

    //printf("void *pkg_config EXIT\n");

    pthread_mutex_unlock(&lock);

    return 0;
}

int main(int argc, char **argv) {

    Argument *argument;
    argument = (Argument *)malloc((2 * sizeof(char *)) + sizeof(Argument));

    argument->pkgconfig = "gtk+-2.0";

    if (pthread_mutex_init(&lock, NULL) != 0) { 
        perror("\n mutex init has failed: "); 
        return 1; 
    } 

    pthread_create(&(tid[0]), NULL, pkg_config, (void *)&argument);
    pthread_create(&(tid[1]), NULL, compile_gtk, (void *)&argument);
    pthread_create(&(tid[2]), NULL, compile_libmasquerade, (void *)NULL);

    pthread_join(tid[0], NULL);
    wait(NULL);
    pthread_join(tid[1], NULL);
    wait(NULL);
    pthread_join(tid[2], NULL);
    wait(NULL);

    pthread_mutex_destroy(&lock);

    //printf("argument->output: %s\n",argument->output);

    return 0;
}
