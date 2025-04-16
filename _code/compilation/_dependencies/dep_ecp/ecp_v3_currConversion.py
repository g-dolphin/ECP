#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 17:00:28 2022

@author: gd
"""

import os
import pandas as pd
import numpy as np
import re

from importlib.machinery import SourceFileLoader

path_dependencies = '/Users/gd/GitHub/ECP/_code/compilation/_dependencies/dep_ecp'
ecp_general = SourceFileLoader('general_func', path_dependencies+'/ecp_v3_gen_func.py').load_module()

path_git_data = "/Users/gd/GitHub/ECP/_raw"

## Emissions prices and rates conversion

def cur_conv(wcpd_all, gas, 
             subnat_can_list, subnat_usa_list, subnat_chn_list,
             xRateFixed,
             baseYear=None):    
    
    #Loading and formatting x-rate dataframe
    x_rate = pd.read_csv("/Users/gd/GitHub/ECP/_raw/wb_rates/xRate_bis.csv")

#    iso3_wb_map={
#        'Antigua And Barbuda':'Antigua and Barbuda',
#        'Bahamas (The)':'Bahamas, The',
#        'Bolivia (Plurinational State Of)':'Bolivia',
#        'Bosnia And Herzegovina':'Bosnia and Herzegovina',
#        'Central African Republic (The)':'Central African Republic',
#        'Comoros (The)':'Comoros',
#        'Congo (The Democratic Republic Of The)':'Congo, Dem. Rep.',
#        'Congo (The)':'Congo, Rep.',
#        'Czechia':'Czech Republic',
#        "Côte D'Ivoire":"Cote d'Ivoire",
#        'Dominican Republic (The)':'Dominican Republic',
#        'Egypt':'Egypt, Arab Rep.',
#        'Gambia (The)':'Gambia, The',
#        'Hong Kong':'Hong Kong SAR, China',
#        'Iran (Islamic Republic Of)':'Iran, Islamic Rep.',
#        'Korea (The Democratic People’S Republic Of)':'Korea, Dem. Rep.',
#        'Korea (The Republic Of)':'Korea, Rep.',
#        'Kyrgyzstan':'Kyrgyz Republic',
#        'Lao People’S Democratic Republic (The)':'Lao PDR',
#        'Macao':'Macao SAR, China',
#        'Marshall Islands (The)':'Marshall Islands',
#        'Micronesia (Federated States Of)':'Federated States of Micronesia',
#        'Moldova (The Republic Of)':'Moldova',
#        'Netherlands (The)':'Netherlands',
#        'Niger (The)':'Niger',
#        'North Macedonia':'Macedonia, FYR',
#        'Philippines (The)':'Philippines',
#        'Russian Federation (The)':'Russian Federation',
#        'Saint Kitts And Nevis':'St. Kitts and Nevis',
#        'Saint Lucia':'St. Lucia',
#        'Saint Vincent And The Grenadines':'St. Vincent and the Grenadines',
#        'Sao Tome And Principe':'Sao Tome and Principe',
#        'Slovakia':'Slovak Republic',
#        'Sudan (The)':'Sudan',
#        'Taiwan (Province Of China)':'Taiwan, China',
#        'Tanzania, United Republic Of':'Tanzania',
#        'Trinidad And Tobago':'Trinidad and Tobago',
#        'United Arab Emirates (The)':'United Arab Emirates',
#        'United Kingdom Of Great Britain And Northern Ireland (The)':'United Kingdom',
#        'United States Of America (The)':'United States',
#        'Venezuela (Bolivarian Republic Of)':'Venezuela, RB',
#        'Viet Nam':'Vietnam',
#        'Yemen':'Yemen, Rep.'}

#    x_rate.loc[:, "jurisdiction"] = x_rate.loc[:, "jurisdiction"].replace(to_replace=iso3_wb_map)

    # GDP deflator
    gdp_dfl = ecp_general.wb_series("GDP deflator: linked series (base year varies by country)", "gdp_dfl")
    gdp_dfl = gdp_dfl.loc[(gdp_dfl.year>=1985) & (gdp_dfl.year<=2023),:]
    gdp_dfl.to_csv(path_git_data+'/wb_rates/gdp_dfl.csv', index=None)

    gdp_dfl_ii = pd.DataFrame()

    ## GDP deflator ratios
    for jur in gdp_dfl.jurisdiction.unique():
        temp = gdp_dfl.loc[(gdp_dfl.jurisdiction==jur), :]
        gdp_dfl_base_yr = gdp_dfl.loc[(gdp_dfl.jurisdiction==jur) & (gdp_dfl.year==baseYear), :]
        gdp_dfl_base_yr.rename(columns={"gdp_dfl":"gdp_dfl_by"}, inplace=True)
        gdp_dfl_base_yr.drop(["year"], axis=1, inplace=True)

        temp = temp.merge(gdp_dfl_base_yr, on=["jurisdiction"], how='left')
        temp["base_year_ratio"] = temp.gdp_dfl_by /temp.gdp_dfl

        if gdp_dfl_ii.empty==True:
            gdp_dfl_ii = temp
        else:
            gdp_dfl_ii = pd.concat([gdp_dfl_ii, temp])

    gdp_dfl = gdp_dfl_ii

    # need to adjust the deflator ratios dataframe so that it includes inflation rates for subnational jurisditions.
    # assuming national inflation rate for subnational entities - might be worth updating to entity-specific rates

    for jur in subnat_can_list: 
        temp_df = gdp_dfl.loc[gdp_dfl.jurisdiction=="Canada", :].copy()
        temp_df["jurisdiction"].replace(to_replace={"Canada":jur}, inplace=True)
        
        gdp_dfl = pd.concat([gdp_dfl, temp_df])
        
    for jur in subnat_usa_list:
        temp_df = gdp_dfl.loc[gdp_dfl.jurisdiction=="United States", :].copy()
        temp_df["jurisdiction"].replace(to_replace={"United States":jur}, inplace=True)
        
        gdp_dfl = pd.concat([gdp_dfl, temp_df])

    for jur in subnat_chn_list:
        temp_df = gdp_dfl.loc[gdp_dfl.jurisdiction=="China", :].copy()
        temp_df["jurisdiction"].replace(to_replace={"China":jur}, inplace=True)
        
        gdp_dfl = pd.concat([gdp_dfl, temp_df])

    # temp fix for year 2024
    gdp_dfl_2024 = gdp_dfl.loc[gdp_dfl.year==2023]
    gdp_dfl_2024["year"] = 2024

    gdp_dfl = pd.concat([gdp_dfl, gdp_dfl_2024])

    gdp_dfl.to_csv(path_git_data+'/wb_rates/gdp_dfl_ratio.csv', index=None)


    # Add x-rate dataframe and gdp deflator dataframes to cp dataframe
    wcpd_usd = wcpd_all.copy()

    wcpd_usd.rename(columns={"ets_price":"ets_price_clcu",
                                "ets_2_price":"ets_2_price_clcu"}, inplace=True)

    dic_keys = [x for x in wcpd_all.columns if "curr_code" in x]
    dic_values = [x[:-4]+"x_rate" for x in wcpd_all.columns if "curr_code" in x]

    curr_code_map = dict(zip(dic_keys, dic_values))

    #Select x-rate assumption
    if xRateFixed == True:
        x_rate = x_rate.loc[x_rate.year==2019,:]
        x_rate.drop(["year"], axis=1, inplace=True)

    # Merge `x_rate` with `cur_code`
#    x_rate = x_rate.merge(cur_code, on="jurisdiction", how="left")    
#    x_rate.dropna(inplace=True)

    if xRateFixed == True:
        x_rate.drop_duplicates(["currency_code"], inplace=True)
    else:
        x_rate.drop_duplicates(["currency_code", "year"], inplace=True)

    x_rate.drop("jurisdiction", axis=1, inplace=True)

    for name in curr_code_map.keys():
        if xRateFixed == True:
            wcpd_usd = pd.merge(wcpd_usd, x_rate, how='left', left_on=[name], right_on=['currency_code'])
        else:
            wcpd_usd = pd.merge(wcpd_usd, x_rate, how='left', left_on=[name, "year"], right_on=['currency_code', "year"])

        wcpd_usd.rename(columns={"x-rate":curr_code_map[name]}, inplace=True)
        wcpd_usd.drop("currency_code", axis=1, inplace=True)

    wcpd_usd = wcpd_usd.merge(gdp_dfl[["jurisdiction", "year", "base_year_ratio"]], on=["jurisdiction", "year"], how="left")


    price_columns = [x for x in wcpd_usd.columns if bool(re.match(re.compile("ets.+price"), x))==True or bool(re.match(re.compile("tax.+rate_incl+."), x))==True]

    x_rate_dic = dict(zip(price_columns, dic_values))

    # Calculate current USD (fixed x-rate), current USD (variable x-rate) or constant USD values for all schemes
    if baseYear==None and xRateFixed==False:
        # create names of new columns
        price_columns_usd = [x[:-5]+"_usd" for x in wcpd_usd.columns if bool(re.match(re.compile("ets.+price"), x))==True or bool(re.match(re.compile("tax.+rate_incl+."), x))==True]
        price_cols_dic = dict(zip(price_columns, price_columns_usd))

        for key in price_cols_dic.keys():
            wcpd_usd.loc[:, price_cols_dic[key]] = wcpd_usd.loc[:, key]*(1/wcpd_usd.loc[:, x_rate_dic[key]])

        versionID = 'cFlxRate'
        path = "currentPrices/FlexXRate"

    if baseYear==None and xRateFixed==True:
        # create names of new columns
        price_columns_usd = [x[:-5]+"_usd" for x in wcpd_usd.columns if bool(re.match(re.compile("ets.+price"), x))==True or bool(re.match(re.compile("tax.+rate_incl+."), x))==True]
        price_cols_dic = dict(zip(price_columns, price_columns_usd))

        for key in price_cols_dic.keys():
            wcpd_usd.loc[:, price_cols_dic[key]] = wcpd_usd.loc[:, key]*(1/wcpd_usd.loc[:, x_rate_dic[key]])

        versionID = 'cFixRate'
        path = "currentPrices/FixedXRate"

    if baseYear!=None and xRateFixed==False:
        # create names of new columns
        price_columns_usd = [x[:-5]+"_usd_k" for x in wcpd_usd.columns if bool(re.match(re.compile("ets.+price"), x))==True or bool(re.match(re.compile("tax.+rate_incl+."), x))==True]
        price_cols_dic = dict(zip(price_columns, price_columns_usd))

        for key in price_cols_dic.keys():
            wcpd_usd.loc[:, price_cols_dic[key]] = wcpd_usd.loc[:, key]*(1/wcpd_usd.loc[:, x_rate_dic[key]])*wcpd_usd.loc[:, "base_year_ratio"]
        
        versionID = 'kFlxRate'
        path = "constantPrices/FlexXRate"

    if baseYear!=None and xRateFixed==True:
        # create names of new columns
        price_columns_usd = [x[:-5]+"_usd_k" for x in wcpd_usd.columns if bool(re.match(re.compile("ets.+price"), x))==True or bool(re.match(re.compile("tax.+rate_incl+."), x))==True]
        price_cols_dic = dict(zip(price_columns, price_columns_usd))

        for key in price_cols_dic.keys():
            wcpd_usd.loc[:, price_cols_dic[key]] = wcpd_usd.loc[:, key]*(1/wcpd_usd.loc[:, x_rate_dic[key]])*wcpd_usd.loc[:, "base_year_ratio"]
        
        versionID = 'kFixRate'
        path = "constantPrices/FixedXRate"

    # jurisdiction names
    std_jur_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in wcpd_usd.jurisdiction.unique()]
    jur_dic = dict(zip(wcpd_usd.jurisdiction.unique(), std_jur_names))

    # remove all files from directory before writing new ones to avoid leaving behind legacy files
    directory = path_git_data+'/wcpd_usd/'+gas+'/'+path
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))

    # write files
    col_sel = ['jurisdiction', 'year', 'ipcc_code', 'iea_code', 'Product']+list(price_cols_dic.keys())+list(curr_code_map.keys())+list(price_cols_dic.values())+list(x_rate_dic.values())

    for jur in wcpd_usd.jurisdiction.unique():
        wcpd_usd.loc[wcpd_usd.jurisdiction==jur][col_sel].to_csv(path_git_data+'/wcpd_usd/'+gas+"/"+path+'/prices_usd_'+versionID+"_"+gas+'_'+jur_dic[jur]+'.csv', index=None)
        
            
    return wcpd_usd