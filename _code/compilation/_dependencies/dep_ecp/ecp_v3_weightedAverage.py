import pandas as pd
import numpy as np
import re


import re
import pandas as pd


def ecp(coverage_df, prices, jur_level, gas, flow_excl, weight_type, weight_year=None, sectors=False):
    
    # 1. Merge keys & filtered price data
    if jur_level == "national":
        merge_keys = ["jurisdiction", "year", "ipcc_code", "iea_code", "Product"]
        prices_temp = prices.copy()
    elif jur_level == "subnational":
        merge_keys = ["jurisdiction", "year", "ipcc_code", "iea_code"]
        prices_temp = prices.loc[prices.Product == "Natural gas"].copy()
        prices_temp.drop(columns=["Product"], inplace=True)
    else:
        raise ValueError(f"Invalid jurisdiction level: {jur_level}")

    # 2. Merge price data into coverage dataframe
    if weight_type == "time_varying":
        temp_df = coverage_df.copy()
        temp_df = temp_df.merge(prices_temp, on=merge_keys, how="left")
    elif weight_type == "fixed":
        temp_df = coverage_df[coverage_df.year == weight_year].drop(columns=["year"])
        merge_keys_fw = [k for k in merge_keys if k != "year"]
        temp_df = temp_df.merge(prices_temp, on=merge_keys_fw, how="right")
    else:
        raise ValueError(f"Invalid weight_type: {weight_type}")
    
    # 3. Define variable mapping (pattern-based)
    def get_cols(patterns):
        return [col for col in temp_df.columns if any(re.search(pat, col) for pat in patterns)]

    ecp_variables_map = {
        f"ecp_ets_jurGHG_usd_k": get_cols([r"ets.*price", r"cov_ets.*jurGHG"]),
        f"ecp_ets_jur{gas}_usd_k": get_cols([r"ets.*price", fr"cov_ets.*jur{gas}"]),
        f"ecp_ets_wldGHG_usd_k": get_cols([r"ets.*price", r"cov_ets.*wldGHG"]),
        f"ecp_ets_wld{gas}_usd_k": get_cols([r"ets.*price", fr"cov_ets.*wld{gas}"]),
        f"ecp_tax_jurGHG_usd_k": get_cols([r"tax.*rate", r"cov_tax.*jurGHG"]),
        f"ecp_tax_jur{gas}_usd_k": get_cols([r"tax.*rate", fr"cov_tax.*jur{gas}"]),
        f"ecp_tax_wldGHG_usd_k": get_cols([r"tax.*rate", r"cov_tax.*wldGHG"]),
        f"ecp_tax_wld{gas}_usd_k": get_cols([r"tax.*rate", fr"cov_tax.*wld{gas}"]),
    }

    ecp_variables_map_sect = {
        f"ecp_ets_sect{gas}_usd_k": get_cols([r"ets.*price", fr"cov_ets.*wld{gas}"]),
        f"ecp_tax_sect{gas}_usd_k": get_cols([r"tax.*rate", fr"cov_tax.*wld{gas}"]),
    }

    if jur_level == "subnational" and not sectors:
        ecp_variables_map.update({
            f"ecp_ets_supraGHG_usd_k": get_cols([r"ets.*price", r"cov_ets.*supraGHG"]),
            f"ecp_ets_supra{gas}_usd_k": get_cols([r"ets.*price", fr"cov_ets.*supra{gas}"]),
            f"ecp_tax_supraGHG_usd_k": get_cols([r"tax.*rate", r"cov_tax.*supraGHG"]),
            f"ecp_tax_supra{gas}_usd_k": get_cols([r"tax.*rate", fr"cov_tax.*supra{gas}"]),
        })

    # 4. Choose correct mapping
    ecp_mapping = ecp_variables_map_sect if sectors else ecp_variables_map

    # 5. Compute effective carbon prices
    print("\nSector ECP mapping:")
    for key, cols in ecp_mapping.items():
        print(f"{key}: {len(cols)} columns → {cols}")

        if len(cols) % 2 != 0:
            raise ValueError(f"Expected pairs of price and coverage columns for {key}, got odd number of columns.")
        
        temp_df[key] = 0.0
        cols = sorted(cols)
        half = len(cols) // 2
        
        for i in range(half):
            temp_df[key] += temp_df[cols[i]].fillna(0) * temp_df[cols[i + half]].fillna(0)

    # 6. Build total ECP columns
    if not sectors:
        temp_df["ecp_all_jurGHG_usd_k"] = temp_df["ecp_tax_jurGHG_usd_k"] + temp_df["ecp_ets_jurGHG_usd_k"]
        temp_df[f"ecp_all_jur{gas}_usd_k"] = temp_df[f"ecp_tax_jur{gas}_usd_k"] + temp_df[f"ecp_ets_jur{gas}_usd_k"]
        temp_df["ecp_all_wldGHG_usd_k"] = temp_df["ecp_tax_wldGHG_usd_k"] + temp_df["ecp_ets_wldGHG_usd_k"]
        temp_df[f"ecp_all_wld{gas}_usd_k"] = temp_df[f"ecp_tax_wld{gas}_usd_k"] + temp_df[f"ecp_ets_wld{gas}_usd_k"]
    
    if sectors==True:
        temp_df[f"ecp_all_sect{gas}_usd_k"] = temp_df[f"ecp_tax_sect{gas}_usd_k"] + temp_df[f"ecp_ets_sect{gas}_usd_k"]

    if jur_level == "subnational" and not sectors:
        temp_df["ecp_all_supraGHG_usd_k"] = temp_df["ecp_tax_supraGHG_usd_k"] + temp_df["ecp_ets_supraGHG_usd_k"]
        temp_df[f"ecp_all_supra{gas}_usd_k"] = temp_df[f"ecp_tax_supra{gas}_usd_k"] + temp_df[f"ecp_ets_supra{gas}_usd_k"]

    # 7. Final cleanup
    ecp_total_keys = [col for col in temp_df.columns if col.startswith("ecp_all_")]
    output_cols = merge_keys + list(ecp_mapping.keys()) + ecp_total_keys
    temp_df = temp_df[output_cols].fillna(0)
    
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