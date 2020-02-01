from tkinter import *
from tkinter import simpledialog as sdg
from tkinter import filedialog 
from tkinter.ttk import *

import uPyExpl.OptionValues
import json
import glob
import serial


class Option(Frame):
    def __init__(self, master,  kw=None):
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
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        #Serial -------

        self.label1=Label(self,text="USB Port:") 
        self.label1.grid(row=0, column=0, sticky="NEW", padx=2)
        self.e1=Combobox(self,values=self.serial_ports(),postcommand=self.serial_ports)
        self.e1.grid(row=0, column=1, sticky="NEW", padx=2)

        try:
            id=self.e1["values"].index(self.op.usb_port)
        except :
            id=0
        self.e1.current(id)

        # wrepl
        self.CheckVar1 = IntVar()

        self.CheckVar1.set(self.op.iSwRepl)
        self.C1 = Checkbutton(self, text = "WRep", variable = self.CheckVar1 ,onvalue = 1, offvalue = 0,command=self.wRepl)
        self.C1.grid(row=1, column=0, sticky="NEW", padx=2)
        self.wRepl()

        self.label3=Label(self,text="Host") 
        self.label3.grid(row=1, column=1, sticky="NEW", padx=2)
        # Tree

        self.label2=Label(self,text="Projekt Root") 
        self.label2.grid(row=2, column=0, sticky="NEW", padx=2)

        
        self.bu1=Button(self,text=self.op.path,command=self.getPath )
        self.bu1.grid(row=2, column=1, sticky="NEW", padx=2)

        # password 
        self.label4=Label(self,text="SSID") 
        self.label4.grid(row=4, column=0, sticky="NEW", padx=2)   

        self.c4=Combobox(self,values=self.serial_ports(),postcommand=self.serial_ports)    
        self.c4.grid(row=4, column=1, sticky="NEW", padx=2)   




        try:
            id=self.e1["values"].index(self.op.usb_port)
        except :
            id=0



        
        self.b1=Button(self,text="safe",command=self.safeOp)
        self.b1.grid(row=3, column=0, sticky="NEW", padx=2)

    def wRepl(self):
        self.op.iSwRepl=self.CheckVar1.get()



    def safeOp(self):
        f=open('uPyExplorer.json','w')

        self.op.usb_port=self.e1.get()
        json.dump(self.op,f,default=lambda o: o.__dict__, indent=4)
        f.close()

    def getPath(self):
        a=filedialog.askdirectory()
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


