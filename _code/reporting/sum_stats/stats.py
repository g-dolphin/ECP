
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CO₂ regional price calculation
"""

import pandas as pd
from pathlib import Path

# === Config ===

# Root directory (use Path for portability)
ROOT_DIR = Path.home() / "GitHub" / "ECP" / "_output"
DATA_DIR = Path.home() / "Library/CloudStorage/OneDrive-rff/Documents/Research/projects/ecp/ecp_dataset"
OUTPUT_FILE = ROOT_DIR / "_dataset/ecp/ipcc/ecp_economy/ecp_CO2_regional.csv"

# === Load data ===

df_prices_econ = pd.read_csv(
    ROOT_DIR / "_dataset/ecp/ipcc/ecp_economy/ecp_CO2.csv"
)
tot_emissions = pd.read_csv(
    DATA_DIR / "source_data/ghg_inventory/processed/ghg_national_total.csv"
)

# === Country groups ===

oecd = [
    "United States", "Mexico", "Japan", "Germany", "Turkey", "France",
    "United Kingdom", "Italy", "Korea, Rep.", "Spain", "Poland", "Canada",
    "Australia", "Chile", "Netherlands", "Belgium", "Greece", "Czech Republic",
    "Portugal", "Sweden", "Hungary", "Austria", "Israel", "Switzerland",
    "Denmark", "Finland", "Slovak Republic", "Norway", "Ireland", "New Zealand",
    "Lithuania", "Slovenia", "Latvia", "Estonia", "Luxembourg", "Iceland"
]

eu27 = [
    "Austria", "Belgium", "Bulgaria", "Cyprus", "Czech Republic", "Germany",
    "Denmark", "Estonia", "Greece", "Spain", "Finland", "France", "Croatia",
    "Hungary", "Ireland", "Italy", "Lithuania", "Luxembourg", "Latvia", "Malta",
    "Netherlands", "Poland", "Portugal", "Romania", "Sweden", "Slovenia", "Slovakia"
]

imf_apac = [
    "Afghanistan", "Australia", "Bangladesh", "Bhutan", "Brunei Darussalam",
    "Cambodia", "China", "Fiji", "India", "Indonesia", "Japan", "Kazakhstan",
    "Kiribati", "Korea, Republic of", "Kyrgyz Republic", "Lao People's Democratic Republic",
    "Malaysia", "Maldives", "Marshall Islands", "Micronesia, Federated States of",
    "Mongolia", "Myanmar", "Nauru", "Nepal", "New Zealand", "Pakistan", "Palau",
    "Papua New Guinea", "Philippines", "Samoa", "Singapore", "Solomon Islands",
    "Sri Lanka", "Tajikistan", "Thailand", "Timor-Leste", "Tonga", "Turkmenistan",
    "Tuvalu", "Uzbekistan", "Vanuatu", "Vietnam"
]

middle_income = [
        "Angola", "Honduras", "Philippines", "Algeria", "India", "Samoa",
    "Bangladesh", "Indonesia", "São Tomé and Principe",
    "Belize", "Iran, Islamic Rep.", "Senegal", "Benin", "Kenya", 	
    "Solomon Islands", "Bhutan", "Kiribati", "Sri Lanka", "Bolivia", 
    "Kyrgyz Republic", "Tanzania", "Cabo Verde", "Lao PDR", "Tajikistan",
    "Cambodia", "Lesotho", "Timor-Leste", "Cameroon", 	"Mauritania",
    "Tunisia", "Comoros", 	"Micronesia, Fed. Sts.", "Ukraine",
    "Congo, Rep.", "Mongolia", "Uzbekistan", "Cote d'Ivoire", 	"Morocco",
    "Vanuatu", "Djibouti", "Myanmar", 	"Vietnam", "Egypt, Arab Rep.",
    "Nepal", "West Bank and Gaza", "El Salvador", 	"Nicaragua", 
    "Zambia", "Eswatini",	"Nigeria", "Zimbabwe", "Ghana",	
    "Pakistan", "Haiti", "Papua New Guinea",
    "Albania", "Gabon", "Namibia", "American Samoa", "Georgia", "North Macedonia",
    "Argentina", "Grenada", "Panama", "Armenia", "Guatemala",
    "Paraguay", "Azerbaijan", "Guyana", "Peru", "Belarus", "Iraq",
    "Romania", "Bosnia and Herzegovina","﻿Jamaica", "Russian Federation",
    "Botswana", "Jordan",	"Serbia", "Brazil",	"Kazakhstan", "South Africa",
    "Bulgaria", "Kosovo", "St. Lucia", "China", "Lebanon", 
    "St. Vincent and the Grenadines", "Colombia",	"Libya", "Suriname",
    "Costa Rica",  "Malaysia", "Thailand", "Cuba", "Maldives", "Tonga",
    "Dominica", "Marshall Islands", "Turkey", "Dominican Republic",   
    "Mauritius", "Turkmenistan", "Equatorial Guinea", "Mexico", "Tuvalu",
    "Ecuador",	"Moldova", "Fiji", "Montenegro"
]

country_groups = {
    "OECD": oecd,
    "EU27": eu27,
    "AsiaPacific": imf_apac,
    "MiddleIncome": middle_income,
}

# === Simple averages ===

avg_by_group = {
    name: df_prices_econ.loc[
        (df_prices_econ.jurisdiction.isin(group)) & (df_prices_econ.year == 2024),
        "ecp_all_jurCO2_usd_k"
    ].mean()
    for name, group in country_groups.items()
}

print("Simple averages (2024):")
for name, value in avg_by_group.items():
    print(f"  {name}: {value:.2f}")

# === Emissions-weighted averages ===

weighted_averages = []

for name, group in country_groups.items():
    df_group = tot_emissions[tot_emissions.jurisdiction.isin(group)]
    emissions_total = df_group.groupby("year")[["CO2", "all_GHG"]].sum().reset_index()
    df_group = df_group.merge(emissions_total, on="year", suffixes=("", "_total"))

    df_group[f"share_CO2"] = df_group["CO2"] / df_group["CO2_total"]

    merged = df_prices_econ[df_prices_econ.jurisdiction.isin(group)].merge(
        df_group[["jurisdiction", "year", f"share_CO2"]],
        on=["jurisdiction", "year"],
        how="left"
    ).sort_values(["jurisdiction", "year"]).fillna(method="ffill")

    merged["CO2_price"] = merged["ecp_all_jurCO2_usd_k"] * merged["share_CO2"]
    average = merged.groupby("year")["CO2_price"].sum().reset_index()
    average["region"] = name

    weighted_averages.append(average)

result = pd.concat(weighted_averages, ignore_index=True)
result.to_csv(OUTPUT_FILE, index=False)

print(f"Emissions-weighted averages saved to: {OUTPUT_FILE}")


# Share of emissions covered by mechanisms implemented by year [yyyy]

