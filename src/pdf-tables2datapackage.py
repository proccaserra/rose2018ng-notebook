import camelot
import os
import pandas as pd
import re
import libchebipy
from datapackage import Package
from goodtables import validate

__author__ = 'proccaserra (Philippe Rocca-Serra)'

# author: philippe rocca-serra (philippe.rocca-serra@oerc.ox.ac.uk)
# ontology: http://www.stato-ontology.org

def get_chebi_ids(dataframe, number_of_items):
    # a method to obtain InChi and Chebi ID from a chemical name using libchebi
    # takes 2 arguments: a data frame and a number of chemicals

    for idx in range(0, number_of_items):
        hit = libchebipy.search(dataframe.loc[idx, 'chemical_name'], True)
        if len(hit) > 0:
            # print("slice -  HIT: ",element, ":", hit[0].get_inchi(), "|", hit[0].get_id())
            dataframe.loc[idx, 'inchi'] = hit[0].get_inchi()
            dataframe.loc[idx, 'chebi_identifier'] = hit[0].get_id()
        else:
            # print("slice - nothing found: ", data_slice.loc[i, 'chemical_name'])
            dataframe.loc[idx, 'inchi'] = ''
            dataframe.loc[idx, 'chebi_identifier'] = ''

    return dataframe


def validate_datapkg(tab_data_package_file, data_package_definition):
    # validating the output against JSON data package specifications
    # Getting the JSON Tabular DataPackage Definition from the store:
    try:
        pack = Package(data_package_definition)
        pack.valid
        pack.errors
        for e_as_error in pack.errors:
            print(e_as_error)
        # print(pack.profile.name)

        report = validate(tab_data_package_file)
        if report:
            # print(report['valid'])
            print("\n" + tab_data_package_file + ": Nice one! A valid \'2 Factor Mean + Standard Error Tabular Data Package\'\n")
        else:
            print("Sorry :( Vadidation failed, please check: ", tab_data_package_file, "\n")
            print(report)
    except IOError as er:
        print(er)


cwd = os.getcwd()
os.chdir('../data/raw')
cwd = os.getcwd()

# invoking camelot to read a pdf file and extracting tables located at specific pages
tables = camelot.read_pdf('MagnardSM.pdf', pages='19,20,21', flavor='stream', split_text=True)
tables.export('science.csv', f='csv', compress=False)

# since the same table is spread over several pages, we push them to an array
array_of_df = []
for i in range(len(tables)):
    array_of_df.append(tables[i].df)

# we merge all these tables held in our array into one same data frame using pandas concat() function
S1_table_data = pd.concat(array_of_df)

# resetting the index and excluded it from the output
S1_table_data = S1_table_data.reset_index(drop=True)

# removing the first 4 lines, which correspond to the a fragment of figure caption
S1_table_data = S1_table_data.drop([0, 1, 2, 3], axis=0)

# resetting the index again
S1_table_data = S1_table_data.reset_index(drop=True)

# renaming dataframe column headers to a predictable pattern:
S1_table_data.rename(columns={0: "chemical_name",
                              1: "sample_mean_1",
                              2: "sample_mean_2",
                              3: "sample_mean_3",
                              4: "sample_mean_4",
                              5: "sample_mean_5",
                              6: "sample_mean_6",
                              7: "sample_mean_7",
                              8: "sample_mean_8",
                              9: "sample_mean_9",
                              10: "sample_mean_0"}, inplace=True)

# fixing the truncated chemical name and some curation on the data
S1_table_data.loc[S1_table_data['chemical_name'] == "3,4-dihydro-β-", 'chemical_name'] = '3,4-dihydro-β-1 ionone'
S1_table_data.loc[S1_table_data['sample_mean_1'] == "1.6a", 'sample_mean_1'] = '1.6'

# removing the extra-line caused by an overhang by long chemical name at row 52
S1_table_data = S1_table_data.drop([52], axis=0)
# resetting the index once more
S1_table_data = S1_table_data.reset_index(drop=True)

# removing the empty lines at the beginning of the data frame, which causes a Key error in wide_to_long() function
S1_table_data = S1_table_data.drop([0, 1], axis=0)
# resetting the index again
S1_table_data = S1_table_data.reset_index(drop=True)

# inserting the chemical annotation fields
S1_table_data.insert(loc=1, column='inchi', value='')
S1_table_data.insert(loc=2, column='chebi_identifier', value='')
S1_table_data.insert(loc=3, column='sem', value='')
S1_table_data['sem'] = S1_table_data['sem'].fillna("0")
S1_table_data.insert(loc=4, column='unit', value='')

# fetching the chemical annotation (InChi and Chebi ID)
S1_table_data = get_chebi_ids(S1_table_data, 52)

#  Here, we drop the first row
S1_table_data=S1_table_data.drop([51, 52], axis=0)
# resetting the index again
S1_table_data = S1_table_data.reset_index(drop=True)

