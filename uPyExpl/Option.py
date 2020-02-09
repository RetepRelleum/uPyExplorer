from tkinter import *
from tkinter import simpledialog as sdg
from tkinter import filedialog 
from tkinter.ttk import *

import uPyExpl.OptionValues
import json
import glob
import serial
import socket


class Option(Frame):
    def __init__(self, master, kw=None):
        super().__init__(master,  kw=kw)
        f=None
        try:
            f= open('uPyExplorer.json','rb') 
        except :
            pass

        if f:
            self.op=uPyExpl.OptionValues.OptionValues.from_json(json.load(f))
        else:
            self.op=uPyExpl.OptionValues.OptionValues()
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, weight=1)
        self.columnconfigure(7, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)
        self.rowconfigure(11, weight=1)

        #Serial -------
        row=0
        self.label1=Label(self,text="USB Port:") 
        self.label1.grid(row=row, column=0, sticky="EW", padx=2)
        self.e1=Combobox(self,values=self.serial_ports(),postcommand=self.serial_ports)
        self.e1.grid(row=row, column=1, sticky="W", padx=2,columnspan=4)

        try:
            id=self.e1["values"].index(self.op.usb_port)
        except :
            id=0
        self.e1.current(id)

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


       

        # password 
        row+=1
        self.label4=Label(self,text="SSID") 
        self.label4.grid(row=row, column=0, sticky="EW", padx=2)   

        self.c4=Combobox(self,values=self.serial_ports(),postcommand=self.serial_ports)    
        self.c4.grid(row=row, column=1, sticky="W", padx=2,columnspan=4)  

        try:
            id=self.e1["values"].index(self.op.usb_port)
        except :
            id=0

    def  silence(self):
        self.op.isSilence=self.isSilence.get()

   
            

    def safeOp(self):
        f=open('uPyExplorer.json','w')
        self.op.usb_port=self.e1.get()
        json.dump(self.op,f,default=lambda o: o.__dict__, indent=4)
        f.close()

    def getPath(self):
        a=filedialog.askdirectory(initialdir=self.op.path)
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
                s = serial.Serial(port,baudrate=115200)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        if hasattr(self,"e1"):
            self.e1["values"]=result
        return result

    def getOptionValues(self):
        return self.op

    def handle_focusOut(self,event):
        self.safeOp()

