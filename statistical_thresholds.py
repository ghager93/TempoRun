import numpy as np
import rolling

import median_absolute_deviation


def rolling_mad(arr, window_length):
    mad, median = median_absolute_deviation.rolling_median_absolute_deviation(arr, window_length)

    return np.where(arr > median + mad, arr, 0)


def rolling_var(arr, window_length):
    arr_pad = np.pad(arr, int(window_length / 2), mode='mean')

    mean = np.array(list(rolling.Mean(arr_pad, window_length)))
    var = np.array(list(rolling.Var(arr_pad, window_length)))

    if window_length % 2:
        threshold = mean + np.sqrt(3) * var
    else:
        threshold = mean[:-1] + np.sqrt(3) * var[:-1]

    return np.where(arr > threshold)

