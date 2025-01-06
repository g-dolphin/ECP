################################################################################
####### Script to Check ECP Price Allocations ##################################
################################################################################


################################################################################
### Setup
wd<-file.path(here::here(),"_code","compilation","ecp","industry")
setwd(wd)


################################################################################
### Import data
# select version
gversion<-"059"
tmpmat=T

gloriawd<-file.path(wd,"1_import","gloria")
if(gversion=="059"){
  if(isTRUE(tmpmat)){
    source(file.path(gloriawd,"run_imports_v59_mat.R"))
  } else {
    source(file.path(gloriawd,"run_imports_v59.R"))
  }
} else if(gversion=="057"){
  source(file.path(gloriawd,"run_imports_v57.R"))
}

# select price level
pl<-"cons_p"
ecpwd<-file.path(wd,"1_import","ecp")
source(file.path(ecpwd,"import_ecp.R"))


################################################################################
### Prepare matching

ecpmwd<-file.path(wd,"2_match")

# Packages
library(dplyr)
library(tidyr)
#library(stringr)
#library(readxl)

dir.create(file.path(ecpmwd, "tmpdir"))

# Define filepaths
fpe<-file.path(wd,"1_import","ecp","tmpdir")
fpg<-file.path(wd,"1_import","gloria","tmpdir")
resultfp<-file.path(ecpmwd,"tmpdir")

# Main function
source(file.path(ecpmwd,"matching_function.R"))

# ECP and sector concordance data
ecp<-read.csv(file.path(fpe,"ecp_ipcc_CO2.csv"))
if(pl=="cons_p"){
  ecp<-ecp %>% rename(ecp_all_usd = ecp_all_usd_k)
} else{}

load(file.path(ecpmwd,"ipcc_conc",paste0("ipcc_conc_",gversion,".RData")))

# define years to run the process for
yrs<-seq(1990,2022)


################################################################################
#### Concordance between country names #########################################

# align country names
load(file.path(wd,"1_import","gloria","tmpdir",paste0("gloria_",yrs[1],".RData")))
rm(demand_ind,satellites_ind,sector_ind,sequential_ind,tqm,yqm)

region_ind$Region_names
unique(ecp$jurisdiction)

countryconc<-as.data.frame(matrix(ncol=2,nrow=length(unique(ecp$jurisdiction))))
colnames(countryconc)<-c("c_ecp","c_gloria")
countryconc$c_ecp<-unique(ecp$jurisdiction)

# to start with
for(i in 1:nrow(countryconc)){
  #
  cg<-region_ind$Region_names[substr(region_ind$Region_names,1,5)==substr(countryconc$c_ecp[i],1,5)]
  #
  if(length(cg)==0){
    countryconc$c_gloria[i]<-NA
  } else{
    countryconc$c_gloria[i]<-cg
  }
  #
}
rm(cg)

