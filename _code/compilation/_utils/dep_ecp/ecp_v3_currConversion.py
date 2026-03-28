# Refactored script for emissions prices and rates conversion

import os
import pandas as pd
import numpy as np
import re
from pathlib import Path
from importlib.machinery import SourceFileLoader

def extend_latest_year_by_group(df, group_cols, year_col, value_cols, target_year):
    if target_year is None or df.empty:
        return df

    max_year = df[year_col].max()
    if pd.isna(max_year) or max_year >= target_year:
        return df

    latest = (
        df.sort_values(group_cols + [year_col])
        .groupby(group_cols, as_index=False)
        .tail(1)
        .copy()
    )

    extensions = []
    for year in range(int(max_year) + 1, int(target_year) + 1):
        ext = latest.copy()
        ext[year_col] = year
        extensions.append(ext)

    if not extensions:
        return df

    return pd.concat([df, *extensions], ignore_index=True)


def load_exchange_rates(path, x_rate_fixed, target_year=None):
    x_rate = pd.read_csv(path)
    if x_rate_fixed:
        x_rate = x_rate[x_rate.year == 2019].drop(columns=["year"])
    else:
        x_rate = extend_latest_year_by_group(
            x_rate,
            group_cols=["currency_code"],
            year_col="year",
            value_cols=["x-rate"],
            target_year=target_year,
        )
    x_rate = x_rate.drop_duplicates(["currency_code"] if x_rate_fixed else ["currency_code", "year"])
    x_rate = x_rate.drop(columns="jurisdiction")
    return x_rate

def load_and_prepare_gdp_deflator(ecp_general, base_year, target_year=None):
    gdp_dfl = ecp_general.wb_series("GDP deflator: linked series (base year varies by country)", "gdp_dfl")
    gdp_dfl = gdp_dfl[gdp_dfl.year >= 1985]
    if target_year is not None:
        gdp_dfl = gdp_dfl[gdp_dfl.year <= target_year]
    gdp_dfl = gdp_dfl.sort_values(["jurisdiction", "year"]).copy()
    gdp_dfl["gdp_dfl"] = gdp_dfl.groupby("jurisdiction")["gdp_dfl"].ffill()

    gdp_dfl_ii = pd.DataFrame()
    for jur in gdp_dfl.jurisdiction.unique():
        temp = gdp_dfl[gdp_dfl.jurisdiction == jur]
        base_row = temp[temp.year == base_year].rename(columns={"gdp_dfl": "gdp_dfl_base_year"}).drop(columns=["year"])
        temp = temp.merge(base_row, on="jurisdiction", how="left")
        temp["base_year_ratio"] = temp.gdp_dfl_base_year / temp.gdp_dfl
        gdp_dfl_ii = pd.concat([gdp_dfl_ii, temp], ignore_index=True)

    gdp_dfl_ii = extend_latest_year_by_group(
        gdp_dfl_ii,
        group_cols=["jurisdiction"],
        year_col="year",
        value_cols=["gdp_dfl", "gdp_dfl_base_year", "base_year_ratio"],
        target_year=target_year,
    )

    return gdp_dfl_ii

def clone_national_to_subnationals(gdp_dfl, national_jur, subnat_list):
    if not subnat_list:
        return gdp_dfl.iloc[0:0].copy()
    template = gdp_dfl[gdp_dfl.jurisdiction == national_jur]
    clones = [template.assign(jurisdiction=subnat) for subnat in subnat_list]
    return pd.concat(clones, ignore_index=True)

def generate_price_columns(wcpd_usd, price_columns, x_rate_dic, base_year, use_fixed_rate):
    suffix = "_usd_k" if base_year else "_usd"
    version_id = ("kFixRate" if use_fixed_rate else "kFlxRate") if base_year else ("cFixRate" if use_fixed_rate else "cFlxRate")
    path = f"{'constantPrices' if base_year else 'currentPrices'}/{'FixedXRate' if use_fixed_rate else 'FlexXRate'}"

    price_cols_dic = {}
    for col in price_columns:
        new_col = col[:-5] + suffix
        factor = 1 / wcpd_usd[x_rate_dic[col]]
        if base_year:
            factor *= wcpd_usd["base_year_ratio"]
        wcpd_usd[new_col] = wcpd_usd[col] * factor
        price_cols_dic[col] = new_col

    return wcpd_usd, price_cols_dic, version_id, path

