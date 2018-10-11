"""
irgason.py
"""
from datetime import datetime, timedelta
from netCDF4 import Dataset
import numpy as np
import os

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
            print('Reading ', os.path.basename(filename))
            data += [line.rstrip() for line in open(filename).readlines()[4:]]
    else:
        raise RuntimeError('filenames must be string or list')

    times, u, v, w, sonic_temperature, cell_temperature, cell_pressure, rh = [], [], [], [], [], [], [], []

    print('Processing IRGASON time series..')

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


def read_irgason_from_netcdf(filename):
    """Reads IRGASON data from a NetCDF file, created by
    asist_nsf_2018.process_level1.process_irgason_to_level2()."""
    data = {}
    with Dataset(filename, 'r') as nc:
        seconds = nc.variables['Time'][:]
        origin = datetime.strptime(nc.variables['Time'].origin, '%Y-%m-%d %H:%M:%S UTC')
        data['time'] = np.array([origin + timedelta(seconds=seconds[n])\
                                 for n in range(seconds.size)])
        data['flag'] = nc.variables['flag'][:]
        data['fan'] = nc.variables['fan'][:]
        data['u'] = nc.variables['u'][:]
        data['v'] = nc.variables['v'][:]
        data['w'] = nc.variables['w'][:]
        data['Ts'] = nc.variables['Ts'][:]
        data['Tc'] = nc.variables['Tc'][:]
        data['Pc'] = nc.variables['Pc'][:]
        data['RH'] = nc.variables['RH'][:]
    return data
