import os
import libchebipy
import re
import pandas as pd
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
        # pack.valid
        # pack.errors
        for e_as_error in pack.errors:
            print(e_as_error)
        # print(pack.profile.name)

        report = validate(tab_data_package_file)
        if report:
            # print(report['valid'])
            print("\n" + tab_data_package_file + ": Nice one! A valid \'2 Factor Mean "
                                                 "and Standard Error Tabular Data Package\'\n")
        else:
            print("Sorry :( Vadidation failed, please check: ", tab_data_package_file, "\n")
            print(report)
    except IOError as er:
        print(er)


try:
    cwd = os.getcwd()
    print("current working directory:", cwd)
except IOError as e:
    print(e)

# Reading the native Excel file into a pandas dataframe
try:
    os.chdir('./data/raw')
    print("reading from directory: ", os.getcwd())
except IOError as e:
    print(e)

try:
    df = pd.read_excel('Supplementary Data 3.xlsx', sheet_name='Feuil1')
except IOError as e:
    print(e)

# Moving to the 'processed' directory, where we'll write the results on the raw data transformations
try:
    if not os.path.exists('../processed/denovo'):
        os.makedirs('../processed/denovo')
        os.chdir('../processed/denovo')
        print("writing to directory: ", os.getcwd())
except IOError as e:
    print(e)

# try:
#     cwd = os.getcwd()
#     print("working directory: ",cwd)
# except IOError as e:
#     print(e)

# Following a manual inspection of the Excel Source, getting the start row of the data
# We use Pandas take() function to extract first a row of headers (hence -axis set to 0)
header_treatment = df.take([13], axis=0)

# We then extract all the columns of interest (same take() function, with -axis set to 1)
data_full = df.take([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], axis=1)
# We now trim by removing the first 15 rows which contain no information
data_slice = data_full.take([16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
                             39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
                             62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76], axis=0)

# We now rename the DataFrame automatically generated field header to something more meaningful
data_slice.rename(columns={"Unnamed: 3": "chemical_name",
                           "Unnamed: 4": "sample_mean_1",
                           "Unnamed: 5": "sem_1",
                           "Unnamed: 6": "sample_mean_2",
                           "Unnamed: 7": "sem_2",
                           "Unnamed: 8": "sample_mean_3",
                           "Unnamed: 9": "sem_3",
                           "Unnamed: 10": "sample_mean_4",
                           "Unnamed: 11": "sem_4",
                           "Unnamed: 12": "sample_mean_5",
                           "Unnamed: 13": "sem_5",
                           "Unnamed: 14": "sample_mean_6",
                           "Unnamed: 15": "sem_6",
                           "Unnamed: 16": "sample_mean_7",
                           "Unnamed: 17": "sem_7",
                           "Unnamed: 18": "sample_mean_8",
                           "Unnamed: 19": "sem_8"}, inplace=True)

# inserting 2 new fields as placeholders for chemical information descriptors
data_slice.insert(loc=1, column='inchi', value='')
data_slice.insert(loc=2, column='chebi_identifier', value='')

# we reinitialize the dataframe index so row numbering start at 0, not 16
data_slice = data_slice.reset_index(drop=True)

# Using LibChebi to retrieve CHEBI identifiers and InChi from a chemical name
# Note: in this call, we retrieve only values for which an exact match on the chemical name is found in Chebi
# libchebi API does not allow easy searching on synonyms, thus we are failing to retrieve all relevant information.
# This is merely to showcase how to use libchebi

for i in range(0, 60):
    hit = libchebipy.search(data_slice.loc[i, 'chemical_name'], True)
    if len(hit) > 0:
        # print("slice -  HIT: ", data_slice.loc[i, 'chemical_name'], ":", hit[0].get_inchi(), "|", hit[0].get_id())
        data_slice.loc[i, 'inchi'] = hit[0].get_inchi()
        data_slice.loc[i, 'chebi_identifier'] = hit[0].get_id()
    else:
        # print("slice - nothing found: ", data_slice.loc[i, 'chemical_name'])
        data_slice.loc[i, 'inchi'] = ''
        data_slice.loc[i, 'chebi_identifier'] = ''

#  Here, we drop the first row
# data_slice.drop([0], inplace=True)

