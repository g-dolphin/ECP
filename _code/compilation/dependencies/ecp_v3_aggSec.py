# script for calculating price series at the level of aggregate IPCC categories

import pandas as pd
import re
import numpy as np
import math
from importlib.machinery import SourceFileLoader
from itertools import chain

path_dependencies = '/Users/gd/GitHub/ECP/_code/compilation/dependencies'

ipccCodes = pd.read_csv("/Users/gd/GitHub/ECP/_raw/_aux_files/ipcc2006_iea_category_codes.csv")

ecp_general = SourceFileLoader('general', path_dependencies+'/ecp_v3_gen_func.py').load_module()

# need to specify which inventory one is drawing from (national or subnational) and specify the corresponding path
inventoryPath = "/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/source_data/ghg_inventory/processed/"

invName = {"national":"nat", "subnational":"subnat"}


def cfWeightedPrices(gas, priceSeries, priceSeriesPath, 
                     price_cols, wcpd_all, IPCC1AList):

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

    return prices_usd, prices_usd_comb, all_inst_col

# function calculating emissions as shares of 

def inventoryShare(category, jurGroup, gas):

    inventory = pd.read_csv(inventoryPath+"/inventory_"+invName[jurGroup]+"_"+gas+".csv")

    # remove unused columns
    inventory = inventory[['jurisdiction', 'year', 'ipcc_code', 'iea_code', 'Product', gas]]
    inventory = inventory.loc[inventory.year<=2018, :]

    for yr in range(2019, 2023):
        temp = inventory.loc[inventory.year==2018, :].copy()
        temp["year"].replace(to_replace={2018:yr}, inplace=True)

        inventory = pd.concat([inventory, temp])

    # inventory subset
    ## creating parent-child category dictionary to include child categories in inventory subset
    ipccList = list(ipccCodes.IPCC_CODE.unique())
    ipccDict = {}
    ipccDict[category] = [x for x in ipccList if (x.startswith(category)) if (len(x)==len(category)+1)]
    
    ## creating subset
    inventory = inventory.loc[inventory.ipcc_code.isin([category]+ipccDict[category])]

    # A. extract/calculate emissions (using emissions inventories)
    # recall that (i) the inventory is constructed from different sources and (ii) for non-combustion emissions, the "Product" disaggregation does not exist
    # figures for some (most) aggregate categories are not in the inventory per se and have to calculated
    
    tempEmissionsAgg = inventory.loc[inventory.ipcc_code.isin([category])]
    tempEmissionsSub = inventory.loc[inventory.ipcc_code.isin(ipccDict[category])]

#    tempEmissionsAgg.drop(["ipcc_code", "iea_code", "Product"], axis=1, inplace=True)

    # B. calculate aggregate category emissions based on subcategory emissions figures, (if not provided and) if possible
    # incidentally, this will take care of the fact that ipcc category level totals for IEA are not consistent with sum of subcat totals (due to rounding errors)

#    if np.isnan(tempEmissionsAgg[gas].unique()).any():
    iea_code = tempEmissionsAgg.iea_code.unique()[0]

    aggSecEm = tempEmissionsSub.groupby(["jurisdiction", "year"]).sum()
    aggSecEm.reset_index(inplace=True)
    
    aggSecEm.rename(columns={"CO2":"CO2_fromSubCat"}, inplace=True)
    aggSecEm["ipcc_code"] = category
    aggSecEm["iea_code"] = iea_code

    #if category.startswith("1A") and jurGroup == "national":
    #    tempEmissionsAgg = tempEmissionsAgg.merge(aggSecEm, on=["jurisdiction", "year", "ipcc_code", "iea_code", "Product"])
    #else:
    #tempEmissionsAgg = tempEmissionsAgg.merge(aggSecEm, on=["jurisdiction", "year", "ipcc_code", "iea_code"],
    #                                          how='left')
    #tempEmissionsAgg.drop(["CO2"], axis=1, inplace=True)
    aggSecEm.rename(columns={"CO2_fromSubCat":"CO2"}, inplace=True)

    # C. for each subcategory, calculate emissions as share of emissions of its parent category

    # handling the fact that national inventories for combustion categories have a Product dimension
    # and that the IEA category totals do not match sum of individual categories

    tempEmissionsSub = tempEmissionsSub.merge(aggSecEm[["jurisdiction", "year", gas]], 
                                              on=["jurisdiction", "year"], how='left')
    tempEmissionsSub[gas+"_shareAggSec"] = tempEmissionsSub[gas+"_x"]/tempEmissionsSub[gas+"_y"]

    tempEmissionsSub.drop(["CO2_y"], axis=1, inplace=True)
    tempEmissionsSub.rename(columns={gas+"_x":gas}, inplace=True)

    fullDF = pd.concat([tempEmissionsAgg, tempEmissionsSub])

    return fullDF