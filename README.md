# rose2018ng-notebook

a repository for notebooks associated with Rose targeted metabolite profiling analysis (nature genetics 2018)

# Specifying an R environment with a runtime.txt file

_Experimental_ You may try running the notebooks using [Binder](https://mybinder.org/). If this route does not behave, the notebooks should be run in your local jupyter notebook installation

Jupyter+R: [![Binder](http://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/dev?filepath=rose-metabolites-analysis.ipynb)

Jupyter+Python+Sparql: [![Binder](http://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/dev?filepath=rose-rdf.ipynb)

[IRKernel](https://irkernel.github.io/)
is installed by default.


# If Jyputer running locally, you'll need to set a python sparql kernel[IRKernel](https://irkernel.github.io/)
is installed by default. up to be able to run SPARQL

(based on https://github.com/paulovn/sparql-kernel)

You will need Jupyter >= 4.0. The module is installable via ``pip``.

The installation process requires two steps:

1. Install the Python package::

     pip install sparqlkernel

2. Install the kernel into Jupyter::

     jupyter sparqlkernel install [--user] [--logdir <dir> ]

The ``--user`` option will install the kernel in the current user's personal
config, while the generic command will install it as a global kernel (but
needs write permissions in the system directories).

