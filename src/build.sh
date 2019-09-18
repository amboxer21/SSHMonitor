#!/bin/bash

if [[ -z $1 ]] ; then
    user='root';
else
    user=${1};
fi

if [[ ! $EUID == 0 ]]; then
    echo -e "Must be root!";
fi

function compile_ui() {
    gcc -g -Wall notify-gtk.c -o notify-gtk `pkg-config --cflags --libs gtk+-2.0`
}

function compile_main() {
    gcc -g -Wall masquerade.c -o masquerade
}

function copy_ui_to_path() {
    sudo cp notify-gtk /usr/local/bin/
}

function chown_ui() {
    sudo chown root:$user /usr/local/bin/notify-gtk
}

function compile_shared_object() {
    gcc -g -Wall -shared -o libmasquerade.so -fPIC masquerade.c
}

function copy_shared_object_to_path() {
  sudo cp libmasquerade.so lib/shared/;
  sudo cp libmasquerade.so /usr/lib/;
}

function main() {
    compile_ui;
    copy_ui_to_path;
    chown_ui;

    #compile_main;
    compile_shared_object;
    copy_shared_object_to_path;
} 

main;
