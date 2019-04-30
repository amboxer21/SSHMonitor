import tkinter

class SSHMonitorUI(object):

    def __init__(self):
        self.window = tkinter.Tk()

        self.window.geometry("%dx%d+%d+%d" % (330, 80, 200, 150))
        self.window.title("Breeds and Characteristics")

        self.display = None;

        self.data=['Successful','Failed','Banned']

    def selected(self,selected):
        self.display.config(text = selected)

    def menu(self):
        var = tkinter.StringVar()
        var.set('Successful')
        p = tkinter.OptionMenu(self.window, var, *self.data, command=self.selected)
        p.pack()

        self.display = tkinter.Label(self.window)
        self.display.pack()

        self.window.mainloop()

if __name__ == '__main__':
    SSHMonitorUI().menu()
