import numpy as np


def rolling_median_absolute_deviation(arr, window_length):
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
