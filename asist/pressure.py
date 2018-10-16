"""
pressure.py
"""
from datetime import datetime, timedelta
import numpy as np
import os

def read_pressure_from_toa5(filenames):
    """Reads MKS pressure difference data from TOA5 file written by
    the Campbell Scientific logger. If filenames is a string, 
    process a single file. If it is a list of strings, 
    process files in order and concatenate."""
    if type(filenames) is str:
        print('Reading ', filenames)
        data = [line.rstrip() for line in open(filenames).readlines()[4:]]
    elif type(filenames) is list:
        data = []
        for filename in filenames:
            print('Reading ', os.path.basename(filename))
            data += [line.rstrip() for line in open(filename).readlines()[4:]]
    else:
        raise RuntimeError('filenames must be string or list')

    dp, times = [], []
    for line in data:
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