# then we fill the gaps manually
countryconc$c_gloria[countryconc$c_ecp=="Andorra"]<-"Rest of Europe"
countryconc$c_gloria[countryconc$c_ecp=="Antigua and Barbuda"]<-"Rest of Americas"
countryconc$c_gloria[countryconc$c_ecp=="Austria"]<-"Austria"
countryconc$c_gloria[countryconc$c_ecp=="Barbados"]<-"Rest of Americas"
countryconc$c_gloria[countryconc$c_ecp=="Cabo Verde"]<-"Rest of Africa"
countryconc$c_gloria[countryconc$c_ecp=="Comoros"]<-"Rest of Africa"
countryconc$c_gloria[countryconc$c_ecp=="Congo, Dem. Rep."]<-"DR Congo"
countryconc$c_gloria[countryconc$c_ecp=="Congo, Rep."]<-"Rep Congo"
countryconc$c_gloria[countryconc$c_ecp=="Czech Republic"]<-"CSSR/Czech Republic (1990/1991)"
countryconc$c_gloria[countryconc$c_ecp=="Dominica"]<-"Rest of Americas"
countryconc$c_gloria[countryconc$c_ecp=="Federated States of Micronesia"]<-"Rest of Asia_Pacific"
countryconc$c_gloria[countryconc$c_ecp=="Fiji"]<-"Rest of Asia_Pacific"
countryconc$c_gloria[countryconc$c_ecp=="Grenada"]<-"Rest of Americas"
countryconc$c_gloria[countryconc$c_ecp=="Guyana"]<-"Rest of Americas"
countryconc$c_gloria[countryconc$c_ecp=="Iran, Islamic Rep."]<-"Iran"
countryconc$c_gloria[countryconc$c_ecp=="Kiribati"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="Korea, Dem. Rep."]<-"North Korea"
countryconc$c_gloria[countryconc$c_ecp=="Korea, Rep."]<-"South Korea"
countryconc$c_gloria[countryconc$c_ecp=="Kosovo"]<-"Rest of Europe"
countryconc$c_gloria[countryconc$c_ecp=="Lao PDR"]<-"Laos"
countryconc$c_gloria[countryconc$c_ecp=="Lesotho"]<-"Rest of Africa"
countryconc$c_gloria[countryconc$c_ecp=="Liechtenstein"]<-"Rest of Europe"
countryconc$c_gloria[countryconc$c_ecp=="Macao SAR, China"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="Maldives"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="Marshall Islands"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="Mauritius"]<-"Rest of Africa"
countryconc$c_gloria[countryconc$c_ecp=="Monaco"]<-"Rest of Europe"
countryconc$c_gloria[countryconc$c_ecp=="Montenegro"]<-"Rest of Europe"
countryconc$c_gloria[countryconc$c_ecp=="Nauru"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="Nigeria"]<-"Nigeria"
countryconc$c_gloria[countryconc$c_ecp=="North Macedonia"]<-"Macedonia"
countryconc$c_gloria[countryconc$c_ecp=="Palau"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="Puerto Rico"]<-"Rest of Americas"
countryconc$c_gloria[countryconc$c_ecp=="Russian Federation"]<-"USSR/Russian Federation (1990/1991)"
countryconc$c_gloria[countryconc$c_ecp=="Samoa"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="San Marino"]<-"Rest of Europe"
countryconc$c_gloria[countryconc$c_ecp=="Sao Tome and Principe"]<-"Rest of Africa"
countryconc$c_gloria[countryconc$c_ecp=="Serbia"]<-"Yugoslavia/Serbia (1991/1992)"
countryconc$c_gloria[countryconc$c_ecp=="Seychelles"]<-"Rest of Africa"
countryconc$c_gloria[countryconc$c_ecp=="Solomon Islands"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="South Africa"]<-"South Africa"
countryconc$c_gloria[countryconc$c_ecp=="South Sudan"]<-"South Sudan"
countryconc$c_gloria[countryconc$c_ecp=="St. Kitts and Nevis"]<-"Rest of Americas"
countryconc$c_gloria[countryconc$c_ecp=="St. Lucia"]<-"Rest of Americas"
countryconc$c_gloria[countryconc$c_ecp=="St. Vincent and the Grenadines"]<-"Rest of Americas"
countryconc$c_gloria[countryconc$c_ecp=="Suriname"]<-"Rest of Americas"
countryconc$c_gloria[countryconc$c_ecp=="Swaziland"]<-"Rest of Africa"
countryconc$c_gloria[countryconc$c_ecp=="Taiwan, China"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="Timor-Leste"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="Tonga"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="Trinidad and Tobago"]<-"Rest of Americas"
countryconc$c_gloria[countryconc$c_ecp=="Tuvalu"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="United Kingdom"]<-"United Kingdom"
countryconc$c_gloria[countryconc$c_ecp=="United States"]<-"United States of America"
countryconc$c_gloria[countryconc$c_ecp=="Vanuatu"]<-"Rest of Asia-Pacific"
countryconc$c_gloria[countryconc$c_ecp=="Vatican City"]<-"Rest of Europe"
countryconc$c_gloria[countryconc$c_ecp=="Vietnam"]<-"Viet Nam"
countryconc$c_gloria[countryconc$c_ecp=="West Bank and Gaza"]<-"Palestine"
countryconc$c_gloria[countryconc$c_ecp=="Western Sahara"]<-"Rest of Africa"
countryconc<-rbind(countryconc,c("Yemen, Rep.","DR Yemen (Aden)"))


