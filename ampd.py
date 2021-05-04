import numpy as np


class AMPDConditions:
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

