################################################################################
### Script to get GLORIA IO data
################################################################################

### 1 Directories & packages ###################################################

library(dplyr)
library(data.table)
library(Rfast)
library(readxl)
library(tidyr)

### specify here the filepath where the data is located
fpe<-file.path("C:", "Users", "jomerkle", 
               "OneDrive - Norwegian University of Life Sciences",
               "data",
               "GLORIA",
               gversion,
               timestep)


## notes:
# economic values in k USD basic price
# we have 120 sectors. Industries, products, industries, products. 
# We delete the product part, as we do not need it.
# we have 164 countries, and 120 sectors
# we only need markup001 (basic prices)




### 1 Import Satellite data ####################################################

# this just to create a vector of index numbers for those rows and columns we want to keep
# we want to keep only MRIO data, so remove the supply matrices within
# fread is a faster reader than read.csv

39360/(2*120)
sec<-seq(1:39360) # sequence of numbers (for columns)
ser<-seq(1:39360) # sequence of numbers (for rows)
ones<-rep(1,times=120)
zeros<-rep(0,times=120)
oz<-c(ones,zeros)
full<-rep(oz,times=164)
sec[full==0]<-NA
ser[full==1]<-NA
cselector<-sec[!is.na(sec)] # removes NA values (from columns sequence)
rselector<-ser[!is.na(ser)] # removes NA values (from rows sequence)
rm(full,ones,oz,ser,sec,zeros) # remove objects no longer needed


# satellites for transaction data (reads the satellite data with fread)
tq<-data.table::fread(file = file.path(fpe,
                                       paste0(qcode,
                                              "_120secMother_AllCountries_002_TQ-Results_",
                                              timestep,"_",gversion,
                                              "_Markup001(full).csv")
                                       ),
                                       header = F,
                                       select = cselector)

tqm<-as.matrix(tq)

yq<-read.csv(file.path(fpe,
                       paste0(qcode,
                              "_120secMother_AllCountries_002_YQ-Results_",
                              timestep,"_",gversion,
                              "_Markup001(full).csv")
                       ),
             header = F)


yqm<-as.matrix(yq)

rm(tq,yq) 

# import index data
sector_ind <- read_excel(file.path(fpe,"..",paste0("GLORIA_ReadMe_",gversion,".xlsx")),sheet = "Sectors")
region_ind <- read_excel(file.path(fpe,"..",paste0("GLORIA_ReadMe_",gversion,".xlsx")),sheet = "Regions")
satellites_ind <- read_excel(file.path(fpe,"..",paste0("GLORIA_ReadMe_",gversion,".xlsx")),sheet = "Satellites")
demand_ind <- read_excel(file.path(fpe,"..",paste0("GLORIA_ReadMe_",gversion,".xlsx")),sheet = "Value added and final demand")
sequential_ind <- read_excel(file.path(fpe,"..",paste0("GLORIA_ReadMe_",gversion,".xlsx")),sheet = "Sequential region-sector labels")

# shorten sequential_ind to reflect the non-product version
all_c_s<-sequential_ind$Sequential_regionSector_labels
short_c_s<-all_c_s[cselector]
sequential_ind$Sequential_regionSector_labels<-NA
sequential_ind<-sequential_ind[1:length(short_c_s),]
sequential_ind$Sequential_regionSector_labels<-short_c_s

# create full countrylabel and full sectorlabel vectors
cq<-region_ind$Region_names
fcql<-list()
for(i in 1:length(cq)){
  fcql[[i]]<-rep(cq[i],times=nrow(sector_ind))
}
sequential_ind['fcq']<-do.call("c",fcql)
sequential_ind['fsq']<-rep(sector_ind$Sector_names,times=nrow(region_ind))

sequentiald_ind<- sequential_ind %>% select(Sequential_finalDemand_labels) %>% drop_na()

fcqld<-list()
for(i in 1:length(cq)){
  fcqld[[i]]<-rep(cq[i],times=nrow(demand_ind))
}

sequentiald_ind['fcqd']<-do.call("c",fcqld)
sequentiald_ind['demandind']<-rep(demand_ind$Final_demand_names,times=nrow(region_ind))


rm(cq,fcql,fcqld)


### 2 Filter as required #######################################################

dim(tqm)
dim(yqm)

# we only want co2 excl short cycle emissions
rindx<-which(grepl("co2_excl_short_cycle",satellites_ind$Sat_indicator) & satellites_ind$Sat_unit=="kilotonnes")

tqm<-tqm[rindx,]
yqm<-yqm[rindx,]
satellites_ind<-satellites_ind[rindx,]

rm(rindx)

### 3 Save in tmp dir and clean up #############################################

save(demand_ind,region_ind,satellites_ind,sector_ind,sequential_ind,sequentiald_ind,tqm,yqm,
     file=file.path(gloriawd,"tmpdir",paste0("gloria_",timestep,".Rdata")))

rm(list=ls()[! ls() %in% c("wd","gversion","gloriawd")])


