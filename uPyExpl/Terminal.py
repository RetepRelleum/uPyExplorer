
from tkinter import *
from tkinter import simpledialog as sdg
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
        self.startSerialRead()

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

    def readSerial(self, replCon):
        while self.__serialRead:
            try:
                char=replCon.uPyRead() 
                self._readLine(char)
            except :
                self.__serialRead=False
            

    def _readLine(self, b): 
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
        self.replCon.uPyWrite(command,end='',wait=false)

    def setCursorPos(self, event):
        self.mark_set("insert", 'end')

    def dele(self):
        self.delete(1.0, END)
        self.replCon.uPyWrite(" ")

    def webrepl(self):
        self.uPyWriteln("s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)")
        self.uPyWriteln("s.bind(('0.0.0.0', 10001))")
        self.uPyWriteln("s.listen(3)")
        self.uPyWrite("conn, addr = s.accept()")
        self.uPyWrite("conn.setblocking(False)")
        self.uPyWrite("conn.setsockopt(socket.SOL_SOCKET, 20, uos.dupterm_notify)")
        self.uPyWrite("print( addr) ")
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('192.168.1.119', 10001)
        self._socket.connect(server_address)
        self.uPyWriteln("uos.dupterm(conn)")
        time.sleep(1)
        while True:
            a=self._socket.recv(1)
            self._readLine(a)
