#define _GNU_SOURCE

#include <ctype.h>

#define SIZE 4
#define BUFFER 1024
#define PBUFFER 4096

typedef struct Arguments {
    int fd[2];
    int s_stdout;
    char *pkgconfig;
    char output[BUFFER];
} Argument;

char *format_pkg_config(char *string) {

    int i, j;
    int n = 0;

    char *fbuffer;
    char delim[SIZE] = "\",\"";

    char nbuffer[PBUFFER];
    char sbuffer[PBUFFER];

    strncpy(sbuffer, "\"", 2);
    strncat(sbuffer, string, strlen(string));

    for(i = 0; i < strlen((char *)sbuffer); i++) {
        if(isspace(sbuffer[i])) {
            if(n == 0) {
                n = i;
            }
            nbuffer[n++] = delim[0];
            nbuffer[n++] = delim[1];
            nbuffer[n++] = delim[2];
        }
        else {
            nbuffer[n++] = sbuffer[i];
        }
    }

    strncat(nbuffer, "\"", 2);
    fbuffer = strndup(nbuffer, strlen(nbuffer));

    return fbuffer;

}

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

char *setpath(void) {

    char *path = getenv("PATH");

    size_t path_size  = strlen(path) + strlen("PATH=") + sizeof(char *);
    char *pathenv = (char *)malloc(path_size*sizeof(char *));
    snprintf(pathenv, path_size, "PATH=%s", path);

    char *ppath = strndup(pathenv, path_size);

    free(pathenv);

    return ppath;

}
