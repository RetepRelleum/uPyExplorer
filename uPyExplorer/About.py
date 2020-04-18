from tkinter import *
from tkinter.ttk import *
import webbrowser
import os


class About(Frame):
    def __init__(self, master, kw=None):
        super().__init__(master,  kw=kw)
        self.columnconfigure(0, weight=1)
        row=0        
        base_folder = os.path.dirname(__file__)
        self.tkimage = PhotoImage(file='{}/uPyExplorer.png'.format(base_folder))
        self.tkimage =self.tkimage.subsample(4) 
        self.limage=Label(self,image = self.tkimage)
        self.limage.image=self.tkimage
        self.limage.grid(row=row, column=0)
        row=row+1
        self.label0=Label(self,text=r"https://github.com/RetepRelleum/uPyExplorer", cursor="hand2",foreground="blue") 
        self.label0.bind("<Button-1>", self.callback)
        self.label0.grid(row=row, column=0)
        row=row+1
        self.label2=Label(self,text=r"https://pypi.org/project/uPyExplorer", cursor="hand2",foreground="blue") 
        self.label2.bind("<Button-1>", self.callback)
        self.label2.grid(row=row, column=0)
        row=row+1
        self.label3=Label(self,text="MIT License") 
        self.label3.grid(row=row, column=0)
        row=row+1
        self.label4=Label(self,text="Copyright (c) 2020 Peter Müller") 
        self.label4.grid(row=row, column=0)


    def callback(self,event):
        webbrowser.open_new(event.widget.cget("text"))
        