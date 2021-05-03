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
        h_freq_window_length = 6
    if p_time_window_length is None:
        p_time_window_length = 10

    freq, _, x = signal.stft(arr, fs, nperseg=stft_window_length, noverlap=(stft_window_length - stft_hop_length))
    sxx = abs(x)**2
    sxx_harmonic = harm_perc_separator.hpr_spectrogram(sxx, factor, h_freq_window_length, p_time_window_length)[0]

    return zero_crossing_rate.tf_zcr(sxx_harmonic, freq)


def hcr_zcr(arr, fs=22050, factor=1, h_freq_window_length=None, p_time_window_length=None,
                 stft_window_length=None, stft_hop_length=None):
    if stft_window_length is None:
        stft_window_length = int(0.03 * fs)
    if stft_hop_length is None:
        stft_hop_length = int(0.01 * fs)
    if h_freq_window_length is None:
        h_freq_window_length = 6
    if p_time_window_length is None:
        p_time_window_length = 10

    freq, _, x = signal.stft(arr, fs, nperseg=stft_window_length, noverlap=(stft_window_length - stft_hop_length))
    sxx = abs(x)**2
    h, p, r = harm_perc_separator.hpr_spectrogram(sxx, factor, h_freq_window_length, p_time_window_length)

    return zero_crossing_rate.tf_zcr(h, freq), zero_crossing_rate.tf_zcr(p, freq), zero_crossing_rate.tf_zcr(r, freq)


def decimate_median_filter(arr, fs=22050, decimate_fs=450, window_length=None):
    if window_length is None:
        window_length = int(0.03 * decimate_fs)

    arr = signal.resample(arr, int(len(arr) * decimate_fs / fs))

    return filters.median_filter(abs(arr), window_length)