
from tkinter import *
from tkinter.ttk import *
import _thread
import time


class Terminal(Text):
    def __init__(self, master, replCon):
        super().__init__(master)
        self.replCon=replCon
        self.keyInput = False
        self.bind("<Key>", self.key)
        self.bind("<ButtonRelease-1>", self.setCursorPos)
        self._timeStamp=0.0
        self.bind("<Button-3>", self.popup)
        self.contextMenu = Menu(None, tearoff=0, takefocus=0)
        self.contextMenu.add_command(label="Clear", command=self.dele)
        self.contextMenu.bind('<Leave>', self.leave)
        self._socket=None
        self._reread=0
        self.__serialRead=True


    def popup(self, event):
        self.contextMenu.entryconfig(0, state=NORMAL)
        self.contextMenu.post(event.x_root, event.y_root)

    def leave(self, event):
        self.contextMenu.unpost()
    
    def startSerialRead(self):
        self.__serialRead=True
        _thread.start_new_thread(self.readSerial, (self.replCon,))


    def stopSerialRead(self):
        self.__serialRead=False    
        self.replCon.uPyWrite(" ",wait=False)

    def readSerial(self, replCon):
        while self.__serialRead:
            try:
                char=replCon.uPyRead() 
                self._readLine(char)
            except :
                self.__serialRead=False
            
    def _readLine(self, b): 
        if b:
            self._timeStamp=time.time()
            if self._reread>0:
                self._reread=self._reread-1   
            else:
                self.see(END)
                a = str(b,encoding='UTF-8',errors="replace")
                self.mark_set(INSERT, END)
                a = a.replace('\r', '', -1)
                if a == '\x1b':
                    self._reread=2
                else:
                    if self.keyInput:
                        pass
                    else:
                        self.insert(END, a)
                    self.keyInput = False
        
    def key(self, event):
        self.keyInput = True
        command=event.char.encode()
        self.replCon.uPyWrite(command,end='',wait=False,displ=True)

    def setCursorPos(self, event):
        self.mark_set("insert", 'end')

    def dele(self):
        self.delete(1.0, END)
        self.replCon.uPyWrite(" ",displ=True)

