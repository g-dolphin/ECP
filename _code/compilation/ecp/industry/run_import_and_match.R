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

## MM hier weiter
source(file.path(ecpmwd,"match_gloria_ecp.R"))