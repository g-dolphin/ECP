import pandas as pd
import numpy as np
import re



def ecp(coverage_df, prices, jur_level, gas, flow_excl, weight_type, weight_year=None, sectors=bool):
    
    global ecp_variables_map 
    
    if jur_level == "national":
        merge_keys = ["jurisdiction", "year", "ipcc_code", "iea_code", "Product"]
        prices_temp = prices.copy()
        
    if jur_level == "subnational":
        merge_keys = ["jurisdiction", "year", "ipcc_code", "iea_code"]
        prices_temp = prices.loc[prices.Product=="Natural gas", :].copy() # currently taking "Natural gas" price for all sector emissions. Not an issue since virtually all subnational prices are the same across fuels.
        prices_temp.drop(["Product"], axis=1, inplace=True)
              
    if weight_type=="time_varying":
        temp_df = coverage_df.copy()
        temp_df = temp_df.merge(prices_temp, on=merge_keys, how="left")
        
    elif weight_type=="fixed":
        temp_df = coverage_df.loc[coverage_df.year==weight_year, :]
        temp_df.drop(["year"], axis=1, inplace=True)
        fw_merge_keys = merge_keys.copy()
        fw_merge_keys.remove("year")
        
        # merging on `prices_temp` keys in this case because this is the dataframe with all years
        temp_df = temp_df.merge(prices_temp, on=fw_merge_keys, how="right")

    ecp_variables_map = {"ecp_ets_jurGHG_usd_k":[x for x in list(temp_df.columns) if bool(re.match(re.compile("ets.+price+."), x))==True or bool(re.match(re.compile("cov_ets.+jurGHG"), x))==True], 
                         "ecp_ets_jur"+gas+"_usd_k":[x for x in list(temp_df.columns) if bool(re.match(re.compile("ets.+price+."), x))==True or bool(re.match(re.compile("cov_ets.+jur"+gas), x))==True], 
                         "ecp_ets_wldGHG_usd_k":[x for x in list(temp_df.columns) if bool(re.match(re.compile("ets.+price+."), x))==True or bool(re.match(re.compile("cov_ets.+wldGHG"), x))==True],
                         "ecp_ets_wld"+gas+"_usd_k":[x for x in list(temp_df.columns) if bool(re.match(re.compile("ets.+price+."), x))==True or bool(re.match(re.compile("cov_ets.+wld"+gas), x))==True],
                         "ecp_tax_jurGHG_usd_k":[x for x in list(temp_df.columns) if bool(re.match(re.compile("tax.+rate+."), x))==True or bool(re.match(re.compile("cov_tax.+jurGHG"), x))==True], 
                         "ecp_tax_jur"+gas+"_usd_k":[x for x in list(temp_df.columns) if bool(re.match(re.compile("tax.+rate+."), x))==True or bool(re.match(re.compile("cov_tax.+jur"+gas), x))==True], 
                         "ecp_tax_wldGHG_usd_k":[x for x in list(temp_df.columns) if bool(re.match(re.compile("tax.+rate+."), x))==True or bool(re.match(re.compile("cov_tax.+wldGHG"), x))==True], 
                         "ecp_tax_wld"+gas+"_usd_k":[x for x in list(temp_df.columns) if bool(re.match(re.compile("tax.+rate+."), x))==True or bool(re.match(re.compile("cov_tax.+wld"+gas), x))==True]}

    ecp_variables_map_sect = {"ecp_ets_sect"+gas+"_usd_k":[x for x in list(temp_df.columns) if bool(re.match(re.compile("ets.+price+."), x))==True or bool(re.match(re.compile("cov_ets.+_share"), x))==True], 
                              "ecp_tax_sect"+gas+"_usd_k":[x for x in list(temp_df.columns) if bool(re.match(re.compile("tax.+rate+."), x))==True or bool(re.match(re.compile("cov_tax.+_share"), x))==True]}
    
    
    if jur_level == "subnational" and sectors == False:
        ecp_variables_map["ecp_ets_supraGHG_usd_k"] = [x for x in list(temp_df.columns) if bool(re.match(re.compile("ets.+price+."), x))==True or bool(re.match(re.compile("cov_ets.+supraGHG"), x))==True]
        ecp_variables_map["ecp_ets_supra"+gas+"_usd_k"] = [x for x in list(temp_df.columns) if bool(re.match(re.compile("ets.+price+."), x))==True or bool(re.match(re.compile("cov_ets.+supra"+gas), x))==True]
        ecp_variables_map["ecp_tax_supraGHG_usd_k"] = [x for x in list(temp_df.columns) if bool(re.match(re.compile("tax.+rate+."), x))==True or bool(re.match(re.compile("cov_tax.+supraGHG"), x))==True]
        ecp_variables_map["ecp_tax_supra"+gas+"_usd_k"] = [x for x in list(temp_df.columns) if bool(re.match(re.compile("tax.+rate+."), x))==True or bool(re.match(re.compile("cov_tax.+supra"+gas), x))==True]

    if sectors == False:
        ecp_mapping = ecp_variables_map
    elif sectors == True:
        ecp_mapping = ecp_variables_map_sect
    
    for key in ecp_mapping.keys():
        temp_df[key] = 0
        length = int(len(ecp_mapping[key])/2)
        
        for i in range(0, length):
            cols = ecp_mapping[key]
            cols.sort()
            
            temp_df[key] = temp_df[cols[i]]*temp_df[cols[i+length]] #+ #nan values need to be replaced with 0 otherwise the sum won't work
        
        temp_df[key] = temp_df[key].astype(float)
    
    temp_df = temp_df[merge_keys+list(ecp_mapping.keys())] 
    
    
    temp_df = temp_df.fillna(0) # CHECK WHY "NA" VALUES ARE PRODUCED IN THE FIRST PLACE

    
    if sectors == False:
        temp_df["ecp_all_jurGHG_usd_k"] = temp_df["ecp_tax_jurGHG_usd_k"]+temp_df["ecp_ets_jurGHG_usd_k"]
        temp_df["ecp_all_jur"+gas+"_usd_k"] = temp_df["ecp_tax_jur"+gas+"_usd_k"]+temp_df["ecp_ets_jur"+gas+"_usd_k"]
        temp_df["ecp_all_wldGHG_usd_k"] = temp_df["ecp_tax_wldGHG_usd_k"]+temp_df["ecp_ets_wldGHG_usd_k"]
        temp_df["ecp_all_wld"+gas+"_usd_k"] = temp_df["ecp_tax_wld"+gas+"_usd_k"]+temp_df["ecp_ets_wld"+gas+"_usd_k"]

    elif sectors == True:
        temp_df["ecp_all_sect"+gas+"_usd_k"] = temp_df["ecp_tax_sect"+gas+"_usd_k"]+temp_df["ecp_ets_sect"+gas+"_usd_k"]
        
    if jur_level == "subnational" and sectors == False:
        temp_df["ecp_all_supraGHG_usd_k"] = temp_df["ecp_tax_supraGHG_usd_k"]+temp_df["ecp_ets_supraGHG_usd_k"]
        temp_df["ecp_all_supra"+gas+"_usd_k"] = temp_df["ecp_tax_supra"+gas+"_usd_k"]+temp_df["ecp_ets_supra"+gas+"_usd_k"]
        
    temp_df = temp_df.loc[~temp_df.ipcc_code.isin(flow_excl), :] # exclude aggregate sectors to avoid double counting
    
    return temp_df
    


