"""
hotfilm.py
"""
from datetime import datetime, timedelta
import numpy as np


def effective_velocity(u, k, theta):
    """Returns hot film effective velocity, given input
    wind speed u from a calibrated instrument, along-film
    cooling factor k, and the angle of wires relative
    to the flow."""
    return np.sqrt(u**2 * (np.cos(theta)**2 + (k * np.sin(theta)**2)))


def read_hotfilm_from_lvm(filename, dt=1e-3):
    """Reads 2-channel hotfilm data from a Labview text file."""
    times = []
    ch1 = []
    ch2 = []
    data = [line.rstrip() for line in open(filename).readlines()]
    line = data[0].split(',')[1:]
    t = [int(float(n)) for n in line[:5]]
    seconds = float(line[5])
    useconds = int(1e6 * (seconds - int(seconds)))
    start_time = datetime(t[0], t[1], t[2], t[3], t[4], int(seconds), useconds)
    seconds = 0
    for line in data:
        line = line.split(',')[1:]
        ch1.append(float(line[6]))
        ch2.append(float(line[7]))
        times.append(seconds)
        seconds += dt
    return start_time, times, ch1, ch2


def read_hotfilm_from_netcdf(filename):
    """Reads 2-channel hotfilm data from a NetCDF file."""
    with Dataset(filename, 'r') as nc:
        seconds = nc.variables['Time'][:]
        origin = datetime.strptime(nc.variables['Time'].origin, '%Y-%m-%d %H:%M:%S UTC')
        time = np.array([origin + timedelta(seconds=seconds[n])\
                                 for n in range(seconds.size)])
        fan = nc.variables['fan'][:]
        ch1 = nc.variables['ch1'][:]
        ch2 = nc.variables['ch2'][:]
    return time, fan, ch1, ch2
