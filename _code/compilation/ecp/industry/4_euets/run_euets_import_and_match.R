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
         verified,verifiedCummulative,surrendered,surrenderedCummulative,
         registry_id,nace15_id,nace20_id,nace_id)

# how many installations?
length(unique(adf$installation_id))

# how many verified emissions in 2019
sum(adf$verified[adf$year==2019],na.rm=T)
# how many allocated free permits in 2019
sum(adf$allocatedFree[adf$year==2019],na.rm=T)
# how many allocated total permits in 2019
sum(adf$allocatedTotal[adf$year==2019],na.rm=T)
# how many surrendered permits in 2019
sum(adf$surrendered[adf$year==2019],na.rm=T)
# how many surrenderedCummulative permits in 2019
sum(adf$surrenderedCummulative[adf$year==2019],na.rm=T)
# how many verifiedCummulative permits in 2019
sum(adf$verifiedCummulative[adf$year==2019],na.rm=T)


# check unique years and industries
unique(adf$year)
unique(adf$nace15_id)
unique(adf$nace20_id)
unique(adf$nace_id)

# keep full version
adff <- adf

# take a look at which ones are NA.
dft<-adf %>% filter(is.na(nace_id))
unique(dft$installation_id)
# quite a few!
# how many?
n.instal.nid.nace<-length(unique(dft$installation_id))
rm(dft)

# we have got NA's here. Remove those cases. Undefined installations.
adf <- adf %>% filter(!is.na(nace_id))
unique(adf$nace15_id)
unique(adf$nace20_id)
unique(adf$nace_id) 
# no NAs in nace_id, so use that one.
length(unique(adf$installation_id))

# any installations that are only part of years after 2023?
dft<-adf %>% filter(year>2023)
setdiff(dft$installation_id,adf$installation_id)
# no, they are all the same.
rm(dft)

# remove years after 2024
adf <- adf %>% filter(year %in% seq(2005,2024))

summary(adf$allocatedFree)
summary(adf$allocatedTotal)
summary(adf$allocated10c)
summary(adf$verified)
summary(adf$surrendered)
# we have quite a few NAs here. Let's test the cases

# allocatedTotal is never NA. So that's already good.
dft <- adf %>% filter(is.na(allocatedFree))
length(unique(dft$installation_id))
unique(dft$nace_id)
summary(dft$allocatedTotal)
# ok I see! All of these have zero allocated total
summary(dft$verified)
summary(dft$surrendered)
hist(dft$year)
rm(dft)

# ok so let's remove the rows with NA under allocatedFree
adf <- adf %>% filter(!is.na(allocatedFree))
length(unique(adf$installation_id))
# so now we have 15,548 installations in the dataset. This means that we have filtered out some years for some installations.
hist(adf$year)

# now let's check the allocated10c one
dft <- adf %>% filter(!is.na(allocated10c))
unique(dft$nace_id)
# mostly electricity and air transport, and then a few weird cases in Poland and Bulgaria.
# we add those to the free allocation
rm(dft)
# turn inapplicable cases to zero
adf$allocated10c[is.na(adf$allocated10c)]<-0
adf['allocatedFreeM']<-adf$allocatedFree+adf$allocated10c

# let's check the verified 
dft <- adf %>% filter(is.na(verified))
hist(dft$year)
# ok so most of those cases are of course in 2024, but some are also earlier.
summary(dft$allocatedFree) # most (but not all) of these have zero allocated free
summary(dft$allocatedTotal) # most (but not all) have zero allocated total
unique(dft$nace_id) # all industries are represented
length(unique(dft$installation_id[dft$year==2024]))
rm(dft)

# remove cases with NA in verified
adf <- adf %>% filter(!is.na(verified))
length(unique(adf$installation_id))

# now let's check surrendered
summary(adf$surrendered)
dft <- adf %>% filter(is.na(surrendered))
hist(dft$year)
summary(dft$allocatedFree)
summary(dft$allocatedTotal)
summary(dft$verified)
summary(dft$allocatedTotal-dft$allocatedFree)
length(unique(dft$installation_id))

# remove cases with NA in surrendered
adf <- adf %>% filter(!is.na(surrendered))
length(unique(adf$installation_id))
unique(adf$nace_id)

