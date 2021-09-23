import os
import sys
import numpy as np
import pydub

from typing import List, Tuple


def read_file(file: str) -> Tuple[np.ndarray, int]:
    try:
        audio = pydub.AudioSegment.from_file(file)
    except FileNotFoundError:
        print("Error: File not found")
        return np.empty(0), -1
    except IndexError:
        print("Error: File could not be read")
        return np.empty(0), -1

    return np.array(audio.get_array_of_samples()), audio.frame_rate


def read_dir(path: str) -> List[Tuple[np.ndarray, int]]:
    audios = []
    files = os.listdir(path)
    for file in files:
        try:
            audios.append(read_file(os.path.join(path, file)))
        except (FileNotFoundError, IndexError):
            continue

    return audios
