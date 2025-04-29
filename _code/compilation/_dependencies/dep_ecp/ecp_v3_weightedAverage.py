import pandas as pd
import numpy as np
import re


def ecp(coverage_df, prices, jur_level, gas, flow_excl, weight_type, weight_year=None, sectors=False):
    global ecp_variables_map

    # Set merge keys and prepare prices
    if jur_level == "national":
        merge_keys = ["jurisdiction", "year", "ipcc_code", "iea_code", "Product"]
        prices_temp = prices.copy()
    else:  # subnational
        merge_keys = ["jurisdiction", "year", "ipcc_code", "iea_code"]
        prices_temp = prices[prices["Product"] == "Natural gas"].drop(columns=["Product"]).copy() # currently taking "Natural gas" price for all sector emissions. Not an issue since virtually all subnational prices are the same across fuels.

    # Merge coverage and price data
    if weight_type == "time_varying":
        temp_df = coverage_df.merge(prices_temp, on=merge_keys, how="left")
    elif weight_type == "fixed":
        temp_df = coverage_df[coverage_df["year"] == weight_year].drop(columns=["year"])
        fw_merge_keys = [k for k in merge_keys if k != "year"]
        temp_df = prices_temp.merge(temp_df, on=fw_merge_keys, how="right")

    # Helper to find columns matching regex patterns
    def find_cols(df, patterns):
        return [col for col in df.columns for pat in patterns if re.search(pat, col)]

    # Mapping variables
    patterns = {
        "ets": ["ets.*price", "cov_ets.*"],
        "tax": ["tax.*rate", "cov_tax.*"]
    }

    ecp_variables_map = {
        f"ecp_ets_jurGHG_usd_k": find_cols(temp_df, patterns["ets"] + [r"cov_ets.*jurGHG"]),
        f"ecp_ets_jur{gas}_usd_k": find_cols(temp_df, patterns["ets"] + [fr"cov_ets.*jur{gas}"]),
        f"ecp_ets_wldGHG_usd_k": find_cols(temp_df, patterns["ets"] + [r"cov_ets.*wldGHG"]),
        f"ecp_ets_wld{gas}_usd_k": find_cols(temp_df, patterns["ets"] + [fr"cov_ets.*wld{gas}"]),
        f"ecp_tax_jurGHG_usd_k": find_cols(temp_df, patterns["tax"] + [r"cov_tax.*jurGHG"]),
        f"ecp_tax_jur{gas}_usd_k": find_cols(temp_df, patterns["tax"] + [fr"cov_tax.*jur{gas}"]),
        f"ecp_tax_wldGHG_usd_k": find_cols(temp_df, patterns["tax"] + [r"cov_tax.*wldGHG"]),
        f"ecp_tax_wld{gas}_usd_k": find_cols(temp_df, patterns["tax"] + [fr"cov_tax.*wld{gas}"]),
    }

    ecp_variables_map_sect = {
        f"ecp_ets_sect{gas}_usd_k": find_cols(temp_df, ["ets.*price", "cov_ets.*_share"]),
        f"ecp_tax_sect{gas}_usd_k": find_cols(temp_df, ["tax.*rate", "cov_tax.*_share"])
    }    
    
    if jur_level == "subnational" and not sectors:
        ecp_variables_map.update({
            f"ecp_ets_supraGHG_usd_k": find_cols(temp_df, ["ets.*price", "cov_ets.*supraGHG"]),
            f"ecp_ets_supra{gas}_usd_k": find_cols(temp_df, ["ets.*price", f"cov_ets.*supra{gas}"]),
            f"ecp_tax_supraGHG_usd_k": find_cols(temp_df, ["tax.*rate", "cov_tax.*supraGHG"]),
            f"ecp_tax_supra{gas}_usd_k": find_cols(temp_df, ["tax.*rate", f"cov_tax.*supra{gas}"]),
        })

    # Choose mapping
    ecp_mapping = ecp_variables_map_sect if sectors else ecp_variables_map

    # Calculate ECP variables
    for key, cols in ecp_mapping.items():
        if not cols:
            temp_df[key] = 0
            continue
        cols = sorted(cols)
        n = len(cols) // 2
        temp_df[key] = (temp_df[cols[:n]].fillna(0) * temp_df[cols[n:]].fillna(0)).sum(axis=1)
        temp_df[key] = temp_df[key].astype(float)

    # Final columns
    temp_df = temp_df[merge_keys + list(ecp_mapping.keys())].fillna(0)

    # Create total ECPs
    if not sectors:
        temp_df["ecp_all_jurGHG_usd_k"] = temp_df["ecp_tax_jurGHG_usd_k"] + temp_df["ecp_ets_jurGHG_usd_k"]
        temp_df["ecp_all_jur" + gas + "_usd_k"] = temp_df["ecp_tax_jur" + gas + "_usd_k"] + temp_df["ecp_ets_jur" + gas + "_usd_k"]
        temp_df["ecp_all_wldGHG_usd_k"] = temp_df["ecp_tax_wldGHG_usd_k"] + temp_df["ecp_ets_wldGHG_usd_k"]
        temp_df["ecp_all_wld" + gas + "_usd_k"] = temp_df["ecp_tax_wld" + gas + "_usd_k"] + temp_df["ecp_ets_wld" + gas + "_usd_k"]

        if jur_level == "subnational":
            temp_df["ecp_all_supraGHG_usd_k"] = temp_df["ecp_tax_supraGHG_usd_k"] + temp_df["ecp_ets_supraGHG_usd_k"]
            temp_df["ecp_all_supra" + gas + "_usd_k"] = temp_df["ecp_tax_supra" + gas + "_usd_k"] + temp_df["ecp_ets_supra" + gas + "_usd_k"]

    else:
        temp_df["ecp_all_sect" + gas + "_usd_k"] = temp_df["ecp_tax_sect" + gas + "_usd_k"] + temp_df["ecp_ets_sect" + gas + "_usd_k"]

    # Exclude aggregate sectors
    temp_df = temp_df[~temp_df["ipcc_code"].isin(flow_excl)]

    return temp_df
    