def cur_conv(wcpd_all, gas, subnat_can_list, subnat_usa_list, subnat_chn_list, xRateFixed, baseYear=None):
    base_path = Path("/Users/geoffroydolphin/GitHub/ECP/_raw")
    dep_path = Path("/Users/geoffroydolphin/GitHub/ECP/_code/compilation/_utils/dep_ecp")
    ecp_general = SourceFileLoader('general_func', str(dep_path / 'ecp_v3_gen_func.py')).load_module()

    target_year = int(wcpd_all["year"].max())

    x_rate = load_exchange_rates(base_path / "wb_rates/xRate_bis.csv", xRateFixed, target_year=target_year)
    gdp_dfl = load_and_prepare_gdp_deflator(ecp_general, baseYear, target_year=target_year)

    gdp_dfl = pd.concat([
        gdp_dfl,
        clone_national_to_subnationals(gdp_dfl, "Canada", subnat_can_list),
        clone_national_to_subnationals(gdp_dfl, "United States", subnat_usa_list),
        clone_national_to_subnationals(gdp_dfl, "China", subnat_chn_list)
    ], ignore_index=True)

    wcpd_usd = wcpd_all.copy()
    fallback_tax_mask = (
        wcpd_usd["tax_rate_incl_ex_clcu"].isna()
        & wcpd_usd["tax_rate_excl_ex_clcu"].notna()
    )
    wcpd_usd.loc[fallback_tax_mask, "tax_rate_incl_ex_clcu"] = (
        wcpd_usd.loc[fallback_tax_mask, "tax_rate_excl_ex_clcu"]
        * (1 - wcpd_usd.loc[fallback_tax_mask, "tax_ex_rate"].fillna(0))
    )
    wcpd_usd.rename(columns={"ets_price":"ets_price_clcu", "ets_2_price":"ets_2_price_clcu"}, inplace=True)

    dic_keys = [x for x in wcpd_usd.columns if "curr_code" in x]
    for col in dic_keys:
        wcpd_usd[col] = wcpd_usd[col].astype("string")
    dic_values = [x[:-4]+"x_rate" for x in dic_keys]
    curr_code_map = dict(zip(dic_keys, dic_values))

    for name in curr_code_map:
        merge_keys_left = [name] if xRateFixed else [name, "year"]
        merge_keys_right = ['currency_code'] if xRateFixed else ["currency_code", "year"]
        x_rate_merge = x_rate.copy()
        wcpd_usd = pd.merge(wcpd_usd, x_rate_merge, how='left', left_on=merge_keys_left, right_on=merge_keys_right)
        wcpd_usd.rename(columns={"x-rate": curr_code_map[name]}, inplace=True)
        wcpd_usd.drop(columns=["currency_code"], inplace=True)

    wcpd_usd = wcpd_usd.merge(gdp_dfl[["jurisdiction", "year", "base_year_ratio"]], on=["jurisdiction", "year"], how="left")

    price_columns = [col for col in wcpd_usd.columns if re.match(r"ets.+price|tax.+rate_incl+.", col)]
    x_rate_dic = dict(zip(price_columns, dic_values))

    wcpd_usd, price_cols_dic, versionID, subdir = generate_price_columns(wcpd_usd, price_columns, x_rate_dic, baseYear, xRateFixed)

    jur_dic = {j: j.replace(".", "").replace(",", "").replace(" ", "_") for j in wcpd_usd.jurisdiction.unique()}
    output_dir = base_path / "wcpd_usd" / gas / subdir
    output_dir.mkdir(parents=True, exist_ok=True)

    for f in os.listdir(output_dir):
        os.remove(output_dir / f)

    col_sel = ['jurisdiction', 'year', 'ipcc_code', 'iea_code', 'Product'] + list(price_cols_dic.keys()) + list(curr_code_map.keys()) + list(price_cols_dic.values()) + list(x_rate_dic.values())
    for jur in wcpd_usd.jurisdiction.unique():
        df_jur = wcpd_usd[wcpd_usd.jurisdiction == jur][col_sel]
        df_jur.to_csv(output_dir / f"prices_usd_{versionID}_{gas}_{jur_dic[jur]}.csv", index=False)

    return wcpd_usd
