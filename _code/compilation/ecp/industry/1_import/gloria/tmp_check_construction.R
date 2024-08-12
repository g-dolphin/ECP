


# identify columns relating to construction
columns_building_constr<-which(sequential_ind$fsq == "Building construction")
columns_civeng_constr<-which(sequential_ind$fsq == "Civil engineering construction")

# identify rows relating to total CO2 emissions
co2_edgar_row<-which(satellites_ind$Sat_indicator=="'co2_excl_short_cycle_org_c_total_EDGAR_consistent'")
co2_oecd_row<-which(satellites_ind$Sat_indicator=="'co2_excl_short_cycle_org_c_total_OECD_consistent'")

# make dataframe
region_ind$Region_names


# look at data

plot(tqm[co2_edgar_row,columns_building_constr])

plot(tqm[co2_edgar_row,columns_civeng_constr])

plot(tqm[co2_oecd_row,columns_building_constr])

plot(tqm[co2_oecd_row,columns_civeng_constr])


# gas
columns_gas<-which(sequential_ind$fsq=="Distribution of gaseous fuels through mains")
rows_co2_edgar<-which(satellites_ind$Sat_head_indicator=="Emissions (EDGAR)")

df<-tqm[rows_co2_edgar,columns_gas]
row.names(df)<-satellites_ind$Sat_indicator[rows_co2_edgar]
colnames(df)<-region_ind$Region_names

write.csv(df,file.path(wd,"1_import","gloria","tmpdir","g59_s94_edgarco2_2020.csv"))

# electricity
columns_elec<-which(sequential_ind$fsq=="Electric power generation, transmission and distribution")
rows_co2_edgar<-which(satellites_ind$Sat_head_indicator=="Emissions (EDGAR)")

df<-tqm[rows_co2_edgar,columns_elec]
row.names(df)<-satellites_ind$Sat_indicator[rows_co2_edgar]
colnames(df)<-region_ind$Region_names

write.csv(df,file.path(wd,"1_import","gloria","tmpdir","g59_s93_edgarco2_2020.csv"))


# water
columns_water<-which(sequential_ind$fsq=="Water collection, treatment and supply; sewerage")
rows_co2_edgar<-which(satellites_ind$Sat_head_indicator=="Emissions (EDGAR)")

df<-tqm[rows_co2_edgar,columns_water]
row.names(df)<-satellites_ind$Sat_indicator[rows_co2_edgar]
colnames(df)<-region_ind$Region_names

write.csv(df,file.path(wd,"1_import","gloria","tmpdir","g59_s95_edgarco2_2020.csv"))








