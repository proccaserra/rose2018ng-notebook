from matplotlib_venn import venn3, venn3_circles
from matplotlib import pyplot as plt
import os, errno
import pandas as pd

__author__ = 'proccaserra (Philippe Rocca-Serra)'

# author: philippe rocca-serra (philippe.rocca-serra@oerc.ox.ac.uk)
# ontology: http://www.stato-ontology.org


plt.rcParams.update({'font.family': 'Arial', 'font.size': 12, 'font.style':'normal'})

# Table S1
# ["(E,E)_farnesal","(E,E)_farnesol","(E,E)_farnesyl acetate","(E)_2_hexen_1_ol","(E)_2_hexenal","(E)_beta_farnesene","(E)_beta_ocimene","(Z)_3_hexen_1_ol","(Z)_3_hexenyl acetate","1,3,5_trimethoxybenzene","2_phenylethanol","3,5_dimethoxytoluene","alpha_cadinol","benzaldehyde","benzylalcohol","beta_myrcene","bicyclogermacrene","citronellol","delta_cadinene","dihydro_beta_ionol","dihydro_beta_ionone","elemol","eugenol","geranial","geranic_acid","geraniol","geranyl acetate","germacrene D","germacrene D_4_ol","hexan_1_ol","hexanal","hexyl acetate","methyl eugenol","neral","nerol","nonanal","phenylacetaldehyde","tau_cadinol","tau_muurolol","Z_β_ocimene"]

TableS1_Science2015 = set(["E_E_farnesal","E_E_farnesol","E_E_farnesyl_acetate","E_2_hexen_1_ol","E_2_hexenal","E_beta_farnesene","E_beta_ocimene","Z_3_hexen_1_ol","Z_3_hexenyl_acetate","1_3_5_trimethoxybenzene","2_phenylethanol","3_5_dimethoxytoluene","alpha_cadinol","benzaldehyde","benzylalcohol","beta_myrcene","bicyclogermacrene","citronellol","delta_cadinene","dihydro_beta_ionol","dihydro_beta_ionone","elemol","eugenol","geranial","geranic_acid","geraniol","geranyl_acetate","germacrene_D","germacrene_D_4_ol","hexan_1_ol","hexanal","hexyl_acetate","methyl_eugenol","neral","nerol","nonanal","phenylacetaldehyde","tau_cadinol","tau_muurolol","Z_beta_ocimene"])
print("size set 1: ", len(TableS1_Science2015))

# Table S3:
# ["(E,E)_farnesol","(E)_beta_farnesene","alpha_cadinol","beta_myrcene","bicyclogermacrene","citronellal","citronellol","delta_cadinene","geranial","geraniol","geranyl acetate","germacrene D","germacrene D_4_ol","limonene","linalool","neral","nerol","beta_caryophyllene","beta_elemene","beta_pinene","tau_cadinol","tau_muurolol","alpha_humulene","alpha_muurolene","alpha_muurolol","alpha_pinene"])

TableS3_Science2015 = set(["E_E_farnesol","E_beta_farnesene","alpha_cadinol","beta_myrcene","bicyclogermacrene","citronellal","citronellol","delta_cadinene","geranial","geraniol","geranyl_acetate","germacrene_D","germacrene_D_4_ol","limonene","linalool","neral","nerol","beta_caryophyllene","beta_elemene","beta_pinene","tau_cadinol","tau_muurolol","alpha_humulene","alpha_muurolene","alpha_muurolol","alpha_pinene"])
print("size set 3: ", len(TableS3_Science2015))

# Table S4:
# set4_Science2015 = set(["(E)_beta_farnesene","(E)_beta_ocimene","allo_ocimene","beta_myrcene","citronellol","citronellyl_acetate","delta_cadinene","geraniol","germacrene D","limonene","neral","nerol","neryl_acetate","tau_cadinol","Z_beta_ocimene","alpha_phellandrene","alpha_terpinene","alpha_terpinolene","gamma_terpinene"])

TableS4_Science2015 = set(["E_beta_farnesene","E_beta_ocimene","allo_ocimene","beta_myrcene","citronellol","citronellyl_acetate","delta_cadinene","geraniol","germacrene_D","limonene","neral","nerol","neryl_acetate","tau_cadinol","Z_beta_ocimene","alpha_phellandrene","alpha_terpinene","alpha_terpinolene","gamma_terpinene"])
print("size set 4: ", len(TableS4_Science2015))

