import numpy as np
import pywt

from scipy import signal
from numpy.lib import stride_tricks
from typing import List


def tempo(sig: np.ndarray, fs: float, dwt_level: int = 4, min_bpm: int = 80) -> int:
    '''
    Estimate the tempo (bpm) of a time-series signal.

    Uses auto-correlation of a cascaded DWT filter bank.

    :param sig: (1-D ndarray) Time-series signal. If sig is N-D, it is flattened before computation.
    :param fs: (float) Sampling frequency.
    :param dwt_level: (int) Number of cascaded DWTs in filter bank. Default is 4.
    :param min_bpm: (int) Returned tempo is within the range [min_bpm, 2*min_bpm].
    :return: (int) Approximate tempo (bpm).
    '''

    if sig.ndim > 1:
        sig = sig.flatten()

    # length of sig is reduced to a factor of 2**dwt_level.
    # Ensures an equal length when downsizing each filter response.
    truncated_sig = sig[:len(sig) - (len(sig) % 2 ** dwt_level)]

    dwt_coeffs = _dwt(truncated_sig, dwt_level)

    # Coefficients downsampled all be an equal length of len(sig)/2**dwt_level
    dwt_coeffs_downsampled = np.array([dc[::2 ** i] for i, dc in enumerate(dwt_coeffs)])

    return _dwt2bpm(dwt_coeffs_downsampled, fs, min_bpm)


def tempo_series(sig: np.ndarray, fs: float, win_length: int = None, hop_length: int = None,
                 dwt_level: int = 4, min_bpm: int = 80) -> np.ndarray:
    '''
    Estimate the tempo (bpm) of the segments of a time-series signal.

    Uses auto-correlation of a cascaded DWT filter bank.

    :param sig: (1-D ndarray) Time-series signal. If sig is N-D, it is flattened before computation.
    :param fs: (float) Sampling frequency.
    :param win_length: (int) Number of samples per segment. If None, defaults to 10 seconds (10*fs).
    :param hop_length: (int) Sample interval between segments. If None, defaults to 1 second (fs).
    :param dwt_level: (int) Number of cascaded DWTs in filter bank. Default is 4.
    :param min_bpm: (int) Returned tempo is within the range [min_bpm, 2*min_bpm].
    :return: (np.ndarray) Series of integer approximations of the tempo (bpm).
    '''

    if sig.ndim > 1:
        sig = sig.flatten()

    if win_length is None:
        win_length = 60 * fs

    if hop_length is None:
        hop_length = 30 * fs

    downsampled_win_length = win_length // (2 ** dwt_level)
    downsampled_hop_length = hop_length // (2 ** dwt_level)

    # length of sig is reduced to a factor of 2**dwt_level.
    # Ensures an equal length when downsizing each filter response.
    truncated_sig = sig[:len(sig) - (len(sig) % 2 ** dwt_level)]

    dwt_coeffs = _dwt(truncated_sig, dwt_level)

    # Coefficients downsampled all be an equal length of len(sig)/2**dwt_level
    dwt_coeffs_downsampled = [dc[::2 ** i] for i, dc in enumerate(dwt_coeffs)]

    dwt_segments = [_segment(dc, downsampled_win_length, downsampled_hop_length) for dc in dwt_coeffs_downsampled]
    dwt_segments = np.array(dwt_segments).transpose((1, 0, 2))

    return np.array([_dwt2bpm(segment, fs, min_bpm) for segment in dwt_segments])


def _dwt2bpm(dwt_coeffs: np.ndarray, fs: float, min_bpm: int = 80) -> int:
    # Estimate the tempo of a segment from its dwt coefficients.
    # Coefficients are assumed to already have been downsampled to equal length.
    # dwt_coeffs should have shape (M x N). Where M is the number of DWT filters and N is the downsampled
    # length of the segment.

    # If tempo is found to be below min_bpm, it is assumed to be a fractional beat.
    # The tempo is doubled until it is higher than or equal to min_bpm.

    # If tempo is found to be above max_bpm, it is assumed to be a multiple of a beat.
    # The tempo is halved until it is lower than max_bpm.
    max_bpm = 2 * min_bpm

    dwt_level = dwt_coeffs.shape[0]

    max_peak_dist = 60 * fs // (min_bpm * 2 ** dwt_level)
    min_peak_dist = 60 * fs // (max_bpm * 2 ** dwt_level)

    dwt_abs = np.abs(dwt_coeffs)
    dwt_detrended = dwt_abs - dwt_abs.mean(axis=1)[:, None]
    dwt_sum = dwt_detrended.sum(axis=0)

    dwt_autocorr = _autocorrelate(dwt_sum)

    lag = _find_peak_lag(dwt_autocorr, min_peak_dist, max_peak_dist)

    def lag2bpm(lag: int) -> int:
        bpm_unrolled = 60 * fs / (lag * 2 ** dwt_level)
        return bpm_unrolled * 2 ** (np.floor(np.log2(max_bpm) - np.log2(bpm_unrolled)))

    return lag2bpm(lag)


def _dwt(sig: np.ndarray, level: int = 4) -> List[np.ndarray]:
    # Only detail coefficients are returned, thus lowest 2**level-th frequencies are discarded.
    _, *details = pywt.wavedec(sig, 'db4', mode='per', level=level)

    return details


def _segment(sig: np.ndarray, win_length: int, hop_length: int) -> np.ndarray:
    return np.copy(stride_tricks.sliding_window_view(sig, win_length)[::hop_length, :])


def _autocorrelate(sig: np.ndarray) -> np.ndarray:
    # Returns second-half (starting at lag 0) of the auto-correlation response of sig.
    return signal.correlate(sig, sig, 'full')[len(sig) - 1:]


def _find_peaks(arr: np.ndarray, min_dist: int = 1) -> np.ndarray:
    return signal.find_peaks(arr, distance=min_dist, height=arr.mean())[0]


def _find_peak_lag(lags: np.ndarray, min_dist, max_dist):
    peaks = _find_peaks(lags[:2 * max_dist], min_dist // 2)
    return peaks[1] if len(peaks) > 1 else peaks[0]
