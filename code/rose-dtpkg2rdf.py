from rdflib import Graph, RDF
import os
import json
import csv
import uuid


cwd = os.getcwd()
os.chdir('../fair-rose-metabo-JSON-DP-validated')

jsonfile = 'rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-datapackage.json'
# tablefile = 'rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.csv'
tablefile = 'rose-aroma-2018-test.csv'

saveAsttl = open('../fair-rose-metabo-profile-in-RDF/rose-aroma-test.ttl', 'w')

header = "#-------------------------------------------------------------------------\n\
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
@prefix ncbitax: <http://purl.obolibrary.org/obo/NCBITaxon_> .\n\n"

saveAsttl.write(header)

# author: philippe rocca-serra (philippe.rocca-serra@oerc.ox.ac.uk)
# ontology: http://www.stato-ontology.org)

with open(tablefile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    treatments = {}
    idv1 = {}
    idv2 = {}

    for row in csv_reader:

        if line_count == 0:
            print("header row: ", row)
            line_count += 1
        else:
            # print(f'\t{row[0]} measured_in [organism part = {row[5]}] of [variety ={row[7]}] over [n= {row[8]}
            # measurements] with [mean = {row[9]}] and [standard error of the mean {row[11]} ].')


            mean_id = str(uuid.uuid4())
            sem_id = str(uuid.uuid4())

            if row[3] not in idv1.keys():
                idv1[row[3]] = 1

            if row[5] not in idv2.keys():
                idv2[row[5]] = 1

            if row[7] not in treatments.keys():
                saveAsttl.write("#/////////////////START_NEW_GROUP///////////////////\n")
                # let's create a new population for this new treatment group
                pop_id = str(uuid.uuid4())
                treatments[row[7]] = pop_id
                pop_rdf_fragment = "<" + pop_id + "> a stato:0000193 ; # a population\n"
                pop_rdf_fragment = pop_rdf_fragment + " rdfs:label \"" + row[7] + "\"^^xsd:string ;\n"
                pop_rdf_fragment = pop_rdf_fragment + " ro:has_value \"" + row[7] + "\"^^xsd:string ;\n"

                specimen_id = str(uuid.uuid4())
                material_rdf_fragment = "<" + specimen_id + "> a obi:0000671 ; # a biological specimen\n"
                material_rdf_fragment = material_rdf_fragment + " rdfs:label \"" + row[5] + "\"^^xsd:string;\n"
                material_rdf_fragment = material_rdf_fragment + " ro:derives_from \"" + row[6].replace('http://purl.obolibrary.org/obo/PO_','po:') + "\";\n"
                material_rdf_fragment = material_rdf_fragment + " ro:part_of \"" + row[4].replace('http://purl.obolibrary.org/obo/NCBITaxon_','ncbitax:') + "\".\n\n"

                for i in range(int(row[8])):
                    chem_conc_id = str(uuid.uuid4())
                    gc_ms_id = str(uuid.uuid4())
                    gc_ms_rdf_fragment = "<" + gc_ms_id + "> a obi:0000070 ; #'assay'\n"
                    gc_ms_rdf_fragment = gc_ms_rdf_fragment + " ro:has_part \"msio:0000100\" ; #'targeted metabolite profiling'\n"
                    gc_ms_rdf_fragment = gc_ms_rdf_fragment + " ro:has_part \"chmo:0000497\" ; #'GC mass spectrometry'\n"
                    gc_ms_rdf_fragment = gc_ms_rdf_fragment + " ro:has_specified_input " + "<" + specimen_id + "> ;\n"
                    gc_ms_rdf_fragment = gc_ms_rdf_fragment + " ro:has_specified_output " + "<" + chem_conc_id + "> .\n"

                    # print(gc_ms_rdf_fragment + "\n")

                    rdf_fragment = "<" + chem_conc_id + "> a obi:0000751 .	#'dependent variable'\n"
                    rdf_fragment = rdf_fragment + "<" + chem_conc_id + "> a stato:0000251. #'continuous variable'\n"
                    rdf_fragment = rdf_fragment + "<" + chem_conc_id + "> a stato:0000072 ;	#'substance concentration'\n"
                    rdf_fragment = rdf_fragment + "    ro:is_specified_output_of " + "<" + gc_ms_id + "> ;\n"
                    if row[2] == "":
                        rdf_fragment = rdf_fragment + "    ro:is_about \"" + row[0] + "\"^^xsd:string;\n"
                    else:
                        rdf_fragment = rdf_fragment + "    ro:is_about \"" + row[2] + "\";\n"

                    rdf_fragment = rdf_fragment + "    ro:located_in \"" + row[6].replace(
                        'http://purl.obolibrary.org/obo/PO_', 'po:') + "\";\n"
                    rdf_fragment = rdf_fragment + "    ro:derives_from \"" + row[4].replace(
                        'http://purl.obolibrary.org/obo/NCBITaxon_', 'ncbitax:') + "\";\n"
                    rdf_fragment = rdf_fragment + "    ro:measured_in \"" + row[7] + "\".\n"

                    # print(rdf_fragment + "\n")
                    saveAsttl.write(gc_ms_rdf_fragment + "\n")
                    saveAsttl.write(rdf_fragment + "\n")

                    if i < int(row[8])-1:
                        pop_rdf_fragment = pop_rdf_fragment + " ro:has_member <" + gc_ms_id + "> ;\n"
                    else:
                        pop_rdf_fragment = pop_rdf_fragment + " ro:has_member <" + gc_ms_id + "> .\n\n"

                pop_size_id = str(uuid.uuid4())
                pop_size_rdf_fragment = "<" + pop_size_id + "> a stato:0000088 ; # a population size\n"
                pop_size_rdf_fragment = pop_size_rdf_fragment + " ro:has_value \"3\"^^xsd:integer ;\n"
                pop_size_rdf_fragment = pop_size_rdf_fragment + " ro:is_about <" + pop_id + "> .\n\n"

                saveAsttl.write(material_rdf_fragment)
                saveAsttl.write(pop_rdf_fragment)
                saveAsttl.write(pop_size_rdf_fragment)

                if row[9] == "" and row[2] == "":
                    print("THIS compound was not measured: ", row[0])
                    qt_rdf_fragment = "<" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + row[0] + "\"^^xsd:string;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + "NA" + "\"^^xsd:string.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<" + sem_id + "> a stato:0000037;  #'standard error of the mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + chem_conc_id + "\"^^xsd:string;\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about <" + chem_conc_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:denotes <" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + "NA" + "\"^^xsd:string.\n"

                elif row[9] == "" and row[2] != "":
                    print("neither this compound was not measured: ", row[0])
                    qt_rdf_fragment = "<" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + chem_conc_id + "\";\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about  \"" + row[2] + "\";\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + "NA" + "\"^^xsd:string.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<" + sem_id + "> a stato:0000037;  #'standard error of the mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + chem_conc_id + "\";\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about <" + chem_conc_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:denotes <" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + "NA" + "\"^^xsd:string.\n"

                elif row[9] != "" and row[2] == "":
                    print("THAT compound: ", row[0])
                    qt_rdf_fragment = "<" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + chem_conc_id + "\"^^xsd:string;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + row[0] + "\"^^xsd:string;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + row[9] + "\"^^xsd:decimal.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<" + sem_id + "> a stato:0000037; # 'standard error of the mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + chem_conc_id + "\"^^xsd:string;\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about <" + chem_conc_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:denotes <" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + row[11] + "\"^^xsd:decimal.\n"

                elif row[9] != "" and row[2] != "":
                    print("row2-chebi id:", row[2])
                    qt_rdf_fragment = "<" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" +chem_conc_id + "\";\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about  \"" + row[2] + "\";\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + row[9] + "\"^^xsd:decimal.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<" + sem_id + "> a stato:0000037; # 'standard error of the mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + chem_conc_id + "\";\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about <" + chem_conc_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:denotes <" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + row[11] + "\"^^xsd:decimal.\n"

                saveAsttl.write(qt_rdf_fragment + "\n")
                # print(qt_rdf_fragment + "\n")
            else:
                if row[9] == "" and row[2] == "":
                    print("THIS compound was not measured: ", row[0])
                    qt_rdf_fragment = "<" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + row[0] + "\"^^xsd:string;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + "NA" + "\"^^xsd:string.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<" + sem_id + "> a stato:0000037;  #'standard error of the mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + chem_conc_id + "\"^^xsd:string;\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about <" + chem_conc_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:denotes <" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + "NA" + "\"^^xsd:string.\n"

                elif row[9] == "" and row[2] != "":
                    print("neither this compound was not measured: ", row[0])
                    qt_rdf_fragment = "<" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + chem_conc_id + "\";\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about  \"" + row[2] + "\";\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + "NA" + "\"^^xsd:string.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<" + sem_id + "> a stato:0000037;  #'standard error of the mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + chem_conc_id + "\";\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about <" + chem_conc_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:denotes <" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + "NA" + "\"^^xsd:string.\n"

                elif row[9] != "" and row[2] == "":
                    print("THAT compound: ", row[0])
                    qt_rdf_fragment = "<" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + chem_conc_id + "\"^^xsd:string;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + row[0] + "\"^^xsd:string;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + row[9] + "\"^^xsd:decimal.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<" + sem_id + "> a stato:0000037; # 'standard error of the mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + chem_conc_id + "\"^^xsd:string;\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about <" + chem_conc_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:denotes <" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + row[11] + "\"^^xsd:decimal.\n"

                else:
                    print("row2-chebi id:", row[2])
                    qt_rdf_fragment = "<" + mean_id + "> a stato:0000402;  # 'population mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" +chem_conc_id + "\";\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + row[2] + "\";\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + row[9] + "\"^^xsd:decimal.\n\n"

                    qt_rdf_fragment = qt_rdf_fragment + "<" + sem_id + "> a stato:0000037; # 'standard error of the mean'\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about \"" + chem_conc_id + "\";\n"
                    # qt_rdf_fragment = qt_rdf_fragment + "  ro:is_about <" + chem_conc_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:denotes <" + mean_id + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  stato:computed_over <" + treatments[row[7]] + ">;\n"
                    qt_rdf_fragment = qt_rdf_fragment + "  ro:has_value \"" + row[11] + "\"^^xsd:decimal.\n"

                saveAsttl.write(qt_rdf_fragment + "\n")
                # print(qt_rdf_fragment + "\n")


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
            #             rdf_fragment = rdf_fragment + "<" + chem_conc_id + "> a stato:0000251. #'continuous variable'\n"
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

        saveAsttl.write("#\\\\\\\\\\\\\\\\\\NEW LINE of RECORDS\\\\\\\\\\\\\\\\\\\n")
    idv1_rdf_fragment = "\n<var1> a obi:0000750.  # 'study design independent variable'  same_as (OBI_0000750)\n"
    idv1_rdf_fragment = idv1_rdf_fragment + "<var1> a stato:0000087;  # 'categorical variable' (STATO_0000087)\n"
    idv1_rdf_fragment = idv1_rdf_fragment + "   rdfs:label  \"genotype\"^^xsd:string;\n"
    count = 0

    idv1_fvs = []

    for key in idv1.keys():
        idv1_fv_id = str(uuid.uuid4())
        idv1_fv_rdf_fragment = "<" + idv1_fv_id + "> a stato:0000265 ; # a factor level\n"
        idv1_fv_rdf_fragment = idv1_fv_rdf_fragment + " rdfs:label \"" + key + "\"^^xsd:string ."
        # saveAsttl.write(idv1_fv_rdf_fragment + "\n")

        if count < len(idv1.keys())-1:
            idv1_rdf_fragment = idv1_rdf_fragment + "   ro:has_part <" + idv1_fv_id + "> ;\n"

            count = count + 1
        else:
            idv1_rdf_fragment = idv1_rdf_fragment + "   ro:has_part <" + idv1_fv_id + "> .\n"

            count = count + 1

        idv1_fvs.append(idv1_fv_rdf_fragment)

    idv2_fvs = []
    idv2_rdf_fragment = "\n<var2> a obi:0000750.   # 'study design independent variable'  same_as (OBI_0000750)\n"
    idv2_rdf_fragment = idv2_rdf_fragment + "<var2> a stato:0000087;  # 'categorical variable' (STATO_0000087)\n"
    idv2_rdf_fragment = idv2_rdf_fragment + "   rdfs:label  \"organism part\"^^xsd:string;\n"
    counter = 0

    for key2 in idv2.keys():
        idv2_fv_id = str(uuid.uuid4())
        idv2_fv_rdf_fragment = "<" + idv2_fv_id + "> a stato:0000265 ; # a factor level\n"
        idv2_fv_rdf_fragment = idv2_fv_rdf_fragment + " rdfs:label \"" + key2 + "\"^^xsd:string ."
        # saveAsttl.write(idv2_fv_rdf_fragment + "\n")

        if counter < len(idv2.keys())-1:
            # idv2_fv_rdf_fragment = idv2_fv_rdf_fragment + " ro:has_value \"" + key2 + "\"^^xsd:string .\n"
            idv2_rdf_fragment = idv2_rdf_fragment + "   ro:has_part <" + idv2_fv_id + ">  ;\n"

            counter = counter + 1
        else:
            idv2_rdf_fragment = idv2_rdf_fragment + "   ro:has_part <" + idv2_fv_id + ">  .\n"

            # counter = counter + 1
        idv2_fvs.append(idv2_fv_rdf_fragment)

    saveAsttl.write("\n# ************ declaration of independent variables and their levels *************\n")
    saveAsttl.write("\n" + idv1_rdf_fragment + "\n")
    i = 0
    for i in range(len(idv1_fvs)):
        saveAsttl.write(idv1_fvs[i]+"\n")

    saveAsttl.write("\n" + idv2_rdf_fragment + "\n")
    j = 0
    for j in range(len(idv2_fvs)):
        saveAsttl.write(idv2_fvs[j]+"\n")

    print(f'Processed {line_count} lines.')

