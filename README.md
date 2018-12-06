# rose2018ng-notebooks

a repository for notebooks associated with the Rose targeted metabolite profiling analysis (nature genetics 2018)

Two notebooks are available, each with specific requirements so we ease of use, we have looked into using the Binder infrastructure.

_Experimental_ You may try running the notebooks using [Binder](https://mybinder.org/).

Note that launching notebook with binder may take several minutes (10-15 minutes) for the installation process to complete the first time around and depending on load on the infrastructure. Once done and as long as the build remains on the Binder infrastructure, starting and running the notebooks is very quick. However, bear in mind that the lifespan of these notebook instances on the virtual infrastructure is by nature limited.

[![Binder](http://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master?filepath=rose-metabolites-analysis.ipynb) A Jupyter+R notebook: rose-metabolites-analysis.ipynb

[![Binder](http://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master?filepath=rose-rdf.ipynb) A Jupyter+Python+Sparql notebook: rose-rdf.ipynb

If the binder route does not behave, you may run the notebooks locally. See below for the instructions.

# If running jupyter locally:

## running the rose-rdf.ipynb requires a python sparql kernel

You'll need to set a python sparql kernel  up to be able to run SPARQL

(based on https://github.com/paulovn/sparql-kernel)

You will need Jupyter >= 4.0. The module is installable via ``pip``.

The installation process requires two steps:

1. Install the Python package::

     pip install sparqlkernel

2. Install the kernel into Jupyter::

     jupyter sparqlkernel install [--user ] [--logdir  ]

The ``--user`` option will install the kernel in the current user's personal
config, while the generic command will install it as a global kernel (but
needs write permissions in the system directories).


## running the rose-metabolites-analysis.ipynb requires an R kernel

It is installed by default with the current set up  configuration

[IRKernel](https://irknernel.github.io)
