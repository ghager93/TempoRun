import numpy as np
import rolling


def rolling_median_absolute_deviation(arr, window_length):
    return _rolling_median_absolute_deviation_by_skip_list(arr, window_length)


def _rolling_median_absolute_deviation_by_numpy(arr, window_length):
    if window_length % 2:
        mid = int((window_length - 1) / 2)
        def median_mid_func(x): return x[mid]
    else:
        mid = int(window_length / 2)
        def median_mid_func(x): return 0.5*(x[mid-1] + x[mid])

    arr_med = np.median(arr)
    medians = np.zeros(len(arr))
    mads = np.zeros(len(arr))

    arr_pad = np.concatenate((arr_med * np.ones(mid), arr, arr_med * np.ones(mid)), axis=None)
    arr_pad = np.pad(arr, mid, mode='median')

    s = np.sort(arr_pad[:window_length])
    for i in range(len(arr) - 1):
        medians[i] = median_mid_func(s)
        t = np.sort(abs(s - medians[i]))
        mads[i] = median_mid_func(t)

        s = np.delete(s, np.searchsorted(s, arr_pad[i]))
        s = np.insert(s, np.searchsorted(s, arr_pad[i + window_length]), arr_pad[i + window_length])

    medians[-1] = median_mid_func(s)
    t = np.sort(abs(s - medians[i]))
    mads[-1] = median_mid_func(t)

    return mads, medians

def _rolling_median_absolute_deviation_by_skip_list(arr, window_length):
    # Using rolling function from https://github.com/ajcr/rolling
    # Which uses skip_list method from Raymond Hettinger - https://code.activestate.com/recipes/577073/

    mid = int(window_length / 2)
    arr_med = np.median(arr)
    arr_pad = np.concatenate((arr_med * np.ones(mid), arr, arr_med * np.ones(mid)), axis=None)
    arr_pad = np.pad(arr, mid, mode='median')

    medians = np.array(list(rolling.Median(arr_pad, window_length)))

    if window_length % 2 == 0:
        medians = medians[:-1]

    median_med = np.median(medians)
    median_pad = np.concatenate((median_med * np.ones(mid), medians, median_med * np.ones(mid)), axis=None)
    median_pad = np.pad(medians, mid, mode='median')

    mads = np.array(list(rolling.Median(median_pad, window_length)))
    if window_length % 2 == 0:
        mads = mads[:-1]

    return mads, medians
