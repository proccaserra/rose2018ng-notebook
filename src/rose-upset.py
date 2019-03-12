from matplotlib_venn import venn3, venn3_circles
from matplotlib import pyplot as plt
import pandas as pd
import os, errno
from upsetplot import plot

try:
    if not os.path.exists('./figures/denovo'):
        os.makedirs('./figures/denovo')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

TableS1_Science2015 = ["E_E_farnesal","E_E_farnesol","E_E_farnesyl_acetate","E_2_hexen_1_ol","E_2_hexenal","E_beta_farnesene","E_beta_ocimene","Z_3_hexen_1_ol","Z_3_hexenyl_acetate","1_3_5_trimethoxybenzene","2_phenylethanol","3_5_dimethoxytoluene","alpha_cadinol","benzaldehyde","benzylalcohol","beta_myrcene","bicyclogermacrene","citronellol","delta_cadinene","dihydro_beta_ionol","dihydro_beta_ionone","elemol","eugenol","geranial","geranic_acid","geraniol","geranyl_acetate","germacrene_D","germacrene_D_4_ol","hexan_1_ol","hexanal","hexyl_acetate","methyl_eugenol","neral","nerol","nonanal","phenylacetaldehyde","tau_cadinol","tau_muurolol","Z_beta_ocimene"]

# Table S3:
# ["(E,E)_farnesol","(E)_beta_farnesene","alpha_cadinol","beta_myrcene","bicyclogermacrene","citronellal","citronellol","delta_cadinene","geranial","geraniol","geranyl acetate","germacrene D","germacrene D_4_ol","limonene","linalool","neral","nerol","beta_caryophyllene","beta_elemene","beta_pinene","tau_cadinol","tau_muurolol","alpha_humulene","alpha_muurolene","alpha_muurolol","alpha_pinene"])

TableS3_Science2015 = ["E_E_farnesol","E_beta_farnesene","alpha_cadinol","beta_myrcene","bicyclogermacrene","citronellal","citronellol","delta_cadinene","geranial","geraniol","geranyl_acetate","germacrene_D","germacrene_D_4_ol","limonene","linalool","neral","nerol","beta_caryophyllene","beta_elemene","beta_pinene","tau_cadinol","tau_muurolol","alpha_humulene","alpha_muurolene","alpha_muurolol","alpha_pinene"]

set_NG2018 = ["hexan-2-ol","hexanal","E_2_hexenal","Z_3_hexen_1_ol","E_2_hexen_1_ol","hexan_1_ol","nonane","alpha_pinene","benzaldehyde","beta_myrcene","Z_3_hexenyl_acetate","hexyl_acetate","E_hexenyl_acetate","limonene","benzylalcohol","phenylacetaldehyde","E_beta_ocimene","linalool","nonanal","2_phenylethanol","beta_citronellal","alpha-terpineol","decanal","nerol","beta_citronellol","neral","geraniol","beta_phenylethyl_acetate","3_5_dimethoxytoluene","geranial","undecanal","theaspirane_A","beta_citronellyl_acetate","eugenol","neryl_acetate","alpha_copaene","geranyl_acetate","beta_elemene","methyl_eugenol","beta_caryophyllene","1_3_5_trimethoxybenzene","dihydro_beta_ionone","alpha_guaiene","dihydro_beta_ionol","E_beta_farnesene","germacrene_D","pentadecane","E_E_alpha_farnesene","gamma_cadinene","delta_cadinene","elemol","germacrene_D_4_ol","hexadecane","tau_cadinol","beta_eudesmol","alpha_cadinol","heptadecene","heptadecane","E_E_farnesol","E_E_farnesal","E_E_farnesyl_acetate"]

df1 = pd.DataFrame({'name': TableS1_Science2015})
df2 = pd.DataFrame({'name': TableS3_Science2015})
df3 = pd.DataFrame({'name': set_NG2018})


df4 = (df1.merge(df2, how='outer', indicator=True)
 .assign(TableS1_Science2015 = lambda x: x._merge != "right_only",
         TableS3_Science2015 = lambda x: x._merge != "left_only")
 .drop("_merge", 1)).merge(df3, how='outer', indicator=True).assign(set_NG2018 = lambda x: x._merge != "left_only").drop("_merge",1)

chemicals = [c for c in df4.columns if c != "name"]
chemicals_count_series = df4.fillna(False).groupby(chemicals).count()["name"]

plot(chemicals_count_series, sort_by="cardinality")
plt.rcParams["figure.figsize"] = (20,3)

plt.savefig('./figures/denovo/Figure_2b-upset-plot-Science2015&NatGen2018.png', bbox_inches='tight')


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



