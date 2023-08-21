# @title new perm cca

import numpy as np
from permcca.inference import permutation_inference
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.pipeline import Pipeline
from sklearn.cross_decomposition import CCA, PLSCanonical, PLSRegression
from scipy.io import loadmat

# X = loadmat("../k10_r3_X.mat")["data"]
# Y = loadmat("../k10_r3_Y.mat")["data"]
X = np.load("../assets/X.npy")
Y = np.load("../assets/Y.npy")

x_preproc = Pipeline(
    [
        ("scale", StandardScaler(with_mean=True, with_std=True)),
        ("var", VarianceThreshold(threshold=0.0)),
        # ("pca", PCA(n_components=5)),
    ]
).fit_transform(X)

y_preproc = Pipeline(
    [
        ("scale", StandardScaler(with_mean=True, with_std=True)),
        ("var", VarianceThreshold(threshold=0.0)),
        # ("pca", PCA(n_components=5)),
    ]
).fit_transform(Y)

# U_hat, V_hat = permutation_inference(x_preproc, y_preproc)
# p = permutation_inference(x_preproc, y_preproc)
# print(p)
from permcca.preproc import get_max_ndim

n_comps = get_max_ndim(x_preproc, y_preproc)
ps = []
for model in [
    CCA(n_components=n_comps),
    PLSCanonical(n_components=n_comps),
    PLSRegression(n_components=n_comps),
]:
    ps.append(permutation_inference(x_preproc, y_preproc, model=model))
#%%
from sklearn.cross_decomposition import CCA
from scipy.linalg import null_space

X = x_preproc.copy()
Y = y_preproc.copy()
n_comps = min(np.linalg.matrix_rank(X), np.linalg.matrix_rank(Y))

cca = CCA(n_components=n_comps, scale=False)
cca.fit_transform(X, Y)
U_hat = X @ np.hstack((cca.x_weights_, null_space(cca.x_weights_.T)))
V_hat = Y @ np.hstack((cca.y_weights_, null_space(cca.y_weights_.T)))
