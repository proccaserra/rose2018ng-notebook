rose2018ng-notebooks
==============================

A data science project aiming at making a GC-MS based metabolite profiles of Rose scent published in Nature Genetics, in June 2018 compliant with the FAIR principles, through the use of several data standards, namely: Frictionless Tabular data package as syntax for the data matrix, Semantic markup of chemicals with CHEBI ontology and InCHI for annotation, markup of measurements with STATO ontology, and insisting on the need to clarify the semantics of data matrices.

A exhaustive documentation of the transformation process is provided in the form of a jupyter notebook.

A full Linked Data (LD) representation is provided and visualization of the metabolite profiles in 6 rose strains and 3 plants parts is presented.

A data exploration and graphical recapitulation of the dataset is performed in python using the graphic grammar library plotnine from either the Tabular Data Package or from the RDF/Linked Data graph, to demonstrate that equivalency of the representations.

A visual exploration also shows how 2 datasets treated with the same protocols can be readily mobilized for a data integration exercise.


Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │    
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         and a short `-` delimited description, `1-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── figures            <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org



rose2018ng-notebooks/notebooks is a a repository for notebooks associated with the Rose targeted metabolite profiling analysis (nature genetics 2018)

Four notebooks are available and can be run locally or using the [Binder](https://mybinder.org/) infrastructure.

Note that launching notebook with binder may take several minutes (10-15 minutes) for the installation process to complete the first time around and depending on load on the infrastructure. Once done and as long as the build remains on the Binder infrastructure, starting and running the notebooks is very quick. However, bear in mind that the lifespan of these notebook instances on the virtual infrastructure is by nature limited.

[![Binder](http://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/dev?filepath=%2Fnotebooks%2F0-rose-metabolites-Python-data-handling.ipynb) A Jupyter+Python notebook: 0-rose-metabolites-Python-data-handling.ipynb

[![Binder](http://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/dev?filepath=%2Fnotebooks%2F1-rose-metabolites-Python-analysis.ipynb) A Jupyter+Python notebook: 1-rose-metabolites-Python-analysis.ipynb

[![Binder](http://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/dev?filepath=%2Fnotebooks%2F2-rose-metabolites-Python-RDF-querying-analysis.ipynb) A Jupyter+Python+Sparql notebook: 2-rose-metabolites-Python-RDF-querying-analysis.ipynb


[![Binder](http://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/dev?filepath=%2Fnotebooks%2F3-rose-metabolites-R-analysis.ipynb) A Jupyter+R notebook: 3-rose-metabolites-R-analysis.ipynb

If the binder route does not behave, you may run the notebooks locally. See below for the instructions.


# If running jupyter locally:

## running the 2-rose-metabolites-Python-RDF-querying-analysis.ipynb requires a python sparql kernel

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


## running the 3-rose-metabolites-R-analysis.ipynb requires an R kernel

It is installed by default with the current set up  configuration

[IRKernel](https://irknernel.github.io)

