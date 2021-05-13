import numpy as np

from scipy import signal

import ampd_peak_detection
import filters
import gmm_outliers
import statistical_thresholds

def ampd(arr, fs):
    if fs > 2000:
        arr = signal.resample(arr, int(len(arr) * 2000 / fs))
        fs = 2000

    return ampd_peak_detection.find_peaks(abs(arr), lag_max=int(min(fs, len(arr) / 2)), lag_min=1)


def max_outliers(arr, fs):
    outliers = gmm_outliers.outliers(abs(arr))

    return max_threshold(outliers, fs)


def max_threshold(arr, fs):
    arr_filtered = filters.max_threshold(abs(arr), int(max(fs//9, 4)))

    return np.flatnonzero(arr_filtered)


def mad_threshold(arr, fs):
    arr_filtered = statistical_thresholds.rolling_mad(abs(arr), int(max(fs//9, 4)))

    return np.flatnonzero(arr_filtered)


def var_threshold(arr, fs):
    arr_filtered = statistical_thresholds.rolling_var(abs(arr), int(max(fs//9, 4)))

    return np.flatnonzero(arr_filtered)


def peak_signal(peaks, length):
    sig = np.zeros(length)
    sig[peaks] = 1

    return sig



