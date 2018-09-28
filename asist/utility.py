"""
utility.py
"""
import numpy as np


def cat_numpy_arrays(arrays):
    """Concatenates numpy arrays."""
    x = []
    for a in arrays:
        x += list(a)
    return np.array(x)


def deg2rad(d):
    """Degrees to radians."""
    return d * np.pi / 180
