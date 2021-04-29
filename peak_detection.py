import numpy as np

from scipy import ndimage


def max_filter(arr, window_length):
    maxs = ndimage.maximum_filter1d(arr, window_length, mode='constant')
    return np.where(arr == maxs, arr, 0)