#  set_NG2018=set(["hexan-2-ol","hexanal","(E)-2-hexenal","(Z)-3-hexen-1-ol","(E)-2-hexen-1-ol","hexan-1-ol","nonane",
#            "alpha-pinene","benzaldehyde","beta-myrcene","(Z)-3-hexenyl acetate","hexyl acetate","(E)-hexenyl acetate",
#            "(+/-)-limonene","benzylalcohol","phenylacetaldehyde","(E)-beta-ocimene","(+/-)-linalool",
#            "nonanal","2-phenylethanol","(+/-)-beta-citronellal","(+/-)-alpha-terpineol","decanal",
#            "nerol","(+/-)-beta-citronellol","neral","geraniol","beta-phenylethyl acetate","3,5-dimethoxytoluene",
#            "geranial","undecanal","theaspirane A","(+/-)-beta-citronellyl acetate","eugenol","neryl acetate",
#            "alpha-copaene","geranyl acetate","beta-elemene","methyl eugenol","(E)-beta-caryophyllene",
#            "1,3,5-trimethoxybenzene","dihydro-beta-ionone","alpha guaiene","dihydro-beta-ionol","(E)-beta-farnesene",
#            "germacrene D","pentadecane","(E,E)-alpha-farnesene","gamma-cadinene","delta-cadinene","elemol",
#            "Germacrene D 4 ol","hexadecane","Tau-cadinol","beta-eudesmol","alpha-cadinol","heptadecene","heptadecane",
#            "(E,E)-farnesol","(E,E)-farnesal","(E,E)-farnesyl acetate"])


set_NG2018=set(["hexan-2-ol","hexanal","E_2_hexenal","Z_3_hexen_1_ol","E_2_hexen_1_ol","hexan_1_ol","nonane","alpha_pinene","benzaldehyde","beta_myrcene","Z_3_hexenyl_acetate","hexyl_acetate","E_hexenyl_acetate","limonene","benzylalcohol","phenylacetaldehyde","E_beta_ocimene","linalool","nonanal","2_phenylethanol","beta_citronellal","alpha-terpineol","decanal","nerol","beta_citronellol","neral","geraniol","beta_phenylethyl_acetate","3_5_dimethoxytoluene","geranial","undecanal","theaspirane_A","beta_citronellyl_acetate","eugenol","neryl_acetate","alpha_copaene","geranyl_acetate","beta_elemene","methyl_eugenol","beta_caryophyllene","1_3_5_trimethoxybenzene","dihydro_beta_ionone","alpha_guaiene","dihydro_beta_ionol","E_beta_farnesene","germacrene_D","pentadecane","E_E_alpha_farnesene","gamma_cadinene","delta_cadinene","elemol","germacrene_D_4_ol","hexadecane","tau_cadinol","beta_eudesmol","alpha_cadinol","heptadecene","heptadecane","E_E_farnesol","E_E_farnesal","E_E_farnesyl_acetate"])

intersect_1v3 = set(TableS1_Science2015) & set(TableS3_Science2015)
intersect_1v4 = set(TableS1_Science2015) & set(TableS4_Science2015)
intersect_3v4 = set(TableS3_Science2015) & set(TableS4_Science2015)
intersect_all = set(TableS1_Science2015) & set(TableS3_Science2015) & set(TableS4_Science2015)

intersect_1vNG = set(TableS1_Science2015) & set(set_NG2018)
intersect_3vNG = set(TableS3_Science2015) & set(set_NG2018)

# print(len(intersect_1v3), "|", sorted(intersect_1v3))
# print(len(intersect_1v4), "|", sorted(intersect_1v4))
# print(len(intersect_3v4), "|", sorted(intersect_3v4))
# print(len(intersect_all), "|", sorted(intersect_all))
# print(len(intersect_1vNG), "|", sorted(intersect_1vNG))
# print(len(intersect_3vNG), "|", sorted(intersect_3vNG))

#creates figure showing the overlap between the different VOCs testing in the 2015 article:
# v=venn3([TableS1_Science2015, TableS3_Science2015, set_NG2018], ('TableS1-10.1126/science.aab0696', 'TableS3-10.1126/science.aab0696', 'SupplementaryData3-NatureGenetics.10.1038/s41588-018-0110-3'))
# plt.show()

v1 = venn3([TableS1_Science2015, TableS3_Science2015, set_NG2018], ('Table S1, doi:10.1126/science.aab0696, (Science, 2015)', 'Table S3, doi:10.1126/science.aab0696, (Science, 2015)', 'Supplementary Data 3, doi:10.1038/s41588-018-0110-3, (Nature Genetics, 2018)'))
c = venn3_circles([TableS1_Science2015, TableS3_Science2015, set_NG2018], linestyle='dotted', linewidth=1, color="black")
# c[0].set_lw(4.0)
# c[0].set_ls('dotted')
# c[0].set_color('skyblue')
# c[0].set_alpha(0.9)
# c[1].set_lw(4.0)
# c[1].set_ls('dotted')
# c[1].set_color('darkblue')
# c[2].set_lw(4.0)
# c[2].set_ls('dotted')
# c[2].set_color('violet')
plt.title('Common and distinct metabolites between 2 rose studies by Bendahmane group in 2015 and 2018\n')


