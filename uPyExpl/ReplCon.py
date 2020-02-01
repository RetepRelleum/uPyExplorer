import socket
import serial


class ReplCon(serial.Serial):
    
    def __init__(self, family, type, proto, fileno):
        super().__init__(family, type, proto, fileno)
