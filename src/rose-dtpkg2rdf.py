import os
import csv
import uuid
import requests


__author__ = 'proccaserra (Philippe Rocca-Serra)'

# author: philippe rocca-serra (philippe.rocca-serra@oerc.ox.ac.uk)
# ontology: http://www.stato-ontology.org


def create_var_rep(fv_dict, factor_name):
    ffv = []
    counter = 0
    f_id = str(uuid.uuid4())
    f_rdf_fragment = "\n<https://example.com/" + f_id + "> a obi:0000750.   # 'study design independent variable'  same_as (OBI_0000750)\n"
    f_rdf_fragment = f_rdf_fragment + "<https://example.com/" + f_id + "> a stato:0000087;  # 'categorical variable' (STATO_0000087)\n"
    f_rdf_fragment = f_rdf_fragment + "  rdfs:label  \"" + factor_name + "\"^^xsd:string;\n"

    fvs = []
    for key in fv_dict.keys():
        fv_id = str(uuid.uuid4())
        if counter < len(fv_dict.keys())-1:
            f_rdf_fragment = f_rdf_fragment + "  has_part: <https://example.com/" + fv_id + ">  ;\n"
            counter = counter + 1
        else:
            f_rdf_fragment = f_rdf_fragment + "  has_part: <https://example.com/" + fv_id + ">  .\n"

        fv_rdf_fragment = "<https://example.com/" + fv_id + "> a stato:0000265; # a factor level\n"
        fv_rdf_fragment = fv_rdf_fragment + "  rdfs:label \"" + key + "\"^^xsd:string ."
        fvs.append(fv_rdf_fragment)

    return f_rdf_fragment, fvs


