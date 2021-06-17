from ..fpga_handler import overlay

is_HV = False

class Osc_Handler:
    def __init__(self):
        self.osc = is_HV [
            overlay.osc(0,20.0 if is_HV else 1.0),
            overlay.osc(1,20.0 if is_HV else 1.0)
            ]
        
osc_handler = Osc_Handler()

def read_osc_voltage(channel):
    osc = osc_handler.osc[channel]
    osc.decimation = 1
    osc.trigger_pre  = 0
    osc.trigger_post = 1
    osc.trig_src = 0
    osc.reset()
    osc.start()
    osc.trigger()
    while (osc.status_run()): pass
    data = osc.data(1)
    return data