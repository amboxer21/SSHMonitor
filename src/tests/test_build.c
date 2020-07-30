#define _GNU_SOURCE

#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char *chomp(char *s) {

    char *n = malloc(strlen( s ? s : "\n"));

    if(s) {
        strcpy(n, s);
    }
    n[strlen(n)-1] = '\0';
    return n;
}

void build(void) {

    time_t t;
    time(&t);

    char *t_time = ctime(&t);

    char *cwd = get_current_dir_name();
    char *program = "/src/notify-gtk.c";
    char *output = "/src/bin/notify-gtk";

    ssize_t p_buffer = strlen(cwd) + strlen(output) + (sizeof(char *) * 2);
    char *exec_path = (char *)malloc(p_buffer * sizeof(char *));
    snprintf(exec_path, p_buffer, "%s%s", cwd, output);

    ssize_t e_buffer = strlen(cwd) + strlen(program) + (sizeof(char *) * 2);
    char *executable = (char *)malloc(e_buffer * sizeof(char *));
    snprintf(executable, e_buffer, "%s%s", cwd, program);

    char *envp[] = {"PATH=/usr/bin", NULL};

    // gcc notify-gtk.c -o notify-gtk `pkg-config --cflags --libs gtk+-2.0` -lpthread
    char *arguments[] = {
        "/usr/bin/gcc", executable, "-o", exec_path, (char *)NULL 
    };
    
    if(fork() == 0) {
        printf("(INFO) %s - SSHMonitor - Compiling masquerade shared object.\n",chomp(ctime(&t)));
        printf("(INFO) %s - SSHMonitor - Copying libmasquerade.so -> src/lib/shared/\n",chomp(ctime(&t)));
        execvpe(arguments[0], arguments, envp);
    }

    free(library);
    free(executable);

}