def ecp_aggregation(ecp_df, gas, intro=None):

    global ecp_agg
    
    ecp_agg = ecp_df.groupby(["jurisdiction", "year"]).sum()
    ecp_agg.reset_index(inplace=True)

    #World calculations
    if intro == None:
        ecp_world_agg = ecp_agg[["jurisdiction", "year", "ecp_ets_wldGHG_usd_k", "ecp_ets_wld"+gas+"_usd_k",
                                "ecp_tax_wldGHG_usd_k", "ecp_tax_wld"+gas+"_usd_k"]]

        ecp_world_agg = ecp_world_agg.groupby(['year']).sum()

        cols_map = {"ecp_tax_wldGHG_usd_k":"ecp_tax_jurGHG_usd_k", "ecp_tax_wld"+gas+"_usd_k":"ecp_tax_jur"+gas+"_usd_k",
                    "ecp_ets_wldGHG_usd_k":"ecp_ets_jurGHG_usd_k", "ecp_ets_wld"+gas+"_usd_k":"ecp_ets_jur"+gas+"_usd_k"}

        ecp_world_agg.rename(columns=cols_map, inplace=True)
        ecp_world_agg["jurisdiction"] = "World"
        ecp_world_agg.reset_index(inplace=True)

        ecp_agg = pd.concat([ecp_agg, ecp_world_agg])

    # all schemes ecp
    ecp_agg["ecp_all_jurGHG_usd_k"] = ecp_agg["ecp_tax_jurGHG_usd_k"] + ecp_agg["ecp_ets_jurGHG_usd_k"]
    ecp_agg["ecp_all_jur"+gas+"_usd_k"] = ecp_agg["ecp_tax_jur"+gas+"_usd_k"] + ecp_agg["ecp_ets_jur"+gas+"_usd_k"]
    ecp_agg["ecp_all_supraGHG_usd_k"] = ecp_agg["ecp_tax_supraGHG_usd_k"] + ecp_agg["ecp_ets_supraGHG_usd_k"]
    ecp_agg["ecp_all_supra"+gas+"_usd_k"] = ecp_agg["ecp_tax_supra"+gas+"_usd_k"] + ecp_agg["ecp_ets_supra"+gas+"_usd_k"]

    return ecp_agg


def national_from_subnat(df, list_subnat, nat_jur, gas):
    
    temp = df.loc[df.jurisdiction.isin(list_subnat), :]
    temp = temp.groupby(["year"]).sum()
    temp.reset_index(inplace=True)
    temp["jurisdiction"] = nat_jur+"sub"

    temp[["ecp_ets_jurGHG_usd_k", "ecp_tax_jurGHG_usd_k", 
          "ecp_ets_jur"+gas+"_usd_k", "ecp_tax_jur"+gas+"_usd_k", 
          "ecp_all_jurGHG_usd_k", "ecp_all_jurGHG_usd_k"]] = np.nan

    swap_list = {"ecp_ets_jurGHG_usd_k":"ecp_ets_supraGHG_usd_k", "ecp_tax_jurGHG_usd_k":"ecp_tax_supraGHG_usd_k", 
                "ecp_ets_jur"+gas+"_usd_k":"ecp_ets_supra"+gas+"_usd_k", "ecp_tax_jur"+gas+"_usd_k":"ecp_tax_supra"+gas+"_usd_k", 
                "ecp_all_jurGHG_usd_k":"ecp_all_supraGHG_usd_k", "ecp_all_jur"+gas+"_usd_k":"ecp_all_supra"+gas+"_usd_k",
                "ecp_ets_supraGHG_usd_k":"ecp_ets_jurGHG_usd_k", "ecp_tax_supraGHG_usd_k":"ecp_tax_jurGHG_usd_k", 
                "ecp_ets_supra"+gas+"_usd_k":"ecp_ets_jur"+gas+"_usd_k", "ecp_tax_supra"+gas+"_usd_k":"ecp_tax_jur"+gas+"_usd_k", 
                "ecp_all_supraGHG_usd_k":"ecp_all_jurGHG_usd_k", "ecp_all_supra"+gas+"_usd_k":"ecp_all_jur"+gas+"_usd_k"}

    temp.rename(columns=swap_list, inplace=True)

    temp_nat = df.loc[df.jurisdiction == nat_jur, :]

    temp_nat_subnat = pd.concat([temp_nat, temp])
    temp_nat_subnat = temp_nat_subnat.groupby(["year"]).sum() # summing country-level ecp from country-level and subnational mechanisms
    temp_nat_subnat.reset_index(inplace=True)

    temp_nat_subnat["jurisdiction"] = nat_jur

    df = df.loc[df.jurisdiction != nat_jur, :]
    df = pd.concat([df, temp_nat_subnat])
        
    return df