def process(a_csv_reader):
    line_count = 0
    treatments = {}
    idv1 = {}
    idv2 = {}
    chemicals = {}
    chem_frags = []

    for row in a_csv_reader:

        if line_count == 0:
            # print("header row: ", row)
            line_count += 1
        else:

            mean_id = str(uuid.uuid4())
            sem_id = str(uuid.uuid4())
            
            if row[2] not in chemicals.keys() and row[2] != "":
                chemicals[row[2]] = 1
                chem_id = str(uuid.uuid4())

                chem_rdf_fragment = "<https://example.com/" + chem_id + "> a " + row[2].rstrip() + " ; # a chemical\n"
                chem_rdf_fragment = chem_rdf_fragment + "  rdfs:label \"" + row[0].rstrip() + "\"^^xsd:string ;\n"
                chem_rdf_fragment = chem_rdf_fragment + "  is_denoted_by: \"" + row[1] + "\"^^xsd:string .\n"

                chem_frags.append(chem_rdf_fragment)
            else:
                chemicals[row[2]] = 1
                chem_id = str(uuid.uuid4())

                chem_rdf_fragment = "<https://example.com/" + chem_id + "> a \"" + row[0].rstrip() + "\"; #a chemical\n"
                chem_rdf_fragment = chem_rdf_fragment + "  rdfs:label \"" + row[0].rstrip() + "\"^^xsd:string ;\n"
                chem_rdf_fragment = chem_rdf_fragment + "  is_denoted_by: \"" + row[1] + "\"^^xsd:string .\n"

                chem_frags.append(chem_rdf_fragment)

            # elif row[2] not in chemicals.keys() and row[2] == "":
            #     chemicals[row[2]] = 1
            #     chem_id = str(uuid.uuid4())
            #
            #     chem_rdf_fragment = "<" + chem_id + "> a " + row[2] + " ; # a chemical\n"
            #     chem_rdf_fragment = chem_rdf_fragment + "  rdfs:label \"" + row[0] + "\"^^xsd:string ;\n"
            #     chem_rdf_fragment = chem_rdf_fragment + "  is_denoted_by: \"" + row[1] + "\"^^xsd:string .\n"
            #
            #     chem_frags.append(chem_rdf_fragment)
                
            if row[3] not in idv1.keys():
                idv1[row[3]] = 1

            if row[5] not in idv2.keys():
                idv2[row[5]] = 1

            if row[7] not in treatments.keys():
                saveAsttl.write("#||-------A GROUP & its associated data --------------------------------------||\n\n")
                # let's create a new population for this new treatment group
                pop_id = str(uuid.uuid4())
                treatments[row[7]] = pop_id
                pop_rdf_fragment = "<https://example.com/" + pop_id + "> a stato:0000193 ; # a population\n"
                pop_rdf_fragment = pop_rdf_fragment + "  rdfs:label \"" + row[7] + "\"^^xsd:string ;\n"
                pop_rdf_fragment = pop_rdf_fragment + "  has_value: \"" + row[7] + "\"^^xsd:string ;\n"

                specimen_id = str(uuid.uuid4())
                material_rdf_fragment = "<https://example.com/" + specimen_id + "> a obi:0000671 ; # a biological specimen\n"
                material_rdf_fragment = material_rdf_fragment + "  rdfs:label \"" + row[5] + "\"^^xsd:string;\n"
                material_rdf_fragment = material_rdf_fragment + "  derives_from: " + row[6].replace('http://purl.obolibrary.org/obo/PO_','po:') + " ;\n"
                material_rdf_fragment = material_rdf_fragment + "  part_of: " + row[4].replace('http://purl.obolibrary.org/obo/NCBITaxon_','ncbitax:') + " .\n\n"

                for i in range(int(row[8])):
                    chem_conc_id = str(uuid.uuid4())
                    gc_ms_id = str(uuid.uuid4())
                    gc_ms_rdf_fragment = "<https://example.com/" + gc_ms_id + "> a obi:0000070 ; #'assay'\n"
                    gc_ms_rdf_fragment = gc_ms_rdf_fragment + "  has_part: msio:0000100 ; #'targeted metabolite profiling'\n"
                    gc_ms_rdf_fragment = gc_ms_rdf_fragment + "  has_part: chmo:0000497 ; #'GC mass spectrometry'\n"
                    gc_ms_rdf_fragment = gc_ms_rdf_fragment + "  has_specified_input: " + "<https://example.com/" + specimen_id + "> ;\n"
                    gc_ms_rdf_fragment = gc_ms_rdf_fragment + "  has_specified_output: " + "<https://example.com/" + chem_conc_id + "> .\n"

                    rdf_fragment = "<https://example.com/" + chem_conc_id + "> a obi:0000751 .	#'dependent variable'\n"
                    rdf_fragment = rdf_fragment + "<https://example.com/" + chem_conc_id + "> a stato:0000251 . #'continuous variable'\n"
                    rdf_fragment = rdf_fragment + "<https://example.com/" + chem_conc_id + "> a stato:0000072 ;	#'substance concentration'\n"
                    rdf_fragment = rdf_fragment + "  is_specified_output_of: " + "<https://example.com/" + gc_ms_id + "> ;\n"
                    if row[2] == "":
                        rdf_fragment = rdf_fragment + "  is_about: \"" + row[0].rstrip() + "\"^^xsd:string;\n"
                    else:
                        rdf_fragment = rdf_fragment + "  is_about: " + row[2].lower() + ";\n"

                    rdf_fragment = rdf_fragment + "  located_in: " + row[6].replace(
                        'http://purl.obolibrary.org/obo/PO_', 'po:') + ";\n"
                    rdf_fragment = rdf_fragment + "  derives_from: " + row[4].replace(
                        'http://purl.obolibrary.org/obo/NCBITaxon_', 'ncbitax:') + ";\n"
                    #rdf_fragment = rdf_fragment + "    measured_in \"" + row[7] + "\".\n"
                    rdf_fragment = rdf_fragment + "  measured_in: <https://example.com/" + pop_id + "> .\n"

                    saveAsttl.write(gc_ms_rdf_fragment + "\n")
                    saveAsttl.write(rdf_fragment + "\n")

                    if i < int(row[8])-1:
                        pop_rdf_fragment = pop_rdf_fragment + "  has_member: <https://example.com/" + gc_ms_id + "> ;\n"
                    else:
                        pop_rdf_fragment = pop_rdf_fragment + "  has_member: <https://example.com/" + gc_ms_id + "> .\n\n"

                pop_size_id = str(uuid.uuid4())
                pop_size_rdf_fragment = "<" + pop_size_id + "> a stato:0000088 ; # a population size\n"
                pop_size_rdf_fragment = pop_size_rdf_fragment + "  has_value: \"3\"^^xsd:integer ;\n"
                pop_size_rdf_fragment = pop_size_rdf_fragment + "  is_about: <https://example.com/" + pop_id + "> .\n\n"

                saveAsttl.write(material_rdf_fragment)
                saveAsttl.write(pop_rdf_fragment)
                saveAsttl.write(pop_size_rdf_fragment)

                if row[9] == "" and row[2] == "":

                    qt_rdf_fragment = "<https://example.com/" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  is_about: \"" + row[0] + "\"^^xsd:string;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + "0" + "\"^^xsd:decimal.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<https://example.com/" + sem_id + "> a stato:0000037;  #'standard error of the mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  denotes: <https://example.com/" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + "0" + "\"^^xsd:decimal.\n\n"

                elif row[9] == "" and row[2] != "":

                    qt_rdf_fragment = "<https://example.com/" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  is_about: " + row[2].lower() + " ;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + "0" + "\"^^xsd:decimal.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<https://example.com/" + sem_id + "> a stato:0000037;  #'standard error of the mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  denotes: <https://example.com/" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + "0" + "\"^^xsd:decimal.\n\n"

                elif row[9] != "" and row[2] == "":

                    qt_rdf_fragment = "<https://example.com/" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  is_about: \"" + row[0] + "\"^^xsd:string;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + row[9] + "\"^^xsd:decimal.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<https://example.com/" + sem_id + "> a stato:0000037; # 'standard error of the mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  denotes: <https://example.com/" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + row[11] + "\"^^xsd:decimal.\n"

                elif row[9] != "" and row[2] != "":

                    qt_rdf_fragment = "<https://example.com/" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  is_about: " + row[2].lower() + " ;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + row[9] + "\"^^xsd:decimal.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<https://example.com/" + sem_id + "> a stato:0000037; # 'standard error of the mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  denotes: <https://example.com/" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + row[11] + "\"^^xsd:decimal.\n"

                saveAsttl.write(qt_rdf_fragment + "\n")

            else:
                if row[9] == "" and row[2] == "":

                    qt_rdf_fragment = "<https://example.com/" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  is_about: \"" + row[0] + "\"^^xsd:string;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + "0" + "\"^^xsd:decimal.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<https://example.com/" + sem_id + "> a stato:0000037;  #'standard error of the mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  denotes: <https://example.com/" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + "0" + "\"^^xsd:decimal.\n\n"

                elif row[9] == "" and row[2] != "":
                    qt_rdf_fragment = "<https://example.com/" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  is_about: " + row[2].lower() + " ;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + "0" + "\"^^xsd:decimal.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<https://example.com/" + sem_id + "> a stato:0000037;  #'standard error of the mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  denotes: <https://example.com/" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + "0" + "\"^^xsd:decimal.\n\n"

                elif row[9] != "" and row[2] == "":

                    qt_rdf_fragment = "<https://example.com/" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  is_about: \"" + row[0] + "\"^^xsd:string;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + row[9] + "\"^^xsd:decimal.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<https://example.com/" + sem_id + "> a stato:0000037; # 'standard error of the mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  denotes: <https://example.com/" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + row[11] + "\"^^xsd:decimal.\n"

                else:

                    qt_rdf_fragment = "<https://example.com/" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  is_about: " + row[2].lower() + " ;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + row[9] + "\"^^xsd:decimal.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<https://example.com/" + sem_id + "> a stato:0000037; # 'standard error of the mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  denotes: <https://example.com/" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  computed_from: <https://example.com/" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  has_value: \"" + row[11] + "\"^^xsd:decimal.\n"

                saveAsttl.write(qt_rdf_fragment + "\n")

            # we assume technical replicates based on the information extracted from the manuscript
            # if int(row[8]) > 0:
            #         for i in range(int(row[8])):
            #
            #             gc_ms_id = str(uuid.uuid4())
            #             # if i < int(row[8]):
            #             #     pop_rdf_fragment = pop_rdf_fragment + " ro:has_member " + gc_ms_id + " ;\n"
            #             # else:
            #             #     pop_rdf_fragment = pop_rdf_fragment + " ro:has_member " + gc_ms_id + " .\n"
            #             # pop_rdf_fragment = pop_rdf_fragment + " ro:has_member <targeted_metprof_gc_ms2> ;\n"
            #             # pop_rdf_fragment = pop_rdf_fragment + " ro:has_member <targeted_metprof_gc_ms3> .\n"
            #
            #             gc_ms_rdf_fragment = "<" + gc_ms_id + "> a obi:0000070 ; #'assay'\n"
            #             gc_ms_rdf_fragment = gc_ms_rdf_fragment + " ro:has_part \"msio:0000100\" ; #'targeted metabolite profiling'\n"
            #             gc_ms_rdf_fragment = gc_ms_rdf_fragment + " ro:has_part \"chmo:0000497\" ; #'GC mass spectrometry'\n"
            #             gc_ms_rdf_fragment = gc_ms_rdf_fragment + " ro:has_specified_input " + "<" + specimen_id + "> ;\n"
            #             gc_ms_rdf_fragment = gc_ms_rdf_fragment + " ro:has_specified_output " + "<" + chem_conc_id + "> .\n"
            #
            #             # print(gc_ms_rdf_fragment + "\n")
            #
            #             rdf_fragment = "<" + chem_conc_id + "> a obi:0000751 .	#'dependent variable'\n"
            #             rdf_fragment = rdf_fragment + "<" + chem_conc_id + "> a stato:0000251 . #'continuous variable'\n"
            #             rdf_fragment = rdf_fragment + "<" + chem_conc_id + "> a stato:0000072 ;	#'substrate concentration'\n"
            #             rdf_fragment = rdf_fragment + "    ro:is_specified_output_of " + "<" + gc_ms_id + "> ;\n"
            #             if row[2] == "":
            #                 rdf_fragment = rdf_fragment + "    ro:is_about \"" + row[0] + "\"^^xsd:string;\n"
            #             else:
            #                 rdf_fragment = rdf_fragment + "    ro:is_about \"" + row[2] + "\";\n"
            #
            #             rdf_fragment = rdf_fragment + "    ro:located_in \"" + row[6].replace('http://purl.obolibrary.org/obo/PO_', 'po:') + "\";\n"
            #             rdf_fragment = rdf_fragment + "    ro:derives_from \"" + row[4].replace('http://purl.obolibrary.org/obo/NCBITaxon_','ncbitax:') + "\";\n"
            #             rdf_fragment = rdf_fragment + "    ro:measured_in \"" + row[7] + "\".\n"
            #
            #             # print(rdf_fragment + "\n")
            #             saveAsttl.write(gc_ms_rdf_fragment + "\n")
            #             saveAsttl.write(rdf_fragment + "\n")
            #
            line_count += 1

    saveAsttl.write("\n# ************ declaration of independent variables and their levels *************\n")

    idv1_f,idv1_fvs = create_var_rep(idv1, "genotype")
    saveAsttl.write(str(idv1_f) + "\n")
    i = 0
    for i in range(len(idv1_fvs)):
        saveAsttl.write(idv1_fvs[i]+"\n")

    idv2_f,idv2_fvs = create_var_rep(idv2, "organism part")
    saveAsttl.write(str(idv2_f) + "\n")
    j = 0
    for j in range(len(idv2_fvs)):
        saveAsttl.write(idv2_fvs[j]+"\n")

    saveAsttl.write("\n# ************ Listing all chemicals found *************\n\n")
    for element in chem_frags:
        saveAsttl.write(element+"\n")

    print('Processed {line_count} lines.')


