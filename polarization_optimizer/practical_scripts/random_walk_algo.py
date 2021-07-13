from ..hardware import read_osc_voltage
from ..hardware import write_channel_volt
import numpy as np

class Random_Walk_Handler:
    def __init__(self):
        self.state_vector = np.array([0.8, 0.8, 0.8], dtype = np.double)
        self.initial_sigma = 0.1
        self.alpha = 0.1
        self.former_voltage = 0.0 #とする
        self.delta = 0.1 #とする
        self.osc_channel = 0
        

    def candidate(self):
        mean = self.state_vector
        cov = self.initial_sigma * self.alpha * np.abs(self.delta) * np.eye(3)
        candidate = np.random.multivariate_normal(mean, cov, size=1)[0]
        return candidate        

    def step(self):
        candidate = self.candidate()
        candidate = np.max(np.vstack([candidate, np.ones(3)*0]), axis = 0)
        candidate = np.max(np.vstack([candidate, np.ones(3)*1.8]), axis = 0)
        
        for i, v in enumerate(candidate):
            write_channel_volt(i, v)
        
        new_value = read_osc_voltage(self.osc_channel)
        self.delta = new_value - self.former_voltage
        self.former_voltage = new_value
        if self.delta > 0:
            self.state_vector = candidate

        return

        