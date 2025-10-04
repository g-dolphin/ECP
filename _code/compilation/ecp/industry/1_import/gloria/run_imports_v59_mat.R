################################################################################
# This script imports GLORIA data for different years (timestep)

dir.create(file.path(gloriawd, "tmpdir"))


timestep<-"1990"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"1991"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"1992"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"1993"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"1994"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"1995"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"1996"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"1997"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"1998"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"1999"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2000"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2001"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2002"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2003"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2004"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2005"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2006"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2007"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2008"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2009"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2010"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2011"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2012"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2013"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2014"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2015"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2016"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2017"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2018"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2019"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2020"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2021"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2022"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2023"
source(file.path(gloriawd,"import_gloria_script_mat.R"))

timestep<-"2024"
source(file.path(gloriawd,"import_gloria_script_mat.R"))


rm(list=ls()[! ls() %in% c("wd","gversion")])

