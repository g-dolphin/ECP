# Run ecp industry matching process

### Setup
wd<-file.path(here::here(),"_code","compilation","ecp","industry")
setwd(wd)

### Import data
gloriawd<-file.path(wd,"1_import","gloria")
source(file.path(gloriawd,"run_imports.R"))

pl<-"curr_p"
ecpwd<-file.path(wd,"1_import","ecp")
source(file.path(ecpwd,"import_ecp.R"))

### Datamatch
ecpmwd<-file.path(wd,"2_match")
sattype<-"EDGAR"
source(file.path(ecpmwd,"match_gloria_ecp.R"))


### Reformat and Save 
yrs<-seq(1990,2022)
zql<-list()
yql<-list()
for(i in 1:length(yrs)){
  ## 1. Fetch data
  load(file.path(ecpmwd,"tmpdir",yrs[i],"ecp_gloria.RData"))
  ## 2. Get industry level data
  zqdf<-as.data.frame(matrix(nrow=nrow(sequential_ind),ncol=6))
  colnames(zqdf)<-c("year","country_sector","country","sector","ecp","CO2")
  zqdf$year<-yrs[i]
  zqdf$country_sector<-sequential_ind$Sequential_regionSector_labels
  zqdf$country<-sequential_ind$fcq
  zqdf$sector<-sequential_ind$fsq
  # ecp is always in the bottom row
  zqdf$ecp<-zq[nrow(zq),]
  # total emissions row is given by satellites_ind
  zqdf$CO2<-zq[which(grepl(sattype,satellites_ind$Sat_head_indicator) & grepl("total",satellites_ind$Sat_indicator)),]
  # move into list element
  zql[[i]]<-zqdf
  rm(zqdf)
  ## 3. Get industry level data
  yqdf<-as.data.frame(matrix(nrow=nrow(sequentiald_ind),ncol=6))
  colnames(yqdf)<-c("year","country_sector","country","sector","ecp","CO2")
  yqdf$year<-yrs[i]
  yqdf$country_sector<-sequentiald_ind$Sequential_finalDemand_labels
  yqdf$country<-sequentiald_ind$fcqd
  yqdf$sector<-sequentiald_ind$demandind
  # ecp is always in the bottom row
  yqdf$ecp<-yq[nrow(yq),]
  # total emissions row is given by satellites_ind
  yqdf$CO2<-yq[which(grepl(sattype,satellites_ind$Sat_head_indicator) & grepl("total",satellites_ind$Sat_indicator)),]
  # move into list element
  yql[[i]]<-yqdf
  rm(yqdf)
}
zqd<-do.call("rbind",zql)
yqd<-do.call("rbind",yql)

if(pl=="curr_p"){
  write.csv(zqd,file.path(here::here(),
                      "_dataset","ecp","industry","ecp_gloria_sectors",
                      "edgar_based","currentPrice","FlexXRate",
                      "ecp_gloria_industry_CO2.csv"))
  write.csv(yqd,file.path(here::here(),
                          "_dataset","ecp","industry","ecp_gloria_sectors",
                          "edgar_based","currentPrice","FlexXRate",
                          "ecp_gloria_finaldem_CO2.csv"))
}


### clean up
unlink(file.path(wd,"1_import","ecp","tmpdir"),recursive = T)
unlink(file.path(wd,"1_import","gloria","tmpdir"),recursive = T)
unlink(file.path(wd,"2_match","tmpdir"),recursive = T)


rm(list=ls())


