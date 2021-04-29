import numpy as np

from scipy import ndimage


def max_filter(arr, window_length):
    return _max_filter3(arr, window_length)

def _max_filter1(arr, window_length):
    arr = np.concatenate((np.zeros(int(window_length / 2)), np.copy(arr), np.zeros(int(window_length / 2))))
    for i in range(int(window_length / 2), len(arr) - int(window_length / 2)):
        if int(window_length / 2) + 1 != np.argmax(arr[i - int(window_length / 2):i + int(window_length / 2)]):
            arr[i] = 0

    return arr[int(window_length / 2):-int(window_length / 2)]


def _max_filter2(arr, window_length):
    arr = np.concatenate((np.zeros(int(window_length / 2)), np.copy(arr), np.zeros(int(window_length / 2))))
    windows = np.lib.stride_tricks.sliding_window_view(arr, window_length)
    maxs = np.max(windows, axis=1)

    return np.where(arr == maxs, arr, 0)


def _max_filter3(arr, window_length):
    maxs = ndimage.maximum_filter1d(arr, window_length, mode='constant')
    return np.where(arr == maxs, arr, 0)

