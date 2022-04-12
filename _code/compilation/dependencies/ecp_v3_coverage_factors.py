#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 10:05:24 2022

@author: gd
"""

import pandas as pd
from importlib.machinery import SourceFileLoader

ecp_general = SourceFileLoader('general', '/Users/gd/GitHub/ECP/_code/compilation/dependencies/ecp_v3_gen_func.py').load_module()

def coverage_factors(inst_df):
    
    ## LOAD COVERAGE FACTORS FILES 
    coverage_factor = ecp_general.concatenate("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/coverage_factor")
    coverage_factor.rename(columns={"Jurisdiction":"jurisdiction","Year":"year","IPCC_code":"ipcc_code"}, inplace=True)
    coverage_factor.drop(["source", "comment"], axis=1, inplace=True)
    
    ## CREATE ONE COVERAGE FACTOR, "cf", COLUMN IN `wcpd_all` DATAFRAME FOR EACH PRICING MECHANISM COLUMN
    ### i.e., tax_cf, tax_II_cf,..., ets_cf, ets_II_cf; NOTE: the WCPD dataset currently has one tax column and one ets column 
    ### but eventually would have more of each instrument type
    
    # merge on [scheme_id, jurisdiction, year, ipcc_code]
    merge_keys = [["jurisdiction", "year", "ipcc_code", "tax_id"], ["jurisdiction", "year", "ipcc_code", "ets_id"]]
    col_names = ["tax_cf", "ets_cf"]
    i = 0
    
    for keys in merge_keys:
        inst_df = inst_df.merge(coverage_factor, left_on=keys,
                              right_on=["jurisdiction", "year", "ipcc_code", "scheme_id"], how="left")
        inst_df.drop(["scheme_id"], axis=1, inplace=True)
        inst_df.rename(columns={"em_share":col_names[i]}, inplace=True)
        i+=1
    
    # re-ordering columns
    inst_df = inst_df[['jurisdiction', 'year', 'ipcc_code', 'iea_code', 'Product', 'tax',
                     'ets', 'tax_id', 'tax_cf', 'tax_rate_excl_ex_clcu', 'tax_ex_rate',
                     'tax_rate_incl_ex_clcu', 'tax_curr_code', 'ets_id', 'ets_cf', 'ets_price',
                     'ets_curr_code']]
    
    return inst_df