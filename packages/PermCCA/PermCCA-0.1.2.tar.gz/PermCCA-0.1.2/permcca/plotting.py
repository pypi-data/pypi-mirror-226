from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import pearsonr


def density_scatter(
    x, y, reg=True, gaussian_density=True, figsize=(10, 10), display=True, **kwargs
):
    xy = np.vstack([x, y])
    if gaussian_density:
        try:
            from numpy.linalg import LinAlgError

            z = gaussian_kde(xy)(xy)
        except LinAlgError:
            import warnings

            warnings.warn(
                "raised LinAlgError: The covariance matrix associated with the data is singular. "
                "The density plot will be computed from the histogram"
            )
            gaussian_density = False

    if not gaussian_density:
        H, x_edges, y_edges = np.histogram2d(x, y)
        x_centers = (x_edges[:-1] + x_edges[1:]) / 2
        y_centers = (y_edges[:-1] + y_edges[1:]) / 2

        # Convert the histogram to a 2D array of densities
        dx = x_centers[1] - x_centers[0]
        dy = y_centers[1] - y_centers[0]
        z = H / (dx * dy)
    # Create the scatter plot with density-based coloring
    fig, ax = plt.subplots(figsize=figsize)
    sc = ax.scatter(x=x, y=y, c=z, cmap="viridis", **kwargs)
    if reg:
        sns.regplot(x=x, y=y, scatter=False, ax=ax, color="black")

    # Add a colorbar to the figure
    cbar = plt.colorbar(sc)
    cbar.set_label("Density")
    if display:
        plt.show()

    return fig, ax


def plot_cca_scatter(transformed_X, transformed_Y, n_comps=1, **kwargs):
    """
    Plots Canonical Correlation Analysis (CCA) scatter plot.

    Parameters:
    transformed_X (array-like): Transformed X data from CCA.
    transformed_Y (array-like): Transformed Y data from CCA.
    n_comps (int): Number of components to plot.

    Returns:
    None
    """
    fig_size = kwargs.get("fig_size", (10, 10))
    marker = kwargs.get("marker", "o")
    color = kwargs.get("color", "b")
    xlabel = kwargs.get("xlabel", None)
    ylabel = kwargs.get("ylabel", None)
    title_prefix = kwargs.get("title_prefix", "Scatter plot of CCA components")
    layout = kwargs.get("layout", "tight")
    p_values = kwargs.get("p_values", None)
    for i in range(n_comps):
        # plt.scatter(transformed_X[:, i], transformed_Y[:, i], marker=marker, color=color, label=f'Component {i+1}')
        density_scatter(transformed_X[:, i], transformed_Y[:, i], display=False)
        corr_coef = np.corrcoef(transformed_X[:, i], transformed_Y[:, i])[0, 1]
        if kwargs.get("xlabel", False) & kwargs.get("ylabel", False):
            title = f"{title_prefix}: {xlabel} vs {ylabel} pearson r = {corr_coef}"
            if p_values:
                title += f" p = {p_values[i]}"
            plt.title(title)
        else:
            title = f"Component {i + 1}: pearson r = {corr_coef}"
            if p_values:
                title += f" p = {p_values[i]}"
            plt.title(title)
        if not xlabel:
            xlabel = "X Component {}".format(i + 1)
        if not ylabel:
            ylabel = "Y Component {}".format(i + 1)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.show()


def plot_cca_weights(
    weights: List or np.ndarray,
    labels: List or np.ndarray,
    ax=False,
    display_thresh=0.2,
    show=False,
    min_font_size=6,
    scaling_factor=50,
    **kwargs,
):
    if isinstance(weights, list):
        weights = np.array(weights)
    elif isinstance(weights, np.ndarray):
        pass
    else:
        raise ValueError("weights must be a list or numpy array")
    if isinstance(labels, list):
        labels = np.array(labels)
    elif isinstance(labels, np.ndarray):
        pass
    else:
        raise ValueError("labels must be a list or numpy array")

    xlim = kwargs.get("xlim", (-1, 1))
    xlabel = kwargs.get("xlabel", "")
    title = kwargs.get("title", "")
    display_title = kwargs.get("display_title", True)
    display_label = kwargs.get("display_label", True)
    sns.set_style("white")
    weights = weights.flatten()
    # get the index of thresholded weights
    idx = np.where(abs(weights) >= display_thresh)[0]
    filtered_weights = weights[idx]
    filtered_labels = labels[idx]
    # Sort weights and labels for X features
    sorted_indices = np.argsort(filtered_weights)
    sorted_weights = filtered_weights[sorted_indices]
    sorted_labels = [filtered_labels[idx] for idx in sorted_indices]
    if not ax:
        fig, ax = plt.subplots(figsize=(8, len(sorted_labels) / 2))
    ax.set_xlim(xlim[0], xlim[1])
    ax.set_ylim(-0.5, len(weights) + 0.5)
    if display_label:
        ax.set_ylabel("Weights")
        ax.set_xlabel(xlabel)
    if display_title:
        ax.set_title(title)
    # perform min-max scalling for weights
    abs_weights = abs(sorted_weights)
    plot_weights = (abs_weights - abs_weights.min()) / (
        abs_weights.max() - abs_weights.min()
    )
    texts = []
    for i, label in enumerate(sorted_labels):
        font_size = max(min_font_size, plot_weights[i] * scaling_factor)
        ax.text(
            0,
            i,
            label + f"  weights {round(sorted_weights[i], 2)}",
            ha="center",
            va="center",
            fontsize=font_size,
        )

    # adjust_text(texts,only_move={ 'text':'X'})
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])

    if show:
        plt.show()

    return ax


