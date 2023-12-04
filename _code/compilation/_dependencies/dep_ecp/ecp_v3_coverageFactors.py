#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 10:05:24 2022

@author: gd
"""

from importlib.machinery import SourceFileLoader

path_dependencies = '/Users/gd/GitHub/ECP/_code/compilation/_dependencies/dep_ecp'
ecp_general = SourceFileLoader('general_func', path_dependencies+'/ecp_v3_gen_func.py').load_module()

def coverageFactors(inst_df, gas):
    
    tax_id_cols = [x for x in inst_df.columns if x.startswith("tax_") and x.endswith("_id")]
    ets_id_cols = [x for x in inst_df.columns if x.startswith("ets_") and x.endswith("_id")]
    
    ## LOAD COVERAGE FACTORS FILES 
    coverageFactor = ecp_general.concatenate("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/coverageFactor")
    coverageFactor = coverageFactor[["scheme_id", "jurisdiction", "year", "ipcc_code", "cf_"+gas]]
    

    if len(coverageFactor[coverageFactor.duplicated(keep=False)]) != 0:
        print("The coverageFactor dataframe contains duplicates! Correct before proceeding further.")

    else:
        ## CREATE ONE COVERAGE FACTOR, "cf", COLUMN IN `wcpd_all` DATAFRAME FOR EACH PRICING MECHANISM COLUMN
        ### i.e., tax_cf, tax_II_cf,..., ets_cf, ets_II_cf; NOTE: the WCPD dataset currently has one tax column and one ets column 
        ### but eventually would have more of each instrument type

        # merge on [jurisdiction, year, ipcc_code, scheme_id]
        mechanism_id_cols = ["ets_id", "ets_2_id", "tax_id", "tax_2_id"]

        cf_col_names = dict(zip(mechanism_id_cols, ["ets_cf", "ets_2_cf", "tax_cf", "tax_2_cf"]))

        cf_cols = []

        for id_col_name in mechanism_id_cols:
            if id_col_name in inst_df.columns:

                merge_keys = ["jurisdiction", "year", "ipcc_code"] + [id_col_name]

                inst_df = inst_df.merge(coverageFactor, left_on=merge_keys,
                                        right_on=["jurisdiction", "year", "ipcc_code", "scheme_id"], how="left")
                inst_df.drop(["scheme_id"], axis=1, inplace=True)
                inst_df.rename(columns={"cf_"+gas:cf_col_names[id_col_name]}, inplace=True)

                cf_cols = cf_cols + [cf_col_names[id_col_name]]

        # re-ordering columns
        # error handling introduced to deal with absence of 'iea_code' in 'overlap' script dataframe
        try:
            inst_df = inst_df[['jurisdiction', 'year', 'ipcc_code', 'iea_code', 'Product', 'tax',
                            'ets']+[tax_id_cols[0]]+['tax_rate_excl_ex_clcu', 'tax_ex_rate',
                            'tax_rate_incl_ex_clcu', 'tax_curr_code']+[ets_id_cols[0]]+['ets_price',
                            'ets_curr_code']+[ets_id_cols[1]]+['ets_2_price',
                            'ets_2_curr_code']+cf_cols]
        except:
            inst_df = inst_df[['jurisdiction', 'year', 'ipcc_code', 'Product', 'tax',
                            'ets']+[tax_id_cols[0]]+['tax_rate_excl_ex_clcu', 'tax_ex_rate',
                            'tax_rate_incl_ex_clcu', 'tax_curr_code']+[ets_id_cols[0]]+['ets_price',
                            'ets_curr_code']+[ets_id_cols[1]]+['ets_2_price',
                            'ets_2_curr_code']+cf_cols]

    return inst_df