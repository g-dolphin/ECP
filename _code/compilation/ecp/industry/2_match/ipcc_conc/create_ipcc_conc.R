### Create ipcc-ecp concordance
# This script will create two files: a .csv file containing the default 
# concordance between GLORIA IPCC disaggregation and ECP IPCC disaggregation.
# a .xlsx file (workbook) containing the concordance for the GLORIA sectors. 
# This workbook contains one sheet per GLORIA (aggregated) sector.

here::here()
# ### Setup
wd<-file.path(here::here(),"_code","compilation","ecp","industry","2_match",
              "ipcc_conc")
setwd(wd)

# Packages
library(dplyr)
library(tidyr)

# Define filepaths
fpe<-file.path(wd,"..","..","1_import","ecp","tmpdir")
fpg<-file.path(wd,"..","..","1_import","gloria","tmpdir")

# data
ecp<-read.csv(file.path(fpe,"ecp_sector_CO2.csv"))
load(file.path(fpg,"gloria_2020.RData"))
rm(demand_ind,tqm,yqm,region_ind,sequential_ind)

sector_ind$Sector_names

g_sat<-satellites_ind %>% filter(grepl("EDGAR",Sat_head_indicator))
rm(satellites_ind)

################################################################################
### First a single general concordance #########################################


# concdf
e_codes<-unique(ecp$ipcc_code) # get ECP IPCC codes
g_codes<-vector()
for(i in 1:nrow(g_sat)){
 g_codes[i]<-substr(g_sat$Sat_indicator[i],start=29,stop=nchar(g_sat$Sat_indicator[i])-18)
} # extract GLORIA IPCC codes
g_codes
# issue with excel removing ' in the totals row. No idea why. correct:
g_codes[1]<-"total"
g_codes[22]<-"1A3b_noRES"
g_codes[28]<-"1A4"
# continue
concdf<-as.data.frame(matrix(nrow=length(g_codes),ncol=length(e_codes))) # create dataframe with dimensions (length(GLORIA IPCC codes), length(ECP IPCC codes))
colnames(concdf)<-e_codes
concdf<-cbind(g_codes,concdf)
colnames(concdf)[1]<-"Sat_ind"


# Fill-in default by cols (ecp) ######

# 0 for no conc 
# 1 for perfect conc
# 2 if ecp is less disaggregated
# 3 if ecp is more disaggregated
# 4 if ecp is at least two digits more disaggregated

# 1A1A
colnames(concdf)[2]
concdf$`1A1A`<-0
concdf$`1A1A`[concdf$Sat_ind == "total"]<-4
concdf$`1A1A`[concdf$Sat_ind=="1A1a"]<-1
# 1A1A1
colnames(concdf)[3]
concdf$`1A1A1`<-0
concdf$`1A1A1`[concdf$Sat_ind == "total"]<-4
concdf$`1A1A1`[concdf$Sat_ind=="1A1a"]<-3
# 1A1A2
colnames(concdf)[4]
concdf$`1A1A2`<-0
concdf$`1A1A2`[concdf$Sat_ind == "total"]<-4
concdf$`1A1A2`[concdf$Sat_ind=="1A1a"]<-3
# 1A1A3
colnames(concdf)[5]
concdf$`1A1A3`<-0
concdf$`1A1A3`[concdf$Sat_ind == "total"]<-4
concdf$`1A1A3`[concdf$Sat_ind=="1A1a"]<-3
# 1A1B
colnames(concdf)[6]
concdf$`1A1B`<-0
concdf$`1A1B`[concdf$Sat_ind == "total"]<-4
concdf$`1A1B`[concdf$Sat_ind == "1A1bc"]<-3
concdf$`1A1B`[concdf$Sat_ind == "1A1b"]<-1
# 1A1C
colnames(concdf)[7]
concdf$`1A1C`<-0
concdf$`1A1C`[concdf$Sat_ind == "total"]<-4
concdf$`1A1C`[concdf$Sat_ind == "1A1bc"]<-3
concdf$`1A1C`[concdf$Sat_ind == "1A1ci"]<-2
concdf$`1A1C`[concdf$Sat_ind == "1A1cii"]<-2
# 1A2
colnames(concdf)[8]
concdf$`1A2`<-0
concdf$`1A2`[concdf$Sat_ind == "total"]<-4
concdf$`1A2`[concdf$Sat_ind == "1A2"]<-1
concdf$`1A2`[concdf$Sat_ind %in% c("1A2a","1A2b","1A2c","1A2d","1A2e",
                                   "1A2f","1A2g","1A2h","1A2i","1A2j","1A2k",
                                   "1A2l","1A2m")]<-2
