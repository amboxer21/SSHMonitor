#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>

char *test(void) {

    char *path = getenv("PATH");

    size_t path_size  = strlen(path) + strlen("PATH=") + sizeof(char *);
    char *pathenv = (char *)malloc(sizeof(path_size));

    char *ppath = pathenv;

    //memcpy(void *dest, const void *src, size_t n);
    snprintf(pathenv, path_size, "PATH=%s", path);

    free(pathenv);

    return ppath;

}

int main(int argc, char **argv) {
   test();
}
