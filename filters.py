import numpy as np

from scipy import ndimage


def moving_average_filter(arr, window_length):
    return np.convolve(arr, np.ones(window_length)/window_length, mode='same')


def median_filter(arr, window_length):
    return ndimage.median_filter(arr, window_length)


def max_threshold(arr, window_length):
    maxs = ndimage.maximum_filter1d(arr, window_length, mode='constant')
    return np.where(arr == maxs, arr, 0)


def median_abs_deviation_threshold(arr, window_length):
    pass
