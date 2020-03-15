import serial
import time
import json
import sys

class ReplCon():
    def __init__(self,option):
        self._prompt = False
        self._timeOut=5
        self._catch = False
        self._catchV = []
        self.__last = '    '
        self.__silence=False

    def updateConnection(self,option):
        try:
            self.__option=option
            self._serial=serial.Serial(self.__option.usb_port.split()[0], baudrate=115200)
        except:
            pass
    
    def closeConnection(self):
        if  hasattr(self,"_serial"):
            time.sleep(0.01)
            self._serial.close()

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
        self.__last = '    '
        self._prompt = True
        if displ:
            self.__silence=False
        else:
            self.__silence=self.__option.isSilence
        if not end=='':
            command="{}{}".format(command,end).encode()
        if hasattr(self,"_serial"):
            if command:
                self._serial.write(command)
        if wait:
            self.prompt()
            self._prompt=False

    def getCommadData(self, command,cpy=False):
        self._catchV = b""
        self._catch = True
        self.uPyWrite("ujson.dumps({})".format(command))
        self._catch = False
        s1=self._catchV.find(b'\r\n')+3
        e1=self._catchV.find(b'\r\n>>> ',s1)-1
        ret = self._catchV[s1:e1]
        if cpy:
            return self._catchV[s1-1:e1-7]
        else:
            try:
                ret=json.loads(ret)
                
            except json.JSONDecodeError as jex :
                ret=self._catchV[s1:e1]
            return ret

    def prompt(self):
        self._timeStamp=time.time() 
        while self._prompt:
            time.sleep(0.01)
            if time.time()-self._timeStamp>self._timeOut:
                self.__silence=False
                break
        self.__silence=False
        