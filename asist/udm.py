"""
pressure.py
"""
from datetime import datetime, timedelta
from netCDF4 import Dataset
import numpy as np
import os

def read_udm_from_toa5(filenames):
    """Reads UDM elevation data from TOA5 file written by
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

    u1, u2, u3, u4, u5, u6, times = [], [], [], [], [], [], []
    for line in data:
        line = line.replace('"', '').split(',')
        t = line[0]
        if len(t) == 19:
            time = datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
        elif len(t) == 21:
            time = datetime.strptime(t[:19], '%Y-%m-%d %H:%M:%S')
            time += timedelta(seconds=float(t[-2:]))
        else:
            time = datetime.strptime(t[:19], '%Y-%m-%d %H:%M:%S')
            time += timedelta(seconds=float(t[-3:]))
        times.append(time)
        u1.append(float(line[2]))
        u2.append(float(line[3]))
        u3.append(float(line[4]))
        u4.append(float(line[5]))
        u5.append(float(line[6]))
        u6.append(float(line[7]))
    return np.array(times), np.array(u1), np.array(u2), np.array(u3),\
        np.array(u4), np.array(u5), np.array(u6)
