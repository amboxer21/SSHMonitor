#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

char *setpath() {

    char *path = getenv("PATH");

    size_t psize  = strlen(path) + strlen("PATH=") + sizeof(int);
    char *pathenv = (char *)malloc(sizeof(psize));

    char *ppath = pathenv;

    snprintf(pathenv, psize, "PATH=%s", path);
    return ppath;

}

char w() {
    //return
}

int main() {

    printf("username: %s\n",getlogin());
    printf("%s\n",setpath());

    return 0;
}
