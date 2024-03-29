import numpy as np

from scipy import signal
from scipy import interpolate

import filters
import zero_crossing_rate
import harm_perc_separator


def harmonic_zcr(arr, fs=22050, factor=1, h_freq_window_length=None, p_time_window_length=None,
                 stft_window_length=None, stft_hop_length=None):
    """Calculates the zero crossing rate of the harmonic component of a signal's power spectral density."""
    if stft_window_length is None:
        stft_window_length = int(0.03 * fs)
    if stft_hop_length is None:
        stft_hop_length = int(0.01 * fs)
    if h_freq_window_length is None:
        h_freq_window_length = min(100, int(len(arr) / 2))
    if p_time_window_length is None:
        p_time_window_length = min(100, int(stft_window_length / 2))

    freq, _, x = signal.stft(arr, fs, nperseg=stft_window_length, noverlap=(stft_window_length - stft_hop_length))
    sxx_harmonic = harm_perc_separator.hpr_spectrogram(abs(x), factor, h_freq_window_length, p_time_window_length)[0]

    return zero_crossing_rate.tf_zcr(sxx_harmonic, freq)


def hpr_zcr(arr, fs=22050, factor=10, h_freq_window_length=None, p_time_window_length=None,
                 stft_window_length=None, stft_hop_length=None):
    """Calculates the zero crossing rate of the harmonic, percussive and residual components of a signal's power spectral density."""
    if stft_window_length is None:
        stft_window_length = int(0.03 * fs)
    if stft_hop_length is None:
        stft_hop_length = int(0.01 * fs)
    if h_freq_window_length is None:
        h_freq_window_length = min(100, int(len(arr) / 2))
    if p_time_window_length is None:
        p_time_window_length = min(100, int(stft_window_length / 2))

    freq, _, x = signal.stft(arr, fs, nperseg=stft_window_length, noverlap=(stft_window_length - stft_hop_length))
    h, p, r = harm_perc_separator.hpr_spectrogram(abs(x), factor, h_freq_window_length, p_time_window_length)

    return zero_crossing_rate.tf_zcr(h, freq), zero_crossing_rate.tf_zcr(p, freq), zero_crossing_rate.tf_zcr(r, freq)


def decimate_median_filter(arr, fs=22050, decimate_fs=450, window_length=None):
    """Resample signal with lower sampling rate and applying sliding median filter."""
    if window_length is None:
        window_length = int(0.03 * decimate_fs)

    arr = signal.resample(arr, int(len(arr) * decimate_fs / fs))

    return filters.median_filter(abs(arr), window_length)


def percussive_separation(arr, fs=22050, factor=10, h_freq_window_length=None, p_time_window_length=None,
                 stft_window_length=None, stft_hop_length=None):
    """Return percussive component of a signal."""
    return harm_perc_separator.separate_hp(arr, fs, factor, h_freq_window_length, p_time_window_length,
                                           stft_window_length, stft_hop_length)[1]


def zero_interp(arr, factor):
    """Interpolate with zero-value samples between original samples."""
    if factor <= 1:
        return arr

    ret = np.zeros(len(arr) * int(factor))
    ret[::int(factor)] = arr
    ret = np.concatenate((ret, np.zeros(int(len(arr) * factor) - len(ret))))

    return ret


def interpolate_beat(arr, factor):
    interp_f = interpolate.interp1d(np.arange(arr.size), arr)

    return interp_f(np.linspace(0, arr.size-1, int(arr.size * factor)))
