from ..fpga_handler import overlay

pdm = overlay.analog_out()

class Pin_Assign:
    def __init__(self):
        self.C1 = 0
        self.C3 = 1
        self.C2 = 2
        self.C4 = 3
        self.C = [self.C1, self.C2, self.C3, self.C4]

pin_assign = Pin_Assign()

def write_channel_volt(channel, volt):
    assert 0<= volt <= 1.8
    pin = pin_assign.C[channel]
    pdm.write(pin, volt)
