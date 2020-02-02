
from tkinter import *
from tkinter import simpledialog as sdg
from tkinter.ttk import *
import serial
import uPyExpl.Screen
import uPyExpl.Option
import uPyExpl.ReplCon




if __name__ == "__main__":
    


    root = Tk()
    root.title('Micropython Explorer')
    root.geometry("600x400")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    tab_parent=Notebook(root)

    tab_parent.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

    option=uPyExpl.Option.Option(tab_parent)
    replCon=uPyExpl.ReplCon.ReplCon(option.getOptionValues())
    screen=uPyExpl.Screen.Screen(tab_parent,replCon,option.getOptionValues())

    tab_parent.add(option, text="Options")

    tab_parent.add(screen, text="Screen")  
    menubar = Menu(root)
    menubar.add_command(label="Quit!", command=root.quit)
    root.config(menu=menubar)
    root.mainloop()


