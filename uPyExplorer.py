
from tkinter import *
from tkinter import simpledialog as sdg
from tkinter.ttk import *
import serial
import uPyExpl.Screen
import uPyExpl.Option

port = '/dev/ttyUSB0'
ser=serial.Serial(port, baudrate=115200)

root = Tk()
root.title('Micropython Explorer')
root.geometry("600x400")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

tab_parent=Notebook(root)
tab_parent.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

screen=uPyExpl.Screen.Screen(tab_parent,ser)
option=uPyExpl.Option.Option(tab_parent)

tab_parent.add(screen, text="Screen")  
tab_parent.add(option, text="Options")



menubar = Menu(root)
menubar.add_command(label="Quit!", command=root.quit)
root.config(menu=menubar)
root.mainloop()