# Refactored and modular version of subnational GHG inventory compilation
import os
import sys
import glob
from pathlib import Path
import pandas as pd
import numpy as np
import dep_ecp

from wcpd_utils.jurisdictions import jurisdictions as jur_loader

from dep_ecp.ipcc_map_subnat import (
    category_names_ipcc_can_map,
    category_names_ipcc_chn_map,
    category_names_ipcc_usa_map,
)
from dep_ecp.jur_names_concordances import subnat_names_map_chn

category_names_ipcc_can_map = {int(k): v for k, v in category_names_ipcc_can_map.items()}

# --- Load subnational jurisdictions ---
subnat_can = jur_loader["subnationals"]["Canada"] 
subnat_chn = jur_loader["subnationals"]["China"] 
subnat_jpn = jur_loader["subnationals"]["Japan"] 
subnat_mex = jur_loader["subnationals"]["Mexico"]
subnat_usa = jur_loader["subnationals"]["United States"]

# --- Constants ---
GHG_COLUMNS = ["CO2", "CH4", "N2O", "HFCs", "PFCs", "SF6", "NF3", "all_GHG"]
CONVERT_COLUMNS = ["CO2", "CH4", "N2O", "F-GASES", "all_GHG"]

DEFAULT_GHG_RAW_ROOT = Path(
    os.environ.get("GHG_INVENTORY_RAW_ROOT", "/Users/geoffroydolphin/GitHub/ECP/_raw/ghg_inventory/raw")
)
DEFAULT_EDGAR_OUTPUT_ROOT = Path(
    os.environ.get(
        "EDGAR_GHG_OUTPUT_ROOT",
        "/Users/geoffroydolphin/GitHub/ECP/_raw/ghg_inventory/raw/subnational/jrc_edgar_gridded/output",
    )
)

EDGAR_JUR_NAME_REMAP = {
    "Hyōgo": "Hyogo",
    "Naoasaki": "Nagasaki",
    "Coahuila": "Coahuila de Zaragoza",
    "Distrito Federal": "Ciudad de Mexico",
    "México": "Mexico State",
    "Michoacán": "Michoacan de Ocampo",
    "Nuevo León": "Nuevo Leon",
    "Querétaro": "Queretaro de Arteaga",
    "San Luis Potosí": "San Luis Potosi",
    "Veracruz": "Veracruz de Ignacio de la Llave",
    "Yucatán": "Yucatan",
}

def _resolve_root(path, default):
    return Path(path) if path else default


# --- Load and clean Canada inventory ---
def load_canada_data(path=None):
    root = _resolve_root(path, DEFAULT_GHG_RAW_ROOT)
    df = pd.read_csv(
        root / "subnational/Canada/harmonized_data/ECCC/GHG_IPCC_Can_Prov_Terr_2023.csv"
    )
    df = df[~df.Region.str.lower().eq("canada")]

    df.drop(columns=["Rollup", "Category", "Source", "Sub-category", "Sub-sub-category", "CH4", "N2O", "Total", "Unit"], errors="ignore", inplace=True)
    df.rename(columns={
        "Region": "jurisdiction", "CategoryID": "ipcc_code", "Year": "year",
        "CH4 (CO2eq)": "CH4", "N2O (CO2eq)": "N2O", "CO2eq": "all_GHG"
    }, inplace=True)

    df = df[~df.ipcc_code.isna()]
    df.ipcc_code.replace(category_names_ipcc_can_map, inplace=True)

    df[GHG_COLUMNS] = df[GHG_COLUMNS].replace("x", np.nan).astype(float)
    df["F-GASES"] = df[["HFCs", "PFCs", "SF6", "NF3"]].sum(axis=1)
    df.drop(columns=["HFCs", "PFCs", "SF6", "NF3"], inplace=True)
    df["supra_jur"] = "Canada"

    return df[["supra_jur", "jurisdiction", "year", "ipcc_code"] + CONVERT_COLUMNS]


