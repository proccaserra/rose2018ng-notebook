# author: philippe rocca-serra (philippe.rocca-serra@oerc.ox.ac.uk)
# ontology: http://www.stato-ontology.org

import os
import libchebipy
import re
import pandas as pd

cwd = os.getcwd()
print(cwd)
os.chdir('../data/raw')

cwd = os.getcwd()
print(cwd)

df = pd.read_excel('Supplementary Data 3.xlsx', sheet_name='Feuil1')
chemical_names = []

# offset = 17
# for i in range(0, 60):
#     index = offset+i
#     hit = libchebipy.search(df.iloc[index][3], True)
#     if len(hit) > 0:
#         # print(hit)
#         print("HIT: ", df.iloc[index][3], ":", hit[0].get_inchi(), "|", hit[0].get_id())
#     else:
#         print("nothing found: ", df.iloc[index][3])

    # libchebipy.Name(df.iloc[index][3])
    # libchebipy.Name()
# chemical_names.append(df.iloc[offset+i][3])

header_treatment = df.take([13], axis=0)
# print(header_treatment)

treatment_slice = df.take([3,9], axis=1)
# print("hello!", treatment_slice)
# print("treatment", header_treatment["Unnamed: 4"])

data_full = df.take([3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19], axis=1)
slice = data_full.take([16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76],axis=0)


slice.rename(columns={"Unnamed: 3": "chemical_name",
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
"Unnamed: 19": "sem_8" }, inplace=True)

# long_df_from_file.insert(loc=1,column='inchi',value='')
# long_df_from_file.insert(loc=2,column='chebi_identifier',value='')
slice.insert(loc=1,column='inchi',value='')
slice.insert(loc=2,column='chebi_identifier',value='')

slice = slice.reset_index(drop=True)
i=0
for i in range(0, 60):
    index = i
    hit = libchebipy.search(slice.iloc[index][0], True)
    if len(hit) > 0:
        # print(hit)
        print("slice -  HIT: ", slice.iloc[index][0], ":", hit[0].get_inchi(), "|", hit[0].get_id())
        slice.at[slice.iloc[index][0], 'inchi'] = hit[0].get_inchi()
        slice.at[slice.iloc[index][0], 'chebi_identifier'] = hit[0].get_id()

    else:
        print("slice - nothing found: ", slice.iloc[index][0])
        slice.at[slice.iloc[index][0], 'inchi'] = ''
        slice.at[slice.iloc[index][0], 'chebi_identifier'] = ''


slice.drop([0], inplace=True)


print(slice)




slice.to_csv("slice.txt", sep='\t', encoding='utf-8', index=False)


# Prep stubnames - pick out all the feature_model variables and remove the model suffices
feature_models = [col for col in slice.columns if re.match("(sample_mean|sem)_[0-9]", col) is not None]
print("models",feature_models)
features = list(set([ re.sub("_[0-9]","",feature_model) for feature_model in feature_models]))
print("features",features)


# call pd.wide_to_long()
long_df = pd.wide_to_long(slice, i=['chemical_name'], j='treatment', stubnames=features, sep="_")
print("LONG_DF HEADERS: ", list(long_df))

print(long_df)
long_df.to_csv("long.txt", sep='\t', encoding='utf-8')

long_df_from_file = pd.read_csv("long.txt", sep="\t")

long_df_from_file.insert(loc=3,column='unit',value='')
# long_df_from_file['inchi'] = ''
# long_df_from_file['chebi_identifier'] = ''
long_df_from_file['var1_levels'] = long_df_from_file['treatment']
long_df_from_file['var1_uri'] = long_df_from_file['treatment']
long_df_from_file['var2_levels'] = long_df_from_file['treatment']
long_df_from_file['var2_uri'] = long_df_from_file['treatment']
long_df_from_file['sample_size'] = 3

print("HEADERS FROM FILE",list(long_df_from_file))
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
long_df_from_file.loc[long_df_from_file['var1_uri'] == 8, 'var1_uri'] = 'http://purl.obolibrary.org/obo/NCBITaxon_2094184'
long_df_from_file.loc[long_df_from_file['var2_levels'] == 8, 'var2_levels'] = 'petals'
long_df_from_file.loc[long_df_from_file['var2_uri'] == 8, 'var2_uri'] = 'http://purl.obolibrary.org/obo/PO_0009032'

