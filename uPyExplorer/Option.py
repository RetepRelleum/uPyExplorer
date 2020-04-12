from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog

import uPyExplorer.OptionValues
import json
import glob
import serial
import time

class Option(Frame):
    def __init__(self, master, kw=None):
        super().__init__(master,  kw=kw)
        f=None
        try:
            f= open('uPyExplorer.json','rb') 
        except :
            pass
 
        try:
            self.op=uPyExplorer.OptionValues.OptionValues.from_json(json.load(f))
        except :
            self.op=uPyExplorer.OptionValues.OptionValues()
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
   
        #Serial -------
        row=0
        self.label1=Label(self,text="USB Port:") 
        self.label1.grid(row=row, column=0, sticky="EW", padx=2)
        self.e1=Combobox(self,values=self.serial_ports(),postcommand=self.serial_ports)
        self.e1.grid(row=row, column=1, sticky="WE", padx=2,columnspan=2)

        try:
            id=self.e1["values"].index(self.op.usb_port)           
        except :
            id=0
        try:
            self.e1.current(id)
        except :
            pass

        # Tree
        row+=1

        self.label2=Label(self,text="Projekt Root") 
        self.label2.grid(row=row, column=0, sticky="EW", padx=2)
        self.bu1=Button(self,text=self.op.path,command=self.getPath )
        self.bu1.grid(row=row, column=1, sticky="W", padx=2,columnspan=4)

        # Silence
        row+=1
                
        self.isSilence = IntVar()
        self.isSilence.set(self.op.isSilence)
        self.C2 = Checkbutton(self, text = "Silence", variable = self.isSilence ,onvalue = 1, offvalue = 0,command=self.silence)
        self.C2.grid(row=row, column=0, sticky="EW", padx=2)
        self.silence()

    def  silence(self):
        self.op.isSilence=self.isSilence.get()

    def safeOp(self):
        try:
            self.op.usb_port=self.e1.get()
            f=open('uPyExplorer.json','w')
            json.dump(self.op,f,default=lambda o: o.__dict__, indent=4)
            f.close()
        except :
            pass
 
    def getPath(self):
        a=tkinter.filedialog.askdirectory(initialdir=self.op.path)
        if a:
            self.op.path=a
            self.bu1.configure(text=a)

    def serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port,baudrate=115200,timeout=0.01)
                s.write(b"\x03\r\n")
                time.sleep(0.1)
                s.reset_input_buffer()
                s.write(b"import machine\r\n")
                s.write(b"machine.unique_id()\r\n")
                time.sleep(0.1)
                a=""
                while s.inWaiting() :
                    a+=s.read().decode()
                    b=5
                b=a.split("\r\n")
                s.close()
                if a.endswith(">>> "):
                    result.append((port,b[2]))
            except (OSError, serial.SerialException):
                pass
        if hasattr(self,"e1"):
            self.e1["values"]=result
        return result

    def getOptionValues(self):
        self.op.usb_port=self.e1.get()
        return self.op

    def handle_focusOut(self,event):
        self.safeOp()

