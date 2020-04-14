from tkinter import *
from tkinter.ttk import *
import tkinter.simpledialog 
import uPyExplorer.Tree
import os
import _thread


class MicroPyTree(uPyExplorer.Tree.Tree):
    def __init__(self, master, replCon, **kw):
        super().__init__(master=master, columns=("one", "two"))
        self.replCon=replCon 
        base_folder = os.path.dirname(__file__)
        self.bildRun = tkinter.PhotoImage(file="{}/Run.png".format(base_folder))
        self.bRun= uPyExplorer.buttonToolTyp.ButtonToolTip(self.frame,  command=self.run,image=self.bildRun ,toolTip="Run")
        self.bRun.grid(row=0,column=7)

    def sele(self,event):
        item = self.selection()[0]
        if self.item(item,"text").lower().endswith('.py'):
            self.bRun.config(state=NORMAL)
        else:
            self.bRun.config(state=DISABLED)
        super().sele(event)

    def run(self):
        _thread.start_new_thread(self._run, ())
    
    def _run(self):
        item = self.selection()[0]
        path=self.getSelItemPath()
        self.replCon.uPyWrite("exec(open('{}').read())".format(path),displ=True)

    def _mkDir(self, user_input, path):
        self.replCon.uPyWrite(" ")
        self.replCon.uPyWrite("uos.mkdir('{}/{}')".format(path, user_input))
        super()._mkDir(user_input, path)
        self.replCon.uPyWrite(" ",displ=True)
        
    def _rmDir(self):
        path = self.getSelItemPath()
        self.replCon.uPyWrite(" ")
        self.replCon.uPyWrite("uos.rmdir('{}')".format(path))
        super()._rmDir()
        self.replCon.uPyWrite(" ",displ=True)

    def _rmFile(self):
        self.replCon.uPyWrite(" ")
        path = self.getSelItemPath()
        self.replCon.uPyWrite("uos.remove('{}')".format(path))
        super()._rmFile()
        self.replCon.uPyWrite(" ",displ=True)

    def _getPlatform(self):
        if hasattr (self.replCon,"_serial"):
            self.replCon.uPyWrite(" ")
            self.replCon.uPyWrite("import sys")
            self.replCon.uPyWrite("import ujson")
            self.replCon.uPyWrite("import os")
            platFormName = self.replCon.getCommadData("sys.platform")
            self.rootData = self.replCon.getCommadData("os.stat('/')")
            self.folder1 = self.insert('', 1,  text='', values=("", platFormName, str(self.rootData[0])))
            self.replCon.uPyWrite(" ",displ=True)
        else:
            self.folder1 = self.insert('', 1,  text='not con', values=("", "uPy Bord :-)", 'not con'))
        self.rootData=''
        super()._getPlatform()

        
    def fillTree(self, folder, dir):
        if hasattr (self.replCon,"_serial"):
            folderx = folder
            dirx = dir
            dataAll = []
            self.replCon.uPyWrite("itr=uos.ilistdir('{}')".format(dirx))  
            count = self.replCon.getCommadData("sum(1 for _ in itr)")
            self.replCon.uPyWrite("itr=uos.ilistdir('{}')".format(dirx))  
            for x in range(count):
                dataAll.append(self.replCon.getCommadData("next(itr)"))
            for data in dataAll:
                if len(data) == 3:
                    data.append(0)
                if data[1] == 0x8000:
                    self.insert(folderx, "end",  text=data[0], values=('' if data[3] == 0 else data[3], "File"))
                else:
                    foldery = self.insert(folderx, "end",  text=data[0], values=('' if data[3] == 0 else data[3], "Dir"))
                    diry = "{}/{}".format(dirx, data[0])
                    self.fillTree(foldery, diry)

    def _display(self,cpy=False):
        self.replCon.uPyWrite(" ")
        path = self.getSelItemPath()
        self.replCon.uPyWrite("def runX():")
        self.replCon.uPyWrite("f = open('{}', 'r')".format(path))
        self.replCon.uPyWrite("a = f.readline()")
        self.replCon.uPyWrite("while a:") 
        self.replCon.uPyWrite("print(a,end = '')")
        self.replCon.uPyWrite("a = f.readline()")
        self.replCon.uPyWrite('\b')
        self.replCon.uPyWrite("print('')")    
        self.replCon.uPyWrite("\b")
        self.replCon.uPyWrite("\b")
        if cpy:
            item = self.selection()[0]
            fname = self.item(item, "text")
            pC = "{}/{}".format(self._otherTree.getSelItemPath(file=False), fname)
            ft=self.replCon.getCommadData("runX()",cpy=True)
            f=open(pC,'wb')
            f.write(ft)
            f.close()
            self.replCon.uPyWrite(" ",displ=True)
        else:
            self.replCon.uPyWrite("runX()",displ=True)
    
    def _copy(self):
        self._display(cpy=True)
        super()._copy()








