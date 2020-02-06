import os

class OptionValues(object):
    def __init__(self,usb_port:str='',path:str=os.getcwd(),iSwRepl:bool=False,isSilence=True):
        self.usb_port=usb_port
        if path=='':
            path=os.getcwd()
        self.path=path
        self.iSwRepl=iSwRepl
        self.isSilence=isSilence


    @classmethod
    def from_json(cls, data):
        return cls(**data)