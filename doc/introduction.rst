.. _scikit-learn: http://scikit-learn.org/stable/

.. _somoclu: https://somoclu.readthedocs.io/en/stable/

.. _introduction:

============
Introduction
============

.. _api_somlearn:

API
---

The package som-learn follows the scikit-learn API using the base
clusterer functionality. More specifically:

It implements a ``fit`` method to learn from data::

      clusterer = object.fit(data)

it implements a ``fit_predict`` method to predict cluster labels::

      cluster_labels = object.fit_predic(data)

SOM clusterer accepts the following inputs:

* ``data``: array-like (2-D list, pandas.Dataframe, numpy.array) or sparse
  matrices;

Self-Organizing Map
-------------------

A Self-Organizing Map (SOM), also called Kohonen map, is a type of
artificial neural network that is trained using unsupervised learning to
produce a low-dimensional, discretized representation of the input space,
called a map. SOM can be used as a clustering algorithm as well as a
dimensionality reduction method. The :class:`SOM` class is a scikit-learn_
compatible wrapper class around somoclu_'s implementation of SOM.
