"""
irgason.py
"""
from datetime import datetime, timedelta
import numpy as np

def read_irgason_from_toa5(filenames):
    """Reads data from IRGASON output file(s) in TOA5 format.
    If filenames is a string, process a single file. If it is 
    a list of strings, process files in order and concatenate."""
    if type(filenames) is str:
        print('Reading ', filenames)
        data = [line.rstrip() for line in open(filenames).readlines()[4:]]
    elif type(filenames) is list:
        data = []
        for filename in filenames:
            print('Reading ', filename)
            data += [line.rstrip() for line in open(filename).readlines()[4:]]
    else:
        raise RuntimeError('filenames must be string or list')

    times, u, v, w, sonic_temperature, cell_temperature, cell_pressure, rh = [], [], [], [], [], [], [], []
    for line in data:
        line = line.split(',')
        timestr = line[0].replace('"','')
        if len(timestr) == 19:
            time = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
        elif len(timestr) == 21:
            time = datetime.strptime(timestr[:19], '%Y-%m-%d %H:%M:%S')
            time += timedelta(seconds=float(timestr[-2:]))
        else:
            time = datetime.strptime(timestr[:19], '%Y-%m-%d %H:%M:%S')
            time += timedelta(seconds=float(timestr[-3:]))
        times.append(time)
        u.append(float(line[26].strip('"')))
        v.append(float(line[27].strip('"')))
        w.append(float(line[28].strip('"')))
        sonic_temperature.append(float(line[29].strip('"')))
        cell_temperature.append(float(line[34].strip('"')))
        cell_pressure.append(float(line[35].strip('"')))
        rh.append(float(line[39].strip('"')))
    return np.array(times), np.array(u), np.array(v), np.array(w), np.array(sonic_temperature), np.array(cell_temperature), 10 * np.array(cell_pressure), np.array(rh)
