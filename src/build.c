#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char *setpath(void) {

    char *path = getenv("PATH");

    size_t path_size  = strlen(path) + strlen("PATH=") + sizeof(char *);
    char *pathenv = (char *)malloc(path_size*sizeof(char *));
    snprintf(pathenv, path_size, "PATH=%s", path);

    char *ppath = pathenv;

    free(pathenv);

    return ppath;

}

void build(void) {

    char *cwd = get_current_dir_name();
    char *program = "/src/masquerade.c";
    char *shared_object = "/src/lib/shared/libmasquerade.so";

    ssize_t so_buffer = strlen(cwd) + strlen(shared_object) + (sizeof(char *) * 2);
    char *library = (char *)malloc(so_buffer * sizeof(char *));
    snprintf(library, so_buffer, "%s%s", cwd, shared_object);

    ssize_t exe_buffer = strlen(cwd) + strlen(program) + (sizeof(char *) * 2);
    char *executable = (char *)malloc(exe_buffer * sizeof(char *));
    snprintf(executable, exe_buffer, "%s%s", cwd, program);

    char *envp[] = {setpath(), NULL};

    char *arguments[] = {
        "/usr/bin/gcc", "-g", "-shared", "-o", library, "-fPIC", executable, (char *)NULL 
    };
    
    if(fork() == 0) {
        printf("Compiling masquerade shared object.\n");
        printf("Copying libmasquerade.so -> src/lib/shared/\n");
        execvpe(arguments[0], arguments, envp);
    }

    free(library);
    free(executable);

}
