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

    char *cwd     = get_current_dir_name();
    char *library = "/usr/lib/libmasquerade.so";
    char *program = "/src/masquerade.c";

    size_t buffer_size = strlen(cwd) + strlen(program) + (sizeof(char *) * 2);
    char *command = (char *)malloc(buffer_size * sizeof(char *));
    snprintf(command, buffer_size, "%s%s", cwd, program);

    char *envp[] = {setpath(), NULL};

    char *arguments[] = {
        "/usr/bin/gcc", "-g", "-shared", "-o", library, "-fPIC", command, (char *)NULL 
    };
    
    if(fork() == 0) {
        printf("Compiling masquerade shared object.\n");
        printf("Copying libmasquerade.so to the /usr/lib/ directory.\n");
        execvpe(arguments[0], arguments, envp);
    }

    free(command);

}
