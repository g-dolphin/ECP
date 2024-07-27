


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



