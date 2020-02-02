
from tkinter import *
from tkinter import simpledialog as sdg
from tkinter.ttk import *
import _thread
import os

class UnixPyTree(Treeview):
    def __init__(self, master, upTree, terminal,option, **kw):
        super().__init__(master=master, columns=("one", "two"))
        self._upTree = upTree
        self._terminal=terminal
        self.option=option

        self.column("#0", width=270, minwidth=270, stretch=NO)
        self.column("one", width=150, minwidth=150, stretch=NO)
        self.column("two", width=400, minwidth=200)

        self.heading("#0", text="Name", anchor=W)
        self.heading("one", text="Size", anchor=W)
        self.heading("two", text="Type", anchor=W)

        self.bind("<Button-3>", self.popup)
        self.contextMenu = Menu(None, tearoff=0, takefocus=0)
        self.contextMenu.add_command(label="Copy", command=self.copy)
        self.contextMenu.add_command(label="Display", command=self.display)
        self.contextMenu.bind('<Leave>', self.leave)

    def getPlatform(self):
        platFormName = sys.platform
        rootData = self.option.path
        self.delete(*self.get_children())
        folder1 = self.insert('', 1,  text=platFormName, values=(
            "", "root uPython Projekt :-)", str(rootData[0])))
        self.selection_set(folder1)
        self.fillTree(folder1, rootData)

    def fillTree(self, folder, dir):
        folderx = folder
        dirx = dir
        dataAll = []
        for dat in os.listdir(dir):
            data = os.stat("{}/{}".format(dirx, dat))
            if os.path.isfile("{}/{}".format(dirx, dat)):
                self.insert(folderx, "end",  text=dat, values=(
                    data.st_size, "File"))
            else:
                foldery = self.insert(folderx, "end",  text=dat, values=(
                    data.st_size, "Dir"))
                diry = "{}/{}".format(dirx, dat)
                self.fillTree(foldery, diry)

    def copy(self):
        _thread.start_new_thread(self._copy, ())

    def _copy(self):
        buffSize=40
        pC = "{}{}".format(self.option.path, self.getSelItemPath())
        pD = "{}/{}".format(self._upTree.getSelItemPath(),
                            pC[pC.rfind('/')+1:])
        self._terminal.uPyWriteln("f=open('{}','wb')".format(pD))
        f = open(pC, "rb")
        a = f.read(buffSize)
        while a:
            self._terminal.uPyWriteln("f.write({})".format(a))
            a = f.read(buffSize)
        self._terminal.uPyWriteln("f.close()")
        f.close()
        item = self.selection()[0]
        t = self.item(item, "text")
        self._upTree.insert(self._upTree.selection()[
                            0], "end",  text=t, values=('', "File"))

    def display(self):
        b = self._upTree._terminal.index(INSERT)
        self._upTree._terminal.insert(INSERT, '\n')
        path = '{}{}'.format(self.option.path, self.getSelItemPath())
        f = open(path, 'rb')
        a = f.readline()
        while a:
            self._upTree._terminal.insert(INSERT, a)
            a = f.readline()
        self._upTree._terminal.tag_add("here", b, INSERT)
        self._upTree._terminal.tag_config("here", foreground="blue")
        self._upTree._terminal.insert(INSERT, '\n')
        self._upTree._terminal.see(END)

    def popup(self, event):
        """action in event of button 3 on tree view"""
        # select row under mouse
        iid = self.identify_row(event.y)
        if iid:
            if self.item(iid, "values")[1] == 'File':
                self.contextMenu.entryconfig(1, state=NORMAL)
                if self._upTree.selIsDir():
                    self.contextMenu.entryconfig(0, state=NORMAL)

                else:
                    self.contextMenu.entryconfig(0, state=DISABLED)
            else:
                self.contextMenu.entryconfig(0, state=DISABLED)
                self.contextMenu.entryconfig(1, state=DISABLED)

            # mouse pointer over item
            self.selection_set(iid)
            self.contextMenu.post(event.x_root, event.y_root)
        else:
            # mouse pointer not over item
            # occurs when items do not fill frame
            # no action required
            pass

    def leave(self, event):
        self.contextMenu.unpost()

    def getSelItemPath(self):
        item = self.selection()[0]
        t = self.item(item, "text")
        p = self.parent(item)
        while p:
            t = self.item(p, "text")+"/"+t
            p = self.parent(p)
        t.find('/')
        return t[t.find('/'):]
