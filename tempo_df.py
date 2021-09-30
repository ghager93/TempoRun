import os
import pandas as pd

import read_audio
import dwt_detection
import tempo_intervals

from typing import List


def build_from_path(path: str) -> pd.DataFrame:
    '''
    Build a dataframe of tempos from a library specified by path. Dataframe includes tempo (bpm), start and stop times
    (samples) and the track name (string).

    :param path: (string) Path to directory of music library.
    :return: (pd.DataFrame) dataframe of tempo intervals for each song in library.
    '''

    audios = read_audio.read_dir(path)
    tempos = [dwt_detection.tempo_series(audio, fs) for audio, fs in audios]
    interval_dfs = [tempo_intervals.tempo_intervals_df(tempo) for tempo in tempos]
    song_names = __song_names(path)
    interval_dfs = __connect_names_to_dfs(interval_dfs, song_names)
    tempo_df = pd.concat(interval_dfs).reset_index(drop=True)

    return tempo_df


def __song_names(path: str) -> List[str]:
    try:
        names = os.listdir(path)
    except FileNotFoundError:
        names = []

    return names


def __connect_names_to_dfs(dfs: List[pd.DataFrame], names: List[str]) -> List[pd.DataFrame]:
    assert(len(dfs) == len(names))

    for df, name in zip(dfs, names):
        df['track'] = name

    return dfs
