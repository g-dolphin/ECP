################################################################################
####### Script to match GLORIA with ECP ########################################
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
ecp<-read.csv(file.path(fpe,"ecp_ipcc_CO2.csv"))
if(pl=="cons_p"){
  ecp<-ecp %>% 
    select(-c(ecp_ets2_coal_usd_k,ecp_ets2_natgas_usd_k,ecp_ets2_oil_usd_k)) %>% 
    rename(ecp_all_usd = ecp_all_usd_k,
           ecp_ets_usd = ecp_ets_usd_k,
           ecp_tax_usd = ecp_tax_usd_k,
           ecp_ets_coal_usd = ecp_ets_coal_usd_k,
           ecp_tax_coal_usd = ecp_tax_coal_usd_k,
           ecp_ets_natgas_usd = ecp_ets_natgas_usd_k,
           ecp_tax_natgas_usd = ecp_tax_natgas_usd_k,
           ecp_ets_oil_usd = ecp_ets_oil_usd_k,
           ecp_tax_oil_usd = ecp_tax_oil_usd_k)
} else if (pl == "curr_p"){
  ecp<-ecp %>% 
    select(-c(ecp_ets2_coal_usd,ecp_ets2_natgas_usd,ecp_ets2_oil_usd)) 
}


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

### prep parallelised loop

l_tqm<-list()
l_yqm<-list()

# import GLORIA CO2 data
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

# define carbon price accounts we want
# list elements are ordered as sattype (EDGAR or OECD), cptype (ecp, ets or tax), etype (emissions category), ftype (fuel)
cpal<-list()
# EDGAR based satellites
cpal[[1]]<-list("EDGAR","ecp","all","all")
cpal[[2]]<-list("EDGAR","ecp","1a","all")
cpal[[3]]<-list("EDGAR","ecp","non1a","all")
cpal[[4]]<-list("EDGAR","ets","all","all")
cpal[[5]]<-list("EDGAR","ets","1a","all")
cpal[[6]]<-list("EDGAR","ets","1a","coal")
cpal[[7]]<-list("EDGAR","ets","1a","natgas")
cpal[[8]]<-list("EDGAR","ets","1a","oil")
cpal[[9]]<-list("EDGAR","ets","non1a","all")
cpal[[10]]<-list("EDGAR","tax","all","all")
cpal[[11]]<-list("EDGAR","tax","1a","all")
cpal[[12]]<-list("EDGAR","tax","1a","coal")
cpal[[13]]<-list("EDGAR","tax","1a","natgas")
cpal[[14]]<-list("EDGAR","tax","1a","oil")
cpal[[15]]<-list("EDGAR","tax","non1a","all")
# OECD based satellites
cpal[[16]]<-list("OECD","ecp","all","all")
cpal[[17]]<-list("OECD","ecp","1a","all")
cpal[[18]]<-list("OECD","ecp","non1a","all")
cpal[[19]]<-list("OECD","ets","all","all")
cpal[[20]]<-list("OECD","ets","1a","all")
cpal[[21]]<-list("OECD","ets","1a","coal")
cpal[[22]]<-list("OECD","ets","1a","natgas")
cpal[[23]]<-list("OECD","ets","1a","oil")
cpal[[24]]<-list("OECD","ets","non1a","all")
cpal[[25]]<-list("OECD","tax","all","all")
cpal[[26]]<-list("OECD","tax","1a","all")
cpal[[27]]<-list("OECD","tax","1a","coal")
cpal[[28]]<-list("OECD","tax","1a","natgas")
cpal[[29]]<-list("OECD","tax","1a","oil")
cpal[[30]]<-list("OECD","tax","non1a","all")