def plot_paired_cca_weights(
    weights_X: np.ndarray or pd.DataFrame,
    weights_Y: np.ndarray or pd.DataFrame,
    x_labels: List = None,
    y_labels: List = None,
    display_thresh: float = 0.2,
    scaling_factor: float = 30,
    subplot_kwargs: dict = None,
):
    """
    Plots Canonical Correlation Analysis (CCA) feature weights.

    Parameters:
    weights_X (array-like): Weights for X features. If passing dataframe, the index represents the feature names.
    weights_Y (array-like): Weights for Y features. If passing dataframe, the index represents the feature names.
    x_labels (list): Labels for X features. Defaults to None. None only works with DataFrame.
    y_labels (list): Labels for Y features. Defaults to None. None only works with DataFrame.
    display_thresh (float): Threshold for displaying feature weights. Defaults to 0.2.
    scaling_factor (float): Scaling factor for font size of displayed weights. Defaults to 30.
    subplot_kwargs (dict, Optional): Default is None, passing to plot_cca_weights() function.
    **kwargs: Additional arguments Controls the figures.
    Returns:
    None
    """
    if isinstance(weights_X, pd.DataFrame):
        x_labels = weights_X.index
        weights_X = weights_X.values
    elif isinstance(weights_X, np.ndarray):
        pass
    else:
        raise TypeError("weights_X must be a numpy array or pandas dataframe.")
    if isinstance(weights_Y, pd.DataFrame):
        y_labels = weights_Y.index
        weights_Y = weights_Y.values
    elif isinstance(weights_Y, np.ndarray):
        pass
    else:
        raise TypeError("weights_Y must be a numpy array or pandas dataframe.")
    if x_labels is not None:
        if not isinstance(x_labels, list):
            try:
                x_labels = list(x_labels)
            except:
                raise TypeError("x_labels must be a list or can be converted to list.")
        if len(x_labels) != weights_X.shape[0]:
            raise ValueError(
                "The length of x_labels must be equal to the number of rows in weights_X"
            )
    else:
        raise ValueError("x_labels must be provided. What are you plotting then?")
    if y_labels is not None:
        if not isinstance(y_labels, list):
            try:
                y_labels = list(y_labels)
            except:
                raise TypeError("y_labels must be a list or can be converted to list.")
        if len(y_labels) != weights_Y.shape[0]:
            raise ValueError(
                "The length of y_labels must be equal to the number of rows in weights_Y"
            )
    else:
        raise ValueError("x_labels must be provided. What are you plotting then?")
    n_comps = weights_X.shape[1]
    for i in range(n_comps):
        fig, (ax1, ax2) = plt.subplots(1, 2)
        plot_cca_weights(
            weights_X[:, i],
            x_labels,
            ax=ax1,
            display_thresh=display_thresh,
            min_font_size=6,
            scaling_factor=scaling_factor,
            xlim=(-1, 1),
            xlabel="X Features",
            title="Component {} X feature weights".format(i + 1),
            **subplot_kwargs,
        )
        plot_cca_weights(
            weights_Y[:, i],
            y_labels,
            ax=ax2,
            display_thresh=display_thresh,
            min_font_size=6,
            scaling_factor=scaling_factor,
            xlabel="Y Features",
            title="Component {} Y feature weights".format(i + 1),
            **subplot_kwargs,
        )
        plt.tight_layout()
        plt.show()
