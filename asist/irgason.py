"""
irgason.py
"""
from datetime import datetime, timedelta
import numpy as np

def read_irgason_from_toa5(filename):
    data = [line.rstrip() for line in open(filename).readlines()]
    u, v, w, t = [], [], [], []
    for line in data[4:]:
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
        t.append(time)
        u.append(float(line[26].strip('"')))
        v.append(float(line[27].strip('"')))
        w.append(float(line[28].strip('"')))
    return np.array(t), np.array(u), np.array(v), np.array(w)