# 1A2A
colnames(concdf)[9]
concdf$`1A2A`<-0
concdf$`1A2A`[concdf$Sat_ind == "total"]<-4
concdf$`1A2A`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2A`[concdf$Sat_ind == "1A2a"]<-1
# 1A2B
colnames(concdf)[10]
concdf$`1A2B`<-0
concdf$`1A2B`[concdf$Sat_ind == "total"]<-4
concdf$`1A2B`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2B`[concdf$Sat_ind == "1A2b"]<-1
# 1A2C
colnames(concdf)[11]
concdf$`1A2C`<-0
concdf$`1A2C`[concdf$Sat_ind == "total"]<-4
concdf$`1A2C`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2C`[concdf$Sat_ind == "1A2c"]<-1
# 1A2D
colnames(concdf)[12]
concdf$`1A2D`<-0
concdf$`1A2D`[concdf$Sat_ind == "total"]<-4
concdf$`1A2D`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2D`[concdf$Sat_ind == "1A2d"]<-1
# 1A2E
colnames(concdf)[13]
concdf$`1A2E`<-0
concdf$`1A2E`[concdf$Sat_ind == "total"]<-4
concdf$`1A2E`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2E`[concdf$Sat_ind == "1A2e"]<-1
# 1A2F
colnames(concdf)[14]
concdf$`1A2F`<-0
concdf$`1A2F`[concdf$Sat_ind == "total"]<-4
concdf$`1A2F`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2F`[concdf$Sat_ind == "1A2f"]<-1
# 1A2G
colnames(concdf)[15]
concdf$`1A2G`<-0
concdf$`1A2G`[concdf$Sat_ind == "total"]<-4
concdf$`1A2G`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2G`[concdf$Sat_ind == "1A2g"]<-1
# 1A2H
colnames(concdf)[16]
concdf$`1A2H`<-0
concdf$`1A2H`[concdf$Sat_ind == "total"]<-4
concdf$`1A2H`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2H`[concdf$Sat_ind == "1A2h"]<-1
# 1A2I
colnames(concdf)[17]
concdf$`1A2I`<-0
concdf$`1A2I`[concdf$Sat_ind == "total"]<-4
concdf$`1A2I`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2I`[concdf$Sat_ind == "1A2i"]<-1
# 1A2J
colnames(concdf)[18]
concdf$`1A2J`<-0
concdf$`1A2J`[concdf$Sat_ind == "total"]<-4
concdf$`1A2J`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2J`[concdf$Sat_ind == "1A2j"]<-1
# 1A2K
colnames(concdf)[19]
concdf$`1A2K`<-0
concdf$`1A2K`[concdf$Sat_ind == "total"]<-4
concdf$`1A2K`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2K`[concdf$Sat_ind == "1A2k"]<-1
# 1A2L
colnames(concdf)[20]
concdf$`1A2L`<-0
concdf$`1A2L`[concdf$Sat_ind == "total"]<-4
concdf$`1A2L`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2L`[concdf$Sat_ind == "1A2l"]<-1
# 1A2M
colnames(concdf)[21]
concdf$`1A2M`<-0
concdf$`1A2M`[concdf$Sat_ind == "total"]<-4
concdf$`1A2M`[concdf$Sat_ind == "1A2"]<-3
concdf$`1A2M`[concdf$Sat_ind == "1A2m"]<-1
# 1A3A
colnames(concdf)[22]
concdf$`1A3A`<-0
concdf$`1A3A`[concdf$Sat_ind == "total"]<-4
concdf$`1A3A`[concdf$Sat_ind == "1A3a"]<-1
# 1A3A1
colnames(concdf)[23]
concdf$`1A3A1`<-0
concdf$`1A3A1`[concdf$Sat_ind == "total"]<-4
concdf$`1A3A1`[concdf$Sat_ind == "1A3a"]<-3
# 1A3A2
colnames(concdf)[24]
concdf$`1A3A2`<-0
concdf$`1A3A2`[concdf$Sat_ind == "total"]<-4
concdf$`1A3A2`[concdf$Sat_ind == "1A3a"]<-3
# 1A3B
colnames(concdf)[25]
concdf$`1A3B`<-0
concdf$`1A3B`[concdf$Sat_ind == "total"]<-4
concdf$`1A3B`[concdf$Sat_ind == "1A3b"]<-1
concdf$`1A3B`[concdf$Sat_ind == "1A3b_noRES"]<-2
concdf$`1A3B`[concdf$Sat_ind == "1A3b_RES"]<-2
# 1A3C
colnames(concdf)[26]
concdf$`1A3C`<-0
concdf$`1A3C`[concdf$Sat_ind == "total"]<-4
concdf$`1A3C`[concdf$Sat_ind == "1A3c"]<-1
# 1A3D
colnames(concdf)[27]
concdf$`1A3D`<-0
concdf$`1A3D`[concdf$Sat_ind == "total"]<-4
concdf$`1A3D`[concdf$Sat_ind == "1A3d"]<-1
# 1A3D1
colnames(concdf)[28]
concdf$`1A3D1`<-0
concdf$`1A3D1`[concdf$Sat_ind == "total"]<-4
concdf$`1A3D1`[concdf$Sat_ind == "1A3d"]<-3
# 1A3D2
colnames(concdf)[29]
concdf$`1A3D2`<-0
concdf$`1A3D2`[concdf$Sat_ind == "total"]<-4
concdf$`1A3D2`[concdf$Sat_ind == "1A3d"]<-3
# 1A3E1
colnames(concdf)[30]
concdf$`1A3E1`<-0
concdf$`1A3E1`[concdf$Sat_ind == "total"]<-4
concdf$`1A3E1`[concdf$Sat_ind == "1A3e"]<-3
# 1A4A
colnames(concdf)[31]
concdf$`1A4A`<-0
concdf$`1A4A`[concdf$Sat_ind == "total"]<-4
concdf$`1A4A`[concdf$Sat_ind == "1A4"]<-3
concdf$`1A4A`[concdf$Sat_ind == "1A4a"]<-1
# 1A4B
colnames(concdf)[32]
concdf$`1A4B`<-0
concdf$`1A4B`[concdf$Sat_ind == "total"]<-4
concdf$`1A4B`[concdf$Sat_ind == "1A4"]<-3
concdf$`1A4B`[concdf$Sat_ind == "1A4b"]<-1
# 1A4C
colnames(concdf)[33]
concdf$`1A4C`<-0
concdf$`1A4C`[concdf$Sat_ind == "total"]<-4
concdf$`1A4C`[concdf$Sat_ind == "1A4"]<-3
concdf$`1A4C`[concdf$Sat_ind %in% c("1A4ci","1A4cii","1A4ciii")]<-2
# 1A4C1
colnames(concdf)[34]
concdf$`1A4C1`<-0
concdf$`1A4C1`[concdf$Sat_ind == "total"]<-4
concdf$`1A4C1`[concdf$Sat_ind == "1A4"]<-4
concdf$`1A4C1`[concdf$Sat_ind == "1A4ci"]<-1
# 1A4C2
colnames(concdf)[35]
concdf$`1A4C2`<-0
concdf$`1A4C2`[concdf$Sat_ind == "total"]<-4
concdf$`1A4C2`[concdf$Sat_ind == "1A4"]<-4
concdf$`1A4C2`[concdf$Sat_ind == "1A4cii"]<-1
# 1A4C3
colnames(concdf)[36]
concdf$`1A4C3`<-0
concdf$`1A4C3`[concdf$Sat_ind == "total"]<-4
concdf$`1A4C3`[concdf$Sat_ind == "1A4"]<-4
concdf$`1A4C3`[concdf$Sat_ind == "1A4ciii"]<-1
# 1A5
colnames(concdf)[37]
concdf$`1A5`<-0
concdf$`1A5`[concdf$Sat_ind == "total"]<-4
concdf$`1A5`[concdf$Sat_ind == "1A5"]<-1
# 1A5A
colnames(concdf)[38]
concdf$`1A5A`<-0
concdf$`1A5A`[concdf$Sat_ind == "total"]<-4
concdf$`1A5A`[concdf$Sat_ind == "1A5"]<-3
# 1A5B
colnames(concdf)[39]
concdf$`1A5B`<-0
concdf$`1A5B`[concdf$Sat_ind == "total"]<-4
concdf$`1A5B`[concdf$Sat_ind == "1A5"]<-3
# 1A5C
colnames(concdf)[40]
concdf$`1A5C`<-0
concdf$`1A5C`[concdf$Sat_ind == "total"]<-4
concdf$`1A5C`[concdf$Sat_ind == "1A5"]<-3
# 1B1
colnames(concdf)[41]
concdf$`1B1`<-0
concdf$`1B1`[concdf$Sat_ind == "total"]<-4
concdf$`1B1`[concdf$Sat_ind == "1B1"]<-1
# 1B2A
colnames(concdf)[42]
concdf$`1B2A`<-0
concdf$`1B2A`[concdf$Sat_ind == "total"]<-4
concdf$`1B2A`[concdf$Sat_ind == "1B2"]<-3
# 1B2B
colnames(concdf)[43]
concdf$`1B2B`<-0
concdf$`1B2B`[concdf$Sat_ind == "total"]<-4
concdf$`1B2B`[concdf$Sat_ind == "1B2"]<-3
# 2A
colnames(concdf)[44]
concdf$`2A`<-0
concdf$`2A`[concdf$Sat_ind == "total"]<-4
concdf$`2A`[concdf$Sat_ind == "2A1"]<-2
concdf$`2A`[concdf$Sat_ind == "2A2"]<-2
concdf$`2A`[concdf$Sat_ind == "2A3"]<-2
concdf$`2A`[concdf$Sat_ind == "2A4"]<-2
# 2A1
colnames(concdf)[45]
concdf$`2A1`<-0
concdf$`2A1`[concdf$Sat_ind == "total"]<-4
concdf$`2A1`[concdf$Sat_ind == "2A1"]<-1
# 2A2
colnames(concdf)[46]
concdf$`2A2`<-0
concdf$`2A2`[concdf$Sat_ind == "total"]<-4
concdf$`2A2`[concdf$Sat_ind == "2A2"]<-1
# 2A3
colnames(concdf)[47]
concdf$`2A3`<-0
concdf$`2A3`[concdf$Sat_ind == "total"]<-4
concdf$`2A3`[concdf$Sat_ind == "2A3"]<-1
# 2A4
colnames(concdf)[48]
concdf$`2A4`<-0
concdf$`2A4`[concdf$Sat_ind == "total"]<-4
concdf$`2A4`[concdf$Sat_ind == "2A4"]<-1
# 2B
colnames(concdf)[49]
concdf$`2B`<-0
concdf$`2B`[concdf$Sat_ind == "total"]<-4
concdf$`2B`[concdf$Sat_ind == "2B"]<-1
# 2C
colnames(concdf)[50]
concdf$`2C`<-0
concdf$`2C`[concdf$Sat_ind == "total"]<-4
concdf$`2C`[concdf$Sat_ind == "2C"]<-1
# 2D
colnames(concdf)[51]
concdf$`2D`<-0
concdf$`2D`[concdf$Sat_ind == "total"]<-4
concdf$`2D`[concdf$Sat_ind == "2D"]<-1
# 2E
colnames(concdf)[52]
concdf$`2E`<-0
concdf$`2E`[concdf$Sat_ind == "total"]<-4
concdf$`2E`[concdf$Sat_ind == "2E"]<-1
# 2F
colnames(concdf)[53]
concdf$`2F`<-0
concdf$`2F`[concdf$Sat_ind == "total"]<-4
concdf$`2F`[concdf$Sat_ind == "2F"]<-1
# 2G
colnames(concdf)[54]
concdf$`2G`<-0
concdf$`2G`[concdf$Sat_ind == "total"]<-4
concdf$`2G`[concdf$Sat_ind == "2G"]<-1
# 2H1
colnames(concdf)[55]
concdf$`2H1`<-0
concdf$`2H1`[concdf$Sat_ind == "total"]<-4
concdf$`2H1`[concdf$Sat_ind == "2H"]<-3
# 2H2
colnames(concdf)[56]
concdf$`2H2`<-0
concdf$`2H2`[concdf$Sat_ind == "total"]<-4
concdf$`2H2`[concdf$Sat_ind == "2H"]<-3
# 3A1
colnames(concdf)[57]
concdf$`3A1`<-0
concdf$`3A1`[concdf$Sat_ind == "total"]<-4
concdf$`3A1`[concdf$Sat_ind == "3A1"]<-1
# 3A2
colnames(concdf)[58]
concdf$`3A2`<-0
concdf$`3A2`[concdf$Sat_ind == "total"]<-4
concdf$`3A2`[concdf$Sat_ind == "3A2"]<-1
# 3B1
colnames(concdf)[59]
concdf$`3B1`<-0
concdf$`3B1`[concdf$Sat_ind == "total"]<-4
concdf$`3B1`[concdf$Sat_ind == "3B1"]<-1
# 3B2
colnames(concdf)[60]
concdf$`3B2`<-0
concdf$`3B2`[concdf$Sat_ind == "total"]<-4
concdf$`3B2`[concdf$Sat_ind == "3B2"]<-1
# 3B3
colnames(concdf)[61]
concdf$`3B3`<-0
concdf$`3B3`[concdf$Sat_ind == "total"]<-4
concdf$`3B3`[concdf$Sat_ind == "3B3"]<-1
# 3B4
colnames(concdf)[62]
concdf$`3B4`<-0
concdf$`3B4`[concdf$Sat_ind == "total"]<-4
concdf$`3B4`[concdf$Sat_ind == "3B4&6"]<-3
# 3B5
colnames(concdf)[63]
concdf$`3B5`<-0
concdf$`3B5`[concdf$Sat_ind == "total"]<-4
concdf$`3B5`[concdf$Sat_ind == "3B5"]<-1
# 3B6
colnames(concdf)[64]
concdf$`3B6`<-0
concdf$`3B6`[concdf$Sat_ind == "total"]<-4
concdf$`3B6`[concdf$Sat_ind == "3B4&6"]<-3
# 3C1
colnames(concdf)[65]
concdf$`3C1`<-0
concdf$`3C1`[concdf$Sat_ind == "total"]<-4
concdf$`3C1`[concdf$Sat_ind == "3C1"]<-1
concdf$`3C1`[concdf$Sat_ind %in% c("3C1a","3C1b","3C1c","3C1d")]<-2
# 3C2
colnames(concdf)[66]
concdf$`3C2`<-0
concdf$`3C2`[concdf$Sat_ind == "total"]<-4
concdf$`3C2`[concdf$Sat_ind == "3C2"]<-1
# 3C3
colnames(concdf)[67]
concdf$`3C3`<-0
concdf$`3C3`[concdf$Sat_ind == "total"]<-4
concdf$`3C3`[concdf$Sat_ind == "3C3"]<-1
# 3C4
colnames(concdf)[68]
concdf$`3C4`<-0
concdf$`3C4`[concdf$Sat_ind == "total"]<-4
concdf$`3C4`[concdf$Sat_ind == "3C4"]<-1
# 3C5
colnames(concdf)[69]
concdf$`3C5`<-0
concdf$`3C5`[concdf$Sat_ind == "total"]<-4
concdf$`3C5`[concdf$Sat_ind == "3C5"]<-1
# 3C6
colnames(concdf)[70]
concdf$`3C6`<-0
concdf$`3C6`[concdf$Sat_ind == "total"]<-4
concdf$`3C6`[concdf$Sat_ind == "3C6"]<-1
# 3C7
colnames(concdf)[71]
concdf$`3C7`<-0
concdf$`3C7`[concdf$Sat_ind == "total"]<-4
concdf$`3C7`[concdf$Sat_ind == "3C7"]<-1
# 3C8
colnames(concdf)[72]
concdf$`3C8`<-0
concdf$`3C8`[concdf$Sat_ind == "total"]<-4
concdf$`3C8`[concdf$Sat_ind == "3C8"]<-1
# 4A
colnames(concdf)[73]
concdf$`4A`<-0
concdf$`4A`[concdf$Sat_ind == "total"]<-4
concdf$`4A`[concdf$Sat_ind == "4A"]<-1
# 4B
colnames(concdf)[74]
concdf$`4B`<-0
concdf$`4B`[concdf$Sat_ind == "total"]<-4
concdf$`4B`[concdf$Sat_ind == "4B"]<-1
# 4C
colnames(concdf)[75]
concdf$`4C`<-0
concdf$`4C`[concdf$Sat_ind == "total"]<-4
concdf$`4C`[concdf$Sat_ind == "4C"]<-1
# 4D
colnames(concdf)[76]
concdf$`4D`<-0
concdf$`4D`[concdf$Sat_ind == "total"]<-4
concdf$`4D`[concdf$Sat_ind == "4D"]<-1
# 4E
colnames(concdf)[77]
concdf$`4E`<-0
concdf$`4E`[concdf$Sat_ind == "total"]<-4
concdf$`4E`[concdf$Sat_ind == "4E"]<-1
# 5A
colnames(concdf)[78]
concdf$`5A`<-0
concdf$`5A`[concdf$Sat_ind == "total"]<-4
concdf$`5A`[concdf$Sat_ind == "5A"]<-1
concdf$`5A`[concdf$Sat_ind == "5B"]<-2 # this one is not strictly correct, but aprx


