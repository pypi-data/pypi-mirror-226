# TO BE DONE

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array
from scipy.linalg import null_space, svd, pinv, sqrtm
import warnings


class RemoveCovars(BaseEstimator, TransformerMixin):
    def __init__(
        self,
        x_covars: np.ndarray = None,
        y_covars: np.ndarray = None,
        partial_type: str or None = "partial",
        method="linear",
    ):
        raise NotImplementedError
        self.x_covars = x_covars
        self.y_covars = y_covars
        if partial_type == "partial":
            self.y_covars = x_covars
            if self.x_covars is None:
                raise ValueError("x_covars must be provided if type is 'partial'.")
        elif partial_type == "semi":
            if (self.y_covars is None) & (self.x_covars is None):
                raise ValueError(
                    "Either x_covars or y_covars must be provided if type is 'semi'."
                )
        elif partial_type is None:
            pass
        else:
            raise ValueError("partial_type must be 'partial', 'semi' or None.")
        self.partial_type = partial_type
        self.method = method

    def multiple_regression(self, x, y):
        # remove x_covariates from x
        x_covars = self.x_covars
        if x_covars is not None:
            x_covars = check_array(x_covars)
            x = x - x_covars @ pinv(x_covars) @ x
        # remove y_covariates from y
        y_covars = self.y_covars
        if y_covars is not None:
            y_covars = check_array(y_covars)
            y = y - y_covars @ pinv(y_covars) @ y

    def fit(self, x: np.ndarray, y: np.ndarray):
        x = check_array(x)
        y = check_array(y)
        if self.method == "linear":
            raise NotImplementedError
        return self

    def transform(self, x, y=None):
        x = check_array(x)
        y = check_array(y)
        return x - self.covars, y - self.covars

    def fit_transform(self, x, y=None, **fit_params):
        return self.fit(x, y).transform(x, y)


class SemiOrthogonal(BaseEstimator, TransformerMixin):
    """
    Compute a semi-orthogonal matrix according to
    the Huh-Jhun or Theil methods.

    Parameters:
    Z (ndarray): Input matrix of shape (N, R).
    Sel (ndarray or int or None): Selection matrix or selection method.
        If Sel is None, use the Huh-Jhun method.
        If Sel is an integer -1, use the Theil method with random selection.
        If Sel is a vector of indices or a boolean mask, use the Theil method with explicit selection.
        If Sel is a matrix, use the Theil method with the given selection matrix.

    Returns:
    Q (ndarray): Semi-orthogonal matrix of shape (N, N).
    """

    def __init__(self, selection=None):
        self.selection = selection
        raise NotImplementedError

    def fit(self, X, y=None):
        # prepare the selection matrix
        if self.selection is None:
            pass
        else:
            # Theil method
            N, R = X.shape
            if isinstance(self.selection, np.ndarray):
                # Sel is a matrix
                return self
            elif np.isscalar(self.selection) and self.selection == -1:
                # Sel is -1
                rZ = np.linalg.matrix_rank(X)
                if rZ < R:
                    raise ValueError(
                        "Impossible to use the Theil method with this set of nuisance variables"
                    )
                _, iU, _ = np.unique(X, axis=0, return_index=True)
                np.random.shuffle(iU)
                unSel0 = []
                rnk0 = 0
                for u in iU:
                    unSel = np.concatenate((unSel0, [u]))
                    Zout = X[unSel, :]
                    rnk = np.linalg.matrix_rank(Zout)
                    if rnk > rnk0:
                        unSel0 = unSel
                        rnk0 = rnk
                    if rnk == R:
                        break
                selection = np.setdiff1d(np.arange(N), unSel)
                self.selection = np.eye(N)[:, selection]
            else:
                # Sel is a vector of indices
                if np.issubdtype(self.selection.dtype, np.bool_):
                    selection = np.nonzero(self.selection)[0]
                else:
                    selection = self.selection
                if selection[0] > 0:
                    unSel = np.setdiff1d(np.arange(N), selection)
                    if np.linalg.matrix_rank(X[unSel, :]) < R:
                        raise ValueError("Selected rows of nuisance not full rank")
                else:
                    raise ValueError("Invalid value for Sel")
                self.selection = np.eye(N)[:, selection]
        return self

    def transform(self, X, y=None):
        N, R = X.shape

        if self.selection is None:
            # Huh-Jhun method
            Q, D, _ = svd(null_space(X.T), full_matrices=False)
            Q = Q @ D
        else:
            Rz = np.eye(N) - X @ pinv(X)
            Q = (
                Rz
                @ self.selection
                @ sqrtm(pinv(self.selection.T @ Rz @ self.selection))
            )
        return Q

    def fit_transform(self, X, y=None, **fit_params):
        return self.fit(X, y).transform(X, y)


