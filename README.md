# rose2018ng-notebook

a repository for notebooks associated with Rose targeted metabolite profiling analysis (nature genetics 2018)

# Specifying an R environment with a runtime.txt file

Jupyter+R: [![Binder](http://mybinder.org/badge.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master?filepath=rose-metabolites-analysis.ipynb)

[IRKernel](https://irkernel.github.io/)
is installed by default.


# Setting up to be able to run SPARQL

(based on https://github.com/paulovn/sparql-kernel)

You will need Jupyter >= 4.0. The module is installable via ``pip``.

The installation process requires two steps:

1. Install the Python package::

     pip install sparqlkernel

2. Install the kernel into Jupyter::

     jupyter sparqlkernel install [--user] [--logdir <dir>]

The ``--user`` option will install the kernel in the current user's personal
config, while the generic command will install it as a global kernel (but
needs write permissions in the system directories).