# We may wish to print intermediate results:
# data_slice.to_csv("slice.txt", sep='\t', encoding='utf-8', index=False)

# The following steps are needed to perform the table transformation from a 'wide' layout to a 'long table' one
# Prep stubnames - pick out all the feature_model variables and remove the model suffices
# 'long table' layout is that relied on by Frictionless Tabular Data Packages
# and consumed by R ggplot2 library and Python plotnine library

# Step1: obtain all the different 'dimension' measured for a given condition
# (i.e. repeating fields with an increment suffix)
feature_models = [col for col in data_slice.columns if re.match("(sample_mean|sem)_[0-9]", col) is not None]
features = list(set([re.sub("_[0-9]", "", feature_model) for feature_model in feature_models]))
# print("features", features)

# Step2: invoke Pandas pd.wide_to_long() function to carry out the table transformation
# See Pandas documentation for more information:
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.wide_to_long.html
# and the excellent blog: https://medium.com/@wangyuw/data-reshaping-with-pandas-explained-80b2f51f88d2
long_df = pd.wide_to_long(data_slice, i=['chemical_name'], j='treatment', stubnames=features, sep="_")

# Apparently a feature in Pandas DataFrame causes an mismatch in the field position
# we solve this by writing the DataFrame to file and reading it back in again, not ideal!
# write to a temporary file
long_df.to_csv("long.txt", sep='\t', encoding='utf-8')
# reading from that file to solve the issue
long_df_from_file = pd.read_csv("long.txt", sep="\t")

# Insert a new field 'unit' in the DataFrame at position 3 and setting value to empty.
long_df_from_file.insert(loc=3, column='unit', value='')

# Adding new fields for each of the independent variable and associated URI, copying from 'treatment field'
long_df_from_file['var1_levels'] = long_df_from_file['treatment']
long_df_from_file['var1_uri'] = long_df_from_file['treatment']
long_df_from_file['var2_levels'] = long_df_from_file['treatment']
long_df_from_file['var2_uri'] = long_df_from_file['treatment']

# adding a new field for 'sample size' and setting the value to n=3
long_df_from_file['sample_size'] = 3