# --- Load and clean China inventory ---
def load_china_data(path=None):
    root = _resolve_root(path, DEFAULT_GHG_RAW_ROOT)
    inv_jur_names = pd.read_excel(
        root / "subnational/China/CEADS/CEADS_provincial_emissions/Emission_inventories_for_30_provinces_1997.xlsx",
        sheet_name="Sum",
    )
    provinces = list(inv_jur_names["Unnamed: 0"])[:-2]
    file_list = [
        f
        for f in os.listdir(root / "subnational/China/CEADS/CEADS_provincial_emissions/")
        if f.endswith(".xlsx")
    ]

    comb, proc = [], []
    for file in file_list:
        for prov in provinces:
            df = pd.read_excel(
                root / f"subnational/China/CEADS/CEADS_provincial_emissions/{file}",
                sheet_name=prov,
                skiprows=[1, 2],
            )
            df.rename(columns={"Unnamed: 0": "ipcc_code"}, inplace=True)
            df["year"] = file[-9:-5]
            df["jurisdiction"] = prov

            df_comb = df[["jurisdiction", "year", "ipcc_code"]].copy()
            df_comb["CO2"] = df["Total"] - df["Process"]

            df_proc = df[["jurisdiction", "year", "ipcc_code"]].copy()
            df_proc["CO2"] = df["Process"]

            comb.append(df_comb)
            proc.append(df_proc[df_proc.ipcc_code == "Nonmetal Mineral Products"])

    df_comb = pd.concat(comb).replace(subnat_names_map_chn).replace(category_names_ipcc_chn_map)
    df_proc = pd.concat(proc).replace(subnat_names_map_chn)
    df_proc.replace({"Nonmetal Mineral Products": "2A"}, inplace=True)

    china = pd.concat([df_comb, df_proc])
    china = china[china.ipcc_code != "Total Consumption"]
    china = china.groupby(["jurisdiction", "year", "ipcc_code"])["CO2"].sum().reset_index()
    china["year"] = china["year"].astype(int)
    for gas in ["CH4", "N2O", "F-GASES", "all_GHG"]:
        china[gas] = np.nan
    for col in CONVERT_COLUMNS:
        china[col] *= 1000
    china["supra_jur"] = "China"
    return china[["supra_jur", "jurisdiction", "year", "ipcc_code"] + CONVERT_COLUMNS]


# --- Load and clean United States inventory ---
def load_usa_data(path=None):
    root = _resolve_root(path, DEFAULT_GHG_RAW_ROOT)
    data_dir = root / "subnational/United_States/Rhodium/2024"
    file_list = glob.glob(os.path.join(data_dir, "*.csv"))

    df_list = []
    for file in file_list:
        temp = pd.read_csv(file, decimal=".")
        temp["Year"] = temp["Year"].apply(lambda x: x.replace(',','')).astype(int)
        state_name = os.path.basename(file)[len("DetailedGHGinventory_"):-4].replace("_", " ").title()
        temp["jurisdiction"] = state_name
        temp.drop(columns=["Ranking", "Sector"], inplace=True)
        df_list.append(temp)

    df = pd.concat(df_list)
    sub_ind = pd.read_csv(
        root / "subnational/United_States/Rhodium/2022/industry/TS2022_central_subind_ghg.csv"
    )
    sub_ind = sub_ind[sub_ind.Gas == "CO2 (combustion)"] # keeping only the more detailed data for CO2 combustion
    sub_ind.rename(columns={"StateName": "jurisdiction", "Industry": "Subsector"}, inplace=True) # excluding this category because we have disaggregated data for the sub-industries

    df = df[df.Subsector != "Industry - All combustion"]
    df = pd.concat([df, sub_ind])
    df["ipcc_code"] = df["Subsector"].replace(category_names_ipcc_usa_map)

    excl = ['Transport - Natural gas pipeline', 'Carbon Dioxide Consumption', 'Abandoned Oil and Gas Wells', 'Phosphoric Acid Production',
            'Natural Gas Systems', 'Petroleum Systems', 'Urea Consumption for Non-Agricultural Purposes', 
            "LULUCF CH4 Emissions", "LULUCF Carbon Stock Change", "LULUCF N2O Emissions", "Balance of Manufacturing", "LNG Export", "MVAC"]
    df = df[~df.ipcc_code.isin(excl)] # excluding LULUCF emissions because we want totals that exclude those

    df["Gas"].replace({"CO2 (combustion)": "CO2", "CO2 (non-combustion)": "CO2"}, inplace=True)
    df.rename(columns={"Year": "year"}, inplace=True)
    df = df[df.year <= 2021]
    df["Total Emission(mmt CO2)"] = df["Total Emission(mmt CO2)"].astype(float)

    df = df.groupby(["jurisdiction", "year", "Gas", "ipcc_code"])["Total Emission(mmt CO2)"].sum().reset_index()
    df = df.pivot(index=["jurisdiction", "year", "ipcc_code"], columns="Gas", values="Total Emission(mmt CO2)").reset_index()

    df["F-GASES"] = df[["HFCs", "PFCs", "NF3", "SF6"]].sum(axis=1)
    df["all_GHG"] = df[["CO2", "CH4", "N2O", "F-GASES"]].sum(axis=1)
    df.drop(columns=["NF3", "SF6", "PFCs", "HFCs"], inplace=True)

    df["jurisdiction"].replace({"Georgia": "Georgia_US"}, inplace=True)
    for col in CONVERT_COLUMNS:
        df[col] *= 1000
    df["supra_jur"] = "United States"
    return df[["supra_jur", "jurisdiction", "year", "ipcc_code"] + CONVERT_COLUMNS]


