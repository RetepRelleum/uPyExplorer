from tkinter import *
import uPyExplorer.Tab
import sys
import platform
import os

def run():
    root = Tk()
    root.title('Micropython Explorer')
    root.geometry("600x400")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    tab_parent=uPyExplorer.Tab.Tab(root)
    root.title("uPyExplorer")   
    base_folder = os.path.dirname(__file__)
    if  platform.system()=="Linux":
        root.iconbitmap("@{}/uPyExplorer.xbm".format(base_folder))
    else:
        root.iconbitmap("{}/uPyExplorer.ico".format(base_folder))
       

    root.mainloop()     


