.. _scikit-learn: http://scikit-learn.org/stable/

.. _somoclu: https://somoclu.readthedocs.io/en/stable/

.. _somlearn:

===================
Self-Organizing Map
===================

.. currentmodule:: somlearn

A practical guide
-----------------

A Self-Organizing Map (SOM) [KSH2001]_, also called Kohonen map, is a type of
artificial neural network that is trained using unsupervised learning to
produce a low-dimensional, discretized representation of the input space,
called a map. SOM can be used as a clustering algorithm as well as a
dimensionality reduction method. The :class:`SOM` class is a scikit-learn_
compatible wrapper class around somoclu_'s implementation of SOM.
It offers such scheme::

   >>> from collections import Counter
   >>> from sklearn.datasets import make_classification
   >>> from somlearn import SOM
   >>> X, _ = make_classification(random_state=0)
   >>> som = SOM(n_columns=2, n_rows=2, random_state=1)
   >>> labels = som.fit_predict(X)
   >>> print(sorted(Counter(labels).items()))
   [(0, 24), (1, 29), (2, 19), (3, 28)]
   >>> print(som.neighbors_.tolist())
   [[0, 1], [0, 2], [1, 3], [2, 3]]

.. topic:: References

   .. [KSH2001] T. Kohonen, M. R. Schroeder, T. S. Huang, "Self-Organizing Maps",
      Springer-Verlag, 2001.
