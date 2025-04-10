################################################################################
### script to import Abrell's data from euets.info on permit allocation
### and map it onto GLORIA
################################################################################

################################################################################
### file.path setup and packages ###############################################
wd<-file.path(here::here(),"_code","compilation","ecp","industry","4_euets")
setwd(wd)
library(here)
library(readxl)
library(dplyr)

################################################################################
### Import GLORIA index data

gversion<-"059"
fpe<-file.path("C:", "Users", "jomerkle", 
               "OneDrive - Norwegian University of Life Sciences",
               "data",
               "GLORIA",
               gversion,
               "Gloria_satellites_20240725")

# this just to create a vector of index numbers for those rows and columns we want to keep
# we want to keep only MRIO data, so remove the supply matrices within

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

# read data
sector_ind <- read_excel(file.path(fpe,"..",paste0("GLORIA_ReadMe_",gversion,".xlsx")),sheet = "Sectors")
region_ind <- read_excel(file.path(fpe,"..",paste0("GLORIA_ReadMe_",gversion,".xlsx")),sheet = "Regions")
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

# store and tidy up
fcq<-sequential_ind$fcq
fsq<-sequential_ind$fsq
rm(fcql,region_ind,sector_ind,sequential_ind,all_c_s,cq,cselector,fpe,i,rselector,short_c_s)


################################################################################
### import eu ets permit data (downloaded from euets.info)
fpa<-file.path("C:", "Users", "jomerkle", 
               "OneDrive - Norwegian University of Life Sciences",
               "data",
               "Abrell",
               "may_2024")

idf<-read.csv(file.path(fpa,"installation.csv"))
cdf<-read.csv(file.path(fpa,"compliance.csv"))
ndf<-read.csv(file.path(fpa,"nace_code.csv"))

# each allowance represents 1 t of ghg emissions
# surrendering an allowance means that you "use" the allowance.

# join together and keep only what we need
adf<-merge(cdf,idf,by.x="installation_id",by.y="id") %>% 
  select(installation_id,year,allocatedFree,allocatedTotal,allocated10c,
         verified,surrendered,surrenderedCummulative,
         registry_id,nace15_id,nace20_id,nace_id)

unique(adf$year)
unique(adf$nace15_id)
unique(adf$nace20_id)
unique(adf$nace_id)

# we have got NA's here. Remove those cases. Undefined installations.
adf <- adf %>% filter(!is.na(nace_id))
unique(adf$nace15_id)
unique(adf$nace20_id)
unique(adf$nace_id) 
# no NAs in nace_id, so use that one.

# remove years after 2023
adf <- adf %>% filter(year %in% seq(2005,2023))

summary(adf$allocatedFree)
summary(adf$allocatedTotal)
summary(adf$allocated10c)
summary(adf$verified)
summary(adf$surrendered)
# we have quite a few NAs here. Will treat those as zero.

# summarise for each nace sector, year and country (treating all NAs as zeros)
adf<-adf %>% group_by(year,registry_id,nace_id) %>%
  summarise(allocatedFree = sum(allocatedFree, na.rm=T),
            allocatedTotal = sum(allocatedTotal, na.rm=T),
            allocated10c = sum(allocated10c, na.rm=T),
            verified = sum(verified, na.rm=T),
            surrendered = sum(surrendered, na.rm=T))

unique(adf$nace_id) %>% sort()

rm(fpa,cdf,idf,ndf)


################################################################################
#### import concordance between nace and isic
inc<-read.delim(url("https://unstats.un.org/unsd/classifications/Econ/tables/ISIC/NACE2_ISIC4/NACE2_ISIC4.txt"),sep=',')
inc['NACE2code_n']<-as.numeric(inc$NACE2code)

## find ISIC code for each installation
adf<-merge(adf,inc,by.x="nace_id",by.y="NACE2code_n")

# check which ISIC codes we have
unique(adf$ISIC4code)

# tidy up
rm(inc)

################################################################################
#### read in GLORIA-ISIC concordance (this one was made by MM - a few hours of 
# working through ISIC rev.4 classification 
# using this resource: https://unstats.un.org/unsd/classifications/Econ/search)
gisic<-read_excel("GLORIA_ISICr4.xlsx",sheet = "Sectors")

# paste all classes, group and divisions in one column
gisic['all']<-NA
for(i in 1:nrow(gisic)){
  gisic$all[i]<-paste(gisic$ISIC_classes[i],gisic$ISIC_group[i],gisic$ISIC_division[i],sep=";")
}
gisic$all<-gsub(" ","",gisic$all)

# put it into a list (for easier looping)
gl<-list()
for(i in 1:nrow(gisic)){
  gl[[i]]<-strsplit(gisic$all[i],split=";")
  gl[[i]]<-unlist(gl[[i]])
}
names(gl)<-gisic$Sector_names
# now we have a vector of ISIC codes for each GLORIA sector.

# tidy up
rm(gisic,i)

