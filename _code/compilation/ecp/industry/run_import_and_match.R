# Run ecp industry matching process

### Setup
wd<-file.path(here::here(),"_code","compilation","ecp","industry")
setwd(wd)

### Import data
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


pl<-"cons_p"
ecpwd<-file.path(wd,"1_import","ecp")
source(file.path(ecpwd,"import_ecp.R"))

### Datamatch
ecpmwd<-file.path(wd,"2_match")
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
  colnames(zqdf)<-c("year","country_sector","country","sector","ecp_edgar","ecp_oecd")
  zqdf$year<-yrs[i]
  zqdf$country_sector<-sequential_ind$Sequential_regionSector_labels
  zqdf$country<-sequential_ind$fcq
  zqdf$sector<-sequential_ind$fsq
  # ecp is always in the bottom rows
  zqdf$ecp_edgar<-zq[nrow(zq)-1,]
  zqdf$ecp_oecd<- zq[nrow(zq)  ,]
  # add emissions columns
  zqdf['co2_edgar_total']<-zq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_total",satellites_ind$Sat_indicator)),]
  zqdf['co2_edgar_1a']<-zq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_1A",satellites_ind$Sat_indicator)),] %>% colSums()
  zqdf['co2_edgar_1b']<-zq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_1B",satellites_ind$Sat_indicator)),] %>% colSums()
  zqdf['co2_edgar_2']<-zq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_2",satellites_ind$Sat_indicator)),] %>% colSums()
  zqdf['co2_edgar_3']<-zq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_3",satellites_ind$Sat_indicator)),] %>% colSums()
  zqdf['co2_edgar_4']<-zq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_4",satellites_ind$Sat_indicator)),] %>% colSums()
  zqdf['co2_edgar_5']<-zq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_5",satellites_ind$Sat_indicator)),] %>% colSums()
  zqdf['co2_oecd_total']<-zq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_total",satellites_ind$Sat_indicator)),]
  zqdf['co2_oecd_1a']<-zq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_1A",satellites_ind$Sat_indicator)),] %>% colSums()
  zqdf['co2_oecd_1b']<-zq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_1B",satellites_ind$Sat_indicator)),] %>% colSums()
  zqdf['co2_oecd_2']<-zq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_2",satellites_ind$Sat_indicator)),] %>% colSums()
  zqdf['co2_oecd_3']<-zq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_3",satellites_ind$Sat_indicator)),] %>% colSums()
  zqdf['co2_oecd_4']<-zq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_4",satellites_ind$Sat_indicator)),] %>% colSums()
  zqdf['co2_oecd_5']<-zq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_5",satellites_ind$Sat_indicator)),] %>% colSums()
  # move into list element
  zql[[i]]<-zqdf
  rm(zqdf)
  ## 3. Get demand level data
  yqdf<-as.data.frame(matrix(nrow=nrow(sequentiald_ind),ncol=6))
  colnames(yqdf)<-c("year","country_sector","country","sector","ecp_edgar","ecp_oecd")
  yqdf$year<-yrs[i]
  yqdf$country_sector<-sequentiald_ind$Sequential_finalDemand_labels
  yqdf$country<-sequentiald_ind$fcqd
  yqdf$sector<-sequentiald_ind$demandind
  # ecp is always in the bottom rows
  yqdf$ecp_edgar<-yq[nrow(yq)-1,]
  yqdf$ecp_oecd<-yq[nrow(yq),]
  # total emissions row is given by satellites_ind
  # add emissions columns
  yqdf['co2_edgar_total']<-yq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_total",satellites_ind$Sat_indicator)),]
  yqdf['co2_edgar_1a']<-yq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_1A",satellites_ind$Sat_indicator)),] %>% colSums()
  yqdf['co2_edgar_1b']<-yq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_1B",satellites_ind$Sat_indicator)),] %>% colSums()
  yqdf['co2_edgar_2']<-yq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_2",satellites_ind$Sat_indicator)),] %>% colSums()
  yqdf['co2_edgar_3']<-yq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_3",satellites_ind$Sat_indicator)),] %>% colSums()
  yqdf['co2_edgar_4']<-yq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_4",satellites_ind$Sat_indicator)),] %>% colSums()
  yqdf['co2_edgar_5']<-yq[which(grepl("EDGAR",satellites_ind$Sat_head_indicator) & grepl("c_5",satellites_ind$Sat_indicator)),] %>% colSums()
  yqdf['co2_oecd_total']<-yq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_total",satellites_ind$Sat_indicator)),]
  yqdf['co2_oecd_1a']<-yq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_1A",satellites_ind$Sat_indicator)),] %>% colSums()
  yqdf['co2_oecd_1b']<-yq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_1B",satellites_ind$Sat_indicator)),] %>% colSums()
  yqdf['co2_oecd_2']<-yq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_2",satellites_ind$Sat_indicator)),] %>% colSums()
  yqdf['co2_oecd_3']<-yq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_3",satellites_ind$Sat_indicator)),] %>% colSums()
  yqdf['co2_oecd_4']<-yq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_4",satellites_ind$Sat_indicator)),] %>% colSums()
  yqdf['co2_oecd_5']<-yq[which(grepl("OECD",satellites_ind$Sat_head_indicator) & grepl("c_5",satellites_ind$Sat_indicator)),] %>% colSums()
  # move into list element
  yql[[i]]<-yqdf
  rm(yqdf)
}
zqd<-do.call("rbind",zql)
yqd<-do.call("rbind",yql)

