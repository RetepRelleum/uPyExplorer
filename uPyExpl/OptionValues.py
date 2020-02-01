import os

class OptionValues(object):
    def __init__(self,usb_port:str='',path:str='',iSwRepl:bool=False):
        self.usb_port=usb_port
        if path=='':
            path=os.getcwd()
        self.path=path
        self.iSwRepl=iSwRepl


    @classmethod
    def from_json(cls, data):
        return cls(**data)