import requests
import json

__author__ = 'proccaserra (Philippe Rocca-Serra)'

# author: philippe rocca-serra (philippe.rocca-serra@oerc.ox.ac.uk)
# ontology: http://www.stato-ontology.org

zenodo_baseurl = "https://zenodo.org/api/"
headers = {"Content-Type": "application/json"}

# create a zenodo account and obtain an API token from the
ACCESS_TOKEN = "<enter-your_writeonly_token_for_testing or your_deposit_token if you want to get a DOI  >"

# testing the connection
r = requests.get("https://zenodo.org/api/deposit/depositions", params={"access_token": ACCESS_TOKEN})

# creating an empty submission to get an zenodo record id:
r = requests.post('https://zenodo.org/api/deposit/depositions', params={'access_token': ACCESS_TOKEN}, json={},
                  headers=headers)
r.status_code

# obtain the zenodo metadata payload as json containing the id
r.json()

# getting the record id
deposition_id = r.json()['id']

# uploading the data

data = {'filename': 'rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.csv'}
files = {'file': open('../data/processed/rose-data/rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.csv', 'rb')}

r = requests.post('https://zenodo.org/api/deposit/depositions/%s/files' % deposition_id,
                   params={'access_token': ACCESS_TOKEN}, data=data,
                   files=files)
r.status_code

# forming the augmented data payload for a dataset corresponding to the JSON data package for the matrix
data = {
     "metadata": {
         "title": "Tabular data package for GC-MS data from Rose Genome article published\
          in Nature genetics, June, 2018",
         "upload_type": "dataset",
         "description": "This dataset, in the form of a Frictionless Tabular Data Package \
         (https://frictionlessdata.io/specs/tabular-data-package/), \
          holds the measurements of 61 known metabolites (all annotated with resolvable CHEBI identifiers and InChi), \
          measured by gas chromatography mass-spectrometry (GC-MS) in 6 different Rose cultivars (all annotated with \
          resolvable NCBITaxId) and 3 organism parts (all annotated with resolvable Plant Ontology identifiers).\
          The data was extracted from a supplementary material table, available from \
          https://static-content.springer.com/esm/art%3A10.1038%2Fs41588-018-0110-3/MediaObjects/41588_2018_110_MOESM3_ESM.zip \
          and published alongside the Nature Genetics manuscript identified by the following doi:\
          https://doi.org/10.1038/s41588-018-0110-3, published in June 2018. \
          This dataset is used to demonstrate how to make data Findeable, Accessible, Discoverable and Interoperable"\
          "(FAIR) and how Tabular Data Package representations can be easily mobilized for re-analysis and data science.\
          It is associated to the following project available from github at: "
          "https://github.com/proccaserra/rose2018ng-notebook with all necessary information and Jupyter notebooks.",
         "creators": [
                      {
                        "affiliation": "University of Oxford",
                        "name": "Philippe Rocca-Serra",
                        "orcid": "0000-0001-9853-5668"
                      },
                      {
                        "affiliation": "University of Oxford",
                        "name": "Susanna Assunta Sansone",
                        "orcid": "0000-0001-5306-5690"
                      }
                    ],
         "access_right": "open",
         "keywords": [
             "FAIR data",
             "Design of Experiment",
             "Rose scent",
             "targeted metabolite profiling",
             "gas chromatography mass spectrometry",
             "Tabular Data Package",
             "STATO ontology",
             "ISA format",
             "interoperability"],
         "language": "eng",
         "license": {
                "id": "CC-BY-4.0"
                    },
         "publication_date": "2019-03-13",
         "references": [
             "The Rosa genome provides new insights into the domestication of modern roses.\
              https://doi.org/10.1038/s41588-018-0110-3"
            ]
        }
    }

r = requests.put("https://zenodo.org/api/deposit/depositions/%s" % deposition_id,
                  params={"access_token": ACCESS_TOKEN}, data=json.dumps(data),
                 headers=headers)

r.status_code
