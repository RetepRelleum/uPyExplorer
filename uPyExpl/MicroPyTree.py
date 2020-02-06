
from tkinter import *
from tkinter import simpledialog as sdg
from tkinter.ttk import *
import _thread

import os

class MicroPyTree(Treeview):
    def __init__(self, master, replCon, **kw):
        super().__init__(master=master, columns=("one", "two"))

        self.replCon=replCon
 
        self.__unixTree=''


        self.column("#0", width=270, minwidth=270, stretch=NO)
        self.column("one", width=150, minwidth=150, stretch=NO)
        self.column("two", width=400, minwidth=200)

        self.heading("#0", text="Name", anchor=W)
        self.heading("one", text="Size", anchor=W)
        self.heading("two", text="Type", anchor=W)

        self.bind("<Double-1>", self.OnDoubleClick)
        self.bind("<Button-3>", self.popup)

        self.contextMenu = Menu(None, tearoff=0, takefocus=0)
        self.contextMenu.add_command(label="MkDir", command=self.mkDir)
        self.contextMenu.add_command(label="RmDir", command=self.rmDir)
        self.contextMenu.add_command(label="Remove File", command=self.rmFile)
        self.contextMenu.add_command(label="Refresh", command=self.getPlatform)
        self.contextMenu.add_command(label="Display", command=self.display)
        self.contextMenu.add_command(label="Copy", command=self.copy)
        
        self.contextMenu.bind('<Leave>', self.leave)

    def setUnixTree(self,unixTree):
        self.__unixTree=unixTree

    def __mkDir(self, user_input, path):
        if not (user_input == None or user_input == ""):
            self.replCon.uPyWrite(" ")
            self.replCon.uPyWrite("uos.mkdir('{}/{}')".format(path, user_input))
            self.insert(self.selection()[0], "end",text=user_input, values=('', "Dir"))
            self.replCon.uPyWrite(" ",displ=True)

    def mkDir(self):
        path = self.getSelItemPath()
        user_input = sdg.askstring(
            "Dir Name?", "input new dir Name", parent=self)
        _thread.start_new_thread(self.__mkDir, (user_input, path))

    def __rmDir(self):
        path = self.getSelItemPath()
        self.replCon.uPyWrite(" ")
        self.replCon.uPyWrite("uos.rmdir('{}')".format(path))
        self.replCon.uPyWrite(" ",displ=True)
        self.delete(self.selection()[0])

    def rmDir(self):
        _thread.start_new_thread(self.__rmDir, ())

    def __rmFile(self):
        self.replCon.uPyWrite(" ")
        path = self.getSelItemPath()
        self.replCon.uPyWrite("uos.remove('{}')".format(path))
        self.replCon.uPyWrite(" ",displ=True)
        self.delete(self.selection()[0])

    def rmFile(self):
        _thread.start_new_thread(self.__rmFile, ())

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

    def leave(self, event):
        self.contextMenu.unpost()

    def getSelItemPath(self):
        item = self.selection()[0]
        t = self.item(item, "text")
        p = self.parent(item)
        while p:
            t = self.item(p, "text")+"/"+t
            p = self.parent(p)
        return t

    def OnDoubleClick(self, event):
        print("you clicked on", self.getSelItemPath())

   

    def fillTree(self, folder, dir):
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
                self.insert(folderx, "end",  text=data[0], values=(
                    '' if data[3] == 0 else data[3], "File"))
            else:
                foldery = self.insert(folderx, "end",  text=data[0], values=(
                    '' if data[3] == 0 else data[3], "Dir"))
                diry = "{}/{}".format(dirx, data[0])
                self.fillTree(foldery, diry)


    def getPlatform(self):
        _thread.start_new_thread(self._getPlatform, ())

    def _getPlatform(self):
        try:
            self.replCon.uPyWrite(" ")
            self.replCon.uPyWrite("import sys")
            self.replCon.uPyWrite("import ujson")
            self.replCon.uPyWrite("import os")

            platFormName = self.replCon.getCommadData("sys.platform")
            rootData = self.replCon.getCommadData("os.stat('/')")

            self.delete(*self.get_children())
            folder1 = self.insert('', 1,  text='', values=(
                "", platFormName, str(rootData[0])))
            self.selection_set(folder1)
            self.fillTree(folder1, '')    
            self.replCon.uPyWrite(" ",displ=True)
        except :
            rootData='not con'
            platFormName='not connected'
            folder1 = self.insert('', 1,  text=platFormName, values=("", "uPy Bord :-)", str(rootData[0])))
            self.selection_set(folder1)
            self.fillTree(folder1, '')
            self.replCon.uPyWrite(" ",displ=True)

    def selIsDir(self):
        return not self.item(self.selection()[0], "values")[1] == 'File'

    def copy(self):
        self.replCon._cpy=True
        _thread.start_new_thread(self.__display, ())

    def display(self):
        _thread.start_new_thread(self.__display, ())

    def __display(self):
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
        if self.replCon._cpy:
            item = self.selection()[0]
            fname = self.item(item, "text")
            pC = "{}/{}".format(os.getcwd(), fname)
            ft=self.replCon.getCommadData("runX()")
            f=open(pC,'wb')
            f.write(ft)
            f.close()
            self.replCon.uPyWrite(" ",displ=True)
        else:
            self.replCon.uPyWrite("runX()",displ=True)





