from ..hardware import write_channel_volt
from ..hardware import write_channel_integer
from ..metric import normal_metric_factory
import numpy as np


class Random_Walk_Handler:
    def __init__(self):
        self.state_vector = np.array([0.5, 0.5, 0.5], dtype = np.double)
        self.initial_sigma = 0.1
        self.alpha = 0.1
        self.former_value = 0.0 #とする
        self.delta = 0.1 #とする
        self.osc_channel = 0
        self.former_candidate = None
        self.metric = normal_metric_factory(self.osc_channel)
        

    def candidate(self):
        mean = self.state_vector
        cov = self.initial_sigma * self.alpha * np.abs(self.delta) * np.eye(3)
        candidate = np.random.multivariate_normal(mean, cov, size=1)[0]
        return candidate        

    def step(self):
        new_value = self.metric()
        self.delta = new_value - self.former_value
        self.former_value = new_value
        if self.delta > 0:
            self.state_vector = self.former_candidate if self.former_candidate is not None else self.state_vector

        candidate = self.candidate()
        candidate = np.max(np.vstack([candidate, np.ones(3)*0]), axis = 0)
        candidate = np.min(np.vstack([candidate, np.ones(3)*1]), axis = 0)
        
        for i, v in enumerate(candidate):
            write_channel_volt(i, v)
            write_channel_integer(i, int(v*((1<<12) - 1)))
        self.former_candidate = candidate
        
        return

