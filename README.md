rose2018ng-notebooks
==============================

A data science project aiming at making a GC-MS based metabolite profiles of Rose scent published in [Nature Genetics, in June 2018](https://doi.org/10.1038/s41588-018-0110-3) compliant with the [FAIR principles](https://doi.org/10.1038/sdata.2016.18), through the use of several data standards, namely: [Frictionless Tabular data package](https://frictionlessdata.io/specs/tabular-data-package/) as syntax for the data matrix, semantic markup of measurements with [STATO ontology](https://github.com/isa-tools/stato), of chemicals with [CHEBI ontology](http://purl.obolibrary.org/obo/chebi.owl) and InChi for annotation, and insisting on the need to clarify the semantics of data matrices.

To re-enact the FAIRification process we have performed on this dataset, 2 options are available: either running the Make command, or run the Jupyter notebooks which are provided. 

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


## 1. Running with Make:
    
- ensure that Python 3.6 is installed or available in a virtual environment.
    - NOTE: On MacOS, whether running a virtualenv or not, you may need to create the following file:
        ```touch /.matplotlib/matplotlibrc```
    - open the file and  add the following to it: ```backend: TkAgg```
    - save and close.
- from the root folder of the project, invoke the following commands:
    - ```make data``` to convert the excel and pdf legacy data into the Frictionaless Data Package: 
        (the ouput of the command will be stored in the 'denovo' folder under './data/processed/')
    - ```make figure``` to generate the figures (the reference output is stored, under './figures' directory):
        (the output of the command will be stored in the 'denovo' folder under './figures') 
    - NOTE: the script ```src/rose-plotting-from-rdf.py``` runs a sparql query, which may take time to execute. One may wish to bypass this and comment out line 41 in the ```make``` file.  
    - ```make clean``` to restore the project to its initial status, this will remove all "denovo" created data).


## 2. Running the Notebooks with Jupyter:

An exhaustive documentation, in the form of a series of jupyter notebooks, is provided. It describes the various steps of the FAIRification process. 
The Four notebooks are available and can be run locally or using the [Binder](https://mybinder.org/) infrastructure.
Note that launching notebook with binder may take several minutes (10-15 minutes) for the installation process to complete the first time around and depending on load on the infrastructure. Once done and as long as the build remains on the Binder infrastructure, starting and running the notebooks is very quick. However, bear in mind that the lifespan of these notebook instances on the virtual infrastructure is by nature limited.

### 2.1 Running the notebooks using mybinder infrastructure:

1. Start Binder environment from the main repository:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master)

Once again, if running with myBinder.org, be aware that it takes some time to build the environment the first time around. Let the process complete. 

2. Start Binder environment from individual notebooks:

    + Converting the original Excel spreadsheet released as supplementary material to a Frictionless Tabular Data package.

    [![Binder](http://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master?filepath=%2Fnotebooks%2F0-rose-metabolites-Python-data-handling.ipynb) A Jupyter+Python notebook: 0-rose-metabolites-Python-data-handling.ipynb

    A data exploration and graphical recapitulation of the dataset is performed in python using the graphic grammar library plotnine from either the Tabular Data Package or from the RDF/Linked Data graph, to demonstrate that equivalency of the representations. A visual exploration also shows how 2 datasets treated with the same protocol can be readily mobilized for a data integration exercise.

    (Note: known issue = when using mybinder infrastructure, the call to the libchebi api may time out. This is an issue with the infrastructure, not the code being run). Running the code locally (see below for instructions).

    + Analysing the metabolite profiles using python and the plotnine library from the Frictionless Data Package:

    [![Binder](http://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master?filepath=%2Fnotebooks%2F1-rose-metabolites-Python-analysis.ipynb) A Jupyter+Python notebook: 1-rose-metabolites-Python-analysis.ipynb

    + Recapitulating the analysis done previously but from an RDF graph and SPARQL queries. 
     A full Linked Data (LD) representation is provided and visualization of the metabolite profiles in 6 rose strains and 3 plants parts is presented.

     (Note: known issue: the 3rd sparql query can take time to execute, be patient) 

    [![Binder](http://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master?filepath=%2Fnotebooks%2F2-rose-metabolites-Python-RDF-querying-analysis.ipynb) A Jupyter+Python+Sparql notebook: 2-rose-metabolites-Python-RDF-querying-analysis.ipynb

    + A fourth notebook performs the visual exploration of the dataset using R, to show case how the Tabular Data Package can be consumed in a different environment very easily.

    [![Binder](http://mybinder.org/badge_logo.svg)](http://beta.mybinder.org/v2/gh/proccaserra/rose2018ng-notebook/master?filepath=%2Fnotebooks%2F3-rose-metabolites-R-analysis.ipynb) A Jupyter+R notebook: 3-rose-metabolites-R-analysis.ipynb


    If the binder route does not behave, simply run the notebooks locally, following the instructions below.


### 2.2. Running the notebooks locally using Jupyter on your machine:

You will need *Python 3.6*, *jupyter*, and *virtualenv* (if you want to use virtual environments).

1. Clone this repository: ```git clone https://github.com/proccaserra/rose2018ng-notebook```  
1. Get into the repository: ```cd rose2018ng-notebook```

If you do not want to use a [virtual environment](http://akbaribrahim.com/managing-python-virtual-environments-with-pyenv-virtualenv/), skip the first two steps below:

1. Create a virtual environment: ```pyenv virtualenv 3.6.5 venv365``` 
1. Activate the virtual environment ```pyenv activate venv365 ```
1. Install all the requirements: ```pip install -r requirements.txt```
1. Make sure the ipython kernel is available: ```ipython kernel install --user```
1. Run jupyter notebook: ```jupyter notebook```


#### Running the 2-rose-metabolites-Python-RDF-querying-analysis.ipynb requires a python sparql kernel

A python sparql kernel is needed to be able to run SPARQL queries

It is installed by default with the current set up  configuration.

(based on https://github.com/paulovn/sparql-kernel)

The installation process requires two steps:

    1. Install the Python package::
         ```pip install sparqlkernel```
    2. Install the kernel into Jupyter::
         jupyter sparqlkernel install [--user ] [--logdir  ]

The ``--user`` option will install the kernel in the current user's personal
config, while the generic command will install it as a global kernel (but
needs write permissions in the system directories).


#### Running the 3-rose-metabolites-R-analysis.ipynb requires R installed and an IPython R kernel

To install R, please see [here](https://www.r-project.org/)
To install the IPython R kernel, refer to [IRKernel](https://irkernel.github.io):
    
    1. Start R from a terminal 
    (Important: *do not* run R from the app if you try to install the kernel, it must be from a terminal)
    2. From the R terminal, issue ```IRkernel::installspec(user=FALSE)```.
    Note: if running into problems (e.g.), try running R with the following command: 
    ```sudo -i R``` first, and then run the kernel installation.
    If you are still stuck, have a look at [this tutorial](https://mpacer.org/maths/r-kernel-for-ipython-notebook)




