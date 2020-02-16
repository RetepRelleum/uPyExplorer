import os

class OptionValues(object):
    def __init__(self,usb_port:str='',path:str=os.getcwd(),isSilence:bool=True):
        self.usb_port=usb_port
        if path=='':
            path=os.getcwd()
        self.path=path
        self.isSilence=isSilence
        
    @classmethod
    def from_json(cls, data):
        return cls(**data)