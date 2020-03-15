
from tkinter import *
from tkinter.ttk import *
import uPyExplorer.Terminal
import uPyExplorer.MicroPyTree
import uPyExplorer.UnixPyTree

class Screen(Frame):
    def __init__(self, master, replCon,option, kw=None):
        super().__init__(master,  kw=kw)
        self.option=option
        self.replCon=replCon
        self.master=master
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

#        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(3, weight=2)

        self.terminal = uPyExplorer.Terminal.Terminal(self, replCon)
        self.terminal.grid(row=3, column=0, sticky="NSEW", columnspan=2, padx=5, pady=5)
    
        self.unixTree = uPyExplorer.UnixPyTree.UnixPyTree(self,replCon,self.option,self.terminal)
        self.unixTree.grid(row=1, column=0, columnspan=1,sticky="NSEW", padx=5)

        self.tree = uPyExplorer.MicroPyTree.MicroPyTree(self, self.replCon)
        self.tree.grid(row=1, column=1, sticky="NSEW",columnspan=1, padx=5)

        self.tree.setOtherTree(self.unixTree)
        self.unixTree.setOtherTree(self.tree)

        self.unixTree.frame.grid(row=0, sticky="W",column=0,  padx=5)
        self.tree.frame.grid(row=0, sticky="W",column=1,  padx=5)

        

        

    def focusIn(self):
        self.terminal.startSerialRead()
        self.unixTree.getPlatform()
        self.tree.getPlatform()


    def focusOut(self):
        self.terminal.stopSerialRead()
       

