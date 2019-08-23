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

int masquerade(char *username, char *command) {

    char *path = getenv("PATH");
    ssize_t psize = strlen(path) + sizeof("PATH=");

    char pathenv[psize];
    snprintf(pathenv, psize, "PATH=%s", path);

    char *envp[] = {pathenv, NULL};
    char *arguments[] = {"sudo", "-i", "su", (char *)username, "-c", WHOAMI, NULL};

    return execvpe(arguments[0], arguments, envp);

}

static void destroy_event(GtkWidget *widget, gpointer data) {
  gtk_main_quit();
}

static gboolean delete_event(GtkWidget *widget, GdkEvent *event, gpointer data) {
  gtk_main_quit();
  return FALSE;
}

int main(int argc, char *argv[]) {

    GtkWidget *view;
    GtkWidget *table;
    GtkWidget *window;
    GtkWidget *scrolledwindow;

    gchar *text;

    GtkTextBuffer *buffer;

    GtkTextIter start, iter, end;

    gtk_init(&argc, &argv);

    window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    gtk_window_set_title(GTK_WINDOW(window), NULL);
    gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER);
    gtk_window_set_default_size(GTK_WINDOW(window), 300, 100);
    gtk_widget_show(window);

    table = gtk_table_new(10, 10, TRUE);
    gtk_container_add(GTK_CONTAINER(window), table);
    gtk_widget_show(table);

    view = gtk_text_view_new();
    gtk_widget_show(view);

    scrolledwindow = gtk_scrolled_window_new(NULL, NULL);
    gtk_scrolled_window_set_shadow_type(GTK_SCROLLED_WINDOW(scrolledwindow), GTK_SHADOW_IN);
    gtk_container_add(GTK_CONTAINER(scrolledwindow), view);
    gtk_table_attach_defaults(GTK_TABLE(table), scrolledwindow, 0, 10, 0, 10);
    gtk_widget_show(scrolledwindow);

    buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(view));
    gtk_text_buffer_get_bounds(buffer, &start, &end);

    gtk_text_buffer_get_start_iter(buffer, &iter);
    gtk_text_buffer_insert(buffer, &iter, "TEST", -1);

    //g_signal_connect_swapped(G_OBJECT(quit), "activate", G_CALLBACK(gtk_main_quit), NULL);
    //g_signal_connect(G_OBJECT(button), "button_press_event", G_CALLBACK(callback), NULL);
    //g_signal_connect(G_OBJECT(button), "clicked", G_CALLBACK(send), context_object);
    g_signal_connect_swapped(G_OBJECT(window), "destroy-event", G_CALLBACK(destroy_event), NULL);
    g_signal_connect_swapped(G_OBJECT(window), "delete-event", G_CALLBACK(delete_event), NULL);

    gtk_main();

    return 0;
}
