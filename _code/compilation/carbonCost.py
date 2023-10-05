#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 17:07:34 2020

@author: G. Dolphin
"""

# This script executes the calculation of:
# - carbon cost (per unit of VA), at country- and industrial sector-level
# - share of GDP covered by carbon prices

# The steps taken are as follows:
# 1. Select environmentally extended MRIO table - 
# The MRIO dataset used here is the Global Resource Input Output Assessment (GLORIA)

# 2. Map carbon pricing data with emissions data contained in the MRIO - 
# This is necessary to accurately calculate the embedded carbon price I need to 
# establish which proportion of an industry's emissions is actually priced and at what level.
# GLORIA EE-MRIO tables provide an implicit concordance between IEA/IPCC and (MRIO) industrial sectors;
# that is, they allocate emissions from IEA/IPCC sectors to specific MRIO industries. 
# This concordance is 1-to-1 or weighted according to shares calculated from monetary IO tables.

# CARBON COST
# 3. Multiply (element-by-element) direct industry-level emissions by the associated price (in current prices)
# 4. Sum carbon cost over all emissions sources and divide by total VA of sector (or country)
# SHARE OF GDP COVERED BY CARBON PRICE
# 3. Multiply (element-by-element) direct industry-level emissions by binary coverage variable
# 4. Shrink dimension to a single binary variable indicating whether the industrial sector is covered by carbon pricing
# 5. Multiply VA of each sector by binary variable and sum over all sectors
# 6. Divide by total country VA (GDP)

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

gloria = SourceFileLoader('gloria', cwd+'/_code/compilation/_dependencies/dep_ccost/gloriaProcessing.py').load_module()
prices = SourceFileLoader('ecp', cwd+'/_code/compilation/_dependencies/dep_ccost/pricingProcessing.py').load_module()
                
# ----------------------------------------------------------------------------

ctryISO3Name = pd.read_csv(cwd+"/_raw/_aux_files/wb_iso3_map.csv")
ctryISO3Name = dict(zip(ctryISO3Name.iso3_code, ctryISO3Name.ctry_name))

ctryNameISO3 = {}

for key in ctryISO3Name.keys():
    ctryNameISO3[ctryISO3Name[key]] = key


# This function does the calculation(s) for one year

def embeddedCP_gloria(year):

    # ---------------------- CARBON PRICES ---------------

    ecp = prices.carbonPrices(year)
    ecp.rename(columns={'carbon_price':"ecp",
                            "country":"regionName"},
                   inplace=True)

    ecp["sector"] = ecp["sector"].apply(lambda x: x.replace("&", " "))
    ecp["sector"] = ecp["sector"].apply(lambda x: x.replace(" ", "."))

    # ----------------------------- EMISSIONS $ VALUE and carbon pricing VA coverage ----------------------

    gloriaProc = gloria.gloria57_proc(year)

    # create emissions dataframe
    emissions = gloriaProc[0]
    tot_out = gloriaProc[1]
    tot_inp = gloriaProc[2]

    # add country group codes
    emissions["regionISO3"] = emissions["regionName"]
    emissions["regionISO3"].replace(to_replace=ctryNameISO3, inplace=True)
    emissions.rename(columns={"variable":"ipcc_cat"},
                     inplace=True)
    emissions = emissions[["regionName", "regionISO3", "sector", "ipcc_cat", "co2_emissions"]]

    # add country group codes
    tot_out["regionISO3"] = tot_out["regionName"]
    tot_out["regionISO3"].replace(to_replace=ctryNameISO3, inplace=True)
    tot_out.rename(columns={"variable":"ipcc_cat"},
                     inplace=True)
    tot_out = tot_out[["regionName", "regionISO3", "sector", "tot_int_demand", "Y", "tot_out"]]

    # Aggregate 'emissions' dataframe before merging with the 'tot_out' and `cprices` dataframes
    # because prices are aggregated at sector level already, not split by IPCC categories.
    # This comes from pre-processing of carbon prices dataset in "ecp_incidence" project.
    
    emissions_agg = emissions.groupby(by=['regionName', 'sector']).sum().reset_index()

    # Merge emissions and carbon pricing dataframe
    # (ensure that GLORIA and ECP ipcc disaggregation match)
    emissions_agg = pd.merge(emissions_agg, ecp, on=["regionName", "sector"],
                             how='left')

    # calculate which emissions are covered by a carbon price
    emissions_agg["co2_pricing"] = emissions_agg.co2_emissions*emissions_agg.pricing
    emissions_agg.loc[emissions_agg.co2_pricing>0, "co2_bin"] = 1

    # calculate value of emissions at [current 2021 prices]
    # - emissions are expressed in Gg (or kt), prices are expressed in current USD per tonne of CO2
    emissions_agg["ecp"] = emissions_agg["ecp"].fillna(0)
    emissions_agg["co2_cost"] = emissions_agg.co2_emissions*emissions_agg.ecp

    # note: accounting for pricing coverage in this way only provides a 'rough'
    # estimate of carbon pricing in the economy - as soon as one type of emissions is covered 
    # in an econmic sector, it will be recorded as 'priced'. However, not all of its emissions may be covered.

    emint = tot_out[["regionName", "sector", "tot_out"]].merge(emissions_agg, on=["regionName", "sector"])

    # ---------------------- END OF INPUTS ----------------------

    # ---------------------- CALCULATING METRICS ----------------------
    ## SHARE OF GDP COVERED BY >0 CARBON PRICES 

    # share of country/region GDP and share of world GDP

    GDP_region = emint[["regionName", "sector", "tot_out"]].groupby(["regionName"]).sum().reset_index()
    GDP_region.rename(columns={"tot_out":"regionGDP"},
                      inplace=True)

    GDP_world = emint[["tot_out"]].sum()

    coverageGDP = pd.merge(emint, GDP_region, on=["regionName"])
    coverageGDP["worldGDP"] = GDP_world

    coverageGDP["shareGDP"] = coverageGDP["tot_out"]/coverageGDP["regionGDP"]
    coverageGDP["shareWldGDP"] = coverageGDP["tot_out"]/GDP_world.item()

    coverageGDP["cpCoverage"] = coverageGDP.shareGDP*coverageGDP.pricing
    coverageRegion = coverageGDP[["regionName", "cpCoverage"]]
    coverageRegion = coverageRegion.groupby(["regionName"]).sum().reset_index()

    coverageGDP["cpCoverageWld"] = coverageGDP.shareWldGDP*coverageGDP.pricing
    coverageWld = coverageGDP[["regionName", "cpCoverageWld"]]
    coverageWld = coverageWld.cpCoverageWld.sum()

    coverageRegion = coverageRegion.append({"regionName":"World", "cpCoverage":coverageWld},
                                             ignore_index=True)

    coverageRegion["year"] = year
    coverageRegion = coverageRegion[['regionName', 'year', 'cpCoverage']]
    coverageRegion.to_csv(cwd+"/_dataset/coverage/cpriceCoverageGDP.csv",
                          index=None)

    ## DIRECT EMISSIONS AND CARBON COST INTENSITY 
    # Intensities calculated here are SCOPE 1 (direct emissions) intensities
    # The emissions intensity is expressed in tCO2/US dollar
    
    emint["co2_int"] = emint.co2_emissions / (emint.tot_out*1000) # see note on units at start of section
    emint["ccost_int"] = emint.co2_cost / (emint.tot_out*1000)
    
    emint[['regionName', 'sector', 'year', "co2_int", "ccost_int"]].to_csv(cwd+"/_dataset/carbonCost/carbonCost.csv",
                 index=None)
    
    emintTot = emint.groupby(["regionName", "year"]).sum().reset_index()
    emintTot[['regionName', 'year', "co2_int", "ccost_int"]].to_csv(cwd+"/_dataset/carbonCost/carbonCostTot.csv",
                 index=None)

    return



#To do's - 
# drop ROW
# ensure that co2_price_per_tonne_co2 is no higher than highest price recorded in ecp_sector
