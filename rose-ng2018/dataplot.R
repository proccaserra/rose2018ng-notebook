
> library(ggplot2)
> library(readr)
> library(devtools)
> install_github("easyGgplot2", "kassambara")
> library(easyGgplot2)

# rose arome nature genetics data from 2018 and plotting for the different treatment groups:
> rosedata <- read_csv("rose-aroma-naturegenetics2018-treatment-group-mean-sem-report-table-example.csv")
> ggplot2.barplot(data=rosedata, xName="chemical_name", yName="sample_mean",
				faceting=TRUE, facetingVarNames="treatment", 
                facetingDirection="vertical",facetingScales="free", groupName="treatment", groupColors=c('#999999','#E69F00','pink','coral','grey','lightblue','aquamarine3','orange'), xtitle="chemical name",ytitle="mean concentration", xtitleFont=c(10,"plain","darkblue"),ytitleFont=c(10,"plain","darkblue"), xTickLabelFont=c(8,"italic", "black"), yTickLabelFont=c(8,"italic","black"),  legendPosition="right",
                legendTitle="Treatment", legendTitleFont=c(10, "bold", "black"),
                legendTextFont=c(9, "plain", "black"),
                legendBackground=c("white", 0.5, "solid", "black" ))
                + theme(axis.text.x=element_text(angle=90, hjust=1),strip.text.y = element_text(angle=0, colour="black",face="plain",size=8))



#loading-ng2018 vs science2015
>ng2018sc2015 <- read_csv("rose_aroma_compound_science2015_vs-NG2018.csv")
> ggplot2.barplot(data=rose_ngVs, xName="compound", yName="normalized_to_total_sum_concentration", faceting=TRUE, facetingVarNames="publication_year", facetingDirection="vertical",facetingScales="free", groupName="publication_year", groupColors=c('aquamarine3','orange'), xtitle="chemical name",ytitle="normalizated to total sum concentration", xtitleFont=c(10,"plain","darkblue"),ytitleFont=c(10,"plain","darkblue"), xTickLabelFont=c(8,"italic", "black"), yTickLabelFont=c(8,"italic","black"),  legendPosition="right", legendTitle="Treatment", legendTitleFont=c(10, "bold", "black"),           legendTextFont=c(9, "plain", "black"), legendBackground=c("white", 0.5, "solid", "black" ))  + theme(axis.text.x=element_text(angle=90, hjust=1),strip.text.y = element_text(angle=0, colour="black",face="plain",size=8))
