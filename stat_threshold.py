import numpy as np


def rolling_median_absolute_deviation(arr, window_length):
    if window_length % 2:
        mid = int((window_length - 1) / 2)
        def median_mid_func(x): return x[mid]
    else:
        mid = int(window_length / 2)
        def median_mid_func(x, mid): return 0.5*(x[mid-1] + x[mid])

    arr_med = np.median(arr)
    medians = np.zeros(len(arr))
    mads = np.zeros(len(arr))

    arr_pad = np.concatenate((arr_med * np.ones(mid), arr, arr_med * np.ones(mid)), axis=None)

    s = np.sort(arr_pad[:window_length])
    for i in range(mid, len(arr) - mid + 1):
        medians[i - mid] = median_mid_func(s)

        t = np.sort(abs(s - medians[i - mid]))
        mads[i - mid] = median_mid_func(t)

        s = np.sort(np.append(s[1:], arr_pad[i]))

    return mads, medians
