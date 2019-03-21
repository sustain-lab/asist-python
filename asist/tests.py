"""
tests.py
"""
from asist.utility import binavg, blackman_harris
import numpy as np

def test_binavg():
    N = 10000
    x = np.random.randn(N)
    assert type(binavg(x, 10)) is np.ndarray
    assert binavg(x, 10).size == N // 10
    assert np.all(binavg(x, 1) == x)

def test_blackman_harris():
    N = 100
    bh = blackman_harris(N)
    assert type(bh) is np.ndarray
    assert bh.size == N
    assert np.max(bh) == 1
