from tkinter import *

import  uPyExpl.Tab
import sys

if __name__ == "__main__":
    root = Tk()
    root.title('Micropython Explorer')
    root.geometry("600x400")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    tab_parent=uPyExpl.Tab.Tab(root)
    root.mainloop()    
