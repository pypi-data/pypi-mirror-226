from tkinter import *

root = Tk()


def readmeopen():
    new_win = Toplevel()
    new_help_label = Label(new_win , text="This application is in progress, the windows emulator will be released soon. This means you can't use  this (YEET)")
    new_help_label.pack()
def windownew():
    os_win = Toplevel()
    file_readme = Button(os_win, text="File: README.md",command=readmeopen)
    file_readme.pack()

    
 


button = Button(root, text="Start OS",command=windownew, width='30', height='20')
button.pack()


root.mainloop()
