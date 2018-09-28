"""
pitot.py
"""
import numpy as np

def pitot_velocity(dp, rho):
    """Given pressure difference dp [Pa] and air density
    rho [kg/m^3], returns the wind speed measured by the
    pitot tube."""
    return np.sqrt(2 * dp / rho)
