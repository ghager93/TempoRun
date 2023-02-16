import numpy as np

from numpy.lib.stride_tricks import as_strided
from scipy import signal


def short_time_autocorrelation(arr, times, lags, window_length, fixed_length=True):
    if fixed_length:
        autocorr = np.array([[np.dot(arr[i:i + window_length - 1], arr[i + j:i + j + window_length - 1])
                              for j in lags] for i in times])
    else:
        autocorr = np.array([[np.dot(arr[i + j:i + window_length - 1], arr[i:i - j + window_length - 1])
                              for j in lags] for i in times])

    return autocorr


def short_lag_autocorrelation(arr, lag):
    # Takes autocorrelation of array, but only of delays up to lag (non-inclusive).

    return np.array([np.dot(arr[:len(arr)-k], arr[k:]) for k in range(lag)])


def autocorrelation(x, maxlag):
    """
    Autocorrelation with a maximum number of lags.

    `x` must be a one-dimensional numpy array.

    This computes the same result as
        numpy.correlate(x, x, mode='full')[len(x)-1:len(x)+maxlag]

    The return value has length maxlag + 1.
    """
    p = np.pad(x.conj(), maxlag, mode='constant')
    T = as_strided(p[maxlag:], shape=(maxlag+1, len(x) + maxlag),
                   strides=(-p.strides[0], p.strides[0]))
    return T.dot(p[maxlag:].conj())


def fft_autocorrelation(arr):
    fft_arr = np.fft.fft(arr)

    return np.fft.ifft(fft_arr * np.conjugate(fft_arr))

