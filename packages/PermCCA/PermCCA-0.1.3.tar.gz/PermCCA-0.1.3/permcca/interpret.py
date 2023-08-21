import numpy as np
from sklearn.base import BaseEstimator
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA


def pca_cca_weights(
    pca_weights: np.ndarray or BaseEstimator or Pipeline, cca_weights: np.ndarray
):
    """Return the original loadings"""
    if isinstance(pca_weights, Pipeline):
        for step_name, step in pca_weights.named_steps.items():
            if isinstance(step, PCA):
                pca_weights = step.components_
        raise ValueError("PCA step not found in the pipeline")
    if isinstance(pca_weights, PCA):
        pca_weights = pca_weights.components_
    # check if dimensions are correct
    if pca_weights.shape[0] != cca_weights.shape[0]:
        raise ValueError("pca_weights and cca_weights must have same number of rows.")
    loadings = pca_weights.T @ cca_weights
    return loadings