rm(region_ind)

################################################################################
### import gloria data
l_tqm<-list()
l_yqm<-list()


for(k in 1:length(yrs)){
  # 1. import
  load(file.path(fpg,paste0("gloria_",yrs[k],".RData")))
  # 2. tmpsave
  l_tqm[[k]]<-tqm
  l_yqm[[k]]<-yqm
  # 3. rm
  rm(yqm,tqm,demand_ind,region_ind,satellites_ind,sector_ind,sequential_ind,sequentiald_ind)
}

load(file.path(fpg,paste0("gloria_",yrs[1],".RData")))
rm(tqm,yqm)


################################################################################
### Define year and countrysector to check

### year

## define here
w<-which(yrs==2021)

yr=yrs[w]
yqm=l_yqm[[w]]
tqm=l_tqm[[w]]
demand_ind=demand_ind
region_ind=region_ind
satellites_ind=satellites_ind
sector_ind=sector_ind
sequential_ind=sequential_ind
sequentiald_ind=sequentiald_ind

### countrysector

nr<-nrow(tqm)+1
zq<-rbind(tqm,NA,NA)
fcq<-sequential_ind$fcq
fsq<-sequential_ind$fsq

# define here
r<-intersect(which(fcq=="Sweden"),which(fsq=="Nitrogenous fertilizers"))

tmpc<-fcq[r] # the country
tmps<-fsq[r] # the sector


################################################################################
### Run Process

yr = yr
indx=r
ecp_jur = countryconc$c_ecp[countryconc$c_gloria==tmpc]
sattype = "EDGAR"
ctry = tmpc
sect = tmps
ecp_data = ecp
gloria_q_data = zq
concordance = conclist[[tmps]]
type = "z"
sector_ind = sector_ind
demand_ind = demand_ind


### Step 1: Create calculation dataframe
df<-as.data.frame(matrix(NA,nrow=nrow(concordance),ncol=2))
colnames(df)<-c("Sat_ind","cp")
df$Sat_ind<-concordance$Sat_ind
# the below is to make the function work for both industry satellites z 
# and demand satellites y
if(type=="z"){
  sectorf<-sequential_ind$Sequential_regionSector_labels[sequential_ind$fcq==ctry & sequential_ind$fsq==sect]
} else if(type=="y"){
  sectorf=sequentiald_ind$Sequential_finalDemand_labels[sequentiald_ind$fcqd==ctry & sequentiald_ind$demandind==sect]
}

### Step 2: Extract ecp data
# Two cases
if(length(ecp_jur)==1){ # if there is only country
  de<-ecp_data %>% filter(jurisdiction == ecp_jur, year==yr)
  de$jurisdiction <- ctry
} else { # if there are several then we need to aggregate
  de<- ecp_data %>% 
    filter (jurisdiction %in% ecp_jur,year==yr) %>%
    mutate (ecp_co2 = `CO2`*`ecp_all_usd`) %>%
    group_by(ipcc_code) %>%
    summarise(`CO2`=sum(`CO2`),`ecp_co2`=sum(ecp_co2)) %>%
    mutate(ecp_all_usd = ecp_co2/`CO2`)
  de$ecp_all_usd[is.na(de$ecp_all_usd)]<-0
  de['jurisdiction']<-ctry
}