### save as default
write.csv(concdf,"ipcc_codes_deflt.csv",row.names = F)




################################################################################
#### Then industry-specific concordance adjustments where necessary ############

# make a list
newcat<-sector_ind$Sector_names
conclist<-list()
for(i in 1:length(newcat)){
 conclist[[i]]<-concdf
}
names(conclist)<-newcat
newcat

### Petroleum extraction
# here we want to map only 1B2A, not 1B2B
conclist[['Petroleum extraction']]$`1B2B`[conclist[['Petroleum extraction']]$Sat_ind == "1B2"]<-0

### Gas extraction
# here we want to map only 1B2B, not 1B2A
conclist[['Gas extraction']]$`1B2A`[conclist[['Gas extraction']]$Sat_ind == "1B2"]<-0

### Pulp and paper
# here we want to map only 2H1, not 2H2
conclist[['Pulp and paper']]$`2H2`[conclist[['Pulp and paper']]$Sat_ind == "2H"]<-0

### All the food and bev product industries
# starting from beef meat (41) down to tobacco products (56)
# here we want to map only 2H2, not 2H1
for(i in 41:56){
  conclist[[i]]$`2H1`[conclist[[i]]$Sat_ind == "2H"]<-0
}
newcat

# save
save(conclist,file=file.path(wd,paste0("ipcc_conc_",gversion,".RData")))
#
# # clean up
rm(list = ls())
#





