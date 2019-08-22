#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

int masquerade(char *username, char *command) {

    char *path = getenv("PATH");
    char pathenv[strlen(path) + sizeof("PATH=")];
    sprintf(pathenv, "PATH=%s", path);
    char *envp[] = {pathenv, NULL};
    char *tests[] = {"sudo", "-i", "su", username, "-c", command, NULL};
    execvpe(tests[0], tests, envp);

    return 0;

}

int main(int argc, char *argv[]) {

    masquerade(argv[1], "whoami");

    return 0;
}
