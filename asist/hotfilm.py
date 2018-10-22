"""
hotfilm.py
"""
from datetime import datetime, timedelta
from netCDF4 import Dataset
import numpy as np


def effective_velocity(u, k=0.3, theta=np.pi / 4):
    """Returns effective velocity, given input wind speed u 
    from a calibrated instrument, along-film cooling factor k, 
    and the angle of wires relative to the flow."""
    return np.sqrt(u**2 * (np.cos(theta)**2 + (k * np.sin(theta)**2)))


def hotfilm_velocity(veff1, veff2, k1=0.3, k2=0.3):
    """For a pair effective velocities from wire 1 and 2,
    calculates u and w components."""
    un = np.sqrt((veff1**2 - k1**2 * veff2**2) / (1 - k1**2 * k2**2))
    ut = np.sqrt((veff2**2 - k2**2 * veff1**2) / (1 - k1**2 * k2**2))
    u = 0.5 * np.sqrt(2.) * (ut + un)
    w = 0.5 * np.sqrt(2.) * (ut - un)
    return u, w


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
        origin = datetime.strptime(nc.variables['Time'].origin, '%Y-%m-%dT%H:%M:%S')
        fan = nc.variables['fan'][:]
        ch1 = nc.variables['ch1'][:]
        ch2 = nc.variables['ch2'][:]
    return origin, seconds, fan, ch1, ch2
