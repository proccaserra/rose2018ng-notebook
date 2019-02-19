rose2018ng-notebooks
==============================

A FAIRification project aiming at recovering GC-MS based metabolite profiles of Rose scent published in Nature Genetics, in June 2018, demonstrating the use of Frictionless Tabular data package, Semantic markup of chemicals with CHEBI ontology and InCHI for annotation, markup of measurements with STATO ontology, and insisting on the need to clarify the semantics of data matrices. A full Linked Data (LD) representation is provided and visualization of the metabolite profiles in 6 rose strains and 3 plants parts is presented.

 rose2018ng-notebooks

a repository for notebooks associated with the Rose targeted metabolite profiling analysis (nature genetics 2018)

Three notebooks are available and can be run locally or using the [Binder](https://mybinder.org/) infrastructure.

Note that launching notebook with binder may take several minutes (10-15 minutes) for the installation process to complete the first time around and depending on load on the infrastructure. Once done and as long as the build remains on the Binder infrastructure, starting and running the notebooks is very quick. However, bear in mind that the lifespan of these notebook instances on the virtual infrastructure is by nature limited.

[![Binder](http://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master?filepath=/notebooks/1-rose-metabolites-Python-analysis.ipynb) A Jupyter+R notebook: 1-rose-metabolites-Python-analysis.ipynb

[![Binder](http://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master?filepath=rose-rdf.ipynb) A Jupyter+Python+Sparql notebook: rose-rdf.ipynb

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





Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
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
    └──  setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.testrun.org


