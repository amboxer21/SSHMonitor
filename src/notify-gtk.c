#define _GNU_SOURCE

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

// GTK header files
#include <glib.h>
#include <gtk/gtk.h>

#define WHOAMI "/usr/bin/whoami"
#define PYTHON "/usr/bin/python"

static void destroy_event(GtkWidget *widget, gpointer data) {
  gtk_main_quit();
}

static gboolean delete_event(GtkWidget *widget, GdkEvent *event, gpointer data) {
  gtk_main_quit();
  return FALSE;
}

int main(int argc, char *argv[]) {

    GtkWidget *window;

    gtk_init(&argc, &argv);

    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), NULL);
    gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER);
    gtk_window_set_default_size(GTK_WINDOW(window), 300, 100);
    gtk_widget_show(window);

    //g_signal_connect_swapped(G_OBJECT(quit), "activate", G_CALLBACK(gtk_main_quit), NULL);
    //g_signal_connect(G_OBJECT(button), "button_press_event", G_CALLBACK(callback), NULL);
    //g_signal_connect(G_OBJECT(button), "clicked", G_CALLBACK(send), context_object);
    g_signal_connect_swapped(G_OBJECT(window), "destroy-event", G_CALLBACK(destroy_event), NULL);
    g_signal_connect_swapped(G_OBJECT(window), "delete-event", G_CALLBACK(delete_event), NULL);

    gtk_main();

    return 0;
}