# so now in this version we do not summarise.
unique(adf$nace_id) %>% sort()
rm(fpa,cdf,idf,ndf)


################################################################################
#### import concordance between nace and isic
inc<-read.delim(url("https://unstats.un.org/unsd/classifications/Econ/tables/ISIC/NACE2_ISIC4/NACE2_ISIC4.txt"),sep=',')
inc['NACE2code_n']<-as.numeric(inc$NACE2code)

# remove those with NA
inc <- inc %>% filter(!is.na(NACE2code_n))

## keep only the most general level (where we have duplicates like 7.1 and 7.10)
inc['unq']<-NA
for(i in 1:nrow(inc)){
  if(inc %>% filter(NACE2code_n==inc$NACE2code_n[i]) %>% nrow() == 1){
    inc$unq[i]<-"yes"
  } else {
    inc$unq[i]<-"no"
  }
}

# first remove the duplicates at the highest level
inc['keeps']<-NA
for(i in 1:nrow(inc)){
  if(inc$unq[i]=="no" & nchar(inc$NACE2code[i])==5){
    inc$keeps[i] <- "remove"
  }
}

inc <- inc %>% filter(is.na(keeps))

# then check the next
inc['unq']<-NA
for(i in 1:nrow(inc)){
  if(inc %>% filter(NACE2code_n==inc$NACE2code_n[i]) %>% nrow() == 1){
    inc$unq[i]<-"yes"
  } else {
    inc$unq[i]<-"no"
  }
}

inc['keeps']<-NA
for(i in 1:nrow(inc)){
  if(inc$unq[i]=="no" & nchar(inc$NACE2code[i])==4){
    inc$keeps[i] <- "remove"
  }
}

inc <- inc %>% filter(is.na(keeps))

# very good, now there shouldn't be any duplicates anymore
inc <- inc %>% select(-c(unq,keeps))
length(unique(inc$NACE2code_n))
# confirmed

unique(adf$nace_id)
unique(inc$NACE2code_n)
## find ISIC code for each installation
adf<-merge(adf,inc,by.x="nace_id",by.y="NACE2code_n",all.x=T)
unique(adf$ISIC4code)
adff<-merge(adff,inc,by.x="nace_id",by.y="NACE2code_n",all.x=T)
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

adff['gloria_sector']<-NA
for(i in 1:nrow(adff)){
  adff$gloria_sector[i]<-paste(which(sapply(gl, FUN=function(X) adff$ISIC4code[i] %in% X)),collapse="_")
}


unique(adf$gloria_sector)
unique(adff$gloria_sector)


# add the correct country names (corresponding to GLORIA)
countryconc<-data.frame(matrix(nrow=length(unique(adf$registry_id)),ncol=2))
colnames(countryconc)<-c("eu2dig","country")
countryconc$eu2dig<-unique(adf$registry_id)
countryconc$country[countryconc$eu2dig=="AT"]<-"Austria"
countryconc$country[countryconc$eu2dig=="BE"]<-"Belgium"
countryconc$country[countryconc$eu2dig=="BG"]<-"Bulgaria"
countryconc$country[countryconc$eu2dig=="CY"]<-"Cyprus"
countryconc$country[countryconc$eu2dig=="CZ"]<-"CSSR/Czech Republic (1990/1991)"
countryconc$country[countryconc$eu2dig=="DE"]<-"Germany"
countryconc$country[countryconc$eu2dig=="DK"]<-"Denmark"
countryconc$country[countryconc$eu2dig=="EE"]<-"Estonia"
countryconc$country[countryconc$eu2dig=="ES"]<-"Spain"
countryconc$country[countryconc$eu2dig=="FI"]<-"Finland"
countryconc$country[countryconc$eu2dig=="FR"]<-"France"
countryconc$country[countryconc$eu2dig=="GB"]<-"United Kingdom"
countryconc$country[countryconc$eu2dig=="GR"]<-"Greece"
countryconc$country[countryconc$eu2dig=="HR"]<-"Croatia"
countryconc$country[countryconc$eu2dig=="HU"]<-"Hungary"
countryconc$country[countryconc$eu2dig=="IE"]<-"Ireland"
countryconc$country[countryconc$eu2dig=="IS"]<-"Iceland"
countryconc$country[countryconc$eu2dig=="IT"]<-"Italy"
countryconc$country[countryconc$eu2dig=="LI"]<-"Liechtenstein"
countryconc$country[countryconc$eu2dig=="LT"]<-"Lithuania"
countryconc$country[countryconc$eu2dig=="LU"]<-"Luxembourg"
countryconc$country[countryconc$eu2dig=="LV"]<-"Latvia"
countryconc$country[countryconc$eu2dig=="MT"]<-"Malta"
countryconc$country[countryconc$eu2dig=="NL"]<-"Netherlands"
countryconc$country[countryconc$eu2dig=="NO"]<-"Norway"
countryconc$country[countryconc$eu2dig=="PL"]<-"Poland"
countryconc$country[countryconc$eu2dig=="PT"]<-"Portugal"
countryconc$country[countryconc$eu2dig=="RO"]<-"Romania"
countryconc$country[countryconc$eu2dig=="SE"]<-"Sweden"
countryconc$country[countryconc$eu2dig=="SI"]<-"Slovenia"
countryconc$country[countryconc$eu2dig=="SK"]<-"Slovakia"
countryconc$country[countryconc$eu2dig=="XI"]<-"United Kingdom"


