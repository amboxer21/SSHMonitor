#include <stdio.h>
#include <ctype.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>

#define SIZE 4
#define BUFFER 4096

char *test_function(char *string) {

    int i, j;
    int n = 0;

    char *fbuffer;
    char delim[SIZE] = "\",\"";

    char nbuffer[BUFFER]; 
    char sbuffer[BUFFER]; 

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

    strncat(nbuffer, "\"", 1);
    fbuffer = strndup(nbuffer, strlen(nbuffer));

    return fbuffer;

}

int main(int argc, char **argv) {

    char test[4096] = "-pthread -I/usr/include/gtk-2.0 -I/usr/lib/x86_64-linux-gnu/gtk-2.0/include -I/usr/include/gio-unix-2.0 -I/usr/include/cairo -I/usr/include/pango-1.0 -I/usr/include/atk-1.0 -I/usr/include/cairo -I/usr/include/pixman-1 -I/usr/include/gdk-pixbuf-2.0 -I/usr/include/libmount -I/usr/include/blkid -I/usr/include/pango-1.0 -I/usr/include/harfbuzz -I/usr/include/pango-1.0 -I/usr/include/fribidi -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/uuid -I/usr/include/freetype2 -I/usr/include/libpng16 -lgtk-x11-2.0 -lgdk-x11-2.0 -lpangocairo-1.0 -latk-1.0 -lcairo -lgdk_pixbuf-2.0 -lgio-2.0 -lpangoft2-1.0 -lpango-1.0 -lgobject-2.0 -lglib-2.0 -lfontconfig -lfreetype";

    test_function(test);

    return 0;

}
