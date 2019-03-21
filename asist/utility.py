"""
asist.utility -- Various utility functions used to process data.
"""
import numpy as np
from scipy.signal import detrend


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


def power_spectrum(x, dt, binsize=1):
    """Power spectrum of x with a sampling interval dt.
    Optionally, average over binsize if provided."""

    assert type(x) is np.ndarray, 'x must be a numpy.ndarray'
    assert dt > 0, 'dt must be > 0'
    assert type(binsize) is int, 'binsize must be an int'
    assert binsize > 0, 'binsize must be > 0'

    N = x.size
    window = blackman_harris(N)
    Sx = np.fft.fft(window * detrend(x))[:N//2]
    C = dt / (np.pi * np.sum(window**2))
    df = 2 * np.pi / (dt * N)
    f = np.array([i * df for i in range(N//2)]) / (2 * np.pi)

    if binsize > 1:
        Sxx = 2 * np.pi * C * binavg(np.abs(Sx)**2, binsize)
        f = binavg(f, binsize)
        df *= binavg
    else:
        Sxx = 2 * np.pi * C * np.abs(Sx)**2

    return Sxx, f, df


def cross_spectrum(x, y, dt, binsize=1):
    """Cross spectrum of x and y with a sampling interval dt.
    Optionally, average over binsize if provided."""

    assert type(x) is np.ndarray, 'x must be a numpy.ndarray'
    assert type(y) is np.ndarray, 'y must be a numpy.ndarray'
    assert x.size == y.size, 'x and y must have same size'
    assert dt > 0, 'dt must be > 0'
    assert type(binsize) is int, 'binsize must be an int'
    assert binsize > 0, 'binsize must be > 0'

    N = x.size
    window = blackman_harris(N)
    Sx = np.fft.fft(window * detrend(x))[:N//2]
    Sy = np.fft.fft(window * detrend(y))[:N//2]
    df = 2 * np.pi / (dt * N)
    f = np.array([i * df for i in range(N//2)]) / (2 * np.pi)
    C = dt / (np.pi * np.sum(window**2))

    if binsize > 1:
        Sxx = 2 * np.pi * C * binavg(np.abs(Sx)**2, binsize)
        Syy = 2 * np.pi * C * binavg(np.abs(Sy)**2, binsize)
        Sxy = 2 * np.pi * C * binavg(np.conj(Sx) * Sy, binsize)
        f = binavg(f, binsize)
        df *= binavg
    else:
        Sxx = 2 * np.pi * C * np.abs(Sx)**2
        Syy = 2 * np.pi * C * np.abs(Sy)**2
        Sxy = 2 * np.pi * C * np.conj(Sx) * Sy

    phase = np.arctan2(-np.imag(Sxy), np.real(Sxy))
    coherence = np.abs(Sxy / np.sqrt(Sxx * Syy))

    return Sxx, Syy, Sxy, phase, coherence, f, df
