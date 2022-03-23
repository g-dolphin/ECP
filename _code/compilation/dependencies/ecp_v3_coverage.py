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
def coverage(df_em_share, last_inv_year, last_cp_year, wcpd_all, overlap,
             sectors=bool, jur_level=None, scope_year=None):

    cp_temp = pd.DataFrame()
    
    # Select institutional data frame
    if scope_year != None:
        cp_temp = wcpd_all.loc[wcpd_all.year==scope_year, :]
    else:
        cp_temp = wcpd_all.copy()
    
    # Assign last inventory year emissions shares to years beyond last year of inventory
    em_share_temp = df_em_share.copy()
    em_share_temp = em_share_temp.loc[em_share_temp.year<=last_inv_year, :]
    
    for yr in range(last_inv_year+1, last_cp_year+1):
        temp = em_share_temp.loc[em_share_temp.Year==last_inv_year, :].copy()
        temp["year"].replace(to_replace={last_inv_year:yr}, inplace=True)
        
        em_share_temp = pd.concat([em_share_temp, temp])

    # scheme_id and cf columns
    scheme_id_cols = [x for x in wcpd_all.columns if "_id" in x]
    scheme_cf_cols = [x for x in wcpd_all.columns if "cf" in x]
    
    coverage_factor = dict(zip(scheme_id_cols, scheme_cf_cols))
    
    # scheme dummies
    dummy = {}
    for col in scheme_id_cols:
        if "tax" in col: 
            dummy[col] = "tax"
        if "ets" in col:
            dummy[col] = "ets"
    
    # national jurisdictions
    if jur_level=="national": 
        cp_keys = sorted(["jurisdiction", "year", 'ipcc_code', "iea_code", "Product"])
        cp_cols = cp_keys+["tax", "ets", "overlap_tax_ets"]+scheme_id_cols+scheme_cf_cols
        cp_temp = cp_temp[cp_cols] 

        if sectors == False:
            emissions_cols = ['CO2_jurGHG', 'CO2_jurCO2', 'CO2_wldGHG', 'CO2_wldCO2']
        if sectors == True: 
            emissions_cols = ["co2_wld_sect_wldCO2"]
            
        df_keys = sorted(list(set(em_share_temp.columns)-set(emissions_cols+["CO2_emissions"]))) #The order of the elements in these lists matters! There must be a one to one correspondence between their respective elements
        
    # subnational jurisdictions
    # Select which fuel-level coverage dummy to use from institutional file
    if jur_level=="subnational": 

        cp_temp = cp_temp[cp_temp.Product=="Natural gas"]
        cp_temp.drop(["Product"], axis=1, inplace=True)
        
        cp_keys = sorted(["jurisdiction", "year", 'ipcc_code', "iea_code"])
        cp_cols = cp_keys+["tax", "ets", "overlap_tax_ets"]+scheme_id_cols+scheme_cf_cols

        cp_temp = cp_temp[cp_cols]
        
        if sectors == False:        
            emissions_cols = ['CO2_jurGHG', 'CO2_jurCO2', 'CO2_wldGHG', 'CO2_wldCO2', 'CO2_supraGHG', 'CO2_supraCO2']
        if sectors == True: 
            emissions_cols = ["co2_wld_sect_wldCO2"]
        
        df_keys = sorted(list(set(em_share_temp.columns)-set(emissions_cols+["supra_jur", "CO2_emissions"]))) 

    # Adjust list of merge keys in case we want to calculate fixed scope coverage
    if scope_year != None:
        df_keys.remove('year')
        cp_keys.remove('year')
        
        cp_temp.drop(["year"], axis=1, inplace=True)

    temp = em_share_temp.merge(cp_temp, 
                               how='left', 
                               left_on=df_keys,
                               right_on=cp_keys)           
    
    #because two IPCC sectors might have the same IEA_CODE, the above merge command leads to a duplication of these entries. 
    #We need keep only one of these
    if scope_year != None:
        temp.drop_duplicates(subset=df_keys+["year"], inplace=True)
    else:
        temp.drop_duplicates(subset=df_keys, inplace=True)
        
    # create column with largest coverage_factor - to calculate overlap
    temp["cf_min"] = temp[["tax_cf", "ets_cf"]].min(axis=1)
        
    # calculation of overlap
    for var in emissions_cols:
        for scheme in scheme_id_cols: # schemes_cols contains id's all schemes
            temp["cov"+"_"+scheme[:-3]+"_"+var] = temp[dummy[scheme]]*temp[coverage_factor[scheme]]*temp[var]
            # scheme[:-10] removes "_id" from name of coverage columns
            
            temp["cov"+"_overlap_"+var] = temp["cf_min"]*temp["overlap_tax_ets"]*temp[var]
    
    coverage_cols = [x for x in temp.columns if "cov" in x]
    
    if scope_year != None:
        temp = temp[cp_keys+["year"]+scheme_id_cols+coverage_cols]
    else:
        temp = temp[cp_keys+scheme_id_cols+coverage_cols]

        
    return temp