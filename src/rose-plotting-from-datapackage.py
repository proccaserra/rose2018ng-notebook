import pandas as pd
import os, errno
from plotnine import *
# matplotlib.use('Qt5Agg')


__author__ = 'proccaserra (Philippe Rocca-Serra)'

# author: philippe rocca-serra (philippe.rocca-serra@oerc.ox.ac.uk)
# ontology: http://www.stato-ontology.org

data = pd.read_csv("../data/processed/rose-data/rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.csv")
# data = pd.read_csv("https://zenodo.org/api/files/2e6d9ab9-b6be-4fcb-89e9-96ce8115b450/rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.csv") #old doi
# data = pd.read_csv("https://zenodo.org/api/files/ba3fbc84-14af-4858-a9ed-e6cfe8d4efd2/rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.csv") #latest doi file path from JSON-LD
data.head()

# width = figure_size[0]
# height = figure_size[0] * aspect_ratio
gray = '#666666'
orange = '#FF8000'
blue = '#3333FF'

p1 = (ggplot(data)
 + aes('chemical_name', 'sample_mean',fill='factor(treatment)')
 + geom_col()
 
 + theme(axis_text_x=element_text(rotation=90, hjust=1, fontsize=6, color=blue))
 + theme(axis_text_y=element_text(rotation=90, hjust=2, fontsize=6, color=orange))
 + scale_y_continuous(expand = (0,0))   
 + facet_wrap('~treatment', dir='v',ncol=1)
 + theme(figure_size = (8, 16))      
)

p1 + theme(panel_background=element_rect(fill=blue)
       )

p1

try:
    if not os.path.exists('./figures/denovo'):
        os.makedirs('./figures/denovo')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

ggsave(plot=p1, filename='./figures/denovo/Fig_3a-rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.png', dpi=100)


ng2018sc2015 = pd.read_csv("./data/processed/rose-data/rose_aroma_compound_science2015_vs_NG2018_data_integration.csv")
# ng2018sc2015 = pd.read_csv("https://zenodo.org/api/files/268f29fc-8ead-4049-bb86-181b72073682/rose_aroma_compound_science2015_vs_NG2018_data_integration.csv") #latest doi file path from JSON-LD

p2 = (ggplot(ng2018sc2015)
 + aes('chemical_name', 'normalized_to_total_sum_concentration',fill='factor(publication_year)')
 + geom_col()
 + facet_wrap('~publication_year', dir='h', ncol=1)
 + theme(axis_text_x=element_text(rotation=90, hjust=1, fontsize=6))

)

ggsave(plot=p2, filename='./figures/denovo/Fig_3b-rose_aroma_compound_science2015_vs-NG2018.png', dpi=100)


