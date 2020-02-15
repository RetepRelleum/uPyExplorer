
from tkinter import *
from tkinter import simpledialog as sdg
from tkinter.ttk import *
import  uPyExpl.Tab




if __name__ == "__main__":

    root = Tk()
    root.title('Micropython Explorer')
    root.geometry("600x400")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    tab_parent=uPyExpl.Tab.Tab(root)

    menubar = Menu(root)
    menubar.add_command(label="Quit!", command=root.quit)
    root.config(menu=menubar)
    root.mainloop()

