# Refactored and modular version of subnational GHG inventory compilation
import os
import sys
import glob
import pandas as pd
import numpy as np

# --- Load dependencies as modules ---
sys.path.append("/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/_dependencies")
from jurisdictions import jurisdictions

# --- Load remaining dependencies as modules ---
sys.path.append("/Users/gd/GitHub/ECP/_code/compilation/_dependencies/dep_ecp")
from ipcc_map_subnat import category_names_ipcc_can_map, category_names_ipcc_chn_map, category_names_ipcc_usa_map
from jur_names_concordances import subnat_names_map_chn

# --- Load subnational jurisdictions ---
subnat_can = jurisdictions["subnationals"]["Canada"] 
subnat_chn = jurisdictions["subnationals"]["China"] 
subnat_jpn = jurisdictions["subnationals"]["Japan"] 
subnat_usa = jurisdictions["subnationals"]["United States"]

# --- Constants ---
GHG_COLUMNS = ["CO2", "CH4", "N2O", "HFCs", "PFCs", "SF6", "NF3", "all_GHG"]
CONVERT_COLUMNS = ["CO2", "CH4", "N2O", "F-GASES", "all_GHG"]


# --- Load and clean Canada inventory ---
def load_canada_data(path):
    df = pd.read_csv(f"{path}/subnational/Canada/harmonized_data/ECCC/GHG_IPCC_Can_Prov_Terr_2021.csv")
    df = df[df.Region != "Canada"]

    df.rename(columns={
        "Region": "jurisdiction", "Category": "ipcc_code", "Year": "year",
        "CH4 (CO2eq)": "CH4", "N2O (CO2eq)": "N2O", "CO2eq": "all_GHG"
    }, inplace=True)

    df.drop(columns=["Rollup", "CategoryID", "CH4", "N2O", "Unit"], errors="ignore", inplace=True)
    df = df[~df.ipcc_code.isna()]
    df.ipcc_code.replace(category_names_ipcc_can_map, inplace=True)

    df[GHG_COLUMNS] = df[GHG_COLUMNS].replace("x", np.nan).astype(float)
    df["F-GASES"] = df[["HFCs", "PFCs", "SF6", "NF3"]].sum(axis=1)
    df.drop(columns=["HFCs", "PFCs", "SF6", "NF3"], inplace=True)
    df["supra_jur"] = "Canada"

    return df[["supra_jur", "jurisdiction", "year", "ipcc_code"] + CONVERT_COLUMNS]


# --- Load and clean China inventory ---
def load_china_data(path):
    inv_jur_names = pd.read_excel(f"{path}/subnational/China/CEADS/CEADS_provincial_emissions/Emission_inventories_for_30_provinces_1997.xlsx", 
                                  sheet_name="Sum")
    provinces = list(inv_jur_names["Unnamed: 0"])[:-2]
    file_list = [f for f in os.listdir(f"{path}/subnational/China/CEADS/CEADS_provincial_emissions/") if f.endswith(".xlsx")]

    comb, proc = [], []
    for file in file_list:
        for prov in provinces:
            df = pd.read_excel(f"{path}/subnational/China/CEADS/CEADS_provincial_emissions/{file}", sheet_name=prov, skiprows=[1, 2])
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
def load_usa_data(path):
    data_dir = f"{path}/subnational/United_States/Rhodium/2024"
    file_list = glob.glob(os.path.join(data_dir, "*.csv"))

    df_list = []
    for file in file_list:
        temp = pd.read_csv(file, decimal=",")
        state_name = os.path.basename(file)[len("DetailedGHGinventory_"):-4].replace("_", " ").title()
        temp["jurisdiction"] = state_name
        temp.drop(columns=["Ranking", "Sector"], inplace=True)
        df_list.append(temp)

    df = pd.concat(df_list)
    sub_ind = pd.read_csv(f"{path}/subnational/United_States/Rhodium/2022/industry/TS2022_central_subind_ghg.csv")
    sub_ind = sub_ind[sub_ind.Gas == "CO2 (combustion)"]
    sub_ind.rename(columns={"StateName": "jurisdiction", "Industry": "Subsector"}, inplace=True)

    df = df[df.Subsector != "Industry - All combustion"]
    df = pd.concat([df, sub_ind])
    df["ipcc_code"] = df["Subsector"].replace(category_names_ipcc_usa_map)

    excl = ["Transport - Natural gas pipeline", "Carbon Dioxide Consumption", ...]  # Truncated for brevity
    df = df[~df.ipcc_code.isin(excl)]

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


# --- Generate totals excluding LULUCF ---
def generate_subnat_total(can, chn, usa):
    can_tot = can[can.ipcc_code == "0"].drop(columns="ipcc_code")
    can_lulucf = can[can.ipcc_code == "3B"].drop(columns=["ipcc_code", "supra_jur"])
    can_tot = can_tot.merge(can_lulucf, on=["jurisdiction", "year"], how="left", suffixes=("", "_lulucf"))

    for gas in CONVERT_COLUMNS:
        can_tot[gas] = can_tot[gas] - can_tot.pop(f"{gas}_lulucf")

    chn_tot = chn.groupby(["supra_jur", "jurisdiction", "year"])[CONVERT_COLUMNS].sum().reset_index()
    usa_tot = usa.groupby(["supra_jur", "jurisdiction", "year"])[CONVERT_COLUMNS].sum().reset_index()

    return pd.concat([can_tot, chn_tot, usa_tot], ignore_index=True)


# --- Combine subnational inventories with WCPD structure ---
def build_inventory_subnat(wcpd_df, subnat_names, mapping_ipcc_iea, gas, can, chn, usa):
    inventory = wcpd_df[wcpd_df.jurisdiction.isin(subnat_names)][["jurisdiction", "year", "ipcc_code", "iea_code"]].drop_duplicates()
    inventory.iea_code.fillna("NA", inplace=True)

    combined = pd.concat([
        can[["supra_jur", "jurisdiction", "year", "ipcc_code", gas]],
        chn[["supra_jur", "jurisdiction", "year", "ipcc_code", gas]],
        usa[["supra_jur", "jurisdiction", "year", "ipcc_code", gas]]
    ])

    combined = combined.merge(mapping_ipcc_iea, on="ipcc_code", how="left")
    combined.iea_code.fillna("NA", inplace=True)

    inventory["supra_jur"] = inventory.jurisdiction.map({
        **{j: "Canada" for j in subnat_can},
        **{j: "United States" for j in subnat_usa},
        **{j: "China" for j in subnat_chn},
        **{j: "Japan" for j in subnat_jpn},
    })

    return inventory.merge(combined, on=["supra_jur", "jurisdiction", "year", "ipcc_code", "iea_code"], how="left")[[
        "supra_jur", "jurisdiction", "year", "ipcc_code", "iea_code", gas
    ]]

test = 