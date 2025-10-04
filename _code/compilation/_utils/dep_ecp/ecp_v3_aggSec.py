# script for calculating price series at the level of aggregate IPCC categories

import pandas as pd
import re
import numpy as np
import math
from itertools import chain
import dep_ecp

from dep_ecp import ecp_v3_gen_func as ecp_gen

ipccCodes = pd.read_csv("/Users/geoffroydolphin/GitHub/ECP/_raw/_aux_files/ipcc2006_iea_category_codes.csv")

# need to specify which inventory one is drawing from (national or subnational) and specify the corresponding path
inventoryPath = "/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/source_data/ghg_inventory/processed/"
invName = {"national":"nat", "subnational":"subnat"}


def cfWeightedPrices(gas, priceSeries, priceSeriesPath, 
                     price_cols, wcpd_all, countries_dic, subnat_dic):

    # PRICES
    prices_usd = ecp_gen.concatenate("/Users/gd/GitHub/ECP/_raw/wcpd_usd/"+gas+priceSeriesPath)

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

    for jur in countries_dic.keys():
        prices_usd.loc[prices_usd.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/ECP/_raw/wcpd_cfWeightedPrices_usd/prices_usd_"+gas+"_"+countries_dic[jur]+".csv", index=None)
    for jur in subnat_dic.keys():
        prices_usd.loc[prices_usd.jurisdiction==jur, :].to_csv("/Users/gd/GitHub/ECP/_raw/wcpd_cfWeightedPrices_usd/prices_usd_"+gas+"_"+subnat_dic[jur]+".csv", index=None)


    return prices_usd, all_inst_col



def inventoryShare(category, jurGroup, gas, level):
    """
    Compute emissions as shares of sector totals from inventory data.

    Parameters:
        category (str): IPCC parent category code.
        jurGroup (str): Jurisdiction group (e.g., "national").
        gas (str): Gas name (e.g., "CO2").
        level (str): Level of aggregation ("level_5" or other).

    Returns:
        pd.DataFrame: Inventory data with added share column (gas_shareAggSec).
    """

    # 1. Load inventory and filter relevant columns
    inventory = pd.read_csv(
        f"{inventoryPath}/inventory_{invName[jurGroup]}_{gas}.csv",
        usecols=['jurisdiction', 'year', 'ipcc_code', 'iea_code', 'Product', gas]
    )
    inventory = inventory[inventory.year <= 2022]

    # 2. Add projections for 2023–2024 by copying 2022
    for yr in range(2023, 2025):
        inventory = pd.concat(
            [inventory, inventory[inventory.year == 2022].assign(year=yr)],
            ignore_index=True
        )

    # 3. Build list of subcategories (children of the given category)
    ipcc_subcats = [
        x for x in ipccCodes.ipcc_code.unique()
        if x.startswith(category) and len(x) == len(category) + 1
    ]
    selected_codes = [category] + ipcc_subcats
    inventory = inventory[inventory.ipcc_code.isin(selected_codes)]

    # 4. Separate aggregate and subcategory emissions
    tempAgg = inventory[inventory.ipcc_code == category]
    tempSub = inventory[inventory.ipcc_code.isin(ipcc_subcats)]

    # 5. Safely extract iea_code
    iea_code_vals = tempAgg['iea_code'].dropna().unique()
    iea_code = iea_code_vals[0] if len(iea_code_vals) > 0 else np.nan

    # 6. Compute parent-sector emissions
    #if level == 'level_5':
    aggEm = tempAgg.groupby(
        ["jurisdiction", "year", "ipcc_code", "iea_code"], as_index=False
    )[gas].sum()

    #else:
    #    aggEm = tempSub.groupby(
    #        ["jurisdiction", "year"], as_index=False
    #    )[gas].sum()
    #    aggEm = aggEm.assign(ipcc_code=category, iea_code=iea_code)


    # 7. Combine aggregate and subcategories
    tempAll = pd.concat([tempAgg, tempSub], ignore_index=True)

    # 8. Merge in aggregate sector totals — exclude 'Product' from merge keys
    tempAll = tempAll.merge(
        aggEm[["jurisdiction", "year", "ipcc_code", gas]],
        on=["jurisdiction", "year", "ipcc_code"],
        how='left',
        suffixes=('', '_agg')
    )

    # 9. Calculate share
    tempAll[f"{gas}_shareAggSec"] = tempAll[gas] / tempAll[f"{gas}_agg"]
    tempAll.drop(columns=[f"{gas}_agg"], inplace=True)

    return tempAll

