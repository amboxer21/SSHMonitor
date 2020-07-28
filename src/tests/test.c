#include <stdio.h>
#include <ctype.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>

#define _XOPEN_SOURCE >= 500 || _ISOC99_SOURCE |

int main(int argc, char **argv) {

    int i, n;

    char test[4096] = "-pthread -I/usr/include/gtk-2.0 -I/usr/lib/x86_64-linux-gnu/gtk-2.0/include -I/usr/include/gio-unix-2.0 -I/usr/include/cairo -I/usr/include/pango-1.0 -I/usr/include/atk-1.0 -I/usr/include/cairo -I/usr/include/pixman-1 -I/usr/include/gdk-pixbuf-2.0 -I/usr/include/libmount -I/usr/include/blkid -I/usr/include/pango-1.0 -I/usr/include/harfbuzz -I/usr/include/pango-1.0 -I/usr/include/fribidi -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/include/uuid -I/usr/include/freetype2 -I/usr/include/libpng16 -lgtk-x11-2.0 -lgdk-x11-2.0 -lpangocairo-1.0 -latk-1.0 -lcairo -lgdk_pixbuf-2.0 -lgio-2.0 -lpangoft2-1.0 -lpango-1.0 -lgobject-2.0 -lglib-2.0 -lfontconfig -lfreetype";

    char nbuffer[4096]; 

    int count;
   
    char delim[5];
    strcpy(delim,"\",\""); 

    for(i = 0; i < strlen((char *)test); i++) {
        if(isspace(test[i])) {
            nbuffer[i+1] = delim[0];
            nbuffer[i+2] = delim[1];
            nbuffer[i+3] = delim[2];
        }
        else {
            nbuffer[i] = test[i];
        }
    }

    for(n = 0; n < strlen((char *)test); n++) {
        printf("%c",nbuffer[n]);
    }

    return 0;

}
