################################################################################
### Script to get GLORIA IO data
################################################################################

### 1 Directories & packages ###################################################

library(dplyr)
library(data.table)
library(Rfast)
library(readxl)


### specify here the filepath where the data is located
fpe<-file.path("C:", "Users", "jomerkle", 
               "OneDrive - Norwegian University of Life Sciences",
               "data",
               "GLORIA",
               "057",
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
                                              timestep,
                                              "_057_Markup001(full).csv")
                                       ),
                                       header = F,
                                       select = cselector)

tqm<-as.matrix(tq)

yq<-read.csv(file.path(fpe,
                       paste0(qcode,
                              "_120secMother_AllCountries_002_YQ-Results_",
                              timestep,
                              "_057_Markup001(full).csv")
                       ),
             header = F)


yqm<-as.matrix(yq)

rm(tq,yq) 


# import index data
sector_ind <- read_excel(file.path(fpe,"..","GLORIA_ReadMe_057.xlsx"),sheet = "Sectors")
region_ind <- read_excel(file.path(fpe,"..","GLORIA_ReadMe_057.xlsx"),sheet = "Regions")
satellites_ind <- read_excel(file.path(fpe,"..","GLORIA_ReadMe_057.xlsx"),sheet = "Satellites")
demand_ind <- read_excel(file.path(fpe,"..","GLORIA_ReadMe_057.xlsx"),sheet = "Value added and final demand")
sequential_ind <- read_excel(file.path(fpe,"..","GLORIA_ReadMe_057.xlsx"),sheet = "Sequential region-sector labels")


newcat<-sector_ind$Sector_names
newcat<-newcat[!is.na(newcat)]

newreg<-region_ind$Region_names
newreg<-newreg[!is.na(newreg)]

nco<-length(unique(region_ind$Region_names))
ncn<-length(newreg)
nso<-length(unique(sector_ind$Sector_names))
nsn<-length(newcat)

nd<-length(demand_ind$Final_demand_names)




### 4 Cut down to the dimensions of interest ###################################
## Using Region and Sector aggregation created by MM

########## first require the index data
sector_ind <- read_excel(file.path(gloriawd,"GLORIA_ReadMe_057_adj.xlsx"), 
                         sheet = "Sectors")
region_ind <- read_excel(file.path(gloriawd,"GLORIA_ReadMe_057_adj.xlsx"),  
                         sheet = "Regions")

demand_ind <- read_excel(file.path(gloriawd,"GLORIA_ReadMe_057_adj.xlsx"),  
                         sheet = "Value added and final demand")

satellites_ind <- read_excel(file.path(gloriawd,"GLORIA_ReadMe_057_adj.xlsx"),
                         sheet = "Satellites")

newcat<-sector_ind$MM_sector_name
newcat<-newcat[!is.na(newcat)]

newreg<-region_ind$MM_region_name
newreg<-newreg[!is.na(newreg)]

nco<-length(unique(region_ind$Region_names))
ncn<-length(newreg)
nso<-length(unique(sector_ind$Sector_names))
nsn<-length(newcat)

nd<-length(demand_ind$Final_demand_names)


## MM to continue


#############################################################################


