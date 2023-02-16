import numpy as np


class AMPDConditionsOld:
    def __init__(self, lmin, lmax, n):
        self.lmin = lmin
        self.lmax = lmax
        self.n = n
        self.m0 = np.array([np.arange(n), ] * (lmax - lmin))
        self.m3 = self.m0 - 1

    def conditions_matrix(self, x):
        return self._condition_one() | self._condition_two() | self._condition_three(x) | self._condition_four(x)

    def _condition_one(self):
        m1 = np.array([np.arange(self.lmin + 2, self.lmax + 2), ] * self.n).T

        return np.where(self.m0 < m1, 1, 0)

    def _condition_two(self):
        m2 = np.array([np.arange(self.n - self.lmax + 2, self.n - self.lmin + 2)[::-1], ] * self.n).T

        return np.where(self.m0 > m2, 1, 0)

    def _condition_three(self, x):
        m4 = np.array([-np.arange(self.lmin, self.lmax), ] * self.n).T + self.m3

        return np.where(x[abs(self.m3)] <= x[abs(m4)], 1, 0)

    def _condition_four(self, x):
        m5 = np.array([np.arange(self.lmin, self.lmax), ] * self.n).T + self.m3
        m5 = np.where(m5 >= len(x), 0, m5)
        return np.where(x[abs(self.m3)] <= x[abs(m5)], 1, 0)


class AMPDConditions:
    def __init__(self, x, lmin, lmax):
        self.lmin = lmin
        self.lmax = lmax
        self.n = len(x)
        self.x = x
        self.m0 = np.array([np.arange(self.n), ] * (lmax - lmin))
        self.m3 = self.m0 - 1

    def conditions_matrix(self):
        return self._condition_one() | self._condition_two() | self._condition_three() | self._condition_four()

    def _condition_one(self):
        m1 = np.array([np.arange(self.lmin + 2, self.lmax + 2), ] * self.n).T

        return self.m0 < m1

    def _condition_two(self):
        m2 = np.array([np.arange(self.n - self.lmax + 2, self.n - self.lmin + 2)[::-1], ] * self.n).T

        return self.m0 > m2

    def _condition_three(self):
        m4 = np.array([-np.arange(self.lmin, self.lmax), ] * self.n).T + self.m3

        return self.x[abs(self.m3)] <= self.x[abs(m4)]

    def _condition_four(self):
        m5 = np.array([np.arange(self.lmin, self.lmax), ] * self.n).T + self.m3
        m5 = np.where(m5 >= len(self.x), 0, m5)

        return self.x[abs(self.m3)] <= self.x[abs(m5)]


def find_peaks(arr, lag_max, lag_min=1):
    lms = _local_maxima_scalogram(arr, lag_max, lag_min)
    lms_r = lms[:_max_lms_scale(lms), :]

    return np.flatnonzero(_lms_stddev(lms_r) == 0)


def _local_maxima_scalogram(arr, lag_max, lag_min):
    conditions_matrix = AMPDConditions(arr, lag_min, lag_max).conditions_matrix()

    return 1 + conditions_matrix * np.random.random(conditions_matrix.shape)


def _max_lms_scale(lms):
    return np.argmin(np.sum(lms, axis=1)) + 1


def _lms_stddev(lms):
    lms_column_sum = np.sum(lms, axis=0)
    n = lms.shape[0]

    return 1 / (n - 1) * np.sqrt(np.sum((lms - lms_column_sum / n)**2, axis=0))
