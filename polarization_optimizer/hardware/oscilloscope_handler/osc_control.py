from ..fpga_handler import overlay

is_HV = False

class Osc_Handler:
    def __init__(self):
        self.osc = [
            overlay.osc(0,20.0 if is_HV else 1.0),
            overlay.osc(1,20.0 if is_HV else 1.0)
            ]
        
osc_handler = Osc_Handler()

def read_osc_voltage(channel, N = 100, decimation = 1):
    # (averaged) single value
    # decimation = d, then sampling rate (125/d)MHz
    data = read_osc_voltage_series(channel, N, decimation)
    return data.mean()

def read_osc_voltage_series(channel, N, decimation = 1):
    # decimation = d, then sampling rate (125/d)MHz
    osc = osc_handler.osc[channel]
    osc.decimation = decimation
    osc.trigger_pre  = 0
    osc.trigger_post = N
    osc.trig_src = 0
    osc.reset()
    osc.start()
    osc.trigger()
    while (osc.status_run()): pass
    data = osc.data(N)
    return data
