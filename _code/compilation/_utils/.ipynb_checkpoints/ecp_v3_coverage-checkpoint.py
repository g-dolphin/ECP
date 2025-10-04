#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 10:32:46 2022

@author: gd
"""

import pandas as pd

# This function combines emissions share dataframes with institutional data
# and calculates 'adjusted' coverage based on sector-specific coverage factor.

# (check that merge dataframes have the same length as the `_share` dataframes)

# Subnational emissions data currently used is disaggragated at the sector level (not sector-fuel). 
# The coverage dummy used to determine sector-level coverage is the sector-level one. 
# This is however not a problem since all US and Canadian subnational pricing schemes (at least in the US) cover all fuels at the same rate.

#**To calculate national-level coverage and average price figures from subnational schemes:**
#1. Create new subnat dataframes with national level emissions total (keeping the same column names, etc)
#2. Calculate emissions shares using the `emissions_share()` function
#3. Carry over these new dataframes in the subsequent steps of the script

#Function pairing `_share` dataframes with coverage dummies
def coverage(inventory, inv_end_year, wcpd_end_year, wcpd_df, overlap_df,
             int_sectors=bool, jur_level=None, scope_year=None):

    wcpd_temp = pd.DataFrame()

    # Select subset of institutional design dataframe 
    if scope_year != None:
        wcpd_temp = wcpd_df.loc[wcpd_df.year==scope_year, :].copy()
    else:
        wcpd_temp = wcpd_df.copy()

    # Assign emissions from the last inventory year to subsequent years
    inventory_temp = inventory.loc[inventory.year<=inv_end_year, :].copy()

    for yr in range(inv_end_year+1, wcpd_end_year+1):
        temp = inventory.loc[inventory.year==inv_end_year, :].copy()
        temp["year"].replace(to_replace={inv_end_year:yr}, inplace=True)
        inventory_temp = pd.concat([inventory_temp, temp])

    # scheme_id and coverage factor columns - sorting lists is needed to ensure dic keys are matched with correct entries
    scheme_id_cols = [x for x in wcpd_df.columns if x.endswith("_id")==True]
    scheme_id_cols.sort()
    scheme_cf_cols = [x for x in wcpd_df.columns if x.endswith("cf")==True]
    scheme_cf_cols.sort()
    overlap_cols = [x for x in wcpd_temp.columns if x.startswith("overlap_") ==True]

    coverage_factor = dict(zip(scheme_id_cols, scheme_cf_cols))

    if int_sectors == True: 
        emissions_cols = ["co2_wld_sect_wldCO2"]
    elif jur_level=="national":
        emissions_cols = ['CO2_jurGHG', 'CO2_jurCO2', 'CO2_wldGHG', 'CO2_wldCO2']
    else:        
        emissions_cols = ['CO2_jurGHG', 'CO2_jurCO2', 'CO2_wldGHG', 'CO2_wldCO2', 'CO2_supraGHG', 'CO2_supraCO2']

    # national jurisdictions
    if jur_level=="national": 
        wcpd_keys = sorted(["jurisdiction", "year", 'ipcc_code', "iea_code", "Product"])
        wcpd_cols = wcpd_keys+["ets", "tax"]+overlap_cols+scheme_id_cols+scheme_cf_cols
        wcpd_temp = wcpd_temp[wcpd_cols]

        df_keys = sorted(list(set(inventory_temp.columns)-set(emissions_cols+["CO2_emissions"]))) 
        #NB: The order of the elements in these lists matters! There must be a one to one correspondence between their respective elements

    # subnational jurisdictions
    # Select which fuel-level coverage dummy to use from institutional file
    if jur_level=="subnational": 

        wcpd_temp = wcpd_temp[wcpd_temp.Product=="Natural gas"]
        wcpd_temp.drop(["Product"], axis=1, inplace=True)

        wcpd_keys = sorted(["jurisdiction", "year", 'ipcc_code', "iea_code"])
        wcpd_cols = wcpd_keys+["ets", "tax"]+overlap_cols+scheme_id_cols+scheme_cf_cols

        wcpd_temp = wcpd_temp[wcpd_cols]

        df_keys = sorted(list(set(inventory_temp.columns)-set(emissions_cols+["supra_jur", "CO2_emissions"]))) 

    # Adjust list of merge keys in case we want to calculate fixed scope coverage
    if scope_year != None:
        df_keys.remove('year')
        wcpd_keys.remove('year')

        wcpd_temp.drop(["year"], axis=1, inplace=True)

    temp = inventory_temp.merge(wcpd_temp, 
                               how='left', 
                               left_on=df_keys,
                               right_on=wcpd_keys)           

    #because two IPCC sectors might have the same IEA_CODE, the above merge command leads to a duplication of these entries. 
    #We need keep only one of these
    if scope_year != None:
        temp.drop_duplicates(subset=df_keys+["year"], inplace=True)
    else:
        temp.drop_duplicates(subset=df_keys, inplace=True)

    # create column with smallest coverage_factor (to calculate overlap); currently between tax and ets; ultimately should cover all schemes
    temp["cf_min"] = temp[["tax", "ets"]].min(axis=1)

    binary = {}
    for i in scheme_id_cols:
        if i.startswith("tax")==True:
            binary[i] = "tax"
        if i.startswith("ets")==True:
            binary[i] = "ets"
    
    # calculation of overlap
    for var in emissions_cols:
        for scheme in scheme_id_cols: # schemes_cols contains id's of all schemes
            temp["cov"+"_"+scheme[:-3]+"_"+var] = temp[binary[scheme]]*temp[coverage_factor[scheme]]*temp[var]

            temp["cov"+"_overlap_"+var] = temp["cf_min"]*temp["overlap_tax_ets"]*temp[var]

        coverage_cols = [x for x in temp.columns if "cov" in x]

    if scope_year != None:
        temp = temp[wcpd_keys+["year"]+scheme_id_cols+coverage_cols]
    else:
        temp = temp[wcpd_keys+scheme_id_cols+coverage_cols]


    return temp