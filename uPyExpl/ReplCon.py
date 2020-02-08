import socket
import serial
import time
import json

class ReplCon():
    def __init__(self,option):
        self._cpy=False
        self._webRepl=False
        self._prompt = False
        self._timeOut=2
        self._catch = False
        self._catchV = []
        self.__last = '    '
        self.__silence=False

    
    def updateConnection(self,option):
        self.__option=option
        self._serial=serial.Serial(self.__option.usb_port, baudrate=115200)
    
    def closeConnection(self):
        while self._prompt:
            time.sleep(0.001)
        if  hasattr(self,"_serial"):
            self._serial.close()
        a=4

    def uPyRead(self):
        b=self._serial.read()
        self.__uPyRead(b)
        if self.__silence:
            return b''
        else:
            return b

    def __uPyRead(self,b):
        a = str(b,encoding='UTF-8',errors="replace")
        self.__last += a
        self.__last = self.__last[1:]
        if self.__last == ">>> ":
            self._prompt = False
        if self.__last == "... ":
            self._prompt = False
        if self._catch:
            self._catchV+=b

    def uPyWrite(self,command,end="\r\n",wait=True,displ=False):
        time.sleep(0.02)
        self._prompt = True
        if displ:
            self.__silence=False
        else:
            self.__silence=self.__option.isSilence
        if not end=='':
            command="{}{}".format(command,end).encode()
        if  self._webRepl:
            if command:
                self._socket.send(command)
        elif hasattr(self,"_serial"):
            if command:
                self._serial.write(command)
        if wait:
            self.prompt()
        else:
            self._prompt=False

    def getCommadData(self, command):
        print('getCommadData command:',command )
        self._catchV = b""
        self._catch = True
        self.uPyWrite("ujson.dumps({})".format(command))
        self._catch = False
        s1=self._catchV.find(b'\r\n')+3
        e1=self._catchV.find(b'\r\n>>> ',s1)-1

        ret = self._catchV[s1:e1]
        print('getCommadData _catchV:',ret )
        if self._cpy:
            return self._catchV[s1-1:e1-7]
        else:
            return json.loads(ret)

    def prompt(self):
        self._timeStamp=time.time() 
        while self._prompt:
            time.sleep(0.01)
            if time.time()-self._timeStamp>self._timeOut:
                self.__silence=False
                break
        self.__silence=False
