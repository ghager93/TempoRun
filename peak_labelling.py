import numpy as np

from scipy import signal
from scipy import ndimage

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


def peak_signal(peaks, length=None, spread=None, filter_='max'):
    if filter_ == 'none':
        return _peak_signal_non_filtered(peaks, length)
    if filter_ == 'max':
        return _peak_signal_max_filtered(peaks, spread, length)
    if filter_ == 'gauss':
        return _peak_signal_gaussian_filtered(peaks, spread, length)


def _peak_signal_non_filtered(peaks, length=None):
    if length is None:
        length = 2*peaks[-1] - peaks[-2]
    sig = np.zeros(length)
    sig[peaks] = 1

    return sig


def _peak_signal_max_filtered(peaks, length=None, spread=None):
    if length is None:
        length = 2*peaks[-1] - peaks[-2]
    if spread is None:
        spread = 0.1 * length / len(peaks)

    return ndimage.maximum_filter1d(_peak_signal_non_filtered(peaks, length), spread, mode='constant')


def _peak_signal_gaussian_filtered(peaks, length=None, spread=None):
    if length is None:
        length = 2*peaks[-1] - peaks[-2]
    if spread is None:
        spread = 0.1 * length / len(peaks)

    return np.convolve(_peak_signal_non_filtered(peaks, length), signal.gaussian(np.ceil(4 * spread), spread), 'same')
