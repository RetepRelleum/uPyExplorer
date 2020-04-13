from tkinter import *
from tkinter.ttk import *
import tkinter.simpledialog 
import _thread
from abc import ABC, abstractmethod
import uPyExplorer.buttonToolTyp
import os


class Tree(Treeview, ABC):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)

        self.column("#0", width=270, minwidth=270, stretch=NO)
        self.column("one", width=150, minwidth=150, stretch=NO)
        self.column("two", width=400, minwidth=200)

        self.heading("#0", text="Name", anchor=W)
        self.heading("one", text="Size", anchor=W)
        self.heading("two", text="Type", anchor=W)
        self.bind("<Button-3>", self.popup)
        self.bind("<<TreeviewSelect>>", self.sele)

        self.contextMenu = Menu(None, tearoff=0, takefocus=0)
        self.contextMenu.add_command(label="MkDir", command=self.mkDir)
        self.contextMenu.add_command(label="RmDir", command=self.rmDir)
        self.contextMenu.add_command(label="Remove File", command=self.rmFile)
        self.contextMenu.add_command(label="Refresh", command=self.getPlatform)
        self.contextMenu.add_command(label="Display", command=self.display)
        self.contextMenu.add_command(label="Copy", command=self.copy)
        self.contextMenu.bind('<Leave>', self.leave)

        self.folder1 = self.insert('', 1,  text='not con', values=("", "uPy Bord :-)", 'not con'))

        self.frame=Frame(master=master)

        base_folder = os.path.dirname(__file__)

        self.bildRefresh = tkinter.PhotoImage(file="{}/Refresh.png".format(base_folder))
        self.bRefresh= uPyExplorer.buttonToolTyp.ButtonToolTip(self.frame,  command=self.getPlatform,image=self.bildRefresh ,toolTip="Refresh")
        self.bRefresh.grid(row=0,column=1 )
        self.bildDispl = tkinter.PhotoImage(file="{}/Displ.png".format(base_folder))
        self.bDispl= uPyExplorer.buttonToolTyp.ButtonToolTip(self.frame,  command=self.display,image=self.bildDispl,toolTip="Display File")
        self.bDispl.grid(row=0,column=2 )
        self.bildCopy= tkinter.PhotoImage(file="{}/Copy.png".format(base_folder))
        self.bCopy= uPyExplorer.buttonToolTyp.ButtonToolTip(self.frame,  command=self.copy,image=self.bildCopy,toolTip="Copy File")
        self.bCopy.grid(row=0,column=3 )
        self.bildMkDir = tkinter.PhotoImage(file="{}/MkDir.png".format(base_folder))
        self.bMkDir= uPyExplorer.buttonToolTyp.ButtonToolTip(self.frame,  command=self.mkDir,image=self.bildMkDir ,toolTip="MkDir")
        self.bMkDir.grid(row=0,column=4)
        self.bildRmDir = tkinter.PhotoImage(file="{}/RmDir.png".format(base_folder))
        self.bRmDir= uPyExplorer.buttonToolTyp.ButtonToolTip(self.frame,  command=self.rmDir,image=self.bildRmDir,state=DISABLED ,toolTip="RmDir")
        self.bRmDir.grid(row=0,column=5)
        self.bildDelFile = tkinter.PhotoImage(file="{}/DelFile.png".format(base_folder))
        self.bDelFile= uPyExplorer.buttonToolTyp.ButtonToolTip(self.frame,  command=self.rmFile,image=self.bildDelFile ,toolTip="Delete File")
        self.bDelFile.grid(row=0,column=6)


    @abstractmethod
    def sele(self,event):
        item = self.selection()[0]
        if self.item(item,"value")[1]=='File':
            self.bMkDir.config(state=DISABLED)
            self.bRmDir.config(state=DISABLED)
            self.bDelFile.config(state=NORMAL)
            self.bDispl.config(state=NORMAL)
            self.bCopy.config(state=NORMAL)
        else:
            self.bMkDir.config(state=NORMAL)
            a = self.get_children(item)
            if len(a) == 0:
                self.bRmDir.config(state=NORMAL)   
            else:
                self.bRmDir.config(state=DISABLED) 
            self.bDelFile.config(state=DISABLED)
            self.bDispl.config(state=DISABLED)
            self.bCopy.config(state=DISABLED)
                    


    
    def setOtherTree(self,otherTree):
        self._otherTree=otherTree

    def mkDir(self):
        path = self.getSelItemPath()
        user_input = tkinter.simpledialog.askstring(
            "Dir Name?", "input new dir Name", parent=self)
        if not (user_input == None or user_input == ""):
            _thread.start_new_thread(self._mkDir, (user_input, path))

    @abstractmethod
    def _mkDir(self, user_input, path):
        self.insert(self.selection()[0], "end",text=user_input, values=('', "Dir"))

    def rmDir(self):
        _thread.start_new_thread(self._rmDir, ())

    @abstractmethod
    def _rmDir(self):
        self.delete(self.selection()[0])

    def rmFile(self):
        _thread.start_new_thread(self._rmFile, ())

    @abstractmethod
    def _rmFile(self):
        self.delete(self.selection()[0])

    def getPlatform(self):
        self.delete(*self.get_children())
        _thread.start_new_thread(self._getPlatform, ())

    @abstractmethod
    def _getPlatform(self):
        self.fillTree(self.folder1, self.rootData)
        self.item(self.folder1, open = True)
        self.selection_set(self.folder1)

    def display(self):
        _thread.start_new_thread(self._display, ())

    @abstractmethod
    def _display(self):
        pass

    def copy(self):
        _thread.start_new_thread(self._copy, ())
    
    @abstractmethod
    def _copy(self):
        item = self.selection()[0]
        t = self.item(item, "text")
        self._otherTree.insert(self._otherTree.selection()[0], "end",  text=t, values=('', "File"))

    def popup(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.identify_row(event.y)
        if iid:
            if self.item(iid, "values")[1] == 'File':
                self.contextMenu.entryconfig(0, state=DISABLED)
                self.contextMenu.entryconfig(1, state=DISABLED)
                self.contextMenu.entryconfig(2, state=NORMAL)
                self.contextMenu.entryconfig(4, state=NORMAL)
                self.contextMenu.entryconfig(5, state=NORMAL)
            else:
                self.contextMenu.entryconfig(0, state=NORMAL)
                a = self.get_children(iid)
                if len(a) == 0:
                    self.contextMenu.entryconfig(1, state=NORMAL)
                else:
                    self.contextMenu.entryconfig(1, state=DISABLED)
                self.contextMenu.entryconfig(2, state=DISABLED)
                self.contextMenu.entryconfig(4, state=DISABLED)
                self.contextMenu.entryconfig(5, state=DISABLED)
            # mouse pointer over item
            self.selection_set(iid)
            self.contextMenu.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def getSelItemPath(self, file=True):
        item = self.selection()[0]
        if file or self.item(item, "value")[1] != 'File':
            path = self.item(item, "text")
        else:
            path = ''
        p = self.parent(item)
        while p:
            path = self.item(p, "text")+"/"+path
            p = self.parent(p)
        return path

    def leave(self, event):
        self.contextMenu.unpost()