# make wrapper function to run the matching
apply_ewcp_calc<-function(ecp,countryconc,yr,yqm,tqm,demand_ind,region_ind,satellites_ind,sector_ind,sequential_ind,sequentiald_ind,cpal){
  
  ### Step 1: Identify countries for which we run the matching (those with any carbon price)
  anycp_c<- ecp %>% filter(year==yr,ecp_all_usd>0) %>% select(jurisdiction) %>% unique()
  anycp_g<-countryconc$c_gloria[countryconc$c_ecp %in% anycp_c$jurisdiction]
  
  ### Step 2: Run for sectoral satellites
  # identify countries and sectors
  fcq<-sequential_ind$fcq
  fsq<-sequential_ind$fsq
  cpc_id<-which(fcq %in% anycp_g)
  # add row into data (i.e., rows corresponding to author-created indicators are added to the Satellite account matrix)
  nr<-nrow(tqm)
  zq <- rbind(tqm,matrix(data=NA,nrow=length(cpal),ncol=ncol(tqm))) # we add empty rows to the satellite data
  # fill in for each relevant column (country-sector)
  for(r in cpc_id){
    # idenify country
    tmpc<-fcq[r] # the country
    # identify sector
    tmps<-fsq[r] # the sector
    # then run
    for(j in 1:length(cpal)){ # loop across carbon price accounts defined in cpal
      zq[nr+j,r]<-calculate_ewcp(yr = yr,
                                 indx=r,
                                 ecp_jur = countryconc$c_ecp[countryconc$c_gloria==tmpc],
                                 sattype = cpal[[j]][[1]],
                                 cptype = cpal[[j]][[2]],
                                 etype = cpal[[j]][[3]],
                                 ftype = cpal[[j]][[4]],
                                 ctry = tmpc,
                                 sect = tmps,
                                 ecp_data = ecp,
                                 gloria_q_data = zq,
                                 concordance = conclist[[tmps]],
                                 type = "z",
                                 sector_ind = sector_ind,
                                 demand_ind = demand_ind)
    }
  }
  rm(cpc_id)
  
  ### Step 3: Run for demand satellites
  # identify countries and sectors
  fcq<-sequentiald_ind$fcqd
  fsq<-sequentiald_ind$demandind
  cpc_id<-which(fcq %in% anycp_g)
  # add row into data
  nr<-nrow(yqm)
  yq<-rbind(yqm,matrix(data=NA,nrow=length(cpal),ncol=ncol(yqm))) # we add empty rows to the satellite data
  # fill in for each column (country-demand)
  for(r in cpc_id){
    tmpc<-fcq[r] # the country
    tmps<-fsq[r] # the demand
    # then run
    for(j in 1:length(cpal)){ # loop across carbon price accounts defined in cpal
      yq[nr+j,r]<-calculate_ewcp(yr = yr,
                                 indx=r,
                                 ecp_jur = countryconc$c_ecp[countryconc$c_gloria==tmpc],
                                 sattype = cpal[[j]][[1]],
                                 cptype = cpal[[j]][[2]],
                                 etype = cpal[[j]][[3]],
                                 ftype = cpal[[j]][[4]],
                                 ctry = tmpc,
                                 sect = tmps,
                                 ecp_data = ecp,
                                 gloria_q_data = yq,
                                 concordance = if(tmps== demand_ind$Final_demand_names[1]) {conclist[['households']]} else {conclist[['Other services']]},
                                 type = "y",
                                 sector_ind = sector_ind,
                                 demand_ind = demand_ind)
    }
  }
  rm(cpc_id)
  ### Step 4: Result list and return
  rl<-list()
  rl[['zq']]<-zq
  rl[['yq']]<-yq
  return(rl)
}



library(foreach)
library(parallel)
library(doParallel)



dd<-list()


# specify number of cores (all but one)
parallel::detectCores()
n.cores <- parallel::detectCores() - 2

#create the cluster
my.cluster <- parallel::makeCluster(
  n.cores, 
  type = "PSOCK"
)

#check cluster definition
print(my.cluster)

#register it to be used by %dopar%
doParallel::registerDoParallel(cl = my.cluster)

#check if it is registered
foreach::getDoParRegistered()

#how many workers are available?
foreach::getDoParWorkers()

# then run
dd <- foreach(w = 1:length(yrs),
              .packages = c("dplyr", "tidyr")
) %dopar% {apply_ewcp_calc(ecp=ecp,
                           countryconc=countryconc,
                           yr=yrs[w],
                           yqm=l_yqm[[w]],
                           tqm=l_tqm[[w]],
                           demand_ind=demand_ind,
                           region_ind=region_ind,
                           satellites_ind=satellites_ind,
                           sector_ind=sector_ind,
                           sequential_ind=sequential_ind,
                           sequentiald_ind=sequentiald_ind,
                           cpal=cpal)}

# stop the cluster
parallel::stopCluster(cl = my.cluster)

# format
names(dd)<-yrs # name list elements as countries

# save
for(k in 1:length(yrs)){
  yq<-dd[[k]][['yq']]
  zq<-dd[[k]][['zq']]
  dir.create(file.path(resultfp, yrs[k]))
  save(yq,zq,demand_ind,region_ind,satellites_ind,sector_ind,sequential_ind,sequentiald_ind, 
       file = file.path(resultfp,yrs[k],"ecp_gloria.RData"))
  rm(yq,zq)
}



## clean up 
rm(list=ls()[! ls() %in% c("wd","pl","gversion","ecpmwd","cpal")])

