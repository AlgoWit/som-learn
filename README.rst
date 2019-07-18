.. -*- mode: rst -*-

.. _scikit-learn: http://scikit-learn.org/stable/

.. _Somoclu: https://somoclu.readthedocs.io/en/stable/

|Travis|_ |Codecov|_ |CircleCI|_ |ReadTheDocs|_ |PythonVersion|_ |Pypi|_ |Conda|_

.. |Travis| image:: https://travis-ci.org/AlgoWit/som-learn.svg?branch=master
.. _Travis: https://travis-ci.org/AlgoWit/som-learn

.. |Codecov| image:: https://codecov.io/gh/AlgoWit/som-learn/branch/master/graph/badge.svg
.. _Codecov: https://codecov.io/gh/AlgoWit/som-learn

.. |CircleCI| image:: https://circleci.com/gh/AlgoWit/som-learn/tree/master.svg?style=svg
.. _CircleCI: https://circleci.com/gh/AlgoWit/som-learn/tree/master

.. |ReadTheDocs| image:: https://readthedocs.org/projects/som-learn/badge/?version=latest
.. _ReadTheDocs: https://som-learn.readthedocs.io/en/latest/?badge=latest

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/som-learn.svg
.. _PythonVersion: https://img.shields.io/pypi/pyversions/som-learn.svg

.. |Pypi| image:: https://badge.fury.io/py/som-learn.svg
.. _Pypi: https://badge.fury.io/py/som-learn

.. |Conda| image:: https://anaconda.org/algowit/som-learn/badges/installer/conda.svg
.. _Conda: https://conda.anaconda.org/algowit

=========
som-learn
=========

Implementation of Self-Organizing Map algorithm [1]_ that is compatible with
scikit-learn_ API. It provides a wrapper class around Somoclu_.

Documentation
-------------

Installation documentation, API documentation, and examples can be found on the
documentation_.

.. _documentation: https://som-learn.readthedocs.io/en/latest/

Dependencies
------------

som-learn is tested to work under Python 3.6+. The dependencies are the
following:

- scikit-learn(>=0.21)
- somoclu(>=1.7.5)

Additionally, to run the examples, you need matplotlib(>=2.0.0) and
pandas(>=0.22).

Installation
------------

som-learn is currently available on the PyPi's repository and you can
install it via `pip`::

  pip install -U som-learn

The package is released also in Anaconda Cloud platform::

  conda install -c algowit som-learn

If you prefer, you can clone it and run the setup.py file. Use the following
commands to get a copy from GitHub and install all dependencies::

  git clone https://github.com/AlgoWit/som-learn.git
  cd som-learn
  pip install .

Or install using pip and GitHub::

  pip install -U git+https://github.com/AlgoWit/som-learn.git

Testing
-------

After installation, you can use `pytest` to run the test suite::

  make test

References:
-----------

.. [1] T. Kohonen, M. R. Schroeder, T. S. Huang, "Self-Organizing Maps",
   Springer-Verlag, 2001.

