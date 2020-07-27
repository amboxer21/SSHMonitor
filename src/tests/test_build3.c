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

static const time_t t_time;

void *compile_libmasquerade(void *arg) {

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
        "/usr/bin/gcc", "-shared", "-o", library, "-fPIC", executable, (char *)NULL 
    };

    if(fork() == 0) {
        printf("(INFO) %s - SSHMonitor - Compiling masquerade shared object.\n",chomp(ctime(&t_time)));
        printf("(INFO) %s - SSHMonitor - Copying libmasquerade.so -> src/lib/shared/\n",chomp(ctime(&t_time)));
        execvpe(arguments[0], arguments, envp);
    }

    free(library);
    free(executable);

    return 0;

}

void *compile_gtk(void *pkg_config) {

    Argument **args = (Argument **)pkg_config;

    char *cwd = get_current_dir_name();
    char *program = "/notify-gtk.c";

    size_t buffer_size = strlen(cwd) + strlen(program) + (sizeof(char *) * 2);
    char *command      = (char *)malloc(buffer_size * sizeof(char *));
    snprintf(command, buffer_size, "%s%s", cwd, program);

    char *exe = "/notify-gtk";

    buffer_size = strlen(cwd) + strlen(exe) + (sizeof(char *) * 2);
    char *executable = (char *)malloc(buffer_size * sizeof(char *));
    snprintf(executable, buffer_size, "%s%s", cwd, exe);

    char *envp[] = {setpath(), NULL};

    char *arguments[] = { "/usr/bin/gcc", command, "-o", executable, chomp((*args)->output)), (char *)NULL };
    
    execvpe(arguments[0], arguments, envp);

    free(command);
    free(executable);

}

void *pkg_config(void *pakage) {

    Argument **pkg = (Argument **)pakage;

    char *envp[] = {setpath(), NULL};

    char *arguments[] = {
        "/usr/bin/pkg-config", "--cflags", "--libs", (*pkg)->pkgconfig, (char *)NULL 
    };

    execvpe(arguments[0], arguments, envp);
}

void *redirect_output() {

}

int main(int argc, char **argv) {

    int status, bytes;

    pid_t pid;
    pthread_t tid[2];

    Argument *argument;
    argument = (Argument *)malloc((3 * sizeof(char *)) + sizeof(Argument));

    argument->pkgconfig = "gtk+-2.0";
    argument->s_stdout = dup(fileno(stdout));

    pthread_create(&(tid[0]), NULL, compile_libmasquerade, (void *)NULL);
    pthread_join(tid[0], NULL);

    if(pipe(argument->fd) == -1) {
        printf("Error occured with pipe call.");
        return 1;
    }

    dup2(argument->fd[1], fileno(stdout));
    close(argument->fd[1]);

    if((pid = fork()) < 0) {
        perror("fork() error");
    }
    else if(pid == 0) {
        pthread_create(&(tid[1]), NULL, pkg_config, (void *)&argument);
        pthread_join(tid[1], NULL);
        sleep(5);
        exit(1);
    }
    else do {
        if((pid = waitpid(pid, &status, WNOHANG)) == -1) {
            perror("wait() error");
        }
        else if(pid == 0) {
            printf("child is still running at %s\n", chomp(ctime(&t_time)));
            sleep(1);
        }
        else {
            if(WIFEXITED(status)) {
                close(argument->fd[1]);
                printf("child exited with status of %d\n", WEXITSTATUS(status));
                while(bytes = read(argument->fd[0], argument->output, BUFFER+1)) {
                    if(bytes != 0) {
                        close(fileno(stdout));
                        dup2(argument->s_stdout, fileno(stdout));
                        close(argument->s_stdout);
                        break;
                    }
                }
                close(argument->fd[0]);
            } 
            else {
                perror("child did not exit successfully: ");
            }
        }
    } while(pid == 0);

    printf("argument->output: %s\n",argument->output);

    pthread_create(&(tid[2]), NULL, compile_gtk, (void *)&argument);
    pthread_join(tid[2], NULL);

    return 0;
}