# Marking up with ontology terms and their resolvable URI for all factor values:
# This requires doing a manual mapping, better ways could be devised.
long_df_from_file.loc[long_df_from_file['treatment'] == 1, 'treatment'] = 'R. chinensis \'Old Blush\' sepals'
long_df_from_file.loc[long_df_from_file['var1_levels'] == 1, 'var1_levels'] = 'R. chinensis \'Old Blush\''
long_df_from_file.loc[long_df_from_file['var1_uri'] == 1, 'var1_uri'] = 'http://purl.obolibrary.org/obo/NCBITaxon_74649'
long_df_from_file.loc[long_df_from_file['var2_levels'] == 1, 'var2_levels'] = 'sepals'
long_df_from_file.loc[long_df_from_file['var2_uri'] == 1, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009031'

long_df_from_file.loc[long_df_from_file['treatment'] == 2, 'treatment'] = 'R. chinensis \'Old Blush\' stamens'
long_df_from_file.loc[long_df_from_file['var1_levels'] == 2, 'var1_levels'] = 'R. chinensis \'Old Blush\''
long_df_from_file.loc[long_df_from_file['var1_uri'] == 2, 'var1_uri'] = 'http://purl.obolibrary.org/obo/NCBITaxon_74649'
long_df_from_file.loc[long_df_from_file['var2_levels'] == 2, 'var2_levels'] = 'stamens'
long_df_from_file.loc[long_df_from_file['var2_uri'] == 2, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009029'

long_df_from_file.loc[long_df_from_file['treatment'] == 3, 'treatment'] = 'R. chinensis \'Old Blush\' petals'
long_df_from_file.loc[long_df_from_file['var1_levels'] == 3, 'var1_levels'] = 'R. chinensis \'Old Blush\''
long_df_from_file.loc[long_df_from_file['var1_uri'] == 3, 'var1_uri'] = 'http://purl.obolibrary.org/obo/NCBITaxon_74649'
long_df_from_file.loc[long_df_from_file['var2_levels'] == 3, 'var2_levels'] = 'petals'
long_df_from_file.loc[long_df_from_file['var2_uri'] == 3, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

long_df_from_file.loc[long_df_from_file['treatment'] == 4, 'treatment'] = 'R. gigantea petals'
long_df_from_file.loc[long_df_from_file['var1_levels'] == 4, 'var1_levels'] = 'R. gigantea'
long_df_from_file.loc[long_df_from_file['var1_uri'] == 4, 'var1_uri'] = 'http://purl.obolibrary.org/obo/NCBITaxon_74650'
long_df_from_file.loc[long_df_from_file['var2_levels'] == 4, 'var2_levels'] = 'petals'
long_df_from_file.loc[long_df_from_file['var2_uri'] == 4, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

long_df_from_file.loc[long_df_from_file['treatment'] == 5, 'treatment'] = 'R. Damascena petals'
long_df_from_file.loc[long_df_from_file['var1_levels'] == 5, 'var1_levels'] = 'R. Damascena'
long_df_from_file.loc[long_df_from_file['var1_uri'] == 5, 'var1_uri'] = 'http://purl.obolibrary.org/obo/NCBITaxon_3765'
long_df_from_file.loc[long_df_from_file['var2_levels'] == 5, 'var2_levels'] = 'petals'
long_df_from_file.loc[long_df_from_file['var2_uri'] == 5, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

long_df_from_file.loc[long_df_from_file['treatment'] == 6, 'treatment'] = 'R. Gallica petals'
long_df_from_file.loc[long_df_from_file['var1_levels'] == 6, 'var1_levels'] = 'R. Gallica'
long_df_from_file.loc[long_df_from_file['var1_uri'] == 6, 'var1_uri'] = 'http://purl.obolibrary.org/obo/NCBITaxon_74632'
long_df_from_file.loc[long_df_from_file['var2_levels'] == 6, 'var2_levels'] = 'petals'
long_df_from_file.loc[long_df_from_file['var2_uri'] == 6, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

long_df_from_file.loc[long_df_from_file['treatment'] == 7, 'treatment'] = 'R. moschata petals'
long_df_from_file.loc[long_df_from_file['var1_levels'] == 7, 'var1_levels'] = 'R. moschata'
long_df_from_file.loc[long_df_from_file['var1_uri'] == 7, 'var1_uri'] = 'http://purl.obolibrary.org/obo/NCBITaxon_74646'
long_df_from_file.loc[long_df_from_file['var2_levels'] == 7, 'var2_levels'] = 'petals'
long_df_from_file.loc[long_df_from_file['var2_uri'] == 7, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

long_df_from_file.loc[long_df_from_file['treatment'] == 8, 'treatment'] = 'R. wichurana petals'
long_df_from_file.loc[long_df_from_file['var1_levels'] == 8, 'var1_levels'] = 'R. wichurana'
long_df_from_file.loc[long_df_from_file['var1_uri'] == 8,
                      'var1_uri'] = 'http://purl.obolibrary.org/obo/NCBITaxon_2094184'
long_df_from_file.loc[long_df_from_file['var2_levels'] == 8, 'var2_levels'] = 'petals'
long_df_from_file.loc[long_df_from_file['var2_uri'] == 8, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

# dealing with missing values: setting empty values to zero for sample_mean and sem to enable calculation:
# to do this, we rely on Pandas fillna function
long_df_from_file['sample_mean'] = long_df_from_file['sample_mean'].fillna("0")
long_df_from_file['sem'] = long_df_from_file['sem'].fillna("0")


# Reorganizing Columns order in the DataFrame/File to match the Frictionless Tabular Data Package Layout
# This is done very easily in Pandas by passing desired column order as an array:
long_df_from_file = long_df_from_file[['chemical_name', 'inchi', 'chebi_identifier', 'var1_levels', 'var1_uri',
                                       'var2_levels', 'var2_uri', 'treatment', 'sample_size', 'sample_mean',
                                       'unit', 'sem']]

# Writing to file as a UTF-8 encoded tab delimited file
try:
    long_df_from_file.to_csv("rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.csv",
                         quoting=1,
                         doublequote=True, sep=',',
                         encoding='utf-8', index=False)
except IOError as e:
    print(e)

try:
    os.remove("long.txt")
except IOError as e:
    print(e)


# validating the output against JSON data package specifications
# Getting the JSON Tabular DataPackage Definition from the store:

validate_datapkg('rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.csv',
'../../../rose-metabo-JSON-DP-validated/rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-datapackage.json')


# TODO: create a function so users can choose whether all features are generated or only a subset
# TODO: below the code for generate an output with only sample_mean or only sem
# TODO: the function ought to take the following arguments:
# TODO: an array of header positions --data_colunms
# TODO: an array of new column names --data_column_handles
# TODO: an array of of data rows --data_rows
# TODO: a regular expression used to match the features to extract --repattern
# TODO: an output file name --output

#
# # DEALING WITH AVERAGE/MEAN" ----------------------------------
# data_mean = df.take([3, 4, 6, 8, 10, 12, 14, 16, 18], axis=1)
# slice_mean = data_mean.take([16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
#                              36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
#                              56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76],
#                             axis=0)
#
# slice_mean.rename(columns={"Unnamed: 3": "chemical_name",
# "Unnamed: 4": "sample_mean_1",
# "Unnamed: 6": "sample_mean_2",
# "Unnamed: 8": "sample_mean_3",
# "Unnamed: 10": "sample_mean_4",
# "Unnamed: 12": "sample_mean_5",
# "Unnamed: 14": "sample_mean_6",
# "Unnamed: 16": "sample_mean_7",
# "Unnamed: 18": "sample_mean_8"}, inplace=True)
#
# slice_mean = slice_mean.reset_index(drop=True)
# slice_mean.drop([0], inplace=True)
# print(slice_mean)
# slice_mean.to_csv("slice_mean.txt", sep='\t', encoding='utf-8', index=False)
#
# # Prep stubnames - pick out all the feature_model variables and remove the model suffices
# feature_models = [col for col in slice_mean.columns if re.match("sample_mean_[0-9]", col) is not None]
# # print("models",feature_models)
# features = list(set([ re.sub("_[0-9]", "", feature_model) for feature_model in feature_models]))
# # print("features",features)
#
# # call pd.wide_to_long()
# mean_long_df = pd.wide_to_long(slice_mean, i=['chemical_name'], j='treatment', stubnames=features, sep="_")
#
# print(mean_long_df)
# mean_long_df.to_csv("mean_long.txt", sep='\t', encoding='utf-8')
# # ----------------------------------


# #D EALING WITH SEM" ----------------------------------
# data_sem = df.take([3, 5, 7, 9, 11, 13, 15, 17, 19], axis=1)
# slice_sem = data_sem.take([16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
#                            39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
#                            62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76], axis=0)
# slice_sem.rename(columns={"Unnamed: 3": "chemical_name",
#                           "Unnamed: 5": "sem_1",
#                           "Unnamed: 7": "sem_2",
#                           "Unnamed: 9": "sem_3",
#                           "Unnamed: 11": "sem_4",
#                           "Unnamed: 13": "sem_5",
#                           "Unnamed: 15": "sem_6",
#                           "Unnamed: 17": "sem_7",
#                           "Unnamed: 19": "sem_8"}, inplace=True)
#
# slice_sem = slice_sem.reset_index(drop=True)
# slice_sem.drop([0], inplace=True)
# slice_sem.to_csv("slice_sem.txt", sep='\t', encoding='utf-8', index=False)
#
# # Prep stubnames - pick out all the feature_model variables and remove the model suffices
# feature_models = [col for col in slice_sem.columns if re.match("sem_[0-9]", col) is not None]
# # print("models",feature_models)
# features = list(set([re.sub("_[0-9]", "", feature_model) for feature_model in feature_models]))
# # print("features",features)
#
# # call pd.wide_to_long()
# sem_long_df = pd.wide_to_long(slice_sem, i=['chemical_name'], j='treatment', stubnames=features, sep="_")
#
# # print(sem_long_df)
# sem_long_df.to_csv("sem_long.txt", sep='\t', encoding='utf-8')
#
# frames = [mean_long_df, sem_long_df]
# molten = pd.concat(frames)
# molten.to_csv("molten.txt", sep='\t', encoding='utf-8')
