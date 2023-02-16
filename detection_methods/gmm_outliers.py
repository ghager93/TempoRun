import numpy as np

from sklearn import mixture


def outliers(arr):
    gmm = mixture.GaussianMixture(n_components=2)
    labels = gmm.fit_predict(arr.reshape(-1, 1))
    outlier_idx = np.argmax(gmm.means_)

    return np.where(labels == outlier_idx, arr, 0)