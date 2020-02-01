
from tkinter import *
from tkinter import simpledialog as sdg
from tkinter.ttk import *
import _thread
import time
import json

class Terminal(Text):
    def __init__(self, master, serial):
        super().__init__(master)
        self._serial =serial
        self.keyInput = False
        self.bind("<Key>", self.key)
        self.bind("<ButtonRelease-1>", self.setCursorPos)
        self._catch = False
        self._catchV = []
        self._prompt = False
        self.__last = '    '
        self._timeOut=30
        self.bind("<Button-3>", self.popup)
        self.contextMenu = Menu(None, tearoff=0, takefocus=0)
        self.contextMenu.add_command(label="Clear", command=self.dele)
        self.contextMenu.bind('<Leave>', self.leave)
        self._webRepl=False
        self._cpy=False
        self._socket=None
        self._reread=0
        _thread.start_new_thread(self.readSerial, (self._serial,))

    def popup(self, event):
        self.contextMenu.entryconfig(0, state=NORMAL)
        self.contextMenu.post(event.x_root, event.y_root)

    def leave(self, event):
        self.contextMenu.unpost()

    def readSerial(self, serial):
        while True:
            try:
                char=serial.read() 
                if not self._webRepl:
                    self._readLine(char)
            except:
                pass

    def _readLine(self, b): 
                if self._reread>0:
                    self._reread=self._reread-1   
                else:
                    self.see(END)
                    a = str(b,encoding='UTF-8',errors="replace")
                    self.__last += a
                    self.__last = self.__last[1:]
                    if self._catch:
                        self._catchV+=b
                    if self.__last == ">>> ":
                        self._prompt = False
                    if self.__last == "... ":
                        self._prompt = False
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
        self.__send(command)

    def setCursorPos(self, event):
        self.mark_set("insert", 'end')

    def prompt(self):
        a=time.time() 
        while self._prompt:
            time.sleep(0.01)
            if (time.time()-a>self._timeOut):
                break

    def __send(self,command):
        if  self._webRepl:
            if command:
                self._socket.send(command)
        else:
            self._serial.write(command)

    def dele(self):
        self.delete(1.0, END)
        command=b'\n\r'
        self.__send(command)



    def uPyWriteln(self, command):
        self._prompt = True
        command="{}\r\n".format(command).encode()
        self.__send(command)
        self.prompt()

    def uPyWrite(self, command):
        command="{}\r\n".format(command).encode()
        self.__send(command)

    def getCommadData(self, command):
        self._catchV = b""
        self._catch = True
        self.uPyWriteln(("ujson.dumps({})".format(command)))
        self._catch = False
        s1=self._catchV.find(b'\r\n')+3
        e1=self._catchV.find(b'\r\n>>> ',s1)-1
        ret = self._catchV[s1:e1]
        if self._cpy:
            return self._catchV[s1-1:e1-7]
        else:
            return json.loads(ret)

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
        self._webRepl=True
        while True:
            a=self._socket.recv(1)
            self._readLine(a)