# print(S1_table_data)
# S1_table_data.to_csv("long.txt", sep='\t', encoding='utf-8')

# The following steps are needed to perform the table transformation from a 'wide' layout to a 'long table' one
# Prep stubnames - pick out all the feature_model variables and remove the model suffices
# 'long table' layout is that relied on by Frictionless Tabular Data Packages
# and consumed by R ggplot2 library and Python plotnine library

# Step1: obtain all the different 'dimension' measured for a given condition
# (i.e. repeating fields with an increment suffix)
feature_models = [col for col in S1_table_data.columns if re.match("(sample_mean)_[0-9]", col) is not None]
features = list(set([re.sub("_[0-9]", "", feature_model) for feature_model in feature_models]))
# print("features", features)


#  Here, we drop the first row
S1_table_data.drop([1], inplace=True)
# resetting the index again
S1_table_data = S1_table_data.reset_index(drop=True)

# print(S1_table_data)
# Step2: invoke Pandas pd.wide_to_long() function to carry out the table transformation
# See Pandas documentation for more information:
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.wide_to_long.html
# and the excellent blog: https://medium.com/@wangyuw/data-reshaping-with-pandas-explained-80b2f51f88d2
long_df = pd.wide_to_long(S1_table_data.reset_index(), i=['chemical_name'], j='treatment', stubnames=features, sep="_")
# S1_table_data_long = pd.wide_to_long(S1_table_data.reset_index(), i=['chemical_name'], j='treatment', stubnames=features, sep="_")
long_df.to_csv("long.txt", sep='\t', encoding='utf-8')
# reading from that file to solve the issue
S1_table_data_long = pd.read_csv("long.txt", sep="\t")

# we can now get rid of it:
try:
    os.remove("long.txt")
    for fnames in os.walk("./"):
        # print("folder: ", fnames)
        for f in fnames:
            # print("filename: ", f)
            if len(f)>0:
                for element in f:
                    if element.endswith(".csv"):
                        #x(os.path.join(dirpath, f))
                        os.remove(element)
except IOError as e:
    print(e)

# Adding new fields for each of the independent variable and associated URI, copying from 'treatment field'
S1_table_data_long['var1_levels'] = S1_table_data_long['treatment']
S1_table_data_long['var1_uri'] = S1_table_data_long['treatment']
S1_table_data_long['var2_levels'] = S1_table_data_long['treatment']
S1_table_data_long['var2_uri'] = S1_table_data_long['treatment']

# adding a new field for 'sample size' and setting the value to n=3
S1_table_data_long['sample_size'] = 3

S1_table_data_long['sem'] = S1_table_data_long['sem'].fillna("0")