# add to dataframe
adf<-merge(adf,countryconc,by.x="registry_id",by.y="eu2dig")
adff<-merge(adff,countryconc,by.x="registry_id",by.y="eu2dig")

#### DO NOT AGGREGATE
# # now summarise the data by year, gloria sector and gloria country
# adf <- adf %>% group_by(year,country,gloria_sector) %>%
#   summarise(allocatedFree = sum(allocatedFree,na.rm=T),
#             allocatedTotal = sum(allocatedTotal,na.rm=T),
#             allocated10c = sum(allocated10c,na.rm=T),
#             verified = sum(verified,na.rm=T),
#             surrendered = sum(surrendered,na.rm=T))

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

adff['gloria_sector_name']<-NA
for(i in 1:nrow(adff)){
  if(isTRUE(grepl("_",adff$gloria_sector[i]))){
    adff$gloria_sector_name[i]<-"Aggregate (see variable gloria_sector)"
  }else{
    adff$gloria_sector_name[i]<-sq[as.numeric(adff$gloria_sector[i])]
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


# then the same for the unfiltered version

sort(unique(adff$gloria_sector))
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
          "78_79_80_81_82_83_84",
          "85","86","87","88","89","90","91","92","93",
          "93_94",
          "94","95","96","97","98","98_99","99",
          "100",
          "102","103","104","105","106","107","108","109","110","111","112","113","114","115","116","117","118",""
)

# impose this order 
adff<-adff %>% mutate(gloria_sector = factor(gloria_sector,levels=avlbls))

# now order the rows according to year, country, and gloria sector
adff<-adff %>% arrange(year,country,gloria_sector) %>% relocate(gloria_sector_name, .after=gloria_sector)

################################################################################
### Now defined the aggregations of interest

gcc<-data.frame(rbind(c("1_2_3_4"             ,"10|AFF"                ,"A|10|Agricult|GLORIA_1:4,6:7,10:12,15,20"),
                      c("6_7"                 ,"10|AFF"                ,"A|10|Agricult|GLORIA_1:4,6:7,10:12,15,20"),
                      c("10"                  ,"10|AFF"                ,"A|10|Agricult|GLORIA_1:4,6:7,10:12,15,20"),
                      c("11"                  ,"10|AFF"                ,"A|10|Agricult|GLORIA_1:4,6:7,10:12,15,20"),
                      c("12"                  ,"10|AFF"                ,"A|10|Agricult|GLORIA_1:4,6:7,10:12,15,20"),
                      c("15"                  ,"10|AFF"                ,"A|10|Agricult|GLORIA_1:4,6:7,10:12,15,20"),
                      c("20"                  ,"10|AFF"                ,"A|10|Agricult|GLORIA_1:4,6:7,10:12,15,20"),
                      c("24"                  ,"12|FOS"                ,"B|30|Othmining|GLORIA_24:25,28:29,37:40"),
                      c("25"                  ,"12|FOS"                ,"B|30|Othmining|GLORIA_24:25,28:29,37:40"),
                      c("26"                  ,"12|FOS"                ,"B|10|Petrextract|GLORIA_26"),
                      c("27"                  ,"12|FOS"                ,"B|20|Gasextract|GLORIA_27"),
                      c("28"                  ,"11|MIN"                ,"B|30|Othmining|GLORIA_24:25,28:29,37:40"),
                      c("29"                  ,"11|MIN"                ,"B|30|Othmining|GLORIA_24:25,28:29,37:40"),
                      c("37"                  ,"11|MIN"                ,"B|30|Othmining|GLORIA_24:25,28:29,37:40"),
                      c("38"                  ,"11|MIN"                ,"B|30|Othmining|GLORIA_24:25,28:29,37:40"),
                      c("39"                  ,"11|MIN"                ,"B|30|Othmining|GLORIA_24:25,28:29,37:40"),
                      c("40"                  ,"11|MIN"                ,"B|30|Othmining|GLORIA_24:25,28:29,37:40"),
                      c("41_42_43_44_45"      ,"13|FOO"                ,"C|10||Meatprod|GLORIA_41:45"),
                      c("46"                  ,"13|FOO"                ,"C|17|Fishandtobac|GLORIA_46,56"),
                      c("47"                  ,"13|FOO"                ,"C|11|Cerealprod|GLORIA_47"),
                      c("48_49"               ,"13|FOO"                ,"C|12|Fruitveg|GLORIA_48:49"),
                      c("50"                  ,"13|FOO"                ,"C|13|Sugarotfoo|GLORIA_50:51"),
                      c("50_51"               ,"13|FOO"                ,"C|13|Sugarotfoo|GLORIA_50:51"),
                      c("51"                  ,"13|FOO"                ,"C|13|Sugarotfoo|GLORIA_50:51"),
                      c("52_53"               ,"13|FOO"                ,"C|14|Oilsandfats|GLORIA_52_53"),
                      c("54"                  ,"13|FOO"                ,"C|15|Dairyprod|GLORIA_54"),
                      c("55"                  ,"13|FOO"                ,"C|16|Beverage_GLORIA_55"),
                      c("56"                  ,"13|FOO"                ,"C|17|Fishandtobac|GLORIA_46,56"),
                      c("57"                  ,"25|OMF"                ,"C|18|Textilesal|GLORIA_57:58"),
                      c("58"                  ,"25|OMF"                ,"C|18|Textilesal|GLORIA_57:58"),
                      c("59"                  ,"25|OMF"                ,"C|19|Wood|GLORIA_59"),
                      c("60"                  ,"14|PAP"                ,"C|20|Paper|GLORIA_60"),
                      c("61"                  ,"25|OMF"                ,"C|41|Othermanuf|GLORIA_61,89:90,92"),
                      c("62"                  ,"12|FOS"                ,"C|21|Rfnpetrolcok|GLORIA_62:63"),
                      c("63"                  ,"12|FOS"                ,"C|21|Rfnpetrolcok|GLORIA_62:63"),
                      c("64"                  ,"15|FER"                ,"C|22|Nitrofert|GLORIA_64"),
                      c("65_70"               ,"18|FER_CHM"            ,"C|23|HLMixfertandc|GLORIA_65,70"),
                      c("66"                  ,"16|PRP"                ,"C|24|Bpetrochemp|GLORIA_66"),
                      c("66_67_68_70"         ,"19|PRP_CHI_CHO_OMF_CHM","C|25|HLChem|GLORIA_66:68,70"),
                      c("69"                  ,"25|OMF"                ,"C|26|Pharma|GLORIA_69"),
                      c("70"                  ,"17|CHM"                ,"C|27|Otherchem|GLORIA_70"),
                      c("71"                  ,"16|PRP"                ,"C|28|Rubber|GLORIA_71"),
                      c("72"                  ,"16|PRP"                ,"C|29|Plastic|GLORIA_72"),
                      c("73_74_75_76"         ,"20|CLY_GAC_CEM_OMF"    ,"C|30|HLNonmetmin|GLORIA_73:76"),
                      c("74"                  ,"21|GAC"                ,"C|31|Glasscer|GLORIA_74"),
                      c("75"                  ,"22|CEM"                ,"C|32|Cement|GLORIA_75"),
                      c("76"                  ,"25|OMF"                ,"C|33|Othernmmin|GLORIA_73:76"),
                      c("77"                  ,"23|IAS"                ,"C|34|Bironst|GLORIA_77"),
                      c("78_79_80_81_82_83_84","24|NFM"                ,"C|35|Bnonferrm|GLORIA_78:84"),
                      c("85"                  ,"25|OMF"                ,"C|36|Fabrmetp|GLORIA_85"),
                      c("86"                  ,"25|OMF"                ,"C|37|Machinery|GLORIA_86"),
                      c("87"                  ,"25|OMF"                ,"C|38|Motorvehic|GLORIA_87"),
                      c("88"                  ,"25|OMF"                ,"C|39|Othertpequip|GLORIA_88"),
                      c("89"                  ,"31|SER"                ,"C|41|Othermanuf|GLORIA_61,89:90,92"),
                      c("90"                  ,"25|OMF"                ,"C|41|Othermanuf|GLORIA_61,89:90,92"),
                      c("91"                  ,"25|OMF"                ,"C|40|Electequip|GLORIA_91"),
                      c("92"                  ,"25|OMF"                ,"C|41|Othermanuf|GLORIA_61,89:90,92"),
                      c("93"                  ,"26|ELE"                ,"D|10|Elepower|GLORIA_93"),
                      c("93_94"               ,"27|ELE_FOS"            ,"D|12|HLElepowerGassteamac|GLORIA_93:94"),
                      c("94"                  ,"12|FOS"                ,"D||11|Gassteamac|GLORIA_94"),
                      c("95"                  ,"28|WTR"                ,"E|10|Otherprov|GLORIA_95:97"),
                      c("96"                  ,"28|WTR"                ,"E|10|Otherprov|GLORIA_95:97"),
                      c("97"                  ,"28|WTR"                ,"E|10|Otherprov|GLORIA_95:97"),
                      c("98"                  ,"25|OMF"                ,"F|10|Construction|GLORIA_98:99"),
                      c("98_99"               ,"25|OMF"                ,"F|10|Construction|GLORIA_98:99"),
                      c("99"                  ,"25|OMF"                ,"F|10|Construction|GLORIA_98:99"),
                      c("100"                 ,"31|SER"                ,"GIJKLMNOPQ||Services|GLORIA_100,108:118"),
                      c("102"                 ,"30|OTP"                ,"H|12|Othertransp|GLORIA_102,106:107"),
                      c("103"                 ,"30|OTP"                ,"H|10|Pipetransp|GLORIA_103"),
                      c("105"                 ,"29|ATP"                ,"H|11|Airtransp|GLORIA_105"),
                      c("106"                 ,"30|OTP"                ,"H|12|Othertransp|GLORIA_102,106:107"),
                      c("107"                 ,"30|OTP"                ,"H|12|Othertransp|GLORIA_102,106:107"),
                      c("108"                 ,"31|SER"                ,"GIJKLMNOPQ|Services|GLORIA_100,108:118"),
                      c("109"                 ,"31|SER"                ,"GIJKLMNOPQ|Services|GLORIA_100,108:118"),
                      c("110"                 ,"31|SER"                ,"GIJKLMNOPQ|Services|GLORIA_100,108:118"),
                      c("111"                 ,"31|SER"                ,"GIJKLMNOPQ|Services|GLORIA_100,108:118"),
                      c("112"                 ,"31|SER"                ,"GIJKLMNOPQ|Services|GLORIA_100,108:118"),
                      c("113"                 ,"31|SER"                ,"GIJKLMNOPQ|Services|GLORIA_100,108:118"),
                      c("114"                 ,"31|SER"                ,"GIJKLMNOPQ|Services|GLORIA_100,108:118"),
                      c("115"                 ,"31|SER"                ,"GIJKLMNOPQ|Services|GLORIA_100,108:118"),
                      c("116"                 ,"31|SER"                ,"GIJKLMNOPQ|Services|GLORIA_100,108:118"),
                      c("117"                 ,"31|SER"                ,"GIJKLMNOPQ|Services|GLORIA_100,108:118"),
                      c("118"                 ,"31|SER"                ,"GIJKLMNOPQ|Services|GLORIA_100,108:118"),
                      c(""                    ,"udf"                   ,"Undefined")
                      )
                ) 

colnames(gcc)<-c("g_id","cge_id","maxres_id")

### then add these to adf and adff
adf<-adf %>% left_join(gcc,by = join_by(gloria_sector == g_id))
adff<-adff %>% left_join(gcc,by = join_by(gloria_sector == g_id))

################################################################################
#### then calculate the indicators

########### now the alternative summary, using weighted means and medians

# new variable paid share of permits
adf <- adf %>%
  mutate(paidShare = (verified - allocatedFreeM)/ verified)

summary(adf$paidShare)
# coercing values below 0 to zero (only matters for mean, not median)
adf['paidShare_a']<-adf$paidShare
adf$paidShare_a[adf$paidShare_a<0]<-0

summary(adf$paidShare_a)

# there are some NAs. These happen when there is zero verified emissions. 
# let's remove those cases
adf <- adf %>% filter(verified>0)

summary(adf$paidShare_a)
# ok very good.

# add a preliminary OBA proxy
adf['oba_proxy']<-1-adf$paidShare_a


################################################################################
#### then summarise


# highest possible resolution (so that n>5 in each year-sector)
adfsh <- adf %>% group_by(year,maxres_id) %>%
  summarise(paidShare_a_md = median(paidShare_a),
            paidShare_a_um = mean(paidShare_a),
            paidShare_a_wm = weighted.mean(paidShare_a,verified),
            oba_proxy_wm = weighted.mean(oba_proxy,verified),
            sum_verified = sum(verified),
            sum_allocatedFreeM = sum(allocatedFreeM),
            sum_allocatedTotal = sum(allocatedTotal),
            sum_surrendered = sum(surrendered),
            n_installations = n())

# cge resolution
adfsc <- adf %>% group_by(year,cge_id) %>%
  summarise(paidShare_a_md = median(paidShare_a),
            paidShare_a_um = mean(paidShare_a),
            paidShare_a_wm = weighted.mean(paidShare_a,verified),
            oba_proxy_wm = weighted.mean(oba_proxy,verified),
            sum_verified = sum(verified),
            sum_allocatedFreeM = sum(allocatedFreeM),
            sum_allocatedTotal = sum(allocatedTotal),
            sum_surrendered = sum(surrendered),
            n_installations = n())

################################################################################
#### then plot
library(ggplot2)


# panel plot


# first maxres
gg<-ggplot(adfsh,
           aes(x=year,y=1-paidShare_a_wm)) + 
  geom_line() + 
  labs(y="OBA Proxy") +
  facet_wrap(vars(maxres_id))

gg

ggsave(gg,filename=paste0("euetsalloc_obaproxy_maxres",".svg"),
       device="svg",
       height=10,
       width=20,
       path=wd)

# then cgeres
gg<-ggplot(adfsc,
           aes(x=year,y=1-paidShare_a_wm)) + 
  geom_line() + 
  labs(y="OBA Proxy") +
  facet_wrap(vars(cge_id))

gg

ggsave(gg,filename=paste0("euetsalloc_obaproxy_cgeres",".svg"),
       device="svg",
       height=10,
       width=20,
       path=wd)


################################################################################
# then save
fpr<-file.path(here::here(),"_dataset","ecp","industry","ecp_gloria_sectors","euets_permits")

write.csv(adf,file.path(fpr,"euetspermits_gloria.csv"),row.names=F)
write.csv(adff,file.path(fpr,"euetspermits_gloria_unfiltered.csv"),row.names=F)
write.csv(adfsc,file.path(fpr,"euetspermits_gloria_summary_cgeres.csv"),row.names=F)
write.csv(adfsc,file.path(fpr,"euetspermits_gloria_summary_maxres.csv"),row.names=F)

# tidy up
rm(list = ls())
