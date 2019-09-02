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
    gcc -g notify-gtk.c -o notify-gtk `pkg-config --cflags --libs gtk+-2.0`
}

function compile_main() {
    echo -e "\n\nSkipping compilation of main c program.";
    echo -e "This option is being skipped and commented out due to the program being"
    echo -e "a library. This means that the program has no main function entry point.";
    echo -e "Uncomment if you want to compile main, just add a main entry point in masquerade.c.\n\n"
    #gcc -g masquerade.c -o masquerade
}

function copy_ui_to_path() {
    sudo cp notify-gtk /usr/local/bin/
}

function chown_ui() {
    sudo chown root:$user /usr/local/bin/notify-gtk
}

function compile_shared_object() {
    gcc -g -shared -o libmasquerade.so -fPIC -lpthread masquerade.c
}

function main() {
    compile_ui;
    copy_ui_to_path;
    chown_ui;

    #compile_main;
    compile_shared_object;
} 

main;
