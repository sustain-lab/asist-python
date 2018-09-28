"""
pressure.py
"""
from datetime import datetime, timedelta
import numpy as np

def read_pressure_from_toa5(filename):
    """Reads pressure data from TOA5 file written by
    the Campbell Scientific logger."""
    dp = []
    times = []
    data = [line.rstrip() for line in open(filename).readlines()]
    for line in data[4:]:
        line = line.split(',')
        t = line[0].replace('"','')
        if len(t) == 19:
            time = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
        else:
            time = datetime.strptime(t[:19], '%Y-%m-%d %H:%M:%S')
            time += timedelta(seconds=float(t[-2:]))
        times.append(time)
        dp.append(float(line[2]))
    return np.array(times), np.array(dp) * 1e3