# --- Load Japan/Mexico subnational inventory from EDGAR gridmaps ---
def load_edgar_subnat_jpn_mex(output_root=None, countries=None, iso3s=None):
    root = _resolve_root(output_root, DEFAULT_EDGAR_OUTPUT_ROOT)
    by_gas = root / "by_gas_sector"
    files = sorted(by_gas.glob("*/*/adm1_inventory_long.csv"))
    if not files:
        raise FileNotFoundError(f"No EDGAR outputs found under {by_gas}")

    supported = {
        "JPN": ("Japan", subnat_jpn),
        "MEX": ("Mexico", subnat_mex),
    }
    if countries is None and iso3s is None:
        iso3_set = set(supported.keys())
    else:
        iso3_set = set()
        if iso3s:
            iso3_set.update(str(x).upper() for x in iso3s)
        if countries:
            for name in countries:
                for iso3, (country, _) in supported.items():
                    if str(name).strip().lower() == country.lower():
                        iso3_set.add(iso3)
                        break

    iso3_set = {i for i in iso3_set if i in supported}
    if not iso3_set:
        raise ValueError("No supported countries provided. Use Japan/Mexico or ISO3 JPN/MEX.")

    frames = []
    usecols = ["iso3", "adm1_name", "year", "ipcc_category", "gas", "emissions"]
    for path in files:
        df = pd.read_csv(path, usecols=usecols)
        df = df[df.iso3.isin(iso3_set)]
        if not df.empty:
            frames.append(df)

    if not frames:
        raise FileNotFoundError(f"No EDGAR rows found for {sorted(iso3_set)}.")

    df = pd.concat(frames, ignore_index=True)
    df = df.rename(
        columns={
            "adm1_name": "jurisdiction",
            "ipcc_category": "ipcc_code",
            "emissions": "value",
        }
    )
    df["ipcc_code"] = df["ipcc_code"].astype(str)
    df["ipcc_code"] = df["ipcc_code"].where(
        ~df["ipcc_code"].str.startswith("1A3a_"), "1A3a"
    )
    df["jurisdiction"] = df["jurisdiction"].replace(EDGAR_JUR_NAME_REMAP)
    df["supra_jur"] = df["iso3"].map({k: v[0] for k, v in supported.items()})
    df = df[df["supra_jur"].notna()]
    df = df[df["ipcc_code"].notna()]

    df = df[df["gas"].isin(["CO2", "CH4", "N2O"])]
    df["value"] = df["value"].astype(float) / 1000.0  # tonnes -> kt

    df = (
        df.groupby(["supra_jur", "jurisdiction", "year", "ipcc_code", "gas"])["value"]
        .sum()
        .reset_index()
    )
    df = df.pivot(
        index=["supra_jur", "jurisdiction", "year", "ipcc_code"],
        columns="gas",
        values="value",
    ).reset_index()

    for col in ["CO2", "CH4", "N2O"]:
        if col not in df.columns:
            df[col] = np.nan
    df["F-GASES"] = np.nan
    df["all_GHG"] = df[["CO2", "CH4", "N2O"]].sum(axis=1, min_count=1)

    valid_rows = False
    masks = []
    for iso3 in iso3_set:
        country, subnat_list = supported[iso3]
        masks.append((df["supra_jur"] == country) & (df["jurisdiction"].isin(subnat_list)))
        valid_rows = True
    if valid_rows:
        mask = masks[0]
        for m in masks[1:]:
            mask = mask | m
        df = df[mask]

    return df[["supra_jur", "jurisdiction", "year", "ipcc_code"] + CONVERT_COLUMNS]


