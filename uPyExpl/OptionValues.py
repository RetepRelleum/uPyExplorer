class OptionValues(object):
    def __init__(self,usb_port=str):
        self.usb_port=usb_port

    @classmethod
    def from_json(cls, data):
        return cls(**data)