def get_max_ndim(X, Y):
    n_comps = min(np.linalg.matrix_rank(X), np.linalg.matrix_rank(Y))
    return n_comps


def check_input(X: np.ndarray, Y: np.ndarray):
    X = check_array(X)
    Y = check_array(Y)
    if X.shape[0] != Y.shape[0]:
        raise ValueError("X and Y must have the same number of rows")
    if X.shape[1] > X.shape[0]:
        warnings.warn(
            "The number of features in X is larger than sample size. Consider using dimension reduction techniques."
        )
    if Y.shape[1] > Y.shape[0]:
        warnings.warn(
            "The number of features in Y is larger than sample size. Consider using dimension reduction techniques."
        )
    return X, Y


def semiortho(Z, selection=None):

    if selection is None:
        # Huh-Jhun method
        Q, D, _ = svd(null_space(Z.T), full_matrices=False)
        Q = Q @ D
    else:
        # Theil method
        N, R = Z.shape
        if isinstance(selection, np.ndarray):
            # Sel is a matrix
            S = selection
        elif np.isscalar(selection) and selection == -1:
            # Sel is -1
            rZ = np.linalg.matrix_rank(Z)
            if rZ < R:
                raise ValueError(
                    "Impossible to use the Theil method with this set of nuisance variables"
                )
            _, iU, _ = np.unique(Z, axis=0, return_index=True)
            np.random.shuffle(iU)
            unSel0 = []
            rnk0 = 0
            for u in iU:
                unSel = np.concatenate((unSel0, [u]))
                Zout = Z[unSel, :]
                rnk = np.linalg.matrix_rank(Zout)
                if rnk > rnk0:
                    unSel0 = unSel
                    rnk0 = rnk
                if rnk == R:
                    break
            selection = np.setdiff1d(np.arange(N), unSel)
            S = np.eye(N)[:, selection]
        else:
            # Sel is a vector of indices
            if np.issubdtype(selection.dtype, np.bool_):
                selection = np.nonzero(selection)[0]
            if selection[0] > 0:
                unSel = np.setdiff1d(np.arange(N), selection)
                if np.linalg.matrix_rank(Z[unSel, :]) < R:
                    raise ValueError("Selected rows of nuisance not full rank")
            else:
                raise ValueError("Invalid value for Sel")
            S = np.eye(N)[:, selection]
        Rz = np.eye(N) - Z @ pinv(Z)
        Q = Rz @ S @ sqrtm(pinv(S.T @ Rz @ S))
    return Q


def center(X):
    """
    Mean center a matrix and remove constant columns.

    Parameters:
    X (ndarray): Matrix of shape (N, p) to center.

    Returns:
    X (ndarray): Centered matrix of shape (N, p') with p' <= p.
    """
    # icte = np.sum(np.diff(X, axis=0) ** 2, axis=0) == 0 # the original code
    icte = np.std(X, axis=0) != 0  # the inconstant columns

    X = X - np.mean(X, axis=0)
    X = X[:, icte]
    return X


def remove_covars(X, Y, covars_x=None, covars_y=None, partial=True, selection=None):
    identity = np.eye(X.shape[0])  # Create an n_samples x n_samples identity matrix
    if selection is None:
        selection = []
    X = center(X)
    Y = center(Y)
    if partial == True or partial == "bipartial":
        if covars_x is None:
            raise ValueError("covars_x must be specified for bi-partial CCA.")
        covars = center(covars_x)
        q_covars_x = semiortho(covars, selection)
        q_covars_y = q_covars_x.copy()

    elif partial == "semi":
        if covars_x is None and covars_y is None:
            raise ValueError(
                "Either covars_x or covars_y must be specified in semi-partial CCA."
            )
        covars_x = center(covars_x)
        covars_y = center(covars_y)
        q_covars_x = semiortho(covars_x, selection)
        q_covars_y = semiortho(covars_y, selection)
    else:
        q_covars_x = identity
        q_covars_y = identity
    X = q_covars_x.T @ X
    Y = q_covars_y.T @ Y
    n_samples_x, feat_num_x = X.shape
    n_samples_y, feat_num_y = Y.shape
    cova_num_x = covars_x.shape[1] if covars_x is not None else 0
    cova_num_y = covars_y.shape[1] if covars_y is not None else 0
