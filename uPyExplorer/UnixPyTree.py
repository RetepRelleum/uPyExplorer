
from tkinter import *
from tkinter.ttk import *
import os
import uPyExplorer.Tree

class UnixPyTree(uPyExplorer.Tree.Tree):
    def __init__(self, master, replCon, option, terminal, **kw):
        super().__init__(master=master, columns=("one", "two"))
        self._replCon = replCon
        self.option = option
        self.terminal = terminal

    def _mkDir(self, user_input, path):
        a = '{}/{}'.format(path, user_input)
        os.mkdir(a)
        super()._mkDir(user_input, path)

    def _rmDir(self):
        path = self.getSelItemPath()
        os.rmdir('{}'.format(path))
        super()._rmDir()

    def _rmFile(self):
        path = self.getSelItemPath()
        os.remove('{}'.format(path))
        super()._rmFile()

    def _getPlatform(self):
        platFormName = sys.platform
        self.rootData = self.option.path
        self.folder1 = self.insert('', 1,  text=self.option.path, values=(
            "", platFormName, str(self.rootData[0])))
        super()._getPlatform()


    def fillTree(self, folder, dir):
        folderx = folder
        dirx = dir
        for dat in os.listdir(dir):
            data = os.stat("{}/{}".format(dirx, dat))
            if os.path.isfile("{}/{}".format(dirx, dat)):
                self.insert(folderx, "end",  text=dat,values=(data.st_size, "File"))
            else:
                foldery = self.insert(folderx, "end",  text=dat, values=("", "Dir"))
                diry = "{}/{}".format(dirx, dat)
                self.fillTree(foldery, diry)

    def _display(self):
        b = self.terminal.index(INSERT)
        self.terminal.insert(INSERT, '\n')
        path = self.getSelItemPath()
        f = open(path, 'rb')
        a = f.readline()
        while a:
            self.terminal.insert(INSERT, a)
            a = f.readline()
        self.terminal.tag_add("here", b, INSERT)
        self.terminal.tag_config("here", foreground="blue")
        self.terminal.insert(INSERT, '\n')
        self.terminal.see(END)

    def _copy(self):
        buffSize = 40
        pC = self.getSelItemPath()
        pD = "{}/{}".format(self._otherTree.getSelItemPath(file=False),
                            pC[pC.rfind('/')+1:])
        self._replCon.uPyWrite("f=open('{}','wb')".format(pD))
        f = open(pC, "rb")
        a = f.read(buffSize)
        while a:
            self._replCon.uPyWrite("f.write({})".format(a))
            a = f.read(buffSize)
        self._replCon.uPyWrite("f.close()")
        f.close()
       
        super()._copy()

    def sele(self,event):
        super().sele(event)