base_cwd = os.getcwd()
print("NOW:", base_cwd)
dir = os.path.dirname(__file__)
print("DIR", dir)

jsonfile = 'rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-datapackage.json'
# tablefile = 'rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.csv'
# tablefile = 'rose-aroma-2018-subset.csv'
# saveAsttl = open('../rose-data-as-rdf/rose-aroma-ng-06-2018-subset.ttl', 'w')

# tablefile = 'https://sandbox.zenodo.org/api/files/65bed921-e764-4418-8f20-077dab0e7a45/rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.csv'

tablefile = os.path.join('../data/processed/rose-data/',
                         'rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.csv')


try:
    if not os.path.exists('../data/processed/denovo/rdf'):
        os.makedirs('../data/processed/denovo/rdf')
        os.chdir('../data/processed/denovo/rdf')
        cwd = os.getcwd()
        print("and here from if", cwd)
        saveAsttl = open('rose-aroma-ng-06-2018-full.ttl', 'w')

    else:
        print("path already created:")
        os.chdir('../data/processed/denovo/rdf')
        cwd = os.getcwd()
        print("and here from else", cwd)
        saveAsttl = open('rose-aroma-ng-06-2018-full.ttl', 'w')

    header = "\n\
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\
        @prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n\
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n\
        @prefix dc:      <http://purl.org/dc/elements/1.1/#> .\n\
        @prefix chmo:   <http://purl.obolibrary.org/obo/CHMO_> .\n\
        @prefix chebi:   <http://purl.obolibrary.org/obo/CHEBI_> .\n\
        @prefix geno:   <http://purl.obolibrary.org/obo/GENO_> .\n\
        @prefix msio:   <http://purl.obolibrary.org/obo/MSIO_> .\n\
        @prefix stato: <http://purl.obolibrary.org/obo/STATO_> .\n\
        @prefix obi: <http://purl.obolibrary.org/obo/OBI_> .\n\
        @prefix po: <http://purl.obolibrary.org/obo/PO_> .\n\
        @prefix ro: <http://purl.obolibrary.org/obo/RO_> .\n\
        @prefix has_value: <http://purl.obolibrary.org/obo/STATO_0000129> . \n\
        @prefix computed_from: <http://purl.obolibrary.org/obo/STATO_0000557> . \n\
        @prefix has_part: <http://purl.obolibrary.org/obo/BFO_0000051> . \n\
        @prefix part_of: <http://purl.obolibrary.org/obo/BFO_0000050> . \n\
        @prefix is_denoted_by: <http://purl.obolibrary.org/obo/STATO_0000205> . \n\
        @prefix denotes: <http://purl.obolibrary.org/obo/IAO_0000219> . \n\
        @prefix has_specified_input: <http://purl.obolibrary.org/obo/OBI_0000293> . \n\
        @prefix has_specified_output: <http://purl.obolibrary.org/obo/OBI_0000299> . \n\
        @prefix is_specified_input_of: <http://purl.obolibrary.org/obo/OBI_0000295> . \n\
        @prefix is_specified_output_of: <http://purl.obolibrary.org/obo/OBI_0000312> . \n\
        @prefix derives_from: <http://purl.obolibrary.org/obo/RO_0001000> . \n\
        @prefix located_in: <http://purl.obolibrary.org/obo/RO_0001025> . \n\
        @prefix has_member: <http://purl.obolibrary.org/obo/RO_0002351> . \n\
        @prefix measured_in: <http://purl.obolibrary.org/obo/RO_0002351> . \n\
        @prefix is_about: <http://purl.obolibrary.org/obo/IAO_0000136> . \n\
        @prefix ncbitax: <http://purl.obolibrary.org/obo/NCBITaxon_> .\n\n"

    saveAsttl.write(header)

    if tablefile.startswith("http"):
        try:
            with requests.get(tablefile, stream=True) as r:
                f = (line.decode('utf-8') for line in r.iter_lines())
                csv_reader = csv.reader(f, delimiter=',', quotechar='"')
                process(csv_reader)
        except IOError as ioe:
            print(ioe)
    else:
        filename = os.path.join(base_cwd,  tablefile)
        print(filename)
        try:
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                process(csv_reader)
        except IOError as ioe1:
            print("error:", ioe1)

except IOError as ioe2:
    print("another error:", ioe2)