# --- Generate totals excluding LULUCF ---
def generate_subnat_total(can, chn, usa, jpn=None, mex=None):
    can_tot = can[can.ipcc_code == "0"].drop(columns="ipcc_code")
    can_lulucf = can[can.ipcc_code == "3B"].drop(columns=["ipcc_code", "supra_jur"])
    can_tot = can_tot.merge(can_lulucf, on=["jurisdiction", "year"], how="left", suffixes=("", "_lulucf"))

    for gas in CONVERT_COLUMNS:
        can_tot[gas] = can_tot[gas] - can_tot.pop(f"{gas}_lulucf")

    def _totals(df):
        return df.groupby(["supra_jur", "jurisdiction", "year"])[CONVERT_COLUMNS].sum().reset_index()

    totals = [can_tot, _totals(chn), _totals(usa)]
    if jpn is not None:
        totals.append(_totals(jpn))
    if mex is not None:
        totals.append(_totals(mex))
    return pd.concat(totals, ignore_index=True)


# --- Combine subnational inventories with WCPD structure ---
def build_inventory_subnat(wcpd_df, subnat_names, mapping_ipcc_iea, gas, can, chn, usa, jpn=None, mex=None):
    inventory = wcpd_df[wcpd_df.jurisdiction.isin(subnat_names)][["jurisdiction", "year", "ipcc_code", "iea_code"]].drop_duplicates()
    inventory.iea_code.fillna("NA", inplace=True)

    parts = [
        can[["supra_jur", "jurisdiction", "year", "ipcc_code", gas]],
        chn[["supra_jur", "jurisdiction", "year", "ipcc_code", gas]],
        usa[["supra_jur", "jurisdiction", "year", "ipcc_code", gas]],
    ]
    if jpn is not None:
        parts.append(jpn[["supra_jur", "jurisdiction", "year", "ipcc_code", gas]])
    if mex is not None:
        parts.append(mex[["supra_jur", "jurisdiction", "year", "ipcc_code", gas]])
    combined = pd.concat(parts)

    combined = combined.merge(mapping_ipcc_iea, on="ipcc_code", how="left")
    combined.iea_code.fillna("NA", inplace=True)

    inventory["supra_jur"] = inventory.jurisdiction.map({
        **{j: "Canada" for j in subnat_can},
        **{j: "United States" for j in subnat_usa},
        **{j: "China" for j in subnat_chn},
        **{j: "Japan" for j in subnat_jpn},
        **{j: "Mexico" for j in subnat_mex},
    })

    return inventory.merge(combined, on=["supra_jur", "jurisdiction", "year", "ipcc_code", "iea_code"], how="left")[[
        "supra_jur", "jurisdiction", "year", "ipcc_code", "iea_code", gas
    ]]
