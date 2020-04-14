from tkinter import *
from tkinter.ttk import *
class About(Frame):
    def __init__(self, master, kw=None):
        super().__init__(master,  kw=kw)

   
        #Serial -------
        row=0
        self.label1=Label(self,text="USB Port:") 
        self.label1.grid(row=row, column=0, sticky="EW")