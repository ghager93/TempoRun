import numpy as np

from scipy import signal


def short_time_autocorrelation(arr, times, lags, window_length, fixed_length=True):
    if fixed_length:
        autocorr = np.array([[np.dot(arr[i:i + window_length - 1], arr[i + j:i + j + window_length - 1])
                              for j in lags] for i in times])
    else:
        autocorr = np.array([[np.dot(arr[i + j:i + window_length - 1], arr[i:i - j + window_length - 1])
                              for j in lags] for i in times])

    return autocorr


def fft_autocorrelation(arr):
    fft_arr = np.fft.fft(arr)

    return np.fft.ifft(fft_arr * np.conjugate(fft_arr))