### Step 3: Extract gloria satellites data
# sattype rows, countrysector column
if(type=="z"){
  zqs<-gloria_q_data[which(grepl(sattype,satellites_ind$Sat_head_indicator)),indx]
} else if(type=="y"){
  # rename colnames
  zqs<-gloria_q_data[which(grepl(sattype,satellites_ind$Sat_head_indicator)),indx]
}
# add to df
df['emissions']<-zqs

### Step 4: Import concordance between ipcc sectors in ECP and in GLORIA
i_c_p <- concordance %>% pivot_longer(-Sat_ind,names_to="cp_ind",values_to="ident")

### Step 5: Map carbon price data from ECP to GLORIA EDGAR/OECD categories
# this is an aggregation from 76 categories to 73 categories
for(i in 2:nrow(df)){
  # extract names of the ECP categories that correspond to GLORIA EDGAR categories
  tmpnms1<-vector()
  tmpnms2<-vector()
  tmpnms3<-vector()
  tmpnms1<-i_c_p$cp_ind[i_c_p$ident==1 & i_c_p$Sat_ind==df$Sat_ind[i]]
  tmpnms2<-i_c_p$cp_ind[i_c_p$ident==2 & i_c_p$Sat_ind==df$Sat_ind[i]]
  tmpnms3<-i_c_p$cp_ind[i_c_p$ident==3 & i_c_p$Sat_ind==df$Sat_ind[i]]
  if(length(tmpnms1==1)){ # if there is unique concordance then use that
    df$cp[i]<-de$ecp_all_usd[de$ipcc_code==tmpnms1]
  } else if (length(tmpnms2==1)){ # if we only have a lower resolution ecp, use that (e.g. 1A1C price for 1A1ci emissions)
    df$cp[i]<-de$ecp_all_usd[de$ipcc_code==tmpnms2]
  } else if (length(tmpnms3)>0){ # if we only have a higher resolution ecp, then use the emissions-weighted average
    tmpvectp<-vector()
    # extract the carbon price data for the subcategories
    tmpvectc<-vector()
    for(j in 1:length(tmpnms3)){
      tmpvectp[j]<-de$ecp_all_usd[de$ipcc_code==tmpnms3[j]]
      tmpvectc[j]<-de$CO2[de$ipcc_code==tmpnms3[j]]
    }
    if(sum(tmpvectc)>0){ # if there are any emissions
      df$cp[i]<-sum((tmpvectc*tmpvectp)/sum(tmpvectc)) # compute emissions-weighted average
    } else {
      df$cp[i]<-0 # in case there are no emissions, we assume zero (otherwise division by zero generates NA)
    }
  } else {
    df$cp[i]<-0 # in case of no concordance we assume zero price
  }
}

