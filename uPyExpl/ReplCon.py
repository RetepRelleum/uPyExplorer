import socket
import serial
import time
import json

class ReplCon():
    def __init__(self,option):
        self.__option=option
        self._cpy=False
        self._webRepl=False
        self._prompt = False
        self._timeOut=1
        self._catch = False
        self._catchV = []
        self.__last = '    '
        try:
             self._serial=serial.Serial(self.__option.usb_port, baudrate=115200)
        except :
            pass
    
    def updateConnection(self):
        if not hasattr(self,"_serial"):
            self._serial=serial.Serial(self.__option.usb_port, baudrate=115200)

        if self._serial.name!=self.__option.usb_port:    
            self._serial.close()
            while self._serial.is_open:
                pass
            self._serial=serial.Serial(self.__option.usb_port, baudrate=115200)
            return True
        else:
            return False

       

    def uPyRead(self):
        b=self._serial.read()
        self.__uPyRead(b)
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

    def uPyWrite(self,command,end="\r\n",wait=True):
        self._prompt = True
        command="{}{}".format(command,end).encode()
        if  self._webRepl:
            if command:
                self._socket.send(command)
        elif hasattr(self,"_serial"):
            if command:
                self._serial.write(command)
        if wait:
            self.prompt()

    def getCommadData(self, command):
        self._catchV = b""
        self._catch = True
        self.uPyWrite("ujson.dumps({})".format(command))
        self._catch = False
        s1=self._catchV.find(b'\r\n')+3
        e1=self._catchV.find(b'\r\n>>> ',s1)-1
        ret = self._catchV[s1:e1]
        if self._cpy:
            return self._catchV[s1-1:e1-7]
        else:
            return json.loads(ret)

    def prompt(self):
        self._timeStamp=time.time() 
        while self._prompt:
            time.sleep(0.01)
            if time.time()-self._timeStamp>self._timeOut:
                break
