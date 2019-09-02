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
    gcc -g notify-gtk2.c -o notify-gtk2 `pkg-config --cflags --libs gtk+-2.0`
}

function compile_main() {
    gcc -g masquerade2.c -o masquerade2
}

function copy_ui_to_path() {
    sudo cp notify-gtk2 /usr/local/bin/
}

function chown_ui() {
    sudo chown root:$user /usr/local/bin/notify-gtk2
}

function compile_shared_object() {
    gcc -g -shared -o libmasquerade2.so -fPIC -lpthread masquerade2.c
}

function main() {
    compile_ui;
    copy_ui_to_path;
    chown_ui;

    compile_main;
    compile_shared_object;
} 

main;