for text in v1.set_labels:
    text.set_fontsize(11)
    text.set_family('arial')
    text.set_style('normal')
# plt.show()

try:
    if not os.path.exists('./figures/denovo'):
        os.makedirs('./figures/denovo')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

plt.savefig('./figures/denovo/Figure_2a-venn-diagram-Science2015&NatGen2018.png', bbox_inches='tight')

#///////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# input for generating figure 2 using upSetR:
# https://gehlenborglab.shinyapps.io/upsetr/
# https://www.biorxiv.org/content/early/2017/03/25/120600.full.pdf+html
# chemical names had to be altered to allow lists to be used as input to the software.
# set1_Science2015 = set([E_E_farnesal,E_E_farnesol,E_E_farnesyl_acetate,E_2_hexen_1_ol,E_2_hexenal,E_beta_farnesene,E_beta_ocimene,Z_3_hexen_1_ol,Z_3_hexenyl_acetate,1_3_5_trimethoxybenzene,2_phenylethanol,3_5_dimethoxytoluene,alpha_cadinol,benzaldehyde,benzylalcohol,beta_myrcene,bicyclogermacrene,citronellol,delta_cadinene,dihydro_beta_ionol,dihydro_beta_ionone,elemol,eugenol,geranial,geranic_acid,geraniol,geranyl_acetate,germacrene_D,germacrene_D_4_ol,hexan_1_ol,hexanal,hexyl_acetate,methyl_eugenol,neral,nerol,nonanal,phenylacetaldehyde,tau_cadinol,tau_muurolol,Z_beta_ocimene])
# set2_Science2015 = set([E_E_farnesol,E_beta_farnesene,alpha_cadinol,beta_myrcene,bicyclogermacrene,citronellal,citronellol,delta_cadinene,geranial,geraniol,geranyl_acetate,germacrene_D,germacrene_D_4_ol,limonene,linalool,neral,nerol,E_beta_caryophyllene,beta_elemene,beta_pinene,tau_cadinol,tau_muurolol,alpha_humulene,alpha_muurolene,alpha_muurolol,alpha_pinene])
# set_NG2018=set([hexan-2-ol,hexanal,E_2_hexenal,Z_3_hexen_1_ol,E_2_hexen_1_ol,hexan_1_ol,nonane,alpha_pinene,benzaldehyde,beta_myrcene,Z_3_hexenyl_acetate,hexyl_acetate,E_hexenyl_acetate,limonene,benzylalcohol,phenylacetaldehyde,E_beta_ocimene,linalool,nonanal,2_phenylethanol,beta_citronellal,alpha-terpineol,decanal,nerol,beta_citronellol,neral,geraniol,beta_phenylethyl_acetate,3_5_dimethoxytoluene,geranial,undecanal,theaspirane_A,beta_citronellyl_acetate,eugenol,neryl_acetate,alpha_copaene,geranyl_acetate,beta_elemene,methyl_eugenol,E_beta_caryophyllene,1_3_5_trimethoxybenzene,dihydro_beta_ionone,alpha_guaiene,dihydro_beta_ionol,E_beta_farnesene,germacrene_D,pentadecane,E_E_alpha_farnesene,gamma_cadinene,delta_cadinene,elemol,germacrene_D_4_ol,hexadecane,tau_cadinol,beta_eudesmol,alpha_cadinol,heptadecene,heptadecane,E_E_farnesol,E_E_farnesal,E_E_farnesyl_acetate])
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\////////////////////////////////////////

