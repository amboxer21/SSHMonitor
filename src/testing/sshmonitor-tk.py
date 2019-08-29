import Tkinter as tkinter

class SSHMonitorUI(object):

    def __init__(self):

        self.tk = tkinter.Tk()

        self.tk.geometry("%dx%d+%d+%d" % (330, 80, 200, 150))
        self.tk.title("SSHMonitor")


        canvas = tkinter.Canvas(self.tk, bg="white", width=500, height=300)
        canvas.pack(side="top", fill="both", expand=True)
        cid = canvas.create_text(10, 10, anchor="nw")

        canvas.itemconfig(cid, text="New SSH activity!")

    def menu(self):
        self.tk.mainloop()

if __name__ == '__main__':
    SSHMonitorUI().menu()
