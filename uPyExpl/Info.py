from tkinter import *
from tkinter.ttk import *
import _thread
import time
class Info(Frame):
    def __init__(self, master,replCon, kw=None):
        super().__init__(master,  kw=kw) 
        self.replCon=replCon


    
    def focusIn(self):
        self.row=0
        _thread.start_new_thread(self._focusIn, ())
    
    def _focusIn(self):
        self.replCon.uPyWrite("import sys")
        self.addRow("sys.argv")
        self.addRow("sys.byteorder")
        self.addRow("sys.implementation")
        self.addRow("sys.maxsize")
        self.addRow("sys.modules")
        self.addRow("sys.path")
        self.addRow("sys.platform")
        self.addRow("sys.version")
        self.addRow("sys.version_info")
        self.addNl()
        self.replCon.uPyWrite("import uos")
        self.addRow("uos.uname()")
        self.addRow("uos.getcwd()")  
        self.addNl()
        self.replCon.uPyWrite("import utime") 
        self.addRow("utime.localtime()")     
        self.addRow("utime.ticks_ms()")  
        self.addRow("utime.ticks_us()")   
        self.addRow("utime.ticks_cpu()")    
        self.addRow("utime.time()") 
        self.addNl()
        self.replCon.uPyWrite("import machine") 
        self.addRow("machine.freq()")     
        self.addRow("machine.unique_id()") 
        self.addNl()
        self.replCon.uPyWrite("import micropython")          
        self.addRow("micropython.opt_level()")   
        self.addRow("micropython.mem_info()")    
        self.addRow("micropython.qstr_info()") 
        self.addRow("micropython.stack_use()")  
        self.addNl()
        self.replCon.uPyWrite("import network")         
        self.replCon.uPyWrite("nic = network.WLAN(network.STA_IF)")   
        self.addRow("nic.active()")   
        self.addRow("nic.scan()")   
        self.addRow("nic.status()")     

    def addRow(self,command):
        text="{} :".format(command)
        a=self.replCon.getCommadData(command)
        try:
            a=a.decode()
            a=a.replace('\r\n',' ')
        except:
            pass

        label1=Label(self,text=text) 
        label1.grid(row=self.row, column=0, sticky="EW", padx=2)

        label1=Label(self,text=a) 
        label1.grid(row=self.row, column=1, sticky="EW", padx=2,columnspan=4)
        self.row=self.row+1


    def addNl(self):
        label1=Label(self,text="") 
        label1.grid(row=self.row, column=0, sticky="EW", padx=2)
        self.row=self.row+1


