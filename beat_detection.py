import numpy as np

from scipy import signal

import filters
import auto_correlation
import zero_crossing_rate
import harm_perc_separator


def harmonic_zcr(arr, fs=22050, factor=1, h_freq_window_length=None, p_time_window_length=None,
                 stft_window_length=None, stft_hop_length=None):
    if stft_window_length is None:
        stft_window_length = int(0.03 * fs)
    if stft_hop_length is None:
        stft_hop_length = int(0.01 * fs)
    if h_freq_window_length is None:
        h_freq_window_length = int(stft_window_length / 4)
    if p_time_window_length is None:
        p_time_window_length = int(np.min((10, len(arr)//2)))

    freq, _, x = signal.stft(arr, fs, nperseg=stft_window_length, noverlap=(stft_window_length - stft_hop_length))
    sxx = abs(x)**2
    sxx_harmonic = harm_perc_separator.hpr_spectrogram(sxx, factor, h_freq_window_length, p_time_window_length)[0]

    return zero_crossing_rate.tf_zcr(x, freq)


def decimate_median_filter(arr, fs=22050, decimate_fs=450, window_length=None):
    if window_length is None:
        window_length = int(0.03 * decimate_fs)

    arr = signal.resample(arr, int(len(arr) * decimate_fs / fs))

    return filters.median_filter(arr, window_length)