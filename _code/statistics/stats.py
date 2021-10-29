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

df_prices_econ = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/data/ecp/ecp_economy/ecp_vw/ecp_tvII.csv")

oecd = ["United States", "Mexico", "Japan", "Germany", "Turkey", "France",
        "United Kingdom", "Italy", "Korea, Rep.", "Spain", "Poland", "Canada",
        "Australia", "Chile", "Netherlands", "Belgium", "Greece", "Czech Republic",
        "Portugal", "Sweden", "Hungary", "Austria", "Israel", "Switzerland",
        "Denmark", "Finland", "Slovak Republic", "Norway", "Ireland", "New Zealand",
        "Lithuania", "Slovenia", "Latvia", "Estonia", "Luxembourg", "Iceland"]

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

sum_stat = df_prices_econ.ecp_all_jurGHG_2019USD.describe()

avg_oecd = df_prices_econ.loc[(df_prices_econ.Jurisdiction.isin(oecd)) & (df_prices_econ.Year==2020), "ecp_all_jurCO2_2019USD"].mean()

avg_midinc = df_prices_econ.loc[(df_prices_econ.Jurisdiction.isin(middle_income)) & (df_prices_econ.Year==2020), "ecp_all_jurGHG_2019USD"].mean()

# Country group weighted average prices

tot_emissions = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/source_data/raw/ghg_emissions/estimated-reported/national/ClimateWatch/CAIT/CAIT_2021/CAIT_country_tot_2021_WBnames.csv")
 
for jur_list in [oecd, middle_income]:
    
    df = tot_emissions.loc[tot_emissions.Jurisdiction.isin(jur_list), :]
    
    emissions_total = df.groupby(["Year"]).sum()
    df = df.merge(emissions_total, on=["Year"], how='left')
    
    df["share_CO2_oecd"] = df.Total_CO2_Emissions_Excluding_LUCF_MtCO2e_x/df.Total_CO2_Emissions_Excluding_LUCF_MtCO2e_y
    df["share_GHG_oecd"] = df.Total_GHG_Emissions_Excluding_LUCF_MtCO2e_x/df.Total_GHG_Emissions_Excluding_LUCF_MtCO2e_y
    
    average = df_prices_econ.loc[(df_prices_econ.Jurisdiction.isin(jur_list)), ["Jurisdiction", "Year", "ecp_all_jurCO2_2019USD"]].merge(df, on=["Jurisdiction", "Year"], how='left').fillna(method='ffill')
    average = average[["Jurisdiction", "Year", "ecp_all_jurCO2_2019USD", "share_CO2_oecd"]]
    average["price_oecd_weight"] = average.ecp_all_jurCO2_2019USD*average.share_CO2_oecd
    
    average = average.groupby(["Year"]).price_oecd_weight.sum()

