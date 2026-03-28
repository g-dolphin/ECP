#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 10:05:24 2022

@author: gd
"""

import os
from pathlib import Path

import pandas as pd

from dep_ecp import ecp_v3_gen_func as ecp_gen

def _resolve_wcpd_repo_root():
    candidates = []

    env_root = os.environ.get("WCPD_REPO_ROOT")
    if env_root:
        candidates.append(Path(env_root).expanduser())

    cwd = Path.cwd().resolve()
    candidates.extend([
        cwd.parent / "WorldCarbonPricingDatabase",
        Path.home() / "GitHub" / "WorldCarbonPricingDatabase",
    ])

    for candidate in candidates:
        if (candidate / "_raw" / "coverageFactor").exists():
            return candidate

    raise FileNotFoundError(
        "Could not find the WorldCarbonPricingDatabase checkout. "
        "Set WCPD_REPO_ROOT to the repo root."
    )

def coverageFactors(inst_df, gas, wcpd_repo_root=None):
    
    tax_id_cols = [x for x in inst_df.columns if x.startswith("tax_") and x.endswith("_id")]
    ets_id_cols = [x for x in inst_df.columns if x.startswith("ets_") and x.endswith("_id")]
    
    ## LOAD COVERAGE FACTORS FILES 
    wcpd_repo_root = Path(wcpd_repo_root).expanduser() if wcpd_repo_root else _resolve_wcpd_repo_root()
    coverage_dir = wcpd_repo_root / "_raw" / "coverageFactor" / gas
    coverage_files = sorted(coverage_dir.glob("*.csv"))
    coverageFactor = pd.concat([pd.read_csv(path) for path in coverage_files], ignore_index=True)
    coverageFactor = coverageFactor[["scheme_id", "jurisdiction", "year", "ipcc_code", "cf_"+gas]]

    dup_keys = ["scheme_id", "jurisdiction", "year", "ipcc_code"]
    duplicate_rows = coverageFactor[coverageFactor.duplicated(subset=dup_keys, keep=False)]
    if not duplicate_rows.empty:
        conflicting = (
            duplicate_rows.groupby(dup_keys)["cf_"+gas]
            .nunique()
            .gt(1)
            .sum()
        )
        print(
            f"coverageFactor has {duplicate_rows[dup_keys].drop_duplicates().shape[0]} duplicate keys "
            f"for {gas}; keeping the last row per key from sorted files "
            f"({int(conflicting)} keys had conflicting cf values)."
        )
        coverageFactor = coverageFactor.drop_duplicates(subset=dup_keys, keep="last")

    ## CREATE ONE COVERAGE FACTOR, "cf", COLUMN IN `wcpd_all` DATAFRAME FOR EACH PRICING MECHANISM COLUMN
    ### i.e., tax_cf, tax_II_cf,..., ets_cf, ets_II_cf; NOTE: the WCPD dataset currently has one tax column and one ets column 
    ### but eventually would have more of each instrument type

    # merge on [jurisdiction, year, ipcc_code, scheme_id]
    mechanism_id_cols = ["ets_id", "ets_2_id", "tax_id", "tax_2_id"]

    cf_col_names = dict(zip(mechanism_id_cols, ["ets_cf", "ets_2_cf", "tax_cf", "tax_2_cf"]))

    cf_cols = []

    for id_col_name in mechanism_id_cols:
        if id_col_name in inst_df.columns:

            merge_keys = ["jurisdiction", "year", "ipcc_code"] + [id_col_name]

            inst_df = inst_df.merge(coverageFactor, left_on=merge_keys,
                                    right_on=["jurisdiction", "year", "ipcc_code", "scheme_id"], how="left")
            inst_df.drop(["scheme_id"], axis=1, inplace=True)
            inst_df.rename(columns={"cf_"+gas:cf_col_names[id_col_name]}, inplace=True)

            cf_cols = cf_cols + [cf_col_names[id_col_name]]

    # re-ordering columns
    # error handling introduced to deal with absence of 'iea_code' in 'overlap' script dataframe
    try:
        inst_df = inst_df[['jurisdiction', 'year', 'ipcc_code', 'iea_code', 'Product', 'tax',
                        'ets']+[tax_id_cols[0]]+['tax_rate_excl_ex_clcu', 'tax_ex_rate',
                        'tax_rate_incl_ex_clcu', 'tax_curr_code']+[ets_id_cols[0]]+['ets_price',
                        'ets_curr_code']+[ets_id_cols[1]]+['ets_2_price',
                        'ets_2_curr_code']+cf_cols]
    except:
        inst_df = inst_df[['jurisdiction', 'year', 'ipcc_code', 'Product', 'tax',
                        'ets']+[tax_id_cols[0]]+['tax_rate_excl_ex_clcu', 'tax_ex_rate',
                        'tax_rate_incl_ex_clcu', 'tax_curr_code']+[ets_id_cols[0]]+['ets_price',
                        'ets_curr_code']+[ets_id_cols[1]]+['ets_2_price',
                        'ets_2_curr_code']+cf_cols]

    return inst_df
