import numpy as np

from scipy import ndimage


def tempo_intervals(tempos: np.ndarray, min_length: int = 5, tolerance: int = 3):
    '''
    Returns dictionary of with a list of intervals for each tempo of the song.
    The keys are the tempos and the values are lists of lists, of the form [start, end]. Ie.

    {tempo1: [[start1_1, end1_1], [start1_2, end1_2], ...],
     tempo2: [[start2_1, end2_1], ...],
     ...}

    :param tempos: (np.ndarray) The tempos of the song.
    :param min_length: (int) Minimum length of an interval (end - start) for it to be counted.
    :param tolerance: (int) Maxium allowable deviation from each tempo to be counted as an interval.
    :return: Dictionary of lists of intervals (see description).
    '''

    interval_dict = {}

    # Pre filter tempos
    tempos_filt = __filter_tempos(tempos, 10)

    i = 0
    while i < len(tempos_filt):
        j = i
        while (j < len(tempos_filt)) and (abs(tempos_filt[i] - tempos_filt[j]) < 3):
            j += 1
        if (j - i) > 5:
            if tempos_filt[i] not in interval_dict.keys():
                interval_dict[tempos_filt[i]] = [[i, j]]
            else:
                interval_dict[tempos_filt[i]].append([i, j])
            i = j
        else:
            i += 1

    return interval_dict


def __filter_tempos(tempos: np.ndarray, length: int):
    # Round tempos to integers and apply a median filter.

    return ndimage.median_filter(tempos.astype(int), length)