# Marking up with ontology terms and their resolvable URI for all factor values:
# This requires doing a manual mapping, better ways could be devised.
S1_table_data_long.loc[S1_table_data_long['treatment'] == 1, 'treatment'] = 'Rosa Papa Meilland petals'
S1_table_data_long.loc[S1_table_data_long['var1_levels'] == 1, 'var1_levels'] = 'Papa Meilland'
S1_table_data_long.loc[S1_table_data_long['var1_uri'] == 1, 'var1_uri'] = ''
S1_table_data_long.loc[S1_table_data_long['var2_levels'] == 1, 'var2_levels'] = 'petals'
S1_table_data_long.loc[S1_table_data_long['var2_uri'] == 1, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

S1_table_data_long.loc[S1_table_data_long['treatment'] == 2, 'treatment'] = 'RosaRouge Meilland petals'
S1_table_data_long.loc[S1_table_data_long['var1_levels'] == 2, 'var1_levels'] = 'Rosa Rouge Meilland'
S1_table_data_long.loc[S1_table_data_long['var1_uri'] == 2, 'var1_uri'] = ''
S1_table_data_long.loc[S1_table_data_long['var2_levels'] == 2, 'var2_levels'] = 'petals'
S1_table_data_long.loc[S1_table_data_long['var2_uri'] == 2, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

S1_table_data_long.loc[S1_table_data_long['treatment'] == 3, 'treatment'] = 'Rosa Alister Stella Grey petals'
S1_table_data_long.loc[S1_table_data_long['var1_levels'] == 3, 'var1_levels'] = 'Rosa Alister Stella Grey '
S1_table_data_long.loc[S1_table_data_long['var1_uri'] == 3, 'var1_uri'] = ''
S1_table_data_long.loc[S1_table_data_long['var2_levels'] == 3, 'var2_levels'] = 'petals'
S1_table_data_long.loc[S1_table_data_long['var2_uri'] == 3, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

S1_table_data_long.loc[S1_table_data_long['treatment'] == 4, 'treatment'] = 'Rosa Hacienda petals'
S1_table_data_long.loc[S1_table_data_long['var1_levels'] == 4, 'var1_levels'] = 'Rosa Hacienda'
S1_table_data_long.loc[S1_table_data_long['var1_uri'] == 4, 'var1_uri'] = ''
S1_table_data_long.loc[S1_table_data_long['var2_levels'] == 4, 'var2_levels'] = 'petals'
S1_table_data_long.loc[S1_table_data_long['var2_uri'] == 4, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

S1_table_data_long.loc[S1_table_data_long['treatment'] == 5, 'treatment'] = 'Rosa Pariser Charme petals'
S1_table_data_long.loc[S1_table_data_long['var1_levels'] == 5, 'var1_levels'] = 'Rosa Pariser Charme'
S1_table_data_long.loc[S1_table_data_long['var1_uri'] == 5, 'var1_uri'] = ''
S1_table_data_long.loc[S1_table_data_long['var2_levels'] == 5, 'var2_levels'] = 'petals'
S1_table_data_long.loc[S1_table_data_long['var2_uri'] == 5, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

S1_table_data_long.loc[S1_table_data_long['treatment'] == 6, 'treatment'] = 'Rosa chinensis \'Old Blush\' petals'
S1_table_data_long.loc[S1_table_data_long['var1_levels'] == 6, 'var1_levels'] = 'Rosa chinensis \'Old Blush\''
S1_table_data_long.loc[S1_table_data_long['var1_uri'] == 6, 'var1_uri'] = 'http://purl.obolibrary.org/obo/NCBITaxon_74649'
S1_table_data_long.loc[S1_table_data_long['var2_levels'] == 6, 'var2_levels'] = 'petals'
S1_table_data_long.loc[S1_table_data_long['var2_uri'] == 6, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

S1_table_data_long.loc[S1_table_data_long['treatment'] == 7, 'treatment'] = 'Rosa Anna petals'
S1_table_data_long.loc[S1_table_data_long['var1_levels'] == 7, 'var1_levels'] = 'Rosa Anna'
S1_table_data_long.loc[S1_table_data_long['var1_uri'] == 7, 'var1_uri'] = ''
S1_table_data_long.loc[S1_table_data_long['var2_levels'] == 7, 'var2_levels'] = 'petals'
S1_table_data_long.loc[S1_table_data_long['var2_uri'] == 7, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

S1_table_data_long.loc[S1_table_data_long['treatment'] == 8, 'treatment'] = 'Rosa Mutabilis petals'
S1_table_data_long.loc[S1_table_data_long['var1_levels'] == 8, 'var1_levels'] = 'Rosa Mutabilis'
S1_table_data_long.loc[S1_table_data_long['var1_uri'] == 8, 'var1_uri'] = ''
S1_table_data_long.loc[S1_table_data_long['var2_levels'] == 8, 'var2_levels'] = 'petals'
S1_table_data_long.loc[S1_table_data_long['var2_uri'] == 8, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

S1_table_data_long.loc[S1_table_data_long['treatment'] == 9, 'treatment'] = 'Rosa Black Baccara petals'
S1_table_data_long.loc[S1_table_data_long['var1_levels'] == 9, 'var1_levels'] = 'Rosa Black Baccara'
S1_table_data_long.loc[S1_table_data_long['var1_uri'] == 9, 'var1_uri'] = ''
S1_table_data_long.loc[S1_table_data_long['var2_levels'] == 9, 'var2_levels'] = 'petals'
S1_table_data_long.loc[S1_table_data_long['var2_uri'] == 9, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

S1_table_data_long.loc[S1_table_data_long['treatment'] == 0, 'treatment'] = 'Rosa Baccara petals'
S1_table_data_long.loc[S1_table_data_long['var1_levels'] == 0, 'var1_levels'] = 'Rosa Baccara'
S1_table_data_long.loc[S1_table_data_long['var1_uri'] == 0, 'var1_uri'] = ''
S1_table_data_long.loc[S1_table_data_long['var2_levels'] == 0, 'var2_levels'] = 'petals'
S1_table_data_long.loc[S1_table_data_long['var2_uri'] == 0, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'


# print(S1_table_data)

# Reorganizing Columns order in the DataFrame/File to match the Frictionless Tabular Data Package Layout
# This is done very easily in Pandas by passing desired column order as an array:
S1_table_data_long = S1_table_data_long[['chemical_name', 'inchi', 'chebi_identifier', 'var1_levels', 'var1_uri',
                                         'var2_levels', 'var2_uri', 'treatment', 'sample_size', 'sample_mean',
                                         'unit', 'sem']]

os.chdir('../processed/denovo')

S1_table_data_long.to_csv("rose-aroma-science2015-Table_S1_long.csv",
                          sep=',',
                          encoding='utf-8',
                          quoting=1,
                          doublequote=True,
                          index=False)

validate_datapkg('rose-aroma-science2015-Table_S1_long.csv',
                 '../../../rose-metabo-JSON-DP-validated/rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-datapackage.json')
