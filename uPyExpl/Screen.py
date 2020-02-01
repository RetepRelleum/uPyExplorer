
from tkinter import *
from tkinter import simpledialog as sdg
from tkinter.ttk import *
import uPyExpl.Terminal
import uPyExpl.MicroPyTree
import uPyExpl.UnixPyTree


class Screen(Frame):
    def __init__(self, master, ser, kw=None):
        super().__init__(master,  kw=kw)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.terminal = uPyExpl.Terminal.Terminal(self, ser)
        self.terminal.grid(row=1, column=0, sticky="NSEW", columnspan=2, padx=5, pady=5)

        self.tree = uPyExpl.MicroPyTree.MicroPyTree(self, self.terminal)
        self.tree.grid(row=0, column=1, sticky="NSEW", padx=5)

        self.unixTree = uPyExpl.UnixPyTree.UnixPyTree(self, self.tree,self.terminal)
        self.unixTree.grid(row=0, column=0, sticky="NSEW", padx=5)
        self.tree.setUnixTree(self.unixTree)
        self.unixTree.getPlatform()
        self.tree.getPlatform()