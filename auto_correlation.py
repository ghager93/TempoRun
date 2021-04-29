import numpy as np

from scipy import signal


def short_time_autocorrelation(arr, times, lags, window_length, fixed_length=True):
    if fixed_length:
        autocorr = np.array([[np.dot(arr[i:i + window_length - 1], arr[i + j:i + j + window_length - 1])
                              for j in lags] for i in times])
    else:
        autocorr = np.array([[np.dot(arr[i + j:i + window_length - 1], arr[i:i - j + window_length - 1])
                              for j in lags] for i in times])

    return autocorr

def stft_autocorrelation(arr, corr_window_length, corr_hop_length, stft_window_length, stft_hop_length):
    s = signal.stft(arr, nperseg=stft_window_length, noverlap=(stft_window_length-stft_hop_length))[2]
    n_segs = int((s.shape[1] - corr_window_length) // corr_hop_length)
    sxx = np.array([s[:, i * corr_hop_length:i * corr_hop_length + corr_window_length]
                    @ s[:, i * corr_hop_length:i * corr_hop_length + corr_window_length].conjugate().T
                    for i in range(n_segs)])
