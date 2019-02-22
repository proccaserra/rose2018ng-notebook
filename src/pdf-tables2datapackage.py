import camelot
import os
import pandas as pd
import re

cwd = os.getcwd()
os.chdir('../data/raw')
cwd = os.getcwd()

tables = camelot.read_pdf('MagnardSM.pdf', pages='19,20,21', flavor='stream', split_text=True)

tables.export('science.csv', f='csv', compress=False)
array_of_df = []
for i in range(len(tables)):
    array_of_df.append(tables[i].df)

S1_table_data = pd.concat(array_of_df)
# resetting the index
S1_table_data = S1_table_data.reset_index(drop=True)

# removing the first 4 lines, which correspond to the a fragment of figure caption
S1_table_data = S1_table_data.drop([0, 1, 2, 3], axis=0)
# resetting the index again
S1_table_data = S1_table_data.reset_index(drop=True)

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

# fixing the truncated chemical name
S1_table_data.loc[S1_table_data['chemical_name'] == "3,4-dihydro-β-", 'chemical_name'] = '3,4-dihydro-β-1 ionone'

# removing an extraline caused by an overhang by long chemical name at row 52
S1_table_data = S1_table_data.drop([52], axis=0)
# resetting the index once more
S1_table_data = S1_table_data.reset_index(drop=True)

S1_table_data = S1_table_data.drop([0], axis=0)
# resetting the index again
S1_table_data = S1_table_data.reset_index(drop=True)

# inserting the chemical annotation fields
S1_table_data.insert(loc=1, column='inchi', value='')
S1_table_data.insert(loc=2, column='chebi_identifier', value='')

# The following steps are needed to perform the table transformation from a 'wide' layout to a 'long table' one
# Prep stubnames - pick out all the feature_model variables and remove the model suffices
# 'long table' layout is that relied on by Frictionless Tabular Data Packages
# and consumed by R ggplot2 library and Python plotnine library

# Step1: obtain all the different 'dimension' measured for a given condition
# (i.e. repeating fields with an increment suffix)
feature_models = [col for col in S1_table_data.columns if re.match("(sample_mean)_[0-9]", col) is not None]
features = list(set([re.sub("_[0-9]", "", feature_model) for feature_model in feature_models]))
print("features", features)

#  Here, we drop the first row
S1_table_data.drop([53, 54], inplace=True)
# resetting the index again
S1_table_data = S1_table_data.reset_index(drop=True)

#  Here, we drop the first row
S1_table_data.drop([1], inplace=True)
# resetting the index again
S1_table_data = S1_table_data.reset_index(drop=True)

# Step2: invoke Pandas pd.wide_to_long() function to carry out the table transformation
# See Pandas documentation for more information:
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.wide_to_long.html
# and the excellent blog: https://medium.com/@wangyuw/data-reshaping-with-pandas-explained-80b2f51f88d2
long_df = pd.wide_to_long(S1_table_data, i=['chemical_name'], j='treatment', stubnames=features, sep="_")
long_df.to_csv("long.txt", sep='\t', encoding='utf-8')
# reading from that file to solve the issue
S1_table_data_long = pd.read_csv("long.txt", sep="\t")


print(S1_table_data)

os.chdir('../processed')
S1_table_data.to_csv('Table_S1.csv', encoding='utf-8', sep=",", index=False)
S1_table_data_long.to_csv("S1_long.txt", sep='\t', encoding='utf-8', index=False)



