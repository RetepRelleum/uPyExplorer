from tkinter import *
import uPyExplorer.Tab
import sys

def run():
    root = Tk()
    root.title('Micropython Explorer')
    root.geometry("600x400")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    tab_parent=uPyExplorer.Tab.Tab(root)
    root.mainloop()     

