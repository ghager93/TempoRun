import numpy as np

from scipy import signal
from scipy import ndimage


def separate_hp(arr, fs=22050, factor=1, h_freq_window_length=None, p_time_window_length=None,
                stft_window_length=None, stft_hop_length=None, residue=False):
    if stft_window_length is None:
        stft_window_length = int(0.03*fs)
    if stft_hop_length is None:
        stft_hop_length = int(0.02*fs)
    # if h_freq_window_length is None:
    #     h_freq_window_length = min(100, int(len(arr) / 4))
    # if p_time_window_length is None:
    #     p_time_window_length = min(100, int(stft_window_length / 4))

    s = signal.stft(arr, nperseg=stft_window_length, noverlap=stft_window_length-stft_hop_length)[2]
    h, p, r = hpr_spectrogram(abs(s), factor, h_freq_window_length, p_time_window_length)

    ih = signal.istft(h, nperseg=stft_window_length, noverlap=stft_window_length-stft_hop_length)[1]
    ip = signal.istft(p, nperseg=stft_window_length, noverlap=stft_window_length-stft_hop_length)[1]

    if residue:
        ir = signal.istft(r, nperseg=stft_window_length, noverlap=stft_window_length-stft_hop_length)[1]
        ret = ih, ip, ir
    else:
        ret = ih, ip

    return ret


def hpr_spectrogram(sxx, factor=1, h_freq_window_length=None, p_time_window_length=None):
    if h_freq_window_length is None:
        h_freq_window_length = min(100, int(sxx.shape[0] / 4))
    if p_time_window_length is None:
        p_time_window_length = min(100, int(sxx.shape[1] / 4))

    h_mask = ndimage.median_filter(sxx, (1, h_freq_window_length))
    p_mask = ndimage.median_filter(sxx, (p_time_window_length, 1))

    h = np.where(h_mask > factor * p_mask, sxx, 10e-5)
    p = np.where(p_mask > factor * h_mask, sxx, 10e-5)
    r = np.where((h_mask <= factor * p_mask) & (p_mask <= factor * h_mask), sxx, 10e-5)

    return h, p, r