def ecp_aggregation(ecp_df, gas, intro=None):
    # Step 1: Aggregate by jurisdiction and year
    ecp_agg = ecp_df.groupby(["jurisdiction", "year"], as_index=False).sum()

    # Step 2: Add world aggregate if not intro
    if intro is None:
        world_cols = [
            "ecp_ets_wldGHG_usd_k", f"ecp_ets_wld{gas}_usd_k",
            "ecp_tax_wldGHG_usd_k", f"ecp_tax_wld{gas}_usd_k"
        ]
        ecp_world_agg = (
            ecp_agg[["year"] + world_cols]
            .groupby("year", as_index=False)
            .sum()
            .rename(columns={
                f"ecp_tax_wldGHG_usd_k": f"ecp_tax_jurGHG_usd_k",
                f"ecp_tax_wld{gas}_usd_k": f"ecp_tax_jur{gas}_usd_k",
                f"ecp_ets_wldGHG_usd_k": f"ecp_ets_jurGHG_usd_k",
                f"ecp_ets_wld{gas}_usd_k": f"ecp_ets_jur{gas}_usd_k"
            })
        )
        ecp_world_agg["jurisdiction"] = "World"
        ecp_agg = pd.concat([ecp_agg, ecp_world_agg], ignore_index=True)

    # Step 3: Compute all-scheme columns
    ecp_agg[f"ecp_all_jurGHG_usd_k"] = (
        ecp_agg[f"ecp_tax_jurGHG_usd_k"] + ecp_agg[f"ecp_ets_jurGHG_usd_k"]
    )
    ecp_agg[f"ecp_all_jur{gas}_usd_k"] = (
        ecp_agg[f"ecp_tax_jur{gas}_usd_k"] + ecp_agg[f"ecp_ets_jur{gas}_usd_k"]
    )
    ecp_agg[f"ecp_all_supraGHG_usd_k"] = (
        ecp_agg[f"ecp_tax_supraGHG_usd_k"] + ecp_agg[f"ecp_ets_supraGHG_usd_k"]
    )
    ecp_agg[f"ecp_all_supra{gas}_usd_k"] = (
        ecp_agg[f"ecp_tax_supra{gas}_usd_k"] + ecp_agg[f"ecp_ets_supra{gas}_usd_k"]
    )

    return ecp_agg



def national_from_subnat(df, list_subnat, nat_jur, gas):
    # Filter and aggregate subnational data
    subnat_df = (
        df[df.jurisdiction.isin(list_subnat)]
        .groupby("year", as_index=False)
        .sum()
    )
    subnat_df["jurisdiction"] = nat_jur + "sub"

    # Set jurisdiction-level columns to NaN (will be filled after renaming)
    for col_base in ["ecp_ets", "ecp_tax", "ecp_all"]:
        for suffix in [f"jurGHG_usd_k", f"jur{gas}_usd_k"]:
            subnat_df[f"{col_base}_{suffix}"] = np.nan

    # Swap jurisdictional with supra-jurisdictional column names
    swap_keys = [
        "ecp_ets", "ecp_tax", "ecp_all"
    ]
    swap_list = {
        f"{key}_jurGHG_usd_k": f"{key}_supraGHG_usd_k" for key in swap_keys
    }
    swap_list.update({
        f"{key}_jur{gas}_usd_k": f"{key}_supra{gas}_usd_k" for key in swap_keys
    })
    # Add reverse mapping (supra → jur)
    swap_list.update({v: k for k, v in swap_list.items()})

    subnat_df.rename(columns=swap_list, inplace=True)

    # Combine with national data
    nat_df = df[df.jurisdiction == nat_jur]
    combined_nat = (
        pd.concat([nat_df, subnat_df])
        .groupby("year", as_index=False)
        .sum()
    )
    combined_nat["jurisdiction"] = nat_jur

    # Final output: remove old national entry and append updated one
    df_filtered = df[df.jurisdiction != nat_jur]
    df_final = pd.concat([df_filtered, combined_nat], ignore_index=True)

    return df_final