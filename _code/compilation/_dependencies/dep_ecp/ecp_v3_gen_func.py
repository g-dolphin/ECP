#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 16:52:03 2022

@author: gd
"""

import os
import pandas as pd
import glob
import numpy as np

path_ghg = '/Users/gd/OneDrive - rff/documents/research/projects/ecp/ecp_dataset/source_data/ghg_inventory/raw'

#---------------------FUNCTIONS-------------------------------------

def concatenate(indir):
    os.chdir(indir) #sets the current directory to 'indir'
    fileList=glob.glob("*.csv") # generates a list of csv files in the directory
    dfList = []

    for filename in fileList: #each iteration of the loop adding a dataframe to the list
        df=pd.read_csv(filename, header=0)
        dfList.append(df)

    concatDf=pd.concat(dfList,axis=0) #'axis=0' ensures that we are concatenating vertically

    return concatDf


# Function executing the concatenation of IEA yearly .csv files, i.e. merging all single-year files into one single all years .csv file.
# That function takes 2 arguments: the directory path of the files to concatenate and the directory path of the output file.

#Change file path in function to choose which raw data to use (pre-/post-2015 files/nomenclature)

# DEPRECATED GIVEN DATA NOW COMING FROM IEA in .TXT FORMAT
# def concat_iea(indir = path_ghg+"/national/IEA/iea_energy_co2_emissions/detailed_figures/emissions_annual/Post2015Nom", 
#               outfile = path_ghg+"/national/IEA/iea_energy_co2_emissions/detailed_figures/emissions_allyears/iea_CO2em_ally.csv"):
#    os.chdir(indir) #sets the current directory to 'indir'
#    fileList=glob.glob("*.csv") #this command generates a list of csv files
#    # to concatenate, we will stack the files into a single Python list
#    # the method will generate a single output file as output
#    # before starting the loop, we need to create an empty list object

#    dfList = []

#    colnames = ["LOCATION","Country","PRODUCT","Product","FLOW",
#                "Flow (kt of CO2)","TIME","Time","Value","Flag Codes","Flags"]

#    #each iteration of the loop will add a dataframe to the list
#    for fileName in fileList:
#        df=pd.read_csv(fileName, header=0, encoding = 'latin-1') #latin-1 encoding to deal with special characters

        # some weird encoding here.
#        df.rename(columns={'ï»¿"LOCATION"':"LOCATION"}, inplace=True)

#        if fileName == "IEA_CO2_AB_2019_2021.csv":
#            MapDF_flow = pd.read_csv("/Users/gd/GitHub/ECP/_raw/_aux_files/iea_ukds_FLOWcodes.csv")
#            MapDF_prod = pd.read_csv("/Users/gd/GitHub/ECP/_raw/_aux_files/iea_ukds_PRODcodes.csv")
#            concordanceFLOW = dict(zip(MapDF_flow.FLOWname, MapDF_flow.FLOW))
#            concordancePROD = dict(zip(MapDF_prod.PRODUCTname, MapDF_prod.PRODUCT))

#            df["FLOW"].replace(to_replace=concordanceFLOW, inplace=True)
#            df["PRODUCT"].replace(to_replace=concordancePROD, inplace=True)
#            df.columns = ["COUNTRY", "Country", "FLOW",
#                          "Flow (kt of CO2)", "PRODUCT", "Product",
#                          "TIME", "Time", "Value", "Flag Codes", "Flags"]
            
            # drop "World aviation bunkers", "World marine bunkers" rows
#            df = df.loc[~df.Country.isin(["World aviation bunkers", "World marine bunkers"])]

            # replace country names
#            df["Country"].replace(to_replace={"Republic of Turkiye":"Turkey", "Guyana":"Memo: Guyana",
#                                              "Uganda":"Memo: Uganda", "Madagascar":"Memo: Madagascar"}, 
#                                              inplace=True)

            # Create 'World' rows
#            dfWld = df.groupby(['FLOW', "Flow (kt of CO2)", 'PRODUCT', 'Product', 'TIME', 'Time', 
#                                    'Flag Codes', 'Flags']).sum().reset_index()
#            dfWld["Country"] = "World"
#            dfWld["COUNTRY"] = "WLD"

#            df = pd.concat([df, dfWld])

            # reordering columns
#            df = df[["COUNTRY", "Country", "PRODUCT", "Product", "FLOW",	
#                     "Flow (kt of CO2)", "TIME", "Time", "Value", "Flag Codes", "Flags"]]
#            df.rename(columns={"COUNTRY":"LOCATION"}, inplace=True)

#        dfList.append(df)

#    concatDf=pd.concat(dfList,axis=0) #'axis=0' ensures that we are concatenating vertically
#    concatDf.columns=colnames
#    concatDf.to_csv(outfile,index=None)
    
######Aggregated product categories######

#This function extracts the last two digits of the product code to substitute it for the main product category name
#'Main product' categories are: 'Coal/peat', 'Natural gas', 'Oil', 'Other'
#This follows IEA aggregated product categories (see IEA (2019), p.26)

#NB: If it turns out that, for some flows, the source file does not contain any product with product number ending 
#with '20' then no 'Natural gas' category is created, which creates problems further down the line...

#def get_product_category(product_code):
#    product_number = int(product_code[-2:]) # only interested in last two digits

#    if(product_number == 1):
#        return 'Total'
#    elif(product_number >= 2 and product_number <= 18): 
#        return 'Coal'
#    #PRODUCTS 18 and 19 are peat and peat products, which are part of the IEA coal category but are treated distinctly by pricing policies
#    #PRODUCT 20 is 'oil shale', which is aggregated into coal category, see IEA documentation
#    elif(product_number == 21):
#        return 'Natural gas'
##    elif(product_number == 20):
##        return 'Oil'
#    elif(product_number >= 22 and product_number <= 45):
#        return 'Oil'
#    elif(product_number >= 46 and product_number <= 47): #The 'Other' category includes (only and exclusively) industrial waste and municipal waste
#        return 'Other'
#    else:
#        return 'Error'

# Dictionary of product categories
productCategories = {"Coal":['HARDCOAL', 'BROWN', 'ANTCOAL', 'COKCOAL', 'BITCOAL', 'SUBCOAL', 
                                'LIGNITE', 'PATFUEL', 'OVENCOKE', 'GASCOKE', 'COALTAR', 'BKB', 
                                'GASWKSGS', 'COKEOVGS', 'BLFURGS', 'OGASES', 'PEAT', 'PEATPROD', 'OILSHALE'],
                     "Natural gas":['NATGA'],
                     "Oil":['CRNGFEED', 'CRUDEOIL', 'NGL', 'REFFEEDS', 'ADDITIVE', 'ORIMUL', 
                             'NONCRUDE', 'REFINGAS', 'ETHANE', 'LPG', 'NONBIOGAS', 'AVGAS', 
                             'JETGAS', 'OTHKE', 'RESFUEL', 'NAPHTA', 'WHITESP', 'LUBRIC', 
                             'BITUMEN', 'PARWAX', 'PETCOKE', 'ONONSPEC', 'NONBIOLJET'],
                     "Other":['INDWASTE', 'MUNWASTE', 'PRIMSBIO', 'BIOGASES', 'BIOGASOL',
                               'BIODIESEL', 'OBIOLIQ', 'RENEWNS', 'CHARCOAL'],
                     "Total":['TOTAL']}

# Country names
iea_wb_map = {'Australi':'Australia', 
            'Bosniaherz':'Bosnia and Herzegovina',
            'Brunei':'Brunei Darussalam', 
            'Congo':'Congo, Rep.', 
            'Congorep':'Congo, Dem. Rep.',
            'Costarica':'Costa Rica',
            'Coteivoire':"Cote d'Ivoire", 
            'Czech':'Czech Republic',
            'Dominicanr':'Dominican Republic',
            'Egypt':'Egypt, Arab Rep.', 
            'Elsalvador':'El Salvador',
            'Eqguinea':'Equatorial Guinea',
            'Eswatini':'Lesotho', 
            'Hongkong':'Hong Kong, SAR', 
            'Iran':'Iran, Islamic, Rep.', 
            'Korea':'Korea, Rep.', 
            'Koreadpr':'Korea, Dem. Rep.', 
            'Kyrgyzstan':'Kyrgyz Republic', 
            'Lao':'Lao PDR', 
            'Luxembou':'Luxembourg',
            'Nethland':'Netherlands',
            'Northmaced':'North Macedonia',
            'Nz':'New Zealand',
            'Philippine':'Philippines',
            'Russia':'Russian Federation',
            'Saudiarabi':'Saudi Arabia', 
            'Slovakia':'Slovak Republic',
            'Southafric':'South Africa',
            'Srilanka':'Sri Lanka', 
            'Ssudan':'South Sudan', 
            'Switland':'Switzerland', 
            'Syria':'Syrian Arab Republic', 
            'Turkmenist':'Turkmenistan',
            'Uae':'United Arab Emirates',
            'Uk':'United Kingdom',
            'Usa':'United States',
            'Venezuela':'Venezuela, RB',
            'Yemen':'Yemen, Rep.'}


######Converts missing values to 0######
def convert_value(value_str):
    value = 0
    try:
        value = float(value_str)
    except ValueError:
        value = 0
    return value

def convert_value_II(na_str):
    value = np.nan
    if na_str == 'n.a.':
        return value
    else:
        try:
            value = float(na_str)
        except ValueError:
            value = np.nan
        return value
    
    
def wb_series(series_name, new_name):
    wdi_series = pd.read_csv('/Users/gd/GitHub/ECP/_raw/wb_rates/wb_rates.csv', low_memory=False)
    
    series = wdi_series[wdi_series["Series Name"]==series_name]
    series = series.drop(["Country Code", "Series Code", "Series Name"], axis=1)
    series = series.melt(id_vars="Country Name")
    series.columns = ["jurisdiction", "year", new_name]
    series.replace(to_replace="#N/A", value=np.nan, inplace=True)

    series["year"] = series.apply(lambda x: x['year'][:4], axis = 1)
    series["year"] = series.year.astype(int)
    
    series["jurisdiction"].replace(to_replace={"Czechia":"Czech Republic"}, inplace=True)

    return series
    
    
    