import numpy as np

import ampd_peak_detection
import filters
import gmm_outliers


def ampd(arr, fs):
    return ampd_peak_detection.find_peaks(arr, lag_max=int(min(fs, len(arr)//2)), lag_min=1)


def max_outliers(arr, fs):
    outliers = gmm_outliers.outliers(arr)

    return max_threshold(arr, fs)


def max_threshold(arr, fs):
    arr_filtered = filters.max_threshold(arr, int(max(fs//9, 4)))

    return np.flatnonzero(arr_filtered)


