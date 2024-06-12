################################################################################
####### Script to match GLORIA 057 with ECP ####################################
################################################################################


################################################################################
## Packages, Filepaths & Data ##################################################

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
ecp<-read.csv(file.path(fpe,"ecp_sector_CO2.csv"))
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
## Run process #################################################################

# for each year
#
for(k in 1:length(yrs)){
  ### Print progress
  print(paste("working on year",yrs[k]))
  
  ### Step 1: Import data
  load(file.path(fpg,paste0("gloria_",yrs[k],".RData")))
  
  ### Step 2: Run for sectoral satellites
  # add row into data (i.e., rows corresponding to author-created indicators are added to the Satellite account matrix)
  print("industrial sectors")
  nr<-nrow(tqm)+1
  zq<-rbind(tqm,NA)
  fcq<-sequential_ind$fcq
  fsq<-sequential_ind$fsq
  
  # fill in for each column
  for(r in 1:ncol(zq)){
    tmpc<-fcq[r] # the country
    tmps<-fsq[r] # the sector
    # If we have ecp data for the country, we fill in
    zq[nr,r]<-calculate_ewcp(yr = yrs[k],
                             ecp_jur = countryconc$c_ecp[countryconc$c_gloria==tmpc],
                             sattype = sattype,
                             ctry = tmpc,
                             sect = tmps,
                             ecp_data = ecp,
                             gloria_q_data = zq,
                             concordance = conclist[[tmps]],
                             type = "z")
  }
  
  ### Step 3: Run for demand satellites
  # add row into data
  print("demand sectors")
  nr<-nrow(yqm)+1
  yq<-rbind(yqm,NA)
  fcq<-sequentiald_ind$fcqd
  fsq<-sequentiald_ind$demandind
  
  # fill in for each column
  for(r in 1:ncol(yq)){
    tmpc<-fcq[r] # the country
    tmps<-fsq[r] # the sector
    # fill in
    yq[nr,r]<-calculate_ewcp(yr = yrs[k],
                             ecp_jur = countryconc$c_ecp[countryconc$c_gloria==tmpc],
                             sattype = sattype,
                             ctry = tmpc,
                             sect = tmps,
                             ecp_data = ecp,
                             gloria_q_data = yq,
                             concordance = conclist[['Other services']], # we choose a non-modified concordance here
                             type = "y")
  }
  
  ### Step 4: Save data and clean up
  dir.create(file.path(resultfp, yrs[k]))
  save(yq,zq,demand_ind,region_ind,satellites_ind,sector_ind,sequential_ind,sequentiald_ind, 
       file = file.path(resultfp,yrs[k],"ecp_gloria.RData"))
  rm(tqm,yq,yqm,zq)
}

## clean up 
rm(list=ls()[! ls() %in% c("wd","pl","sattype","gversion","ecpmwd")])

