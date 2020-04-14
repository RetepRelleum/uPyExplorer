from tkinter import *
from tkinter.ttk import *
import webbrowser

class About(Frame):
    def __init__(self, master, kw=None):
        super().__init__(master,  kw=kw)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        #Serial -------
        row=0

        self.label2=Label(self,text=r"https://github.com/RetepRelleum/uPyExplorer", cursor="hand2",foreground="blue") 
        self.label2.bind("<Button-1>", self.callback)
        self.label2.grid(row=row, column=0)

    def callback(self,event):
        webbrowser.open_new(event.widget.cget("text"))
        