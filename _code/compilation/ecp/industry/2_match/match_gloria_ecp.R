################################################################################
####### Script to match GLORIA 057 with ECP ####################################
################################################################################


# Notes:
# GLORIA is at basic prices. we use ECP at basic prices as well


################################################################################
## Packages, Filepaths & Data ##################################################

# Packages
library(dplyr)
library(tidyr)
#library(stringr)
#library(readxl)

dir.create(file.path(ecpmwd, "tmpdir"))

# Define filepaths
fpe<-file.path(wd,"1_import","ecp","tmpdir")
fpg<-file.path(wd,"1_import","gloria","tmpdir")
resultfp<-file.path(ecpmwd,"tmpdir")

# Main function
source(file.path(ecpmwd,"matching_function.R"))

# ECP and concordance data
ecp<-read.csv(file.path(fpe,"ecp_sector_CO2.csv"))

svect<-excel_sheets(file.path(ecpmwd,"ipcc_conc.xlsx"))
svect
iclist<-list()
for(i in 1:length(svect)){
  iclist[[i]]<-read_excel(file.path(ecpmwd,"ipcc_conc.xlsx"),sheet = svect[i])
}
names(iclist)<-svect

# define years to run the process for
yrs<-c(2010,2015,2020)

# align country names
load(file.path(wd,"1_import_&_format_raw","gloria","tmpdir",paste0("gloria_",yrs[1],".RData")))
rm(leo,x,y,yq,z,zq,zocases)
newreg

unique(ecp$jurisdiction)

ecp$jurisdiction[ecp$jurisdiction=="Czech Republic"]<-"Czech_Republic"
ecp$jurisdiction[ecp$jurisdiction=="United Kingdom"]<-"United_Kingdom"
ecp$jurisdiction[ecp$jurisdiction=="Korea, Rep."]<-"Korea_Rep"
ecp$jurisdiction[ecp$jurisdiction=="Russian Federation"]<-"Russian_Federation"
ecp$jurisdiction[ecp$jurisdiction=="Saudi Arabia"]<-"Saudi_Arabia"
ecp$jurisdiction[ecp$jurisdiction=="Slovak Republic"]<-"Slovak_Republic"
ecp$jurisdiction[ecp$jurisdiction=="United States"]<-"United_States"
ecp$jurisdiction[ecp$jurisdiction=="South Africa"]<-"South_Africa"


################################################################################
## Run process #################################################################

# for each year
#
for(k in 1:length(yrs)){
  ### Print progress
  print(paste("working on year",yrs[k]))
  
  ### Step 1: Import data
  load(file.path(fpg,paste0("gloria_",yrs[k],".RData")))
  
  ### Step 2: Run for sectoral satellites
  # add row into data (i.e., rows corresponding to author-created indicators are added to the Satellite account matrix)
  nr<-nrow(zq)+2
  zq<-rbind(zq,NA,NA)
  zq$Sat_indicator[nr-1]<-"emissions-weighted carbon price" # adding name of indicator (this line) and unit of indicator (next line)
  zq$Sat_unit[nr-1]<-"USD/t"
  zq$Sat_indicator[nr]<-"ets_ii_coverage" # adding name of indicator (this line) and unit of indicator (next line)
  zq$Sat_unit[nr]<-"share of emissions"
  # fill in for each column
  for(r in 3:ncol(zq)){
    tmpc<-fcq[r-2] # the country
    tmps<-fsq[r-2] # the sector
    # If we have ecp data for the country, we fill in
    if(tmpc %in% ecp$jurisdiction){
      zq[nr-1,r]<-calculate_ewcp(yr = yrs[k],
                                 ctry = tmpc,
                                 sect = tmps,
                                 ecp_data = ecp,
                                 gloria_q_data = zq,
                                 concordance = iclist[[tmps]],
                                 type = "z")
      zq[nr,r]<-ets2_coverage_fun(yr=yrs[k],
                                  ctry=tmpc,
                                  sect=tmps,
                                  gloria_q_data = zq,
                                  concordance = iclist[[tmps]],
                                  type = "z")
    } else {} # otherwise we keep it as NA
  }
  
  ### Step 3: Run for demand satellites
  # add row into data
  nr<-nrow(yq)+2
  yq<-rbind(yq,NA,NA)
  yq$Sat_indicator[nr-1]<-"emissions-weighted carbon price"
  yq$Sat_unit[nr-1]<-"USD/t"
  yq$Sat_indicator[nr]<-"ets_ii_coverage"
  yq$Sat_unit[nr]<-"share of emissions"
  # fill in for each column
  for(r in 3:ncol(yq)){
    tmpc<-substr(colnames(yq[r]),start=1,stop=nchar(colnames(yq[r]))-nchar("_Household final consumption P.3h")) # the country
    # If we have ecp data for the country, we fill in
    if(tmpc %in% ecp$jurisdiction){
      yq[nr-1,r]<-calculate_ewcp(yr = yrs[k],
                                 ctry = tmpc,
                                 sect = NA,
                                 ecp_data = ecp,
                                 gloria_q_data = yq,
                                 concordance = iclist[['Arts_and_recreation']], # we choose a non-modified concordance here
                                 type = "y")
      yq[nr,r]<-ets2_coverage_fun(yr=yrs[k],
                                  ctry=tmpc,
                                  sect=tmps,
                                  gloria_q_data = yq,
                                  concordance = iclist[[tmps]],
                                  type = "y")
    } else {} # otherwise we keep it as NA
  }
  
  ### Step 4: Save data and clean up
  dir.create(file.path(resultfp, yrs[k]))
  save(leo,x,y,yq,z,zq,fsq,fcq,newcat,newreg, file = file.path(resultfp,yrs[k],"ecp_gloria.RData"))
  rm(leo,x,y,yq,z,zq)
}

## clean up 
rm(list=ls()[! ls() %in% c("wd")])