################################################################################
### matching

# now loop across the permit dataframe and find gloria sector for each
# this is the main operation
adf['gloria_sector']<-NA
for(i in 1:nrow(adf)){
  adf$gloria_sector[i]<-paste(which(sapply(gl, FUN=function(X) adf$ISIC4code[i] %in% X)),collapse="_")
}


unique(adf$gloria_sector)

# add the correct country names (corresponding to GLORIA)
countryconc<-data.frame(matrix(nrow=length(unique(adf$registry_id)),ncol=2))
colnames(countryconc)<-c("eu2dig","country")
countryconc$eu2dig<-unique(adf$registry_id)
countryconc$country[1]<-"Austria"
countryconc$country[2]<-"Belgium"
countryconc$country[3]<-"Bulgaria"
countryconc$country[4]<-"Cyprus"
countryconc$country[5]<-"CSSR/Czech Republic (1990/1991)"
countryconc$country[6]<-"Germany"
countryconc$country[7]<-"Denmark"
countryconc$country[8]<-"Estonia"
countryconc$country[9]<-"Spain"
countryconc$country[10]<-"Finland"
countryconc$country[11]<-"France"
countryconc$country[12]<-"United Kingdom"
countryconc$country[13]<-"Greece"
countryconc$country[14]<-"Croatia"
countryconc$country[15]<-"Hungary"
countryconc$country[16]<-"Ireland"
countryconc$country[17]<-"Iceland"
countryconc$country[18]<-"Italy"
countryconc$country[19]<-"Liechtenstein"
countryconc$country[20]<-"Lithuania"
countryconc$country[21]<-"Luxembourg"
countryconc$country[22]<-"Latvia"
countryconc$country[23]<-"Malta"
countryconc$country[24]<-"Netherlands"
countryconc$country[25]<-"Norway"
countryconc$country[26]<-"Poland"
countryconc$country[27]<-"Portugal"
countryconc$country[28]<-"Romania"
countryconc$country[29]<-"Sweden"
countryconc$country[30]<-"Slovenia"
countryconc$country[31]<-"Slovakia"
countryconc$country[32]<-"United Kingdom"

# add to dataframe
adf<-merge(adf,countryconc,by.x="registry_id",by.y="eu2dig")


# now summarise the data by year, gloria sector and gloria country
adf <- adf %>% group_by(year,country,gloria_sector) %>%
  summarise(allocatedFree = sum(allocatedFree,na.rm=T),
            allocatedTotal = sum(allocatedTotal,na.rm=T),
            allocated10c = sum(allocated10c,na.rm=T),
            verified = sum(verified,na.rm=T),
            surrendered = sum(surrendered,na.rm=T))

#tidy up
rm(countryconc,gl)

################################################################################
#### format and save

# get GLORIA sector names for each row
# note: sector aggregates happen when a NACE sector cannot be uniquely allocated to
# a single GLORIA sector. Open the file GLORIA_ISICrf.xlsx to see where this comes from.

# add gloria names
sq<-unique(fsq)
adf['gloria_sector_name']<-NA
for(i in 1:nrow(adf)){
  if(isTRUE(grepl("_",adf$gloria_sector[i]))){
    adf$gloria_sector_name[i]<-"Aggregate (see variable gloria_sector)"
  }else{
    adf$gloria_sector_name[i]<-sq[as.numeric(adf$gloria_sector[i])]
  }
}

### define a useful order of sectors and sector aggregates
sort(unique(adf$gloria_sector))
avlbls<-c("1_2_3_4",
          "6_7",
          "10","11","12",
          "15",
          "20",
          "24","25","26","27","28","29",
          "37","38","39","40",
          "41_42_43_44_45",
          "46","47",
          "48_49",
          "50",
          "50_51",
          "51",
          "52_53",
          "54","55","56","57","58","59","60","61","62","63","64",
          "65_70",
          "66",
          "66_67_68_70",
          "69","70","71","72","73",
          "73_74_75_76",
          "74",
          "74_76",
          "75","76","77",
          "77_78_79_80_81_82_83_84",
          "78_79_80_81_82_83_84",
          "85","86","87","88","89","90","91","92","93",
          "93_94",
          "94","95","96","97","98","98_99","99",
          "100",
          "102","103","104","105","106","107","108","109","110","111","112","113","114","115","116","117","118"
          )

# impose this order 
adf<-adf %>% mutate(gloria_sector = factor(gloria_sector,levels=avlbls))

# now order the rows according to year, country, and gloria sector
adf<-adf %>% arrange(year,country,gloria_sector) %>% relocate(gloria_sector_name, .after=gloria_sector)

# ca y est

# then save
fpr<-file.path(here::here(),"_dataset","ecp","industry","ecp_gloria_sectors","euets_permits")

write.csv(adf,file.path(fpr,"euetspermits_gloria.csv"),row.names=F)

# tidy up
rm(list = ls())
