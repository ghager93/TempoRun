import numpy as np
import librosa

from scipy import signal


def zcr_librosa(arr, fs=22050, window_length=None, hop_length=None):
    if window_length is None:
        window_length = int(0.03 * fs)
    if hop_length is None:
        hop_length = int(0.01 * fs)

    return librosa.feature.zero_crossing_rate(arr, frame_length=window_length, hop_length=hop_length)[0]


def zcr_stft(arr, fs=22050, window_length=None, hop_length=None):
    if window_length is None:
        window_length = int(0.03 * fs)
    if hop_length is None:
        hop_length = int(0.01 * fs)

    freq, _, x = signal.stft(arr, fs, nperseg=window_length, noverlap=(window_length - hop_length))

    return np.sum(freq[:, None] * abs(x), axis=0) / np.sum(abs(x))


def zero_interpolate(arr, scale):
    ret = np.zeros(len(arr) * scale)
    ret[::scale] = arr

    return ret

