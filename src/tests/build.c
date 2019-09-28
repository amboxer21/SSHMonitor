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
    char *program = "/src/notify-gtk.c";

    size_t buffer_size = strlen(cwd) + strlen(program) + (sizeof(char *) * 2);
    char *command      = (char *)malloc(buffer_size * sizeof(char *));
    snprintf(command, buffer_size, "%s%s", cwd, program);

    printf("%s\n",command);

    char *exe = "/src/notify-gtk";
    char *pkg_config = "/usr/bin/pkg-config --cflags --libs gtk+-2.0";

    buffer_size = strlen(cwd) + strlen(exe) + (sizeof(char *) * 2);
    char *executable = (char *)malloc(buffer_size * sizeof(char *));
    snprintf(executable, buffer_size, "%s%s", cwd, exe);

    printf("%s\n",executable);

    char *envp[] = {setpath(), NULL};

    char *arguments[] = { "/usr/bin/gcc", command, "-o", executable, pkg_config, (char *)NULL };
    
    //if(fork() == 0) {
        //execvpe(arguments[0], arguments, envp);
        execve(arguments[0], arguments, envp);
    //}

    free(command);
    free(executable);

}

int main(int argc, char **argv) {

    build();

    return 0;
}

