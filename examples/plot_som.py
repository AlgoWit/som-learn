"""
====================================
Clustering using Self-Organizing Map
====================================

This example illustrates the fitted Self-Organizing Map
for various datasets as well as the resulting neighboring
structure between clusters.

"""

# Author: Georgios Douzas <gdouzas@icloud.com>
# Licence: MIT

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
from sklearn.base import clone
from sklearn.datasets import make_blobs, make_s_curve, make_swiss_roll

from somlearn import SOM

print(__doc__)

RANDOM_STATE = 170
N_SAMPLES = 500
NAMES = [
    'Basic',
    'Anisotropic',
    'Unequal Variance',
    'Uneven Blobs',
    'S Curve',
    'Swiss Roll',
]
CLUSTERER = SOM(n_columns=2, n_rows=2, gridtype='hexagonal', random_state=RANDOM_STATE)


def generate_data(name):
    """Generate data for various cases."""
    if name in ('Basic', 'Anisotropic', 'Uneven Blobs'):
        X, y = make_blobs(n_samples=N_SAMPLES, random_state=RANDOM_STATE, centers=4)
    if name == 'Anisotropic':
        transformation = [[0.60834549, -0.63667341], [-0.40887718, 0.85253229]]
        X = np.dot(X, transformation)
    elif name == 'Unequal Variance':
        X, _ = make_blobs(
            n_samples=N_SAMPLES, cluster_std=[1.0, 2.5, 0.5], random_state=RANDOM_STATE
        )
    elif name == 'Uneven Blobs':
        X = np.vstack((X[y == 0][:150], X[y == 1][:50], X[y == 2][:10]))
    elif name == 'S Curve':
        X, _ = make_s_curve(n_samples=N_SAMPLES, random_state=RANDOM_STATE)
        X = X[:, [0, 2]]
    elif name == 'Swiss Roll':
        X, _ = make_swiss_roll(n_samples=N_SAMPLES, random_state=RANDOM_STATE)
        X = X[:, [0, 2]]
    return X


def plot_data(X, som_clusterer, title, ind):
    """Plot data with cluster labels."""
    y_pred = som_clusterer.fit_predict(X)
    plt.subplot(321 + ind)
    plt.scatter(X[:, 0], X[:, 1], c=y_pred)
    plt.title(title)


###############################################################################
# Generate data
###############################################################################

###############################################################################
# We are generating a variety of datasets that cover different scenarios.
# More specifically, a basic dataset with three similar clusters, an
# anisotropic variation of the previous case, another varition with unequal
# variance a dataset with unevenly sized blobs and the S curve and swiss roll
# datasets.

Xs = [generate_data(name) for name in NAMES]

###############################################################################
# Plot datasets with cluster labels
###############################################################################

###############################################################################
# We plot the datasets and the cluster labels predicted by Self-Organizing Map.

plt.figure(figsize=(12, 12))
for ind, (X, title) in enumerate(zip(Xs, NAMES)):
    clusterer = clone(CLUSTERER)
    plot_data(X, clusterer, title, ind)
plt.show()
