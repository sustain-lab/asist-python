"""
tests.py
"""
from asist.utility import blackman_harris
import numpy as np

def test_blackman_harris():
    N = 100
    bh = blackman_harris(N)
    assert type(bh) is np.ndarray
    assert bh.size == N
    assert np.max(bh) == 1
