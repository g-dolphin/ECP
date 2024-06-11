## step by step

k=32

### Print progress
print(paste("working on year",yrs[k]))

### Step 1: Import data
load(file.path(fpg,paste0("gloria_",yrs[k],".RData")))

### Step 2: Run for sectoral satellites
# add row into data (i.e., rows corresponding to author-created indicators are added to the Satellite account matrix)
nr<-nrow(tqm)+1
zq<-rbind(tqm,NA)
fcq<-sequential_ind$fcq
fsq<-sequential_ind$fsq



### check Latvia Basic Metals
# r 11477:11484

r=11495

tmpc<-fcq[r] # the country
tmps<-fsq[r] # the sector


### now moving into the maytchiing function

yr = yrs[k]
ecp_jur = countryconc$c_ecp[countryconc$c_gloria==tmpc]
ctry = tmpc
sect = tmps
ecp_data = ecp
gloria_q_data = zq
concordance = conclist[[tmps]]
type = "z"



### Step 1: Create calculation dataframe
df<-as.data.frame(matrix(NA,nrow=nrow(concordance),ncol=2))
colnames(df)<-c("Sat_ind","cp")
df$Sat_ind<-concordance$Sat_ind
# the below is to make the function work for both industry satellites z 
# and demand satellites y
if(type=="z"){
  sectorf<-sequential_ind$Sequential_regionSector_labels[sequential_ind$fcq==ctry & sequential_ind$fsq==sect]
} else if(type=="y"){
  sectorf=sequentiald_ind$Sequentiald_finalDemand_labels[sequentiald_ind$fcqd==ctry & sequentiald_ind$demandind==sect]
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
# EDGAR rows, countrysector column
if(type=="z"){
  zqs<-zq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator)),r]
} else if(type=="y"){
  # rename colnames
  zqs<-yq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator)),r]
}
# add to df
df['emissions']<-zqs

###########################
df$emissions[df$Sat_ind=="total"]
sum(df$emissions[-1])

###########################

### Step 4: Import concordance between ipcc sectors in ECP and in GLORIA
i_c_p <- concordance %>% pivot_longer(-Sat_ind,names_to="cp_ind",values_to="ident")


### Step 5: Map carbon price data from ECP to GLORIA EDGAR categories
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
  } else {} # otherwise e.g. in case of 5B, where we have no conc, do nothing
}

### Step 6: Rename 5 digit codes
df$Sat_ind[df$Sat_ind=="1A1ci"]<-"1A1c1"
df$Sat_ind[df$Sat_ind=="1A1cii"]<-"1A1c2"
df$Sat_ind[df$Sat_ind=="1A4ci"]<-"1A4c1"
df$Sat_ind[df$Sat_ind=="1A4cii"]<-"1A4c2"
df$Sat_ind[df$Sat_ind=="1A4ciii"]<-"1A4c3"

### Step 7: Calculate emissions-weighted average carbon price for missing cases
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

### Step 8: Calculate overall emissions-weighted carbon price for the sector
# divide categorical emissions by total
df['relem']<-df$emissions/df$emissions[df$Sat_ind=="total"]
# if we have zero total emissions this introduces NAs. Change those cases to zero
# df$relem[is.na(df$relem)]<-0
# multiply relative emissions by categorical prices
df['relcc']<-df$relem*df$acp
df$relcc[df$Sat_ind=="total"]<-0
# result is the sum of all categorical weighted prices
result<-sum(df$relcc)






