#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 10:30:44 2022

@author: gd
"""

import pandas as pd
import copy

def overlap(inst_df):
    
    ## LOAD OVERLAP DATAFRAMES
    overlap = pd.read_csv("/Users/gd/GitHub/WorldCarbonPricingDatabase/_raw/overlap/overlap_mechanisms.csv")
    
    ## CREATE OVERLAP COLUMNS
    # Encode overlap as binary variable at jurisdiction-year-sector-product level using wcpd_all and overlapping mechanisms file
    # create as many columns as there are possible overlapping pairs 
    
    inst_df_ids = inst_df[["jurisdiction", "year", "ipcc_code", "iea_code", "Product", "tax_id", "ets_id"]]
    
    tax_columns = {"tax":"tax_id"}
    ets_columns = {"ets":"ets_id"} #"ets_II":"ets_II_id"
    
    # Overlap identification columnns
    ovp_columns = {}
    
    for i in tax_columns.keys():
        for j in ets_columns.keys():
            inst_df_ids.loc[:, "overlap_"+i+"_"+j] = 0
            inst_df_ids.loc[:, "overlap_"+i+"_"+j+"_ids"] = inst_df_ids.loc[:, tax_columns[i]] + inst_df_ids.loc[:, ets_columns[j]]
    
            ovp_columns["overlap_"+i+"_"+j] = "overlap_"+i+"_"+j+"_ids"
    
    # Creating a new dataframe containing unique [inst_1, inst_2, ipcc_code entries]
    overlap_unique = overlap.drop_duplicates(["inst_1", "inst_2", "ipcc_code"]) 
    
    for ovp_col in ovp_columns.keys():
        for index, row in overlap_unique.iterrows():
            overlap = copy.deepcopy(overlap)
    
            # extracting the years in which an overalp exists for any pair of schemes
            years = overlap.loc[(overlap.inst_1 == row.inst_1) & (overlap.inst_2 == row.inst_2) & (overlap.ipcc_code == row.ipcc_code), "year"].unique()
    
            row_sel = (inst_df_ids[ovp_columns[ovp_col]].str.contains(row.inst_1)) & (inst_df_ids[ovp_columns[ovp_col]].str.contains(row.inst_2)) & (inst_df_ids.ipcc_code==row.ipcc_code) & (inst_df_ids.year.isin(years))
            inst_df_ids.loc[row_sel, ovp_col] = 1
    
        inst_df_ids.drop(ovp_columns[ovp_col], axis=1, inplace=True)
    
    # merge overlap df into cp df
    inst_df = inst_df.merge(inst_df_ids, on=['jurisdiction', 'year', 'ipcc_code', 'iea_code', 'Product', 'tax_id', 'ets_id'])

    
    return inst_df