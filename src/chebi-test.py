import camelot
import os
import pandas as pd
import re
import libchebipy
from datapackage import Package
from goodtables import validate

S1_table_data = {'chemical_name':  ["2-Hexanol", "(E)-2-hexenal", "aspirin", "ethanol"]}
df = pd.DataFrame(data=S1_table_data)


def get_chebi_ids(dataframe, number_of_items):
    # a method to obtain InChi and Chebi ID from a chemical name using libchebi
    # takes 2 arguments: a data frame and a number of chemicals

    for idx in range(0, number_of_items):
        hit = libchebipy.search(dataframe.loc[idx, 'chemical_name'], True)
        print(hit)
        if len(hit) > 0:
            print("slice -  HIT: ",dataframe.loc[idx, 'chemical_name'], ":", hit[0].get_inchi(), "|", hit[0].get_id())
            dataframe.loc[idx, 'inchi'] = hit[0].get_inchi()
            dataframe.loc[idx, 'chebi_identifier'] = hit[0].get_id()
        else:
            print("slice - nothing found: ", dataframe.loc[idx, 'chemical_name'])
            print("trying out search of synonyms:")
            new_search = libchebipy.search(dataframe.loc[idx, 'chemical_name'], False)
            print("expanded search:", new_search)

            for element in new_search:
                print("element:", element.get_id(), element.get_name())
                print(element.get_names())
                # for item in element:
                #
                #     print(element.get_names()[item].keys())
                # for key in element.get_names().keys():
                #     print(element.get_names()[key])
                #
                # else:
                #     print("no match")

    return dataframe



S1_table_data = get_chebi_ids(df, 4)