import numpy as np
from sklearn.base import BaseEstimator


def pca_cca_weights(pca_weights: np.ndarray or BaseEstimator, cca_weights: np.ndarray):
    """Return the original loadings"""
    if isinstance(pca_weights, BaseEstimator):
        pca_weights = pca_weights.components_
    # check if dimensions are correct
    if pca_weights.shape[0] != cca_weights.shape[0]:
        raise ValueError("pca_weights and cca_weights must have same number of rows.")
    loadings = pca_weights.T @ cca_weights
    return loadings
