#define _GNU_SOURCE

#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int length(char **array) {
     int len = *(&array + 1) - array;
     return len;
}

char *chomp(char *s) {

    char *n = malloc(strlen( s ? s : "\n"));

    if(s) {
        strcpy(n, s);
    }
    n[strlen(n)-1] = '\0';
    return n;
}

int compile_libmasquerade() {

    time_t t;
    time(&t);

    char *t_time = ctime(&t);

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
        printf("(INFO) %s - SSHMonitor - Compiling masquerade shared object.\n",chomp(ctime(&t)));
        printf("(INFO) %s - SSHMonitor - Copying libmasquerade.so -> src/lib/shared/\n",chomp(ctime(&t)));
        execvpe(arguments[0], arguments, envp);
    } else {
        printf("An issue occured while compiling the .SO!");
    }

    free(library);
    free(executable);

    return 0;

}

char *setpath(void) {

    char *path = getenv("PATH");

    size_t path_size  = strlen(path) + strlen("PATH=") + sizeof(char *);
    char *pathenv = (char *)malloc(path_size*sizeof(char *));
    snprintf(pathenv, path_size, "PATH=%s", path);

    char *ppath = pathenv;

    free(pathenv);

    return ppath;

}

int compile_gtk(char *pkg_config) {

    char *cwd = get_current_dir_name();
    char *program = "/notify-gtk.c";

    size_t buffer_size = strlen(cwd) + strlen(program) + (sizeof(char *) * 2);
    char *command      = (char *)malloc(buffer_size * sizeof(char *));
    snprintf(command, buffer_size, "%s%s", cwd, program);

    char *exe = "/notify-gtk";

    buffer_size = strlen(cwd) + strlen(exe) + (sizeof(char *) * 2);
    char *executable = (char *)malloc(buffer_size * sizeof(char *));
    snprintf(executable, buffer_size, "%s%s", cwd, exe);

    printf("executable path: %s\n",executable);

    char *envp[] = {setpath(), NULL};

    char *arguments[] = { "/usr/bin/gcc", command, "-o", executable, pkg_config, (char *)NULL };
    
    if(fork() == 0) {
        execvpe(arguments[0], arguments, envp);
        _exit(-1);
    }

    free(command);
    free(executable);

    return 0;

}

char *pkg_config(char *pkg) {

    char *envp[] = {setpath(), NULL};

    char *arguments[] = {
        "/usr/bin/pkg-config", "--cflags", "--libs", pkg, (char *)NULL 
    };

    ssize_t exec_buffer = length(arguments) + length(envp) + (sizeof(char *) * 2);
    char *executable = (char *)malloc(exec_buffer * sizeof(char *));

    if(fork() == 0) {
        snprintf(executable, exec_buffer, "%s", execvpe(arguments[0], arguments, envp));
        _exit(-1);
    }

    char *pkgconfig = strndup(executable, sizeof(executable));
    free(executable);

    return pkgconfig;

}

int main(int argc, char *argv) {
  printf("TEST\n");
  compile_gtk(pkg_config("gtk+-2.0"));
  return 0;
}
