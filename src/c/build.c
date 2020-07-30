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

    char *program = "/src/c/masquerade.c";
    char *shared_object = "/src/lib/shared/libmasquerade.so";
    char *cwd = get_current_dir_name();

    ssize_t so_buffer = strlen(cwd) + strlen(shared_object) + (sizeof(char *) * 2);
    char *library = (char *)malloc(so_buffer * sizeof(char *));
    snprintf(library, so_buffer, "%s%s", cwd, shared_object);

    ssize_t exe_buffer = strlen(cwd) + strlen(program) + (sizeof(char *) * 2);
    char *executable = (char *)malloc(exe_buffer * sizeof(char *));
    snprintf(executable, exe_buffer, "%s%s", cwd, program);

    char *envp[] = {setpath(), NULL};

    char *arguments[] = {
        "/usr/bin/gcc", "-w", "-shared", "-o", library, "-fPIC", executable, (char *)NULL 
    };

    if(fork() == 0) {
        execvpe(arguments[0], arguments, envp);
    }

    free(library);
    free(executable);

    pthread_mutex_unlock(&lock);

    return 0;

}

void *compile_gtk(void *pkg_config) {

    pthread_mutex_lock(&lock);

    Argument **args = (Argument **)pkg_config;

    char *gcc = "/usr/bin/gcc";
    char *exe = "/src/bin/notify-gtk";
    char *program = "/src/c/notify-gtk.c";

    char *cwd = get_current_dir_name();
    char *output = (chomp((*args)->output));

    size_t gcc_buffer_size = strlen(gcc) + sizeof(char *);
    size_t output_buffer_size = strlen(output) + sizeof(char *);
    size_t command_buffer_size = strlen(cwd) + strlen(program) + (sizeof(char *) * 2);
    size_t executable_buffer_size = strlen(cwd) + strlen(exe) + (sizeof(char *) * 2);

    char *libraries = (char *)malloc(output_buffer_size * sizeof(char *));
    char *compiler = (char *)malloc(gcc_buffer_size * sizeof(char *));
    char *command  = (char *)malloc(command_buffer_size * sizeof(char *));
    char *executable = (char *)malloc(executable_buffer_size * sizeof(char *));

    snprintf(compiler, gcc_buffer_size, "%s", gcc);
    snprintf(libraries, output_buffer_size, "%s", output);
    snprintf(command, command_buffer_size, "%s%s", cwd, program);
    snprintf(executable, executable_buffer_size, "%s%s", cwd, exe);

    size_t system_command_size = gcc_buffer_size + output_buffer_size + command_buffer_size + executable_buffer_size;
    char *system_command = (char *)malloc(system_command_size * sizeof(char *));
    snprintf(system_command, system_command_size, "%s -w %s -o %s %s", compiler, command, executable, libraries);    
    
    if(fork() == 0) {
        system(system_command);
    }

    free(command);
    free(compiler);
    free(libraries);
    free(executable);

    pthread_mutex_unlock(&lock);

    return 0;

}

void *pkg_config(void *package) {

    pthread_mutex_lock(&lock);

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

    pthread_mutex_unlock(&lock);

    return 0;
}

void build(void) {

    Argument *argument;
    argument = (Argument *)malloc((2 * sizeof(char *)) + sizeof(Argument));

    argument->pkgconfig = "gtk+-2.0";

    if (pthread_mutex_init(&lock, NULL) != 0) { 
        perror("\n mutex init has failed: "); 
        exit(1);
    } 

    printf("(INFO) %s - SSHMonitor - Grabbing output of `pkg-config --cflags --libs gtk+-2.0`.\n",chomp(ctime(&t_time)));
    pthread_create(&(tid[0]), NULL, pkg_config, (void *)&argument);
    printf("(INFO) %s - SSHMonitor - Compiling GTK2 executable.\n",chomp(ctime(&t_time)));
    pthread_create(&(tid[1]), NULL, compile_gtk, (void *)&argument);
    printf("(INFO) %s - SSHMonitor - Compiling masquerade shared object.\n",chomp(ctime(&t_time)));
    printf("(INFO) %s - SSHMonitor - Copying libmasquerade.so -> src/lib/shared/\n",chomp(ctime(&t_time)));
    pthread_create(&(tid[2]), NULL, compile_libmasquerade, (void *)NULL);

    pthread_join(tid[0], NULL);
    wait(NULL);
    pthread_join(tid[1], NULL);
    wait(NULL);
    pthread_join(tid[2], NULL);
    wait(NULL);

    pthread_mutex_destroy(&lock);
}
