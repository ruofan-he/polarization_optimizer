from redpitaya.overlay.mercury import mercury as FPGA
from ..fpga_handler import overlay
import time
GPIO = FPGA.gpio

def is_nth_bit_set(num: int, n: int):
    if num & (1 << n):
        return True
    return False

class Pin_Assign:
    def __init__(self):
        self.CS  = ('p',0)
        self.RST = ('n',0)
        self.A0  = ('p',1)
        self.A1  = ('n',1)
        self.D1  = ('p',2)
        self.D2  = ('n',2)
        self.D3  = ('p',3)
        self.D4  = ('n',3)
        self.D5  = ('p',4)
        self.D6  = ('n',4)
        self.D7  = ('p',5)
        self.D8  = ('n',5)
        self.D9  = ('p',6)
        self.D10 = ('n',6)
        self.D11 = ('p',7)
        self.D12 = ('n',7)

pin_assign = Pin_Assign()

class Pin_Handler:
    def __init__(self):
        self.CS = GPIO(*pin_assign.CS,'out')
        self.RST = GPIO(*pin_assign.RST,'out')
        self.A = [
            GPIO(*pin_assign.A0,'out'),
            GPIO(*pin_assign.A1,'out')
            ]
        self.D = [
            GPIO(*pin_assign.D1,'out'),
            GPIO(*pin_assign.D2,'out'),
            GPIO(*pin_assign.D3,'out'),
            GPIO(*pin_assign.D4,'out'),
            GPIO(*pin_assign.D5,'out'),
            GPIO(*pin_assign.D6,'out'),
            GPIO(*pin_assign.D7,'out'),
            GPIO(*pin_assign.D8,'out'),
            GPIO(*pin_assign.D9,'out'),
            GPIO(*pin_assign.D10,'out'),
            GPIO(*pin_assign.D11,'out'),
            GPIO(*pin_assign.D12,'out')
        ]

        self.CS.write(True)
        self.RST.write(True)
        self.set_address(0)
        self.set_data(0)
        self.write()

        self.reset()

    def reset(self):
        self.RST.write(False)
        time.sleep(0.01)
        self.RST.write(True)
    
    def set_address(self, channel):
        assert type(channel) == int
        assert 0 <= channel < 4
        for i, gpio in enumerate(self.A):
            bit = is_nth_bit_set(channel, i)
            self.A[i].write(bit)

    def set_data(self,data):
        assert type(data) == int
        assert 0 <= data < (1<<12)
        for i, gpio in enumerate(self.A):
            bit = is_nth_bit_set(data, i)
            self.D[i].write(bit)

    def write_trigger(self):
        self.CS.write(False)
        time.sleep(0.01)
        self.CS.write(True)
    
pin_handler = Pin_Handler()

def write_channel_integer(channel, integer):
    pin_handler.set_address(channel)
    pin_handler.set_data(integer)
    pin_handler.write_trigger()

    