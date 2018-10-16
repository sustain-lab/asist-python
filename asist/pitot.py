"""
pitot.py
"""
from datetime import datetime, timedelta
from netCDF4 import Dataset
import numpy as np

def pitot_velocity(dp, rho):
    """Given pressure difference dp [Pa] and air density
    rho [kg/m^3], returns the wind speed measured by the
    pitot tube."""
    return np.sqrt(2 * dp / rho)


def read_pitot_from_netcdf(filename):
    """Reads pitot data from a NetCDF file."""
    with Dataset(filename, 'r') as nc:
        seconds = nc.variables['Time'][:]
        origin = datetime.strptime(nc.variables['Time'].origin, '%Y-%m-%dT%H:%M:%S')
        fan = nc.variables['fan'][:]
        u = nc.variables['u'][:]
    return origin, seconds, fan, u
