# script for calculating price series at the level of aggregate IPCC categories

import pandas as pd
import re
import numpy as np
import math

ipccCodes = pd.read_csv("/Users/gd/GitHub/ECP/_raw/_aux_files/ipcc2006_iea_category_codes.csv")

# need to specify which inventory one is drawing from (national or subnational) and specify the corresponding path
inventoryPath = "/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/source_data/ghg_inventory/processed/"

invName = {"national":"nat", "subnational":"subnat"}


def cfWeightedPrices(gas, priceSeries):

    global prices_usd, prices_usd_comb, all_inst_col

    # PRICES
    prices_usd = ecp_general.concatenate("/Users/gd/GitHub/ECP/_raw/wcpd_usd/"+gas+priceSeriesPath[priceSeries])

    # currently including the price of the main tax or ets scheme; should be revised to account for all schemes
    prices_usd = prices_usd[["jurisdiction", "year", "ipcc_code", "iea_code", "Product"]+price_cols[priceSeries]]

    prices_usd = prices_usd.merge(wcpd_all[["jurisdiction", "year", "ipcc_code", "iea_code", "Product", "tax_cf", "ets_cf"]], 
                                on=["jurisdiction", "year", "ipcc_code", "iea_code", "Product"])

    # calculate total price by summing across all mechanisms columns
    if priceSeries=="kFixRate":
        prices_usd["tax_rate_incl_ex_usd_k"] = prices_usd.tax_rate_incl_ex_usd_k*prices_usd.tax_cf
        prices_usd["ets_price_usd_k"] = prices_usd.ets_price_usd_k*prices_usd.ets_cf

        price_columns = [x for x in prices_usd.columns if (x.endswith("usd_k"))]
        all_inst_col = "all_inst_usd_k"
        prices_usd[all_inst_col] = prices_usd[price_columns].sum(axis=1)

    else:
        prices_usd["tax_rate_incl_ex_usd"] = prices_usd.tax_rate_incl_ex_usd*prices_usd.tax_cf
        prices_usd["ets_price_usd"] = prices_usd.ets_price_usd*prices_usd.ets_cf

        price_columns = [x for x in prices_usd.columns if (x.endswith("usd"))]
        all_inst_col = "all_inst_usd"
        prices_usd[all_inst_col] = prices_usd[price_columns].sum(axis=1)

    prices_usd.drop(["tax_cf", "ets_cf"], axis=1, inplace=True)

    prices_usd  = prices_usd[["jurisdiction", "year", "ipcc_code", "iea_code", "Product"]+price_cols[priceSeries]+[all_inst_col]].sort_values(by=["jurisdiction", "year"])
    prices_usd_comb = prices_usd[prices_usd["ipcc_code"].isin(IPCC1AList)]

# function calculating emissions as shares of 

def inventoryShare(category, jurGroup, gas):

    inventory = pd.read_csv(inventoryPath+"/inventory_"+invName[jurGroup]+"_"+gas+".csv")

    # remove unused columns
    inventory = inventory[['jurisdiction', 'year', 'ipcc_code', 'iea_code', 'Product', gas]]

    # extending inventory to years beyond the last year
    for yr in range(2019, 2023):
        temp = inventory.loc[inventory.year==2018, :].copy()
        temp["year"].replace(to_replace={2018:yr}, inplace=True)

        inventory = pd.concat([inventory, temp])

    if jurGroup == "national":
        inventoryIPCC1A = inventory.loc[inventory.ipcc_code.isin(IPCC1AList), :]

        #recalculating ipcc category level totals (to account for rounding errors)
        inventoryIPCC1A_sectot = inventoryIPCC1A.groupby(by=["jurisdiction", "year", "iea_code"]).sum()
        inventoryIPCC1A_sectot.reset_index(inplace=True)
        inventoryIPCC1A_sectot.rename(columns={gas:gas+"_sectot"}, inplace=True)

        inventoryIPCC1A = inventoryIPCC1A.merge(inventoryIPCC1A_sectot, on=["jurisdiction", "year", "iea_code"])
        inventoryIPCC1A[gas+"_sharesec"] = inventoryIPCC1A[gas]/inventoryIPCC1A[gas+"_sectot"]

        inventoryIPCC1A.loc[:, gas+"_sharesec"] = inventoryIPCC1A.loc[:, gas+"_sharesec"].fillna(0)
        inventoryIPCC1A.drop([gas+"_sectot"], axis=1, inplace=True)

        inventory = inventory.loc[~inventory.ipcc_code.isin(IPCC1AList)]
        inventory = pd.concat([inventory, inventoryIPCC1A])
        inventory.sort_values(by=["jurisdiction", "year", "ipcc_code", "iea_code", "Product"], inplace=True)

    ipccList = list(ipccCodes.IPCC_CODE.unique())
    ipccDict = {}

    # creating parent-child category dictionary
    for category in ipccList:
        ipccDict[category] = [x for x in ipccList if (x.startswith(category)) if (len(x)==len(category)+1)]

    # this will calculate weights for each emission category that is specified
    # a. extract/calculate emissions (using emissions inventories)
    # recall that (i) the inventory is constructed from different sources and (ii) for non-combustion emissions, the "Product" disaggregation does not exist
    # figures for some (most) aggregate categories are not in the inventory per se and have to calculated
    
    tempEmissionsAgg = inventory.loc[inventory.ipcc_code.isin([category])]
    tempEmissionsSub = inventory.loc[inventory.ipcc_code.isin(ipccDict[category])]

    tempEmissionsAgg.drop(["ipcc_code", "iea_code", "Product"], axis=1, inplace=True)

    # b. calculate aggregate category emissions, if not provided
    if np.isnan(tempEmissionsAgg.unique()).any():
        aggSecEm = tempEmissionsSub.groupby(["jurisdiction", "year"]).sum()
        aggSecEm.reset_index(inplace=True)
        
        aggSecEm.rename(columns={"CO2":"CO2_fromSubCat"})
        aggSecEm["ipcc_code"] = category
        aggSecEm["iea_code"] = ""

        if category.startswith("1A") and jurGroup == "national":
            tempEmissionsAgg = tempEmissionsAgg.merge(aggSecEm, on=["jurisdiction", "year", "ipcc_code", "iea_code", "Product"])
        else:
            tempEmissionsAgg = tempEmissionsAgg.merge(aggSecEm, on=["jurisdiction", "year", "ipcc_code", "iea_code"])

    # c. for each subcategory, calculate emissions as share of emissions of its parent category
    tempEmissionsSub = tempEmissionsSub.merge(tempEmissionsAgg, on=["jurisdiction", "year"])
    tempEmissionsSub["shareAggSec"] = tempEmissionsSub[gas+"_x"]/tempEmissionsSub[gas+"_y"]

    fullDF = pd.concat([tempEmissionsAgg, tempEmissionsSub])

    return fullDF

