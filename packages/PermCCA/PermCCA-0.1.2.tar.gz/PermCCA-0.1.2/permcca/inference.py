import numpy as np
from sklearn.cross_decomposition import CCA
from scipy.linalg import null_space
from scipy.stats import pearsonr
from permcca.permute import PermutationMultiVar
from typing import Callable, Dict, Optional
from sklearn.base import BaseEstimator


def can_corr(X_c: np.ndarray, Y_c: np.ndarray):
    return np.array([pearsonr(X_c[:, i], Y_c[:, i])[0] for i in range(X_c.shape[1])])


def _wilk_statistic(can_corr: np.ndarray):
    return -np.flip(np.cumsum(np.flip(np.log(1 - can_corr**2))))[0]


def _calc_cum_rs(
    U_hat: np.ndarray,
    V_hat: np.ndarray,
    n_comps: int,
    model: BaseEstimator,
):
    latent_cum_rs = []
    for k in range(n_comps):
        try:
            working_model = model.set_params(
                **{"n_components": n_comps - k}
            )  # sklearn models
        except AttributeError:
            raise NotImplementedError("Currently only supports sklearn models.")
        tmp_x, tmp_y = working_model.fit_transform(U_hat[:, k:], V_hat[:, k:])
        permed_rs = can_corr(tmp_x, tmp_y)
        cum_r = _wilk_statistic(permed_rs)
        latent_cum_rs.append(cum_r)

    return np.array(latent_cum_rs)


def _get_ndim(model: BaseEstimator):
    try:
        model_params = model.get_params()
        n_comps = model_params["n_components"]
    except:
        raise NotImplementedError("Currently only supports sklearn models.")
    return n_comps


def permutation_inference(
    X: np.ndarray,
    Y: np.ndarray,
    model: Callable or BaseEstimator = None,
    model_kwargs: Dict or Optional = None,
    n_perms: int = 1000,
    fwe_correction: bool = True,
):
    """
    :param X: predictor datasets
    :param Y: target datasets
    :param model: The model can be set or passed as a callable. If callable, then model_kwargs must be set.
    :param model_kwargs:
    :param n_perms:
    :param fwe_correction: Return the cumulated max p-value
    :return
    """
    # TODO: add support for passing model
    # TODO: add support for passing n_jobs
    if X.shape[0] != Y.shape[0]:
        raise ValueError("Y and X do not have same number of rows.")
    if model is None:
        n_comps = min(np.linalg.matrix_rank(X), np.linalg.matrix_rank(Y))
        model_kwargs = {"scale": False}
        working_model = CCA(n_components=n_comps, **model_kwargs)
        model = working_model
    else:
        working_model = model
        if model_kwargs is not None:
            try:
                model.set_params(**model_kwargs)  # sklearn models
            except AttributeError:
                working_model = model(**model_kwargs)
        else:
            model_kwargs = {}
        n_comps = _get_ndim(working_model)

    # Fit the model
    try:
        X_c, Y_c = working_model.fit_transform(X, Y)
    except AttributeError:
        raise AttributeError("Currently only supports sklearn style model.")
    # Get the weights
    try:
        x_weights = working_model.x_weights_
        y_weights = working_model.y_weights_
    except AttributeError:
        # TODO: add support for cca-zoo models
        raise AttributeError("Currently only supports sklearn models.")
    # Expanded canonical variables

    U_hat = X @ np.hstack((x_weights, null_space(x_weights.T)))
    V_hat = Y @ np.hstack((y_weights, null_space(y_weights.T)))
    # Permutation test
    cnt = np.zeros(n_comps)
    seeds = np.random.randint(0, 10000, size=n_perms)
    latent_cum_rs = _calc_cum_rs(U_hat, V_hat, n_comps, model)
    for perm in range(0, n_perms):
        perm_U_hat, perm_V_hat = PermutationMultiVar(
            random_state=seeds[perm], shuffle_target=True, selection=None
        ).fit_transform(U_hat, V_hat)
        permuted_latent_cum_rs = _calc_cum_rs(
            perm_U_hat,
            perm_V_hat,
            n_comps,
            model,
        )
        cnt += (permuted_latent_cum_rs >= latent_cum_rs).astype(int)

    # Compute p-values
    punc = np.minimum(cnt / n_perms, 1)
    p = np.maximum.accumulate(punc) if fwe_correction else punc
    return p, X_c, Y_c, x_weights, y_weights, model
