#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 17:07:34 2020

@author: GD
"""
#https://pymrio.readthedocs.io/en/latest/index.html

# This script executes the calculation of:
# - carbon cost (per unit of VA)
# - share of GDP covered by carbon prices
# - embedded carbon prices

# 1. Choose environmentally extended MRIO table

# GLORIA EE-MRIO tables provide an implicit concordance between IEA/IPCC and (MRIO) industrial sectors;
# that is, they allocate emissions from IEA/IPCC sectors to specific MRIO industries. 
# This concordance is 1-to-1 or weighted according to shares calculated from monetary IO tables.

# Yet, carbon pricing database is structured by IPCC/IEA item; so, in order to accurately 
# calculate the embedded carbon price I need to establish which proportion of an industry's 
# emissions is actually priced and at what level.

# Note: the GLORIA environmental matrix (Q) includes a breakdown of emissions by IPCC category. 
# This allows for mapping with the carbon pricing database, since it is structured by IPCC sector.


# 2. Multiply (element-by-element) direct industry-level emissions by the associated price

# 3. Multiply vector in 2. by L matrix

# This gives the carbon price embedded in each product/industry from a given country of origin

# 4. Use data in 3 to calculate actual (hypothetical BCAs)


# scope 1 emissions are all direct emissions 
# scope 2 includes all direct emissions + emissions from "energy-related" products    
    # add emissions factor from direct emissions and from purchase of electricity and heat
    # this requires to truncate the technical requirements matrix
    
# scope 3 includes all emissions (direct and indirect) - this is the leontief multiplier obtained from the inversion of the matrix

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import re

from scipy import linalg
from dask import dataframe as dd
from importlib.machinery import SourceFileLoader

plt.style.use("ggplot")

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 500)

cwd = os.getcwd()

# dependencies

gloria = SourceFileLoader('gloria', cwd+'/_code/calculations/dependencies/gloriaProcessing.py').load_module()
prices = SourceFileLoader('ecp', cwd+'/_code/calculations/dependencies/pricingProcessing.py').load_module()

# ----------------------------------------------------------------------------

out_path = "/Users/gd/OneDrive - rff/Documents/Research/projects/embedded_carbon_price/data/"
                
# ----------------------------------------------------------------------------

ctryName_iso3 = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/climate_policy_and_trade/embedded_carbon_price/data/wb_iso3_map.csv")
ctryName_iso3_map = dict(zip(ctryName_iso3.iso3_code, ctryName_iso3.ctry_name))

# This function does the calculation(s) for one year

def embeddedCP_gloria(year):

    # ---------------------- CARBON PRICES ---------------

    ecp = prices.carbonPrices(year)
    ecp.rename(columns={'carbon_price':"ecp",
                            "country":"regionName"},
                   inplace=True)
#    ecp.drop(["'co2_excl_short_cycle_org_c_total_EDGAR_consistent'"], axis=1, inplace=True)    

    ecp["sector"] = ecp["sector"].apply(lambda x: x.replace("&", " "))
    ecp["sector"] = ecp["sector"].apply(lambda x: x.replace(" ", "."))

    # ----------------------------- EMISSIONS $ VALUE and carbon pricing VA coverage ----------------------

    gloriaProc = gloria.gloria57_proc(year)

    # create emissions dataframe and add country names
    emissions = gloriaProc[0]
    tot_out = gloriaProc[1]
    tot_inp = gloriaProc[2]

    #emissions["regionName"] = emissions["region"]
    #emissions["regionName"].replace(to_replace=ctryName_iso3_map, inplace=True)
    #emissions = emissions[["regionName", "region", "sector", "ipcc_cat", "co2_emissions"]]

    # Aggregate 'emissions' dataframe before merging with the 'tot_out' and `cprices` dataframes
    # because prices are aggregated at sector level already, not split by IPCC categories
    
    emissions_agg = emissions.groupby(by=['regionName', 'sector']).sum()
    #emissions_agg = emissions_agg.drop(["ecp"], axis=1)
    emissions_agg = emissions_agg.reset_index()

    # merge emissions and carbon pricing dataframe
    # (ensure that GLORIA and ECP ipcc disaggregation match)
    emissions_agg = pd.merge(emissions_agg, ecp, on=["regionName", "sector"],
                             how='left')

    # calculate which emissions are covered by a carbon price
    emissions_agg["co2_binary"] = emissions_agg.co2_emissions*emissions_agg.pricing
    emissions_agg.loc[emissions_agg.co2_binary>0, "co2_binary"] = 1

    # calculate value of emissions at [constant 2021 prices]
    # - emissions are expressed in Gg (or kt), prices are expressed in current USD per tonne of CO2
    emissions_agg["ecp"] = emissions_agg["ecp"].fillna(0)
    emissions_agg["co2_value"] = (emissions_agg.co2_emissions)*emissions_agg.ecp


    # note: accounting for pricing coverage in this way only provides a 'rough'
    # estimate of carbon pricing in the economy - as soon as one type of emissions is covered 
    # in an econmic sector, it will be recorded as 'priced'. However, not all of its emissions may be covered.

    emint = tot_out[["regionName", "sector", "tot_out"]].merge(emissions_agg, on=["regionName", "sector"])

    # ---------------------- SHARE OF GDP COVERED BY >0 CARBON PRICES ---------------

    # share of country/region GDP and share of world GDP

    GDP_region = emint[["regionName", "sector", "tot_out"]].groupby(["regionName"]).sum()
    GDP_region.reset_index(inplace=True)
    GDP_region.rename(columns={"tot_out":"regionGDP"},
                      inplace=True)

    GDP_world = emint[["tot_out"]].sum()

    coverageGDP = pd.merge(emint, GDP_region, on=["regionName"])
    coverageGDP["worldGDP"] = GDP_world

    coverageGDP["shareGDP"] = coverageGDP["tot_out"]/coverageGDP["regionGDP"]
    coverageGDP["shareWldGDP"] = coverageGDP["tot_out"]/GDP_world.item()

    coverageGDP["coverageRegion"] = coverageGDP.shareGDP*coverageGDP.pricing#co2_binary
    coverageRegion = coverageGDP[["regionName", "coverageRegion"]]
    coverageRegion = coverageRegion.groupby(["regionName"]).sum()
    coverageRegion.reset_index(inplace=True)

    coverageGDP["coverageWld"] = coverageGDP.shareWldGDP*coverageGDP.pricing#co2_binary
    coverageWld = coverageGDP[["regionName", "coverageWld"]]
    coverageWld = coverageWld.coverageWld.sum()

    coverageRegion = coverageRegion.append({"regionName":"World", "coverageRegion":coverageWld},
                                             ignore_index=True)

    coverageRegion["year"] = year
    coverageRegion = coverageRegion[['year', 'regionName', 'coverageRegion']]
    coverageRegion.to_csv("/Users/gd/GitHub/EmbeddedCarbonPrice/output/data/cpriceCoverageGDP.csv",
                          index=None)

    # ---------------------- DIRECT EMISSIONS AND CARBON COST INTENSITY ---------------
    # Intensities calculated here are SCOPE 1 (direct emissions) intensities
    # The emissions intensity is expressed in tCO2/US dollar
    
    emint["int_co2_em"] = (emint.co2_emissions) / (emint.tot_out*1000) # see note on units at start of section
    emint["int_co2_val"] = emint.co2_value / (emint.tot_out*1000)
    
    emint[['regionName', 'sector', 'year', "int_co2_em", "int_co2_val"]].to_csv("/Users/gd/GitHub/EmbeddedCarbonPrice/output/data/carbonCost.csv",
                 index=None)
    
    emintTot = emint.groupby(["regionName", "year"]).sum()
    emintTot.reset_index(inplace=True)
    emintTot[['regionName', 'year', "int_co2_em", "int_co2_val"]].to_csv("/Users/gd/GitHub/EmbeddedCarbonPrice/output/data/carbonCostTot.csv",
                 index=None)

    return



#To do's - 
# drop ROW
# ensure that co2_price_per_tonne_co2 is no higher than highest price recorded in ecp_sector