# set1_Science2015 = pd.Series([E_E_farnesal,E_E_farnesol,E_E_farnesyl_acetate,E_2_hexen_1_ol,E_2_hexenal,E_beta_farnesene,E_beta_ocimene,Z_3_hexen_1_ol,Z_3_hexenyl_acetate,1_3_5_trimethoxybenzene,2_phenylethanol,3_5_dimethoxytoluene,alpha_cadinol,benzaldehyde,benzylalcohol,beta_myrcene,bicyclogermacrene,citronellol,delta_cadinene,dihydro_beta_ionol,dihydro_beta_ionone,elemol,eugenol,geranial,geranic_acid,geraniol,geranyl_acetate,germacrene_D,germacrene_D_4_ol,hexan_1_ol,hexanal,hexyl_acetate,methyl_eugenol,neral,nerol,nonanal,phenylacetaldehyde,tau_cadinol,tau_muurolol,Z_beta_ocimene])
# set2_Science2015 = pd.Series([E_E_farnesol,E_beta_farnesene,alpha_cadinol,beta_myrcene,bicyclogermacrene,citronellal,citronellol,delta_cadinene,geranial,geraniol,geranyl_acetate,germacrene_D,germacrene_D_4_ol,limonene,linalool,neral,nerol,E_beta_caryophyllene,beta_elemene,beta_pinene,tau_cadinol,tau_muurolol,alpha_humulene,alpha_muurolene,alpha_muurolol,alpha_pinene])
# set_NG2018 = pd.Series([hexan-2-ol,hexanal,E_2_hexenal,Z_3_hexen_1_ol,E_2_hexen_1_ol,hexan_1_ol,nonane,alpha_pinene,benzaldehyde,beta_myrcene,Z_3_hexenyl_acetate,hexyl_acetate,E_hexenyl_acetate,limonene,benzylalcohol,phenylacetaldehyde,E_beta_ocimene,linalool,nonanal,2_phenylethanol,beta_citronellal,alpha-terpineol,decanal,nerol,beta_citronellol,neral,geraniol,beta_phenylethyl_acetate,3_5_dimethoxytoluene,geranial,undecanal,theaspirane_A,beta_citronellyl_acetate,eugenol,neryl_acetate,alpha_copaene,geranyl_acetate,beta_elemene,methyl_eugenol,E_beta_caryophyllene,1_3_5_trimethoxybenzene,dihydro_beta_ionone,alpha_guaiene,dihydro_beta_ionol,E_beta_farnesene,germacrene_D,pentadecane,E_E_alpha_farnesene,gamma_cadinene,delta_cadinene,elemol,germacrene_D_4_ol,hexadecane,tau_cadinol,beta_eudesmol,alpha_cadinol,heptadecene,heptadecane,E_E_farnesol,E_E_farnesal,E_E_farnesyl_acetate])

# set1_Science2015 = set([E_E_farnesal,E_E_farnesol,E_E_farnesyl_acetate,E_2_hexen_1_ol,E_2_hexenal,E_beta_farnesene,E_beta_ocimene,Z_3_hexen_1_ol,Z_3_hexenyl_acetate,1_3_5_trimethoxybenzene,2_phenylethanol,3_5_dimethoxytoluene,alpha_cadinol,benzaldehyde,benzylalcohol,beta_myrcene,bicyclogermacrene,citronellol,delta_cadinene,dihydro_beta_ionol,dihydro_beta_ionone,elemol,eugenol,geranial,geranic_acid,geraniol,geranyl_acetate,germacrene_D,germacrene_D_4_ol,hexan_1_ol,hexanal,hexyl_acetate,methyl_eugenol,neral,nerol,nonanal,phenylacetaldehyde,tau_cadinol,tau_muurolol,Z_beta_ocimene])
# set2_Science2015 = set([E_E_farnesol,E_beta_farnesene,alpha_cadinol,beta_myrcene,bicyclogermacrene,citronellal,citronellol,delta_cadinene,geranial,geraniol,geranyl_acetate,germacrene_D,germacrene_D_4_ol,limonene,linalool,neral,nerol,E_beta_caryophyllene,beta_elemene,beta_pinene,tau_cadinol,tau_muurolol,alpha_humulene,alpha_muurolene,alpha_muurolol,alpha_pinene])
# set_NG2018 = set([hexan-2-ol,hexanal,E_2_hexenal,Z_3_hexen_1_ol,E_2_hexen_1_ol,hexan_1_ol,nonane,alpha_pinene,benzaldehyde,beta_myrcene,Z_3_hexenyl_acetate,hexyl_acetate,E_hexenyl_acetate,limonene,benzylalcohol,phenylacetaldehyde,E_beta_ocimene,linalool,nonanal,2_phenylethanol,beta_citronellal,alpha-terpineol,decanal,nerol,beta_citronellol,neral,geraniol,beta_phenylethyl_acetate,3_5_dimethoxytoluene,geranial,undecanal,theaspirane_A,beta_citronellyl_acetate,eugenol,neryl_acetate,alpha_copaene,geranyl_acetate,beta_elemene,methyl_eugenol,E_beta_caryophyllene,1_3_5_trimethoxybenzene,dihydro_beta_ionone,alpha_guaiene,dihydro_beta_ionol,E_beta_farnesene,germacrene_D,pentadecane,E_E_alpha_farnesene,gamma_cadinene,delta_cadinene,elemol,germacrene_D_4_ol,hexadecane,tau_cadinol,beta_eudesmol,alpha_cadinol,heptadecene,heptadecane,E_E_farnesol,E_E_farnesal,E_E_farnesyl_acetate])





