
from tkinter import *
from tkinter import simpledialog as sdg
from tkinter.ttk import *
import _thread

class MicroPyTree(Treeview):
    def __init__(self, master, terminal, **kw):
        super().__init__(master=master, columns=("one", "two"))

        self._terminal = terminal
 
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
            self._terminal.uPyWriteln("uos.mkdir('{}/{}')".format(path, user_input))
            self.insert(self.selection()[0], "end",text=user_input, values=('', "Dir"))

    def mkDir(self):
        path = self.getSelItemPath()
        user_input = sdg.askstring(
            "Dir Name?", "input new dir Name", parent=self)
        _thread.start_new_thread(self.__mkDir, (user_input, path))

    def __rmDir(self):
        path = self.getSelItemPath()
        self._terminal.uPyWriteln("uos.rmdir('{}')".format(path))
        self.delete(self.selection()[0])

    def rmDir(self):
        _thread.start_new_thread(self.__rmDir, ())

    def __rmFile(self):
        path = self.getSelItemPath()
        self._terminal.uPyWriteln("uos.remove('{}')".format(path))
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
        if t.find('/') == -1:
            t = ''
        return t[t.find('/'):]

    def OnDoubleClick(self, event):
        print("you clicked on", self.getSelItemPath())

   

    def fillTree(self, folder, dir):
        folderx = folder
        dirx = dir
        dataAll = []

        self._terminal.uPyWriteln("itr=uos.ilistdir('{}')".format(dirx))
        count = self._terminal.getCommadData("sum(1 for _ in itr)")
        self._terminal.uPyWriteln("itr=uos.ilistdir('{}')".format(dirx))  

        for x in range(count):
            dataAll.append(self._terminal.getCommadData("next(itr)"))
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
            self._terminal.uPyWriteln("")
            self._terminal.uPyWriteln("import sys")
            self._terminal.uPyWriteln("import ujson")
            self._terminal.uPyWriteln("import os")

            platFormName = self._terminal.getCommadData("sys.platform")
            rootData = self._terminal.getCommadData("os.stat('/')")

            self.delete(*self.get_children())
            folder1 = self.insert('', 1,  text=platFormName, values=(
                "", "uPy Bord :-)", str(rootData[0])))
            self.selection_set(folder1)

            self.fillTree(folder1, '')    
        except :
            rootData='not con'
            platFormName='not connected'
            folder1 = self.insert('', 1,  text=platFormName, values=("", "uPy Bord :-)", str(rootData[0])))
            self.selection_set(folder1)
            self.fillTree(folder1, '')

    def selIsDir(self):
        return not self.item(self.selection()[0], "values")[1] == 'File'

    

    def copy(self):
        self._cpy=True
        _thread.start_new_thread(self.__display, ())

    def display(self):
        _thread.start_new_thread(self.__display, ())

    def __display(self):
        path = self.getSelItemPath()
        self._terminal.uPyWriteln("def runX():")
        self._terminal.uPyWriteln("f = open('{}', 'r')".format(path))
        self._terminal.uPyWriteln("a = f.readline()")
        self._terminal.uPyWriteln("while a:") 
        self._terminal.uPyWriteln("print(a,end = '')")
        self._terminal.uPyWriteln("a = f.readline()")
        self._terminal.uPyWriteln('\b')
        self._terminal.uPyWriteln("print('')")    
        self._terminal.uPyWriteln("\b")
        self._terminal.uPyWriteln("\b")
        b =int( self._terminal.index(INSERT).split('.')[0])
        b = b+1
        b="{}.{}".format(b,0)
        if self._terminal._cpy:
            item = self.selection()[0]
            fname = self.item(item, "text")
            pC = "{}/{}".format(os.getcwd(), fname)

            ft=self.getCommadData("runX()")
            f=open(pC,'wb')
            f.write(ft)
            f.close()
        else:
            self._terminal.uPyWriteln("runX()")
        c =int( self._terminal.index(INSERT).split('.')[0])
        c="{}.{}".format(c,0)
        self._terminal.tag_add("here", b, c)
        self._terminal.tag_config("here", foreground="green")
        self._terminal.see(END)
        self._cpy=False

