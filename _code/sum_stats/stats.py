#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 15:31:38 2021

@author: gd
"""

import pandas as pd

user_root_path = "/Users/gd/GitHub"
git_repo_path = "/ECP"

output_dir = ""

df_prices_econ = pd.read_csv("/Users/gd/GitHub/ECP/_dataset/price/ecp_economy/ecp_CO2.csv")

oecd = ["United States", "Mexico", "Japan", "Germany", "Turkey", "France",
        "United Kingdom", "Italy", "Korea, Rep.", "Spain", "Poland", "Canada",
        "Australia", "Chile", "Netherlands", "Belgium", "Greece", "Czech Republic",
        "Portugal", "Sweden", "Hungary", "Austria", "Israel", "Switzerland",
        "Denmark", "Finland", "Slovak Republic", "Norway", "Ireland", "New Zealand",
        "Lithuania", "Slovenia", "Latvia", "Estonia", "Luxembourg", "Iceland"]

eu27 = ['Austria', 'Belgium', 'Bulgaria', 'Cyprus', 'Czech Republic', 'Germany', 'Denmark', 
         'Estonia', 'Greece', 'Greece', 'Spain', 'Finland', 'France', 'Croatia', 'Hungary', 
         'Ireland', 'Ireland', 'Italy', 'Lithuania', 'Luxembourg', 'Latvia', 'Malta', 'Netherlands', 
         'Poland', 'Portugal', 'Romania', 'Sweden', 'Slovenia', 'Slovakia']

oecd_subnat = [] #list of US states and Canadian provinces

middle_income = ["Angola", "Honduras", "Philippines", "Algeria", "India", "Samoa",
                 "Bangladesh", "Indonesia", "São Tomé and Principe",
                 "Belize", "Iran, Islamic Rep.", "Senegal", "Benin", "Kenya", 	
                 "Solomon Islands", "Bhutan", "Kiribati", "Sri Lanka", "Bolivia", 
                 "Kyrgyz Republic", "Tanzania", "Cabo Verde", "Lao PDR", "Tajikistan",
                 "Cambodia", "Lesotho", "Timor-Leste", "Cameroon", 	"Mauritania",
                 "Tunisia", "Comoros", 	"Micronesia, Fed. Sts.", "Ukraine",
                 "Congo, Rep.", "Mongolia", "Uzbekistan", "Cote d'Ivoire", 	"Morocco",
                 "Vanuatu", "Djibouti", "Myanmar", 	"Vietnam", "Egypt, Arab Rep.",
                 "Nepal", "West Bank and Gaza", "El Salvador", 	"Nicaragua", 
                 "Zambia", "Eswatini",	"Nigeria", "Zimbabwe", "Ghana",	
                 "Pakistan", "Haiti", "Papua New Guinea",
                 "Albania", "Gabon", "Namibia", "American Samoa", "Georgia", "North Macedonia",
                 "Argentina", "Grenada", "Panama", "Armenia", "Guatemala",
                 "Paraguay", "Azerbaijan", "Guyana", "Peru", "Belarus", "Iraq",
                 "Romania", "Bosnia and Herzegovina","﻿Jamaica", "Russian Federation",
                 "Botswana", "Jordan",	"Serbia", "Brazil",	"Kazakhstan", "South Africa",
                 "Bulgaria", "Kosovo", "St. Lucia", "China", "Lebanon", 
                 "St. Vincent and the Grenadines", "Colombia",	"Libya", "Suriname",
                 "Costa Rica",  "Malaysia", "Thailand", "Cuba", "Maldives", "Tonga",
                 "Dominica", "Marshall Islands", "Turkey", "Dominican Republic",   
                 "Mauritius", "Turkmenistan", "Equatorial Guinea", "Mexico", "Tuvalu",
                 "Ecuador",	"Moldova", "Fiji", "Montenegro"]

sum_stat = df_prices_econ.ecp_all_jurCO2_usd_k.describe()

# Country group simple average

avg_oecd = df_prices_econ.loc[(df_prices_econ.jurisdiction.isin(oecd)) & (df_prices_econ.year==2021), "ecp_all_jurCO2_usd_k"].mean()
avg_midinc = df_prices_econ.loc[(df_prices_econ.jurisdiction.isin(middle_income)) & (df_prices_econ.year==2021), "ecp_all_jurCO2_usd_k"].mean()
avg_eu27 = df_prices_econ.loc[(df_prices_econ.jurisdiction.isin(eu27)) & (df_prices_econ.year==2021), "ecp_all_jurCO2_usd_k"].mean()

# Country group emissions-weighted average prices

tot_emissions = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/source_data/ghg_inventory/raw/national/ClimateWatch/CAIT/CAIT_2021/CAIT_country_tot_2021_WBnames.csv")
 
ctryGroups = {"oecd":oecd, "MiddleIncome":middle_income, "eu27":eu27}

averageCtryGroup = {}

for ctryGroup in ctryGroups.keys():
    
    df = tot_emissions.loc[tot_emissions.jurisdiction.isin(ctryGroups[ctryGroup]), :]
    
    emissionsCtryGroup = df.groupby(["year"]).sum()
    df = df.merge(emissionsCtryGroup, on=["year"], how='left')
    
    df["share_CO2_"+ctryGroup] = df.Total_CO2_Emissions_Excluding_LUCF_MtCO2e_x/df.Total_CO2_Emissions_Excluding_LUCF_MtCO2e_y
    df["share_GHG_"+ctryGroup] = df.Total_GHG_Emissions_Excluding_LUCF_MtCO2e_x/df.Total_GHG_Emissions_Excluding_LUCF_MtCO2e_y
    
    average = df_prices_econ.loc[(df_prices_econ.jurisdiction.isin(ctryGroups[ctryGroup])), ["jurisdiction", "year", "ecp_all_jurCO2_usd_k"]].merge(df, on=["jurisdiction", "year"], how='left').fillna(method='ffill')
    average = average[["jurisdiction", "year", "ecp_all_jurCO2_usd_k", "share_CO2_"+ctryGroup]]
    average["price_"+ctryGroup+"_weighted"] = average.ecp_all_jurCO2_usd_k*average["share_CO2_"+ctryGroup]
    
    average = average.groupby(["year"])["price_"+ctryGroup+"_weighted"].sum()

    averageCtryGroup[ctryGroup] = average


# Share of emissions covered by mechanisms implemented by year [yyyy]




