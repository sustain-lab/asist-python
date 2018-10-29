"""
wave_probe.py
"""
from datetime import datetime, timedelta
import numpy as np
import os


def read_end_time(filename):
    return datetime.strptime(open(filename).read().strip(),\
                             '%Y-%m-%d %H:%M:%S')


def read_wave_probe_csv(filename):
    """Reads wave probe (staff) data from CSV file.
    filename must be full path that includes endtime.txt
    with the ending time stamp."""
    time, eta = [], []
    data = [line.strip() for line in open(filename).readlines()][2:]
    for line in data:
        line = line.split(',')
        time.append(float(line[0]))
        eta.append(float(line[4]))
    end_time = read_end_time(os.path.dirname(filename) + '/endtime.txt')
    start_time = end_time - timedelta(seconds=time[-1])
    return start_time, np.array(time), np.array(eta)
