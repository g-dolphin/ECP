################################################################################
# This script imports GLORIA data for different years (timestep)

dir.create(file.path(gloriawd, "tmpdir"))


timestep<-"1990"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"1991"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"1992"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"1993"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"1994"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"1995"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"1996"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"1997"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"1998"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"1999"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2000"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2001"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2002"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2003"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2004"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2005"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2006"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2007"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2008"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2009"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2010"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2011"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2012"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2013"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2014"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2015"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2016"
qcode<-"20230310"
mcode<-"20230314"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2017"
qcode<-"20230310"
mcode<-"20230315"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2018"
qcode<-"20230310"
mcode<-"20230315"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2019"
qcode<-"20230310"
mcode<-"20230315"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2020"
qcode<-"20230310"
mcode<-"20230315"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2021"
qcode<-"20230310"
mcode<-"20230320"
source(file.path(gloriawd,"import_gloria_script.R"))

timestep<-"2022"
qcode<-"20230310"
mcode<-"20230315"
source(file.path(gloriawd,"import_gloria_script.R"))

rm(list=ls()[! ls() %in% c("wd","pl","gversion")])

