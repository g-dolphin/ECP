#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 17:00:28 2022

@author: gd
"""
import pandas as pd
import numpy as np
import re
import os

from importlib.machinery import SourceFileLoader

ecp_general = SourceFileLoader('general', '/Users/gd/GitHub/ECP/_code/compilation/dependencies/ecp_v3_gen_func.py').load_module()

path_git_data = '/Users/gd/GitHub/ECP/_raw'

## Emissions prices and rates conversion
# All prices converted to [2019] USD

def cur_conv(wcpd_all, inv_can, inv_usa, inv_chn):    
 
    #Loading and formatting x-rate dataframe
    
    x_rate = ecp_general.wb_series("Official exchange rate (LCU per US$, period average)", "official_x_rate")    
        
    #Select [2019] x-rate
    x_rate = x_rate.loc[x_rate.year==2019,:]
    x_rate.drop(["year"], axis=1, inplace=True)
    
    # Attaching currency code
    # [Make sure that the jurisdiction names are identical to World Bank names]
    cur_code = pd.read_csv(path_git_data+'/wb_rates/iso_cur_code.csv', 
                             skiprows=[0,1,2], encoding="latin-1")
    
    cur_code.drop(["Currency", "Numeric Code", "Minor unit", "Fund"], axis=1, inplace=True)
    cur_code.rename(columns={"ENTITY":"jurisdiction", "Alphabetic Code":"currency_code"}, inplace=True)
    cur_code.drop_duplicates(["jurisdiction"], inplace=True)
    
    cur_code["jurisdiction"] = cur_code["jurisdiction"].apply(lambda x: str(x).lower().title())
    cur_code.drop(cur_code.tail(10).index, inplace=True)
    
    iso3_wb_map={
     'Antigua And Barbuda':'Antigua and Barbuda',
     'Bahamas (The)':'Bahamas, The',
     'Bolivia (Plurinational State Of)':'Bolivia',
     'Bosnia And Herzegovina':'Bosnia and Herzegovina',
     'Central African Republic (The)':'Central African Republic',
     'Comoros (The)':'Comoros',
     'Congo (The Democratic Republic Of The)':'Congo, Dem. Rep.',
     'Congo (The)':'Congo, Rep.',
     'Czechia':'Czech Republic',
     "Côte D'Ivoire":"Cote d'Ivoire",
     'Dominican Republic (The)':'Dominican Republic',
     'Egypt':'Egypt, Arab Rep.',
     'Gambia (The)':'Gambia, The',
     'Hong Kong':'Hong Kong SAR, China',
     'Iran (Islamic Republic Of)':'Iran, Islamic Rep.',
     'Korea (The Democratic People’S Republic Of)':'Korea, Dem. Rep.',
     'Korea (The Republic Of)':'Korea, Rep.',
     'Kyrgyzstan':'Kyrgyz Republic',
     'Lao People’S Democratic Republic (The)':'Lao PDR',
     'Macao':'Macao SAR, China',
     'Marshall Islands (The)':'Marshall Islands',
     'Micronesia (Federated States Of)':'Federated States of Micronesia',
     'Moldova (The Republic Of)':'Moldova',
     'Netherlands (The)':'Netherlands',
     'Niger (The)':'Niger',
     'North Macedonia':'Macedonia, FYR',
     'Philippines (The)':'Philippines',
     'Russian Federation (The)':'Russian Federation',
     'Saint Kitts And Nevis':'St. Kitts and Nevis',
     'Saint Lucia':'St. Lucia',
     'Saint Vincent And The Grenadines':'St. Vincent and the Grenadines',
     'Sao Tome And Principe':'Sao Tome and Principe',
     'Slovakia':'Slovak Republic',
     'Sudan (The)':'Sudan',
     'Taiwan (Province Of China)':'Taiwan, China',
     'Tanzania, United Republic Of':'Tanzania',
     'Trinidad And Tobago':'Trinidad and Tobago',
     'United Arab Emirates (The)':'United Arab Emirates',
     'United Kingdom Of Great Britain And Northern Ireland (The)':'United Kingdom',
     'United States Of America (The)':'United States',
     'Venezuela (Bolivarian Republic Of)':'Venezuela, RB',
     'Viet Nam':'Vietnam',
     'Yemen':'Yemen, Rep.'}
    
    cur_code.loc[:, "jurisdiction"] = cur_code.loc[:, "jurisdiction"].replace(to_replace=iso3_wb_map)
    
    # Merge x_rate with cur_code
    x_rate = x_rate.merge(cur_code, on="jurisdiction", how="left")
    x_rate.dropna(inplace=True)
    x_rate.drop_duplicates(["currency_code"], inplace=True)
    
    x_rate.drop("jurisdiction", axis=1, inplace=True)
    
    # Loading and formatting inflation dataframe
    inf_rate = ecp_general.wb_series("Inflation, GDP deflator: linked series (annual %)", "inf_rate")
    inf_rate = inf_rate.loc[(inf_rate.year>=1985) & (inf_rate.year<=2020),:]
    inf_rate.to_csv(path_git_data+'/wb_rates/inf_rate.csv', index=None)
    
    
    cum_inf = pd.DataFrame()
    
    price_year = 2019
    
    for jur in inf_rate.jurisdiction.unique():
        temp = inf_rate.loc[inf_rate.jurisdiction==jur, :].copy()
        temp["cum_inf"] = np.nan
            
        for yr in temp.year.unique():
            x = 1 #initialization of cumulative inflation value
            
            if yr < price_year:
                for i in range(yr, price_year):
                    inflation = temp.loc[temp.year==i, "inf_rate"].item()
                    x = x*(1+inflation/100)
    
            if yr > price_year:
                for i in (price_year, yr):
                    inflation = temp.loc[temp.year==i, "inf_rate"].item()
                    x = x/(1+inflation/100)
        
            temp.loc[temp.year==yr, "cum_inf"] = x
        
        if cum_inf.empty==True:
            cum_inf = temp
        else:
            cum_inf = pd.concat([cum_inf, temp])
    
    # need to adjust the cum_inf dataframe so that it includes inflation rates for subnational jurisditions.
    # assuming national inflation rate for subnational entities - might be worth updating to entity-specific rates
    
    for jur in list(inv_can.jurisdiction.unique())[:-1]: # remove 'canada' entry from list
        temp_df = cum_inf.loc[cum_inf.jurisdiction=="Canada", :].copy()
        temp_df["jurisdiction"].replace(to_replace={"Canada":jur}, inplace=True)
        
        cum_inf = pd.concat([cum_inf, temp_df])
        
    for jur in list(inv_usa.jurisdiction.unique()):
        temp_df = cum_inf.loc[cum_inf.jurisdiction=="United States", :].copy()
        temp_df["jurisdiction"].replace(to_replace={"United States":jur}, inplace=True)
        
        cum_inf = pd.concat([cum_inf, temp_df])
    
    for jur in list(inv_chn.jurisdiction.unique()):
        temp_df = cum_inf.loc[cum_inf.jurisdiction=="China", :].copy()
        temp_df["jurisdiction"].replace(to_replace={"China":jur}, inplace=True)
        
        cum_inf = pd.concat([cum_inf, temp_df])
    
        
    cum_inf.to_csv(path_git_data+'/wb_rates/cum_infl.csv', index=None)
    
    
    # Add exchange rate to cp dataframe
    wcpd_usd = wcpd_all
    
    wcpd_usd.rename(columns={"ets_price":"ets_price_clcu",
                             "ets_2_price":"ets_2_price_clcu"}, inplace=True)
    
    dic_keys = [x for x in wcpd_all.columns if "curr_code" in x]
    dic_values = [x[:-4]+"x_rate" for x in wcpd_all.columns if "curr_code" in x]
    
    curr_code_map = dict(zip(dic_keys, dic_values))
    
    for name in curr_code_map.keys():
        wcpd_usd = pd.merge(wcpd_usd, x_rate, how='left', left_on=[name], right_on=['currency_code'])
        wcpd_usd.rename(columns={"official_x_rate":curr_code_map[name]}, inplace=True)
        wcpd_usd.drop("currency_code", axis=1, inplace=True)
    
    wcpd_usd = wcpd_usd.merge(cum_inf[["jurisdiction", "year", "cum_inf"]], on=["jurisdiction", "year"], how="left")
    
    price_columns = [x for x in wcpd_usd.columns if bool(re.match(re.compile("ets.+price"), x))==True or bool(re.match(re.compile("tax.+rate_incl+."), x))==True]
    price_columns_usd = [x[:-5]+"_usd" for x in wcpd_usd.columns if bool(re.match(re.compile("ets.+price"), x))==True or bool(re.match(re.compile("tax.+rate_incl+."), x))==True]
    price_columns_const_usd = [x[:-5]+"_kusd" for x in wcpd_usd.columns if bool(re.match(re.compile("ets.+price"), x))==True or bool(re.match(re.compile("tax.+rate_incl+."), x))==True]
    
    price_cols_dic = dict(zip(price_columns, price_columns_usd))
    price_const_cols_dic = dict(zip(price_columns, price_columns_const_usd))
    x_rate_dic = dict(zip(price_columns, dic_values))
    
    # Calculate USD and 2019USD values for all schemes
    for key in price_cols_dic.keys():
        wcpd_usd.loc[:, price_cols_dic[key]] = wcpd_usd.loc[:, key]*(1/wcpd_usd.loc[:, x_rate_dic[key]])
        wcpd_usd.loc[:, price_const_cols_dic[key]] = wcpd_usd.loc[:, price_cols_dic[key]]*wcpd_usd.loc[:, "cum_inf"]
        
        
    col_sel = ['jurisdiction', 'year', 'ipcc_code', 'iea_code', 'Product']+list(price_cols_dic.keys())+list(curr_code_map.keys())+list(price_cols_dic.values())+list(price_const_cols_dic.values())+list(x_rate_dic.values())
    
    std_jur_names = [x.replace(".", "").replace(",", "").replace(" ", "_") for x in wcpd_usd.jurisdiction.unique()]
    jur_dic = dict(zip(wcpd_usd.jurisdiction.unique(), std_jur_names))
    
    
    # remove all files from directory before writing new ones to avoid leaving behind legacy files
    
    directory = path_git_data+'/wcpd_usd/'
    for f in os.listdir(directory):
        os.remove(os.path.join(directory, f))
    
    # write files
    for jur in wcpd_usd.jurisdiction.unique():
        wcpd_usd.loc[wcpd_usd.jurisdiction==jur][col_sel].to_csv(path_git_data+'/wcpd_usd/prices_usd_'+jur_dic[jur]+'.csv', index=None)
        
           
    return wcpd_usd
    
    