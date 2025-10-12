#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 09:27:32 2022

@author: gd
"""

import pandas as pd
from typing import Optional, Iterable
import pandas as pd
import numpy as np


# EMISSIONS SHARES

# National jurisdictions

def emissions_share(
    emissions: pd.DataFrame,
    jur_tot_emissions: pd.DataFrame,
    world_total: pd.DataFrame,
    gas: str,
    national_total: Optional[pd.DataFrame] = None,
    jur_level: str = "national",
) -> pd.DataFrame:
    """
    Add share columns for a given gas relative to jurisdiction/national, world, and (if subnational) supra totals.
    Produces NaN for divide-by-zero or missing denominators. Drops 'World' jurisdiction and Product in {'Total','Other'} if present.
    Keeps all original `emissions` columns except the gas column, plus the computed share columns.
    """

    # --- Validate inputs ---
    required_em_cols = {"jurisdiction", "year", gas}
    missing = required_em_cols - set(emissions.columns)
    if missing:
        raise KeyError(f"`emissions` missing columns: {sorted(missing)}")

    for df, name in [(jur_tot_emissions, "jur_tot_emissions"), (world_total, "world_total")]:
        need = {"year", gas, "all_GHG"}
        miss = need - set(df.columns)
        if miss:
            raise KeyError(f"`{name}` missing columns: {sorted(miss)}")

    if jur_level == "subnational":
        if "supra_jur" not in emissions.columns:
            raise KeyError("`emissions` must have 'supra_jur' for jur_level='subnational'.")
        if national_total is None:
            raise ValueError("`national_total` is required when jur_level='subnational'.")
        miss = {"jurisdiction", "year", gas, "all_GHG"} - set(national_total.columns)
        if miss:
            raise KeyError(f"`national_total` missing columns: {sorted(miss)}")

    # --- Prep totals (rename to avoid suffix juggling) ---
    temp_jur = jur_tot_emissions[["jurisdiction", "year", gas, "all_GHG"]].rename(
        columns={gas: f"{gas}_nat", "all_GHG": "all_GHG_nat"}
    )
    temp_wld = world_total[["year", gas, "all_GHG"]].rename(
        columns={gas: f"{gas}_wld", "all_GHG": "all_GHG_wld"}
    )

    # --- Merge totals onto emissions ---
    out = emissions.copy()
    out = out.merge(temp_jur, on=["jurisdiction", "year"], how="left")
    out = out.merge(temp_wld, on=["year"], how="left")

    # --- Optional supra totals for subnational ---
    share_vars_map = {
        f"{gas}_jurGHG": "all_GHG_nat",
        f"{gas}_jur{gas}": f"{gas}_nat",
        f"{gas}_wldGHG": "all_GHG_wld",
        f"{gas}_wld{gas}": f"{gas}_wld",
    }

    if jur_level == "subnational":
        supra_df = national_total.rename(columns={"all_GHG": "supra_all_GHG", gas: f"supra_{gas}"})
        out = out.merge(
            supra_df[["jurisdiction", "year", "supra_all_GHG", f"supra_{gas}"]],
            left_on=["supra_jur", "year"],
            right_on=["jurisdiction", "year"],
            how="left",
            suffixes=("", "_drop"),
        )
        # clean helper column from right_on
        if "jurisdiction_drop" in out.columns:
            out.drop(columns=["jurisdiction_drop"], inplace=True)

        share_vars_map[f"{gas}_supraGHG"] = "supra_all_GHG"
        share_vars_map[f"{gas}_supra{gas}"] = f"supra_{gas}"

    # --- Safe division helper (NaN on 0 or missing) ---
    def safe_div(num: pd.Series, denom: pd.Series) -> pd.Series:
        return num.astype(float).div(denom.replace({0: np.nan}))

    # --- Build return column list: keep all original except gas, then add shares ---
    ret_cols = [c for c in emissions.columns if c != gas]
    for share_col, denom_col in share_vars_map.items():
        out[share_col] = safe_div(out[gas], out[denom_col])

    out = out[ret_cols + list(share_vars_map.keys())]

    # --- Optional tidy-ups (best-effort) ---
    if "Product" in out.columns:
        out = out[~out["Product"].isin(["Total", "Other"])]
    if "jurisdiction" in out.columns:
        out = out[out["jurisdiction"] != "World"]

    return out



# World sectors

# Merge of 'Main_sectors.csv' and 'CAIT_Country_GHG_Emissions_TotEm.csv'. 
# Merge according to two keys, Country and Year, since the total yearly emissions figure for a given country and year is the same across Flows (sectors) and products (fuels). Output file: 'IEA_Em_share.csv'
    

def emissions_share_wld_sectors(
    emissions: pd.DataFrame,
    sectors_wld_total: pd.DataFrame,
    gas: str,
    jur_level: Optional[str] = None,
) -> pd.DataFrame:
    """
    Compute each record's share of the world-sector total for a given gas.

    Parameters
    ----------
    emissions : DataFrame
        Must contain 'year', 'ipcc_code', 'iea_code', the column named by `gas`,
        and id columns depending on `jur_level`:
          - jur_level == "national": includes 'jurisdiction' (and optionally 'Product').
          - other / None: includes 'jurisdiction' and (optionally) 'supra_jur'.
    sectors_wld_total : DataFrame
        Must contain 'year', 'ipcc_code', and the column named by `gas`
        giving world-sector totals for that gas.
    gas : str
        Name of the emissions column to use (e.g., "CO2e").
    jur_level : {"national", "subnational", None}, optional
        Controls which ID columns to retain (no effect on the math).

    Returns
    -------
    DataFrame
        Original rows plus a new column:
          f"wld_sect_share_{gas}"
        which is `emissions[gas] / world_sector_total`.
    """
    if gas not in emissions.columns:
        raise KeyError(f"`gas` column '{gas}' not found in `emissions`.")
    if gas not in sectors_wld_total.columns:
        raise KeyError(f"`gas` column '{gas}' not found in `sectors_wld_total`.")

    # Decide ID columns to keep (only what exists to avoid KeyErrors)
    base_cols: Iterable[str] = ["jurisdiction", "year", "ipcc_code", "iea_code", gas]
    keep_cols = [c for c in base_cols if c in emissions.columns]

    if jur_level == "national":
        # keep Product if present
        if "Product" in emissions.columns:
            keep_cols.append("Product")
    else:
        # non-national levels: keep supra_jur if present
        if "supra_jur" in emissions.columns:
            keep_cols.append("supra_jur")

    inventory = emissions[keep_cols].copy()

    # Prepare the world totals slice with a clear column name to avoid suffix juggling
    total_col = f"{gas}_wldSect"
    wld_totals = sectors_wld_total[["ipcc_code", "year", gas]].rename(columns={gas: total_col})

    # Merge only on the needed keys
    merged = inventory.merge(wld_totals, how="left", on=["ipcc_code", "year"])

    # Compute share safely (avoid divide-by-zero and preserve NaNs where totals are missing)
    share_col = f"{gas}_wld_sect_wld{gas}"
    denom = merged[total_col]
    with np.errstate(divide="ignore", invalid="ignore"):
        merged[share_col] = merged[gas].astype(float).div(denom.replace({0: np.nan}))

    # Drop helper total column
    merged.drop(columns=[total_col], inplace=True)

    return merged



# Share of subnational sector-level emissions in corresponding country-sector-level emissions

# sectors_ctry_total contains total emissions at country-sector level; `sectors_ctry_total` created in script ecp_v3.ipynb

def emissions_share_ctry_sectors(
    emissions: pd.DataFrame,
    sectors_ctry_total: pd.DataFrame,
    gas: str,
) -> pd.DataFrame:
    """
    Compute each record's share of the *country* sector total for `gas`.

    Output column added (same naming as your original):
        f"{gas}_ctry_sect_ctry{gas}"  # = emissions[gas] / country_sector_total(gas)

    Behavior:
      - Returns NaN where the denominator is 0 or missing.
      - Keeps original identifying columns (incl. 'iea_code' if present).
      - Does not create merge suffix columns.
    """

    # -------- Validate required columns --------
    required_em = {"supra_jur", "jurisdiction", "year", "ipcc_code", gas}
    missing_em = required_em - set(emissions.columns)
    if missing_em:
        raise KeyError(f"`emissions` missing columns: {sorted(missing_em)}")

    required_ctry = {"jurisdiction", "year", "ipcc_code", gas}
    missing_ctry = required_ctry - set(sectors_ctry_total.columns)
    if missing_ctry:
        raise KeyError(f"`sectors_ctry_total` missing columns: {sorted(missing_ctry)}")

    # -------- Select/prepare columns --------
    # Keep 'iea_code' if available (not required for merge)
    base_cols: List[str] = ["supra_jur", "jurisdiction", "year", "ipcc_code", gas]
    if "iea_code" in emissions.columns:
        base_cols.append("iea_code")

    inventory = emissions[base_cols].copy()

    # Rename right-hand columns to avoid _x/_y and keep only what's needed
    right = (
        sectors_ctry_total[["jurisdiction", "year", "ipcc_code", gas]]
        .rename(columns={
            "jurisdiction": "country_jur",
            gas: f"{gas}_ctrySect"
        })
    )

    # -------- Merge and compute safe share --------
    merged = inventory.merge(
        right,
        how="left",
        left_on=["supra_jur", "year", "ipcc_code"],
        right_on=["country_jur", "year", "ipcc_code"],
    )

    # Safe division: NaN if denominator is 0 or missing
    share_col = f"{gas}_ctry_sect_ctry{gas}"
    denom_col = f"{gas}_ctrySect"
    with np.errstate(divide="ignore", invalid="ignore"):
        merged[share_col] = merged[gas].astype(float).div(merged[denom_col].replace({0: np.nan}))

    # -------- Clean helpers and order columns --------
    # Remove helper columns from the right-hand frame
    merged.drop(columns=[denom_col, "country_jur"], inplace=True, errors="ignore")

    # Return original inventory columns + the share column
    return merged[inventory.columns.tolist() + [share_col]]
