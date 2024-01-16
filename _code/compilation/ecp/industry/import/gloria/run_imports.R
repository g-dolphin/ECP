################################################################################
# This script imports GLORIA data for different years (timestep)

dir.create(file.path(gloriawd, "tmpdir"))

timestep<-"2010"
qcode<-"20230727"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2015"
qcode<-"20230727"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2020"
qcode<-"20230727"
mcode<-"20230315"
source(file.path(gloriawd,"import_gloria_script.R"))


## MM to continue


rm(list=ls()[! ls() %in% c("wd")])