# long_df_cols = list(long_df_from_file)

long_df_from_file = long_df_from_file[['chemical_name','inchi','chebi_identifier','var1_levels','var1_uri','var2_levels','var2_uri','treatment','sample_size','sample_mean','unit','sem']]

long_df_from_file.to_csv("long_df_from_file.txt", sep='\t', encoding='utf-8',index=False)





#DEALING WITH AVERAGE/MEAN"
data_mean = df.take([3,4,6,8,10,12,14,16,18], axis=1)
slice_mean = data_mean.take([16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76],axis=0)

slice_mean.rename(columns={"Unnamed: 3": "chemical_name",
"Unnamed: 4": "sample_mean_1",
"Unnamed: 6": "sample_mean_2",
"Unnamed: 8": "sample_mean_3",
"Unnamed: 10": "sample_mean_4",
"Unnamed: 12": "sample_mean_5",
"Unnamed: 14": "sample_mean_6",
"Unnamed: 16": "sample_mean_7",
"Unnamed: 18": "sample_mean_8"}, inplace=True)

slice_mean = slice_mean.reset_index(drop=True)
slice_mean.drop([0], inplace=True)
print(slice_mean)
slice_mean.to_csv("slice_mean.txt", sep='\t', encoding='utf-8', index=False)

# Prep stubnames - pick out all the feature_model variables and remove the model suffices
feature_models = [col for col in slice_mean.columns if re.match("sample_mean_[0-9]",col) is not None]
#print("models",feature_models)
features = list(set([ re.sub("_[0-9]","",feature_model) for feature_model in feature_models]))
#print("features",features)
	# ['H1','H2','H3']

# call pd.wide_to_long()
mean_long_df = pd.wide_to_long(slice_mean, i=['chemical_name'], j='treatment', stubnames=features, sep="_")

print(mean_long_df)
mean_long_df.to_csv("mean_long.txt", sep='\t', encoding='utf-8')



#DEALING WITH SEM"

data_sem = df.take([3,5,7,9,11,13,15,17,19], axis=1)
slice_sem = data_sem.take([16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76],axis=0)


slice_sem.rename(columns={"Unnamed: 3": "chemical_name",
"Unnamed: 5": "sem_1",
"Unnamed: 7": "sem_2",
"Unnamed: 9": "sem_3",
"Unnamed: 11": "sem_4",
"Unnamed: 13": "sem_5",
"Unnamed: 15": "sem_6",
"Unnamed: 17": "sem_7",
"Unnamed: 19": "sem_8"}, inplace=True)

slice_sem = slice_sem.reset_index(drop=True)
slice_sem.drop([0], inplace=True)
slice_sem.to_csv("slice_sem.txt", sep='\t', encoding='utf-8', index=False)
# Prep stubnames - pick out all the feature_model variables and remove the model suffices
feature_models = [col for col in slice_sem.columns if re.match("sem_[0-9]",col) is not None]
#print("models",feature_models)
features = list(set([ re.sub("_[0-9]","",feature_model) for feature_model in feature_models]))
#print("features",features)
	# ['H1','H2','H3']

# call pd.wide_to_long()
sem_long_df = pd.wide_to_long(slice_sem, i=['chemical_name'], j='treatment', stubnames=features, sep="_")

#print(sem_long_df)
sem_long_df.to_csv("sem_long.txt", sep='\t', encoding='utf-8')


frames = [mean_long_df,sem_long_df]
molten = pd.concat(frames)
molten.to_csv("molten.txt", sep='\t', encoding='utf-8')




# print("iloc",header_treatment.iloc[0]['Unnamed: 4'])
# offset=-1
# for i in [4,6,8,10,12,14,16,18]:
#
#     print("there:",header_treatment.iloc[0]["Unnamed: "+str(i)])
#     column_header = ("Treatment"+str(i))
#     print(column_header)
#     slice.insert(loc=i+offset,column=column_header, value=header_treatment.iloc[0]["Unnamed: "+str(i)])
#     offset = offset+1


# print(chemical_names)