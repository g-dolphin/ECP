### Import ecp data


library("dplyr")
library("tidyr")


dir.create(file.path(ecpwd, "tmpdir"))

########### find ipcc-level ecp data

## specify source filepath here
if(pl=="curr_p"){
  fpe<-file.path("C:","Users","jomerkle",
                 "OneDrive - Norwegian University of Life Sciences","data",
                 "ECP_RESTRICTEDACCESS",ecpv,"currentPrices","FlexXRate")
} else if(pl=="cons_p"){
  fpe<-file.path("C:","Users","jomerkle",
                 "OneDrive - Norwegian University of Life Sciences","data",
                 "ECP_RESTRICTEDACCESS",ecpv,"constantPrices","FixedXRate")
}

## copy data
file.copy(from = file.path(fpe,"ecp_ipcc_CO2.csv"),
          to = file.path(ecpwd,"tmpdir"))

########### add fuel-specific data

## read aggregate ecp data
ecpd<-read.csv(file.path(ecpwd,"tmpdir","ecp_ipcc_CO2.csv"))

## identify all jurisdictions
allctrs<-unique(ecpd$jurisdiction)

## define file paths and read in data
if(pl=="curr_p"){
  # file path
  fpw<-file.path(here::here(),"_raw","wcpd_usd","CO2","currentPrices","FlexXRate")
  # data
  dtl<-list()
  for(i in 1:length(allctrs)){
    # only if there is any carbon price data
    if(sum(ecpd$ecp_all_usd[ecpd$jurisdiction==allctrs[i]]) > 0){
      if(allctrs[i] == "Korea, Rep."){
        dtl[[i]]<-read.csv(file.path(fpw,paste0("prices_usd_cFlxRate_CO2_","Korea_Rep",".csv")))
      } else {
        dtl[[i]]<-read.csv(file.path(fpw,paste0("prices_usd_cFlxRate_CO2_",gsub(" ", "_", allctrs[i]),".csv")))
      }
    } else{
      dtl[[i]]<-NULL
    }
  }
  # collapse and filter
  dt<-do.call("rbind",dtl)
  rm(dtl)
  dt <- dt %>% 
    select(jurisdiction,year,ipcc_code,Product
           ,tax_rate_incl_ex_usd
           ,ets_price_usd
           ,ets_2_price_usd
    )
} else if (pl=="cons_p"){
  # file path
  fpw<-file.path(here::here(),"_raw","wcpd_usd","CO2","constantPrices","FixedXRate")
  # data
  dtl<-list()
  for(i in 1:length(allctrs)){
    # only if there is any carbon price data
    if(sum(ecpd$ecp_all_usd_k[ecpd$jurisdiction==allctrs[i]]) > 0){
      if(allctrs[i] == "Korea, Rep."){
        dtl[[i]]<-read.csv(file.path(fpw,paste0("prices_usd_kFixRate_CO2_","Korea_Rep",".csv")))
      } else {
        dtl[[i]]<-read.csv(file.path(fpw,paste0("prices_usd_kFixRate_CO2_",gsub(" ", "_", allctrs[i]),".csv")))
      }
    } else{
      dtl[[i]]<-NULL
    }
  }
  # collapse and filter
  dt<-do.call("rbind",dtl)
  rm(dtl)
  dt <- dt %>% 
    select(jurisdiction,year,ipcc_code,Product
           ,tax_rate_incl_ex_usd_k
           ,ets_price_usd_k
           ,ets_2_price_usd_k
    )
}

## map onto ecpd
if(pl=="cons_p"){
  # for coal
  ecpd<-left_join(ecpd,dt %>% filter(Product=="Coal") %>% select(-Product),
                  by=c("jurisdiction","year","ipcc_code"))
  
  ecpd['ecp_tax_coal_usd_k']<-ecpd$tax_rate_incl_ex_usd_k
  ecpd['ecp_ets_coal_usd_k']<-ecpd$ets_price_usd_k
  ecpd['ecp_ets2_coal_usd_k']<-ecpd$ets_2_price_usd_k
  ecpd <- ecpd %>% select(-c(tax_rate_incl_ex_usd_k,ets_price_usd_k,ets_2_price_usd_k))
  
  # for natural gas
  ecpd<-left_join(ecpd,dt %>% filter(Product=="Natural gas") %>% select(-Product),
                  by=c("jurisdiction","year","ipcc_code"))
  
  ecpd['ecp_tax_natgas_usd_k']<-ecpd$tax_rate_incl_ex_usd_k
  ecpd['ecp_ets_natgas_usd_k']<-ecpd$ets_price_usd_k
  ecpd['ecp_ets2_natgas_usd_k']<-ecpd$ets_2_price_usd_k
  ecpd <- ecpd %>% select(-c(tax_rate_incl_ex_usd_k,ets_price_usd_k,ets_2_price_usd_k))
  
  # for oil
  ecpd<-left_join(ecpd,dt %>% filter(Product=="Oil") %>% select(-Product),
                  by=c("jurisdiction","year","ipcc_code"))
  
  ecpd['ecp_tax_oil_usd_k']<-ecpd$tax_rate_incl_ex_usd_k
  ecpd['ecp_ets_oil_usd_k']<-ecpd$ets_price_usd_k
  ecpd['ecp_ets2_oil_usd_k']<-ecpd$ets_2_price_usd_k
  ecpd <- ecpd %>% select(-c(tax_rate_incl_ex_usd_k,ets_price_usd_k,ets_2_price_usd_k))
} else if (pl=="curr_p"){
  # for coal
  ecpd<-left_join(ecpd,dt %>% filter(Product=="Coal") %>% select(-Product),
                  by=c("jurisdiction","year","ipcc_code"))
  
  ecpd['ecp_tax_coal_usd']<-ecpd$tax_rate_incl_ex_usd
  ecpd['ecp_ets_coal_usd']<-ecpd$ets_price_usd
  ecpd['ecp_ets2_coal_usd']<-ecpd$ets_2_price_usd
  ecpd <- ecpd %>% select(-c(tax_rate_incl_ex_usd,ets_price_usd,ets_2_price_usd))
  
  # for natural gas
  ecpd<-left_join(ecpd,dt %>% filter(Product=="Natural gas") %>% select(-Product),
                  by=c("jurisdiction","year","ipcc_code"))
  
  ecpd['ecp_tax_natgas_usd']<-ecpd$tax_rate_incl_ex_usd
  ecpd['ecp_ets_natgas_usd']<-ecpd$ets_price_usd
  ecpd['ecp_ets2_natgas_usd']<-ecpd$ets_2_price_usd
  ecpd <- ecpd %>% select(-c(tax_rate_incl_ex_usd,ets_price_usd,ets_2_price_usd))
  
  # for oil
  ecpd<-left_join(ecpd,dt %>% filter(Product=="Oil") %>% select(-Product),
                  by=c("jurisdiction","year","ipcc_code"))
  
  ecpd['ecp_tax_oil_usd']<-ecpd$tax_rate_incl_ex_usd
  ecpd['ecp_ets_oil_usd']<-ecpd$ets_price_usd
  ecpd['ecp_ets2_oil_usd']<-ecpd$ets_2_price_usd
  ecpd <- ecpd %>% select(-c(tax_rate_incl_ex_usd,ets_price_usd,ets_2_price_usd))
}



## save new file
write.csv(ecpd,file.path(ecpwd,"tmpdir","ecp_ipcc_CO2.csv"))


## clean up (remove files)
rm(list=ls()[! ls() %in% c("wd","pl","gversion")])
