from tkinter import *
from tkinter.ttk import *
import _thread
import time
class Info(Frame):
    def __init__(self, master,replCon, kw=None):
        super().__init__(master,  kw=kw) 
        self.replCon=replCon
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.l=Listbox(self)
        self.l.grid(row=0, column=0, sticky="EWSN")
        self.ret=''
        self.row=0

    def focusIn(self):
        _thread.start_new_thread(self._focusIn, ())
    
    def _focusIn(self):
        self.row=0
        self.l.delete(0,'end')
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
        self.replCon.uPyWrite("from machine import Pin")
        x=0
        self.ret=1
        while type(self.ret)is int:
            self.replCon.uPyWrite("p{}=Pin({})".format(x,x))    
            self.addRow("p{}.value()".format(x)) 
            self.replCon.uPyWrite("del p{}".format(x))          
            x=x+1
        self.l.delete(self.row-1)
        self.row=self.row-1
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
        self.replCon.uPyWrite("del nic")          

 

    def addRow(self,command):


        a=self.replCon.getCommadData(command)
        self.ret=a
        try:
            a=a.decode()
            a=a.replace('\r\n',' ')
        except:
            pass

        text="{} : {}".format(command,a)
        self.l.insert(self.row,text)
        self.row+=1
        

    def addNl(self):
        text="{}  {}".format(' ',' ')
        self.l.insert(self.row,text)
        self.row+=1
        


