
from tkinter import *
from tkinter.ttk import *
import uPyExpl.Screen
import uPyExpl.Option
import uPyExpl.ReplCon
import uPyExpl.Info

class Tab(Notebook):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.tabFrom='Option'

        self.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)
        self.option=uPyExpl.Option.Option(self)
        
        self.replCon=uPyExpl.ReplCon.ReplCon(self.option.getOptionValues())
        self.screen=uPyExpl.Screen.Screen(self,self.replCon,self.option.getOptionValues())
        self.info=uPyExpl.Info.Info(self,self.replCon)
        self.add(self.screen, text="Screen")  
        self.add(self.option, text="Options")
        self.add(self.info, text="Info")

    
        
        self.bind("<<NotebookTabChanged>>", self.notebookTabChanged)
    
    def notebookTabChanged(self, event):
        if self.select()==self.option._w:
            self.tab(2,state="hidden")
            if self.tabFrom=='Screen':
                self.screen.focusOut()
                self.replCon.closeConnection()
            elif self.tabFrom=='Info':
                self.screen.focusOut()
                self.replCon.closeConnection()
            self.tabFrom='Option'
            
        if  self.select()==self.screen._w:
            self.tab(2,state="normal")
            if self.tabFrom=='Option':
                self.option.safeOp()
                self.replCon.updateConnection(self.option.getOptionValues())
                self.screen.focusIn()
            elif self.tabFrom=='Info':
                pass
            self.tabFrom='Screen'

        if  self.select()==self.info._w:
            if self.tabFrom=='Screen':
               pass
            elif self.tabFrom=='Option':
                self.option.safeOp()
                self.replCon.updateConnection(self.option.getOptionValues())
                self.screen.focusIn()
            self.info.focusIn()
            self.tabFrom='Info'