# we save seperate these files separately due to GitHub restrictions on file size
if(pl=="curr_p"){
  write.csv(zqd %>% select(year,country_sector,country,sector,contains("EDGAR")),
            file.path(here::here(),
                      "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                      "currentPrice","FlexXRate",
                      "ecp_gloria_edgar_industry_CO2.csv"),row.names = F)
  write.csv(zqd %>% select(year,country_sector,country,sector,contains("OECD")),
            file.path(here::here(),
                      "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                      "currentPrice","FlexXRate",
                      "ecp_gloria_oecd_industry_CO2.csv"),row.names = F)
  write.csv(yqd %>% select(year,country_sector,country,sector,contains("EDGAR")),
            file.path(here::here(),
                          "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                          "currentPrice","FlexXRate",
                          "ecp_gloria_edgar_finaldem_CO2.csv"),row.names = F)
  write.csv(yqd %>% select(year,country_sector,country,sector,contains("OECD")),
            file.path(here::here(),
                      "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                      "currentPrice","FlexXRate",
                      "ecp_gloria_oecd_finaldem_CO2.csv"),row.names = F)
} else if (pl=="cons_p"){
  write.csv(zqd %>% select(year,country_sector,country,sector,contains("EDGAR")),
            file.path(here::here(),
                          "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                          "constantPrice","FixedXRate",
                          "ecp_gloria_edgar_industry_CO2.csv"),row.names = F)
  write.csv(zqd %>% select(year,country_sector,country,sector,contains("OECD")),
            file.path(here::here(),
                      "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                      "constantPrice","FixedXRate",
                      "ecp_gloria_oecd_industry_CO2.csv"),row.names = F)
  write.csv(yqd %>% select(year,country_sector,country,sector,contains("EDGAR")),
            file.path(here::here(),
                          "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                          "constantPrice","FixedXRate",
                          "ecp_gloria_edgar_finaldem_CO2.csv"),row.names = F)
  write.csv(yqd %>% select(year,country_sector,country,sector,contains("OECD")),
            file.path(here::here(),
                      "_dataset","ecp","industry","ecp_gloria_sectors",gversion,
                      "constantPrice","FixedXRate",
                      "ecp_gloria_oecd_finaldem_CO2.csv"),row.names = F)
}


### clean up
unlink(file.path(wd,"1_import","ecp","tmpdir"),recursive = T)
unlink(file.path(wd,"1_import","gloria","tmpdir"),recursive = T)
unlink(file.path(wd,"2_match","tmpdir"),recursive = T)


rm(list=ls())


