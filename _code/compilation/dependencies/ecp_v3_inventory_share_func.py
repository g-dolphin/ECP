#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 09:27:32 2022

@author: gd
"""

import pandas as pd

# EMISSIONS SHARES

# National jurisdictions

def emissions_share(emissions, jur_tot_emissions, world_total, national_total=None, 
                    jur_level = "national"): #, unit = None
    # only country and year are used as keys, meaning that all sectors and fuel types within a same country and for a given year 
    # receive the same 'total GHG' figure
    emissions_share = pd.merge(emissions, jur_tot_emissions, how='left', on=['jurisdiction','year'])
    emissions_share = pd.merge(emissions_share, world_total, how='left', on=['year'])
    
    share_vars_map = {"CO2_jurGHG":"Total_GHG_Emissions_Excluding_LUCF_MtCO2e", 
                      "CO2_jurCO2":"Total_CO2_Emissions_Excluding_LUCF_MtCO2e", 
                      "CO2_wldGHG":"World_GHG_Emissions", 
                      "CO2_wldCO2":"World_CO2_Emissions"}
    
    if jur_level == "subnational":
        temp = national_total.copy()
        temp.rename(columns={"Total_GHG_Emissions_Excluding_LUCF_MtCO2e":"Total_supra_GHG_Emissions_Excluding_LUCF_MtCO2e",
                             "Total_CO2_Emissions_Excluding_LUCF_MtCO2e":"Total_supra_CO2_Emissions_Excluding_LUCF_MtCO2e"}, 
                    inplace=True)

        emissions_share = emissions_share.merge(temp, left_on=["supra_jur", "year"], right_on=["jurisdiction", "year"], how='left')
        emissions_share.drop(["jurisdiction_y"], axis=1, inplace=True)
        emissions_share.rename(columns={"jurisdiction_x":"jurisdiction"}, inplace=True)

        share_vars_map["CO2_supraGHG"] = "Total_supra_GHG_Emissions_Excluding_LUCF_MtCO2e"
        share_vars_map["CO2_supraCO2"] = "Total_supra_GHG_Emissions_Excluding_LUCF_MtCO2e"
    
    ret_df_vars = list(emissions.columns)
    ret_df_vars.remove("CO2_emissions")
    
    for var in share_vars_map.keys():
        emissions_share[var] = emissions_share.CO2_emissions/(emissions_share[share_vars_map[var]])

    emissions_share = emissions_share[ret_df_vars+list(share_vars_map.keys())]
    
    try:
        emissions_share = emissions_share[~emissions_share["Product"].isin(["Total","Other"])]
    except:
        pass

    #Drop the "World" jurisdiction from dataframe - keeping only national jurisdiction
    emissions_share = emissions_share.loc[emissions_share.jurisdiction != "World"]
    
    return emissions_share


# World sectors

# Merge of 'Main_sectors.csv' and 'CAIT_Country_GHG_Emissions_TotEm.csv'. 
# Merge according to two keys, Country and Year, since the total yearly emissions figure for a given country and year is the same across Flows (sectors) and products (fuels). Output file: 'IEA_Em_share.csv'
    
def emissions_share_sectors(emissions, sectors_wld_total, jur_level=None):
    if jur_level == "national":
        inventory_temp = emissions[["jurisdiction", "year", "ipcc_code", "iea_code", "Product", "CO2_emissions"]]
    if jur_level == "subnational":
        inventory_temp = emissions[["jurisdiction", "year", "ipcc_cat_code", "iea_code", "CO2_emissions"]]
        
    emissions_sect_share = pd.merge(inventory_temp, sectors_wld_total, how='left', on=['ipcc_code', 'year'])

    emissions_sect_share["co2_wld_sect_wldCO2"] = emissions_sect_share.CO2_emissions_x/emissions_sect_share.CO2_emissions_y
    emissions_sect_share.rename(columns={"CO2_emissions_x":"CO2_emissions"}, inplace=True)
    emissions_sect_share.drop(["CO2_emissions_y"], axis=1, inplace=True)

    return emissions_sect_share
