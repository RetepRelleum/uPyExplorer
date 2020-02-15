
from tkinter import *
from tkinter import simpledialog as sdg
from tkinter.ttk import *
import uPyExpl.Screen
import uPyExpl.Option
import uPyExpl.ReplCon

class Tab(Notebook):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)
        self.option=uPyExpl.Option.Option(self)
        
        self.replCon=uPyExpl.ReplCon.ReplCon(self.option.getOptionValues())
        self.screen=uPyExpl.Screen.Screen(self,self.replCon,self.option.getOptionValues())
        self.add(self.screen, text="Screen")  
        self.add(self.option, text="Options")


        self.bind("<<NotebookTabChanged>>", self.notebookTabChanged)
    
    def notebookTabChanged(self, event):
        if self.select()==self.option._w:
            self.screen.focusOut()
            self.replCon.closeConnection()
            
        if  self.select()==self.screen._w:
            self.option.safeOp()
            self.replCon.updateConnection(self.option.getOptionValues())
            self.screen.focusIn()
