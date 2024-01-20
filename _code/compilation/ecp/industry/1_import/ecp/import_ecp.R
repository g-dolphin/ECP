### Import ecp data


library("dplyr")
library("tidyr")


dir.create(file.path(ecpwd, "tmpdir"))

## specify source filepath here
if(pl=="curr_p"){
  fpe<-file.path(here::here(),"_dataset","ecp","ipcc","ecp_sectors","currentPrices","FlexXRate")
} else if(pl=="cons_p"){
  fpe<-file.path(here::here(),"_dataset","ecp","ipcc","ecp_sectors","constantPrices","FixedXRate")
}


file.copy(from = file.path(fpe,"ecp_sector_CO2.csv"),
          to = file.path(ecpwd,"tmpdir"))


## clean up (remove files)
rm(list=ls()[! ls() %in% c("wd","pl")])
