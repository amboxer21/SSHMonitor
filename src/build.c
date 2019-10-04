#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

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

    char *envp[] = {"PATH=/usr/bin", NULL};

    char *arguments[] = {
        "/usr/bin/gcc", "-shared", "-o", library, "-fPIC", executable, (char *)NULL 
    };
    
    if(fork() == 0) {
        printf("Compiling masquerade shared object.\n");
        printf("Copying libmasquerade.so -> src/lib/shared/\n");
        execvpe(arguments[0], arguments, envp);
    }

    free(library);
    free(executable);

}
