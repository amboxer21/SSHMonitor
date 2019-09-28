#!/bin/bash

if [[ -z $1 ]] ; then
    user=`w -h | awk '{print $1}'`;
else
    user=${1};
fi

if [[ ! $EUID == 0 ]]; then
    echo -e "Must be root!";
    exit;
fi

echo -e "Using user ${user}.";

function compile_ui() {
    echo -e "Compiling GTK2 UI.";
    gcc -g -Wall notify-gtk.c -o notify-gtk `pkg-config --cflags --libs gtk+-2.0`
}

function compile_main() {
    echo -e "Compiling masquerade.";
    gcc -g -Wall masquerade.c -o masquerade
}

function copy_ui_to_path() {
    echo -e "Copying UI to path.";
    sudo cp notify-gtk /usr/local/bin/
}

function chown_ui() {
    echo -e "Changing ownership of UI.";
    sudo chown root:$user /usr/local/bin/notify-gtk
}

function compile_shared_object() {
    echo -e "Compiling Shared Object.";
    gcc -g -Wall -shared -o libmasquerade.so -fPIC masquerade.c
}

function copy_shared_object_to_path() {
  echo -e "Copying Shared Object to path.";
  sudo cp libmasquerade.so lib/shared/;
  sudo cp libmasquerade.so /usr/lib/;
}

function main() {
    echo -e "Entering main.";
    compile_ui;
    copy_ui_to_path;
    chown_ui;

    #compile_main;
    compile_shared_object;
    copy_shared_object_to_path;
} 

main;
