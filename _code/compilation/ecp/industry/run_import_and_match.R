# Run ecp industry matching process

### Setup
wd<-file.path(here::here(),"_code","compilation","ecp","industry")
setwd(wd)

### Import data
gloriawd<-file.path(wd,"import","gloria")
source(file.path(gloriawd,"run_imports.R"))


# MM to continue