import os
import functools

from typing import Tuple

import pydub
import numpy as np
import librosa

from scipy import ndimage


def get_global_tempo(audio_segment: pydub.AudioSegment) -> float:
    tempo, _ = _calculate_beat_track(audio_segment)
    return tempo


def get_periodic_tempo(audio_segment: pydub.AudioSegment, period: float = 25, method: str = "beattrack") -> list[float]:
    if method == "plp":
        beat_times = get_beat_times_plp(audio_segment)
    else:
        beat_times = get_beat_times(audio_segment) 
    beat_deltas = np.array(beat_times[1:]) - np.array(beat_times[:-1])
    beat_deltas = np.where(beat_deltas == 0, np.max(beat_deltas), beat_deltas)

    delta_tempo = 1/beat_deltas

    return ndimage.uniform_filter1d(delta_tempo, period, mode="nearest") * 60


def get_beat_indices(audio_segment: pydub.AudioSegment) -> list[float]:
    _, beat_indices = _calculate_beat_track(audio_segment)
    return beat_indices.tolist()


def get_beat_times(audio_segment: pydub.AudioSegment) -> list[float]:
    beat_indices = get_beat_indices(audio_segment)
    return librosa.frames_to_time(beat_indices, sr=audio_segment.frame_rate).tolist()


def get_beat_times_plp(audio_segment: pydub.AudioSegment) -> list[float]:
    signal = _get_signal_array(audio_segment)
    sampling_rate = audio_segment.frame_rate
    onset_env = librosa.onset.onset_strength(y=signal, sr=sampling_rate)
    pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sampling_rate)
    pulse_indices = np.flatnonzero(librosa.util.localmax(pulse))
    return librosa.frames_to_time(pulse_indices, sr=sampling_rate).tolist()

@functools.lru_cache
def _calculate_beat_track(audio_segment: pydub.AudioSegment) -> Tuple[float, np.ndarray]:
    signal = _get_signal_array(audio_segment)
    sampling_rate = audio_segment.frame_rate

    tempo, beat_indices = librosa.beat.beat_track(y=signal, sr=sampling_rate)

    return tempo, beat_indices


def _get_signal_array(audio_segment: pydub.AudioSegment) -> np.ndarray:
    return np.array(audio_segment.get_array_of_samples(), dtype=np.float32)