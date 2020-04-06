"""
It contains the Self-Organizing Map (SOM) clusterer.
"""

# Author: Georgios Douzas <gdouzas@icloud.com>
# License: BSD 3 clause

from itertools import product

import numpy as np
from sklearn.base import BaseEstimator, ClusterMixin
from sklearn.utils import check_random_state
from sklearn.utils.validation import check_array
from sklearn.preprocessing import minmax_scale
from somoclu import Somoclu


class SOM(BaseEstimator, ClusterMixin):
    """Class to fit and visualize a Self-Organizing Map (SOM).

    The implementation uses SOM from Somoclu.

    Read more in the :ref:`User Guide <user_guide>`.

    Parameters
    ----------

    n_columns : int, optional (default=5)
        The number of columns in the map.

    n_rows : int, optional (default=5)
        The number of rows in the map.

    initialcodebook : 2D numpy.array of float32, str or None, optional (default=None)
        Define the codebook to start the training. If ``initialcodebook='pca'`` then
        the codebook is initialized from the first subspace spanned by the first two
        eigenvectors of the correlation matrix.

    kerneltype : int, optional (default=0)
        Specify which kernel to use. If ``kerneltype=0`` use dense CPU kernel.
        Else if ``kerneltype=1`` use dense GPU kernel if compiled with it.

    maptype : str, optional (default='planar')
        Specify the map topology. If ``maptype='planar'`` use planar map.
        Else if ``maptype='toroid'`` use toroid map.

    gridtype : str, optional (default='rectangular')
        Specify the grid form of the nodes. If ``gridtype='rectangular'``
        use rectangular neurons. Else if ``gridtype='hexagonal'`` use
        hexagonal neurons.

    compactsupport : bool, optional (default=True)
        Cut off map updates beyond the training radius with the Gaussian neighborhood.

    neighborhood : str, optional (default='gaussian')
        Specify the neighborhood. If ``neighborhood='gaussian'`` use
        Gaussian neighborhood. Else if `neighborhood='bubble'`` use
        bubble neighborhood function.

    std_coeff : float, optional (default=0.5)
        Set the coefficient in the Gaussian
        neighborhood :math:`exp(-||x-y||^2/(2*(coeff*radius)^2))`.

    random_state : int, RandomState instance or None, optional (default=None)
        Control the randomization of the algorithm by specifying the
        codebook initalization. It is ignored when ``initialcodebook`` is
        not ``None``.

        - If int, ``random_state`` is the seed used by the random number
          generator.
        - If ``RandomState`` instance, random_state is the random number
          generator.
        - If ``None``, the random number generator is the ``RandomState``
          instance used by ``np.random``.

    verbose : int, optional (default=0)
        Specify verbosity level (0, 1, or 2).

    """

    _attributes = ['train', 'codebook', 'bmus']

    def __init__(
        self,
        n_columns=5,
        n_rows=5,
        initialcodebook=None,
        kerneltype=0,
        maptype="planar",
        gridtype="rectangular",
        compactsupport=True,
        neighborhood="gaussian",
        std_coeff=0.5,
        random_state=None,
        verbose=0,
    ):

        self.n_columns = n_columns
        self.n_rows = n_rows
        self.initialcodebook = initialcodebook
        self.kerneltype = kerneltype
        self.maptype = maptype
        self.gridtype = gridtype
        self.compactsupport = compactsupport
        self.neighborhood = neighborhood
        self.std_coeff = std_coeff
        self.random_state = random_state
        self.verbose = verbose

    @staticmethod
    def _generate_labels_mapping(grid_labels):
        """Generate a mapping between grid labels and cluster labels."""

        # Identify unique grid labels
        unique_labels = [
            tuple(grid_label) for grid_label in np.unique(grid_labels, axis=0)
        ]

        # Generate mapping
        labels_mapping = {
            grid_label: cluster_label
            for grid_label, cluster_label in zip(
                unique_labels, range(len(unique_labels))
            )
        }

        return labels_mapping

    def _return_topological_neighbors(self, col, row):
        """Return the topological neighbors of a neuron."""

        # Return common topological neighbors for the two grid types
        topological_neighbors = [
            (col - 1, row),
            (col + 1, row),
            (col, row - 1),
            (col, row + 1),
        ]

        # Append extra topological neighbors for hexagonal grid type
        if self.gridtype == 'hexagonal':
            offset = (-1) ** row
            topological_neighbors += [
                (col - offset, row - offset),
                (col - offset, row + offset),
            ]

        # Apply constraints
        topological_neighbors = [
            (col, row)
            for col, row in topological_neighbors
            if 0 <= col < self.n_columns
            and 0 <= row < self.n_rows
            and [col, row] in self.algorithm_.bmus.tolist()
        ]

        return topological_neighbors

    def _generate_neighbors(self, grid_labels, labels_mapping):
        """Generate pairs of neighboring labels."""

        # Generate grid topological neighbors
        grid_topological_neighbors = [
            product(
                [tuple(grid_label)], self._return_topological_neighbors(*grid_label)
            )
            for grid_label in grid_labels
        ]

        # Flatten grid topological neighbors
        grid_topological_neighbors = [
            pair for pairs in grid_topological_neighbors for pair in pairs
        ]

        # Generate cluster neighbors
        all_neighbors = [
            (labels_mapping[pair[0]], labels_mapping[pair[1]])
            for pair in grid_topological_neighbors
        ]
        all_neighbors = [tuple(pair) for pair in np.unique(all_neighbors, axis=0)]

        # Keep unique unordered pairs
        neighbors = []
        for pair in all_neighbors:
            if pair not in neighbors and pair[::-1] not in neighbors:
                neighbors.append(pair)

        return np.array(neighbors)

    def fit(self, X, y=None, **fit_params):
        """Train the self-organizing map.

        Parameters
        ----------
        X : array-like or sparse matrix, shape=(n_samples, n_features)
            Training instances to cluster.

        y : Ignored
        """

        # Check and normalize input data
        X = minmax_scale(check_array(X, dtype=np.float32))

        # Check random_state
        self.random_state_ = check_random_state(self.random_state)

        # Initialize codebook
        if self.initialcodebook is None:
            if self.random_state is None:
                initialcodebook = None
                initialization = 'random'
            else:
                codebook_size = self.n_columns * self.n_rows * X.shape[1]
                initialcodebook = self.random_state_.random_sample(
                    codebook_size
                ).astype(np.float32)
                initialization = None
        elif self.initialcodebook == 'pca':
            initialcodebook = None
            initialization = 'random'
        else:
            initialcodebook = self.initialcodebook
            initialization = None

        # Create Somoclu object
        self.algorithm_ = Somoclu(
            n_columns=self.n_columns,
            n_rows=self.n_rows,
            initialcodebook=initialcodebook,
            kerneltype=self.kerneltype,
            maptype=self.maptype,
            gridtype=self.gridtype,
            compactsupport=self.compactsupport,
            neighborhood=self.neighborhood,
            std_coeff=self.std_coeff,
            initialization=initialization,
            data=None,
            verbose=self.verbose,
        )

        # Fit Somoclu
        self.algorithm_.train(data=X, **fit_params)

        # Grid labels
        grid_labels = [tuple(grid_label) for grid_label in self.algorithm_.bmus]

        # Generate labels mapping
        self.labels_mapping_ = self._generate_labels_mapping(grid_labels)

        # Generate cluster labels
        self.labels_ = np.array(
            [self.labels_mapping_[grid_label] for grid_label in grid_labels]
        )

        # Generate labels neighbors
        self.neighbors_ = self._generate_neighbors(
            np.unique(grid_labels, axis=0), self.labels_mapping_
        )

        return self

    def fit_predict(self, X, y=None, **fit_params):
        """Train the self-organizing map and assign a cluster label to each sample.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = [n_samples, n_features]
            New data to transform.

        u : Ignored

        Returns
        -------
        labels : array, shape [n_samples,]
            Index of the cluster each sample belongs to.
        """
        return self.fit(X, **fit_params).labels_
