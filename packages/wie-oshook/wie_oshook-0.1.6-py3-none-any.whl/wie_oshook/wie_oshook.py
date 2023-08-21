from tkinter import *

root = Tk()


def READMEOPEN():
    new_win = Toplevel()
    new_help_label = Label(new_win , text="This application is in progress, the windows emulator will be released soon. This means you can't use  this (YEET)")
    new_help_label.pack()
def OS_window():
    os_win = Toplevel()
    file_readme = Button(os_win, text="File: README.md",command=READMEOPEN)
def OS():
    button = Button(root, text="Start OS",command=OS_window)
 

def start():
    OS()
    root.mainloop()
