# rose2018ng-notebook

a repository for notebooks associated with Rose targeted metabolite profiling analysis (nature genetics 2018)

# Specifying an R environment with a runtime.txt file

Jupyter+R: [![Binder](http://mybinder.org/badge.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master?filepath=rose-metabolites-analysis.ipynb)

TEST: [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/ISA-tools/dtp-isa-exercises/master?filepath=exercise.ipynb)

RStudio: [![Binder](http://mybinder.org/badge.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master?urlpath=rstudio)

RShiny: [![Binder](http://mybinder.org/badge.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master?urlpath=shiny/)

Binder supports using R and RStudio, with libraries pinned to a specific
snapshot on [MRAN](https://mran.microsoft.com/documents/rro/reproducibility).

You need to have a `runtime.txt` file that is formatted like:

```
r-<YYYY>-<MM>-<DD>
```

where YYYY-MM-DD is a snapshot at MRAN that will be used for installing
libraries.

You can also have an `install.R` file that will be executed during build,
and can be used to install libraries.

Both [RStudio](https://www.rstudio.com/) and [IRKernel](https://irkernel.github.io/)
are installed by default, so you can use either the Jupyter notebook interface or
the RStudio interface.


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

