from ..hardware import read_osc_voltage
from ..hardware import read_osc_voltage_series
import numpy as np

def normal_metric_factory(channel):
    def func():
        value = read_osc_voltage(channel)
        return value
    return func

def visibility_metric_factory(channel, ground_level = 0):
    def func():
        series = read_osc_voltage_series(channel, N = 2000, decimation=31250) # 0.5s measurement
        max_value = np.max(series) - ground_level
        min_value = np.min(series) - ground_level
        visibility = (max_value - min_value) / (max_value + min_value)
        return visibility
    return func

def max_min_difference_metric_factory(channel):
    def func():
        series = read_osc_voltage_series(channel, N = 2000, decimation=31250) # 0.5s measurement
        max_value = np.max(series)
        min_value = np.min(series)
        difference = max_value - min_value
        return difference
    return func

def power_ratio_metric_factory(channel_primary, channel_secondary):
    def func():
        value_target = read_osc_voltage(channel_primary)
        value_sub = read_osc_voltage(channel_secondary)
        total = value_target + value_sub
        power_ratio = value_target / total
        return power_ratio
    return func