### new Step 6: post-process df for correct 1A4 allocation (GLORIA provides only 1A4 aggregates)
# case agri and forest
if(sect %in% sector_ind$Sector_names[1:21]){
  # first find out proportions of how we allocate 1A4C. Do this with IEA data.
  p1A4ci<-de$CO2[de$ipcc_code %in% c("1A4C1")]/sum(de$CO2[de$ipcc_code %in% c("1A4C1","1A4C2")])
  p1A4cii<-de$CO2[de$ipcc_code %in% c("1A4C2")]/sum(de$CO2[de$ipcc_code %in% c("1A4C1","1A4C2")])
  # then allocate the GLORIA 1A4 data accordingly.
  df$emissions[df$Sat_ind=="1A4ci"]<-df$emissions[df$Sat_ind=="1A4"]*p1A4ci
  df$emissions[df$Sat_ind=="1A4cii"]<-df$emissions[df$Sat_ind=="1A4"]*p1A4cii
  df$emissions[df$Sat_ind=="1A4"]<-0
} 
# case fishing
if(sect %in% sector_ind$Sector_names[22:23]){
  # first find out proportions of how we allocate 1A4C. Do this with IEA data.
  p1A4ci<-de$CO2[de$ipcc_code %in% c("1A4C1")]/sum(de$CO2[de$ipcc_code %in% c("1A4C1","1A4C3")])
  p1A4ciii<-de$CO2[de$ipcc_code %in% c("1A4C3")]/sum(de$CO2[de$ipcc_code %in% c("1A4C1","1A4C3")])
  # then allocate the GLORIA 1A4 data accordingly.
  df$emissions[df$Sat_ind=="1A4ci"]<-df$emissions[df$Sat_ind=="1A4"]*p1A4ci
  df$emissions[df$Sat_ind=="1A4ciii"]<-df$emissions[df$Sat_ind=="1A4"]*p1A4ciii
  df$emissions[df$Sat_ind=="1A4"]<-0
} 
# case commercial/institutional
if(sect %in% c(sector_ind$Sector_names[24:120],demand_ind$Final_demand_names[2:6])){
  # allocate the GLORIA 1A4 data accordingly.
  df$emissions[df$Sat_ind=="1A4a"]<-df$emissions[df$Sat_ind=="1A4"]*1
  df$emissions[df$Sat_ind=="1A4"]<-0
} 
# case households final
if(sect == demand_ind$Final_demand_names[1]){
  # allocate GLORIA 1A4 data accordingly
  df$emissions[df$Sat_ind=="1A4b"]<-df$emissions[df$Sat_ind=="1A4"]*1
  df$emissions[df$Sat_ind=="1A4"]<-0
}

### Step 7: Rename 5 digit codes
df$Sat_ind[df$Sat_ind=="1A1ci"]<-"1A1c1"
df$Sat_ind[df$Sat_ind=="1A1cii"]<-"1A1c2"
df$Sat_ind[df$Sat_ind=="1A4ci"]<-"1A4c1"
df$Sat_ind[df$Sat_ind=="1A4cii"]<-"1A4c2"
df$Sat_ind[df$Sat_ind=="1A4ciii"]<-"1A4c3"

### Step 8: Calculate emissions-weighted average carbon price for missing cases
# we identify the applicable carbon price for each category with emissions
# this step is only there for special cases (1A2, 1A3b, 3C1). If these categories
# have no price, but subcategories do, then we calculate the emissions-weighted
# average across subcategories and use the result.
df['acp']<-NA
for(i in 1:nrow(df)){
  # find all subcategories
  tmpnms<-vector()
  tmpnms<-df[startsWith(df$Sat_ind, df$Sat_ind[i]),1]
  tmpnms<-tmpnms[-1] # keep only subcategories
  # get prices for those subcategories
  tmpvectp<-df$cp[df$Sat_ind %in% tmpnms]
  # get carbon for those subcategories
  tmpvectc<-df$emissions[df$Sat_ind %in% tmpnms]
  # if the main category has no aggregate price, but subcategories do,
  # we use the emissions-weighted average price across subcategories
  if (df$cp[i] == 0 & sum(tmpvectp) > 0) {
    df$acp[i] <- sum(tmpvectp*tmpvectc)/sum(tmpvectc)
  } else { # otherwise we use the price of the main category (it might be 0)
    df$acp[i] <- df$cp[i]
  }
}

### Step 9: Calculate overall emissions-weighted carbon price for the sector
# divide categorical emissions by total
df['relem']<-df$emissions/df$emissions[df$Sat_ind=="total"]
# if we have zero total emissions this introduces NAs. Change those cases to zero
# df$relem[is.na(df$relem)]<-0
# multiply relative emissions by categorical prices
df['relcc']<-df$relem*df$acp
df$relcc[df$Sat_ind=="total"]<-0
# result is the sum of all categorical weighted prices
result<-sum(df$relcc)


################################################################################
#### remove tmp dirs
unlink(file.path(wd,"1_import","ecp","tmpdir"),recursive = T)
unlink(file.path(wd,"1_import","gloria","tmpdir"),recursive = T)
unlink(file.path(wd,"2_match","tmpdir"),recursive = T)





