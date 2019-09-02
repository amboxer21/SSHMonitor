gcc -shared -o libmasquerade2.so -fPIC masquerade2.c -lpthread
gcc notify-gtk2.c -o notify-gtk2 `pkg-config --cflags --libs gtk+-2.0` -lpthread
sudo cp notify-gtk2 /usr/local/bin/
