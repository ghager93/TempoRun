from unittest import TestCase
from auto_correlation import short_lag_autocorrelation
import numpy as np

class Test(TestCase):
    def test_short_lag_autocorrelation(self):
        arr = np.ones(10)
        lag = 5
        out = np.array([10, 9, 8, 7, 6])

        self.assertTrue(np.allclose(out, short_lag_autocorrelation(arr, lag)))