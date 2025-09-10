#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 09:27:32 2022

@author: gd
"""

import pandas as pd

# EMISSIONS SHARES

# National jurisdictions

def emissions_share(emissions, jur_tot_emissions, world_total, gas, national_total=None, 
                    jur_level = "national"): #, unit = None
    # only country and year are used as keys, meaning that all sectors and fuel types within a same country and for a given year 
    # receive the same 'total GHG' figure

    temp_jur = jur_tot_emissions[["jurisdiction", "year", gas, "all_GHG"]]
    print("temp_jur columns:", temp_jur.columns)
    temp_wld = world_total[["year", gas, "all_GHG"]]

    temp_jur = temp_jur.rename(columns={gas:gas+"_nat", "all_GHG":"all_GHG_nat"})
    temp_wld = temp_wld.rename(columns={gas:gas+"_wld", "all_GHG":"all_GHG_wld"})
    print("temp_wld", temp_wld.columns)

    emissions[gas] = pd.to_numeric(emissions[gas], errors='coerce')

    emissions_share = pd.merge(emissions, temp_jur, how='left', on=['jurisdiction','year'])
    print("emissions_share columns after merge with temp_jur:", emissions_share.columns)
    emissions_share = pd.merge(emissions_share, temp_wld, how='left', on=['year'])
    print("emissions_share columns after merge with temp_wld:", emissions_share.columns)
    
    
    share_vars_map = {gas+"_jurGHG":"all_GHG_nat", 
                      gas+"_jur"+gas:gas+"_nat", 
                      gas+"_wldGHG":"all_GHG_wld", 
                      gas+"_wld"+gas:gas+"_wld"}
    
    if jur_level == "subnational":
        temp = national_total.copy()
        temp.drop(["ipcc_code"], axis = 1, inplace=True) 
        temp.rename(columns={"all_GHG":"supra_all_GHG",
                             gas:"supra_"+gas}, 
                    inplace=True)

        emissions_share = emissions_share.merge(temp, left_on=["supra_jur", "year"], right_on=["jurisdiction", "year"], how='left')
        emissions_share.drop(["jurisdiction_y"], axis=1, inplace=True)
        emissions_share.rename(columns={"jurisdiction_x":"jurisdiction"}, inplace=True)

        share_vars_map[gas+"_supraGHG"] = "supra_all_GHG"
        share_vars_map[gas+"_supra"+gas] = "supra_"+gas
    
    ret_df_vars = list(emissions.columns)
    ret_df_vars.remove(gas)
    
    for var in share_vars_map.keys():
        print(var)
        emissions_share[var] = emissions_share[gas]/(emissions_share[share_vars_map[var]])
        print(f"Completed {var}")

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
    
def emissions_share_wld_sectors(emissions, sectors_wld_total, gas, jur_level=None):
    
    emissions[gas] = pd.to_numeric(emissions[gas], errors='coerce')
    sectors_wld_total[gas] = pd.to_numeric(sectors_wld_total[gas], errors='coerce')
    
    if jur_level == "national" and gas == "CO2":
        inventory_temp = emissions[["jurisdiction", "year", "ipcc_code", "iea_code", "Product", gas]]
    else:
        if jur_level == "subnational":
            inventory_temp = emissions[["jurisdiction", "year", "ipcc_code", "iea_code", gas]]
        else:
            inventory_temp = emissions[["jurisdiction", "year", "ipcc_code", "iea_code", gas]]

    emissions_sect_share = pd.merge(inventory_temp, sectors_wld_total, how='left', on=['ipcc_code', 'year'])
    emissions_sect_share.rename(columns={gas+"_x":gas, gas+"_y":gas+"_wldSect"}, inplace=True)

    emissions_sect_share[gas+"_wld_sect_wld"+gas] = emissions_sect_share[gas]/emissions_sect_share[gas+"_wldSect"]
    emissions_sect_share.drop([gas+"_wldSect"], axis=1, inplace=True)

    return emissions_sect_share


# Share of subnational sector-level emissions in corresponding country-sector-level emissions

# sectors_ctry_total contains total emissions at country-sector level; `sectors_ctry_total` created in script ecp_v3.ipynb

def emissions_share_ctry_sectors(emissions, sectors_ctry_total, gas):
    
    emissions[gas] = pd.to_numeric(emissions[gas], errors='coerce')
    sectors_ctry_total[gas] = pd.to_numeric(sectors_ctry_total[gas], errors='coerce')

    inventory_temp = emissions[["supra_jur", "jurisdiction", "year", "ipcc_code", "iea_code", gas]]

    emissions_sect_share = pd.merge(inventory_temp, sectors_ctry_total, how='left', 
                                    left_on=['supra_jur', 'year', 'ipcc_code'], right_on=['jurisdiction', 'year', 'ipcc_code'])
    emissions_sect_share.rename(columns={gas+"_x":gas, gas+"_y":gas+"_ctrySect", "jurisdiction_x":"jurisdiction"}, 
                                inplace=True)

    emissions_sect_share[gas+"_ctry_sect_ctry"+gas] = emissions_sect_share[gas]/emissions_sect_share[gas+"_ctrySect"]
    emissions_sect_share.drop([gas+"_ctrySect", "jurisdiction_y"], axis=1, inplace=True)

    return emissions_sect_share