"""
asist.utility -- Various utility functions used to process data.
"""
import numpy as np


def binavg(x, binsize):
    """Simple binned average over binsize elements."""
    return np.array([np.mean(x[n:n+binsize])\
        for n in range(0, len(x), binsize)])

def blackman_harris(n):
    """Returns the n-point Blackman-Harris window."""
    x = np.linspace(0, 2 * np.pi, n, endpoint=False)
    p = [0.35875, -0.48829, 0.14128, -0.01168]
    res = np.zeros((n))
    for i in range(4):
        res += p[i] * np.cos(i * x)
    return res

def cat_numpy_arrays(arrays):
    """Concatenates numpy arrays."""
    x = []
    for a in arrays:
        x += list(a)
    return np.array(x)

def limit_to_percentile_range(x, plow, phigh):
    """Limits the values of x to low and high percentile limits."""
    xlow, xhigh = np.percentile(x, plow), np.percentile(x, phigh)
    x[x < xlow] = xlow
    x[x > xhigh] = xhigh
    return x

def deg2rad(d):
    """Degrees -> radians."""
    return d * np.pi / 180

def running_mean(x, n):
    """Running mean with the window n."""
    return np.convolve(x, np.ones((n,)) / n, mode='same')
