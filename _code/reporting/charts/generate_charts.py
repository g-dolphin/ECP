import os
import sys
import json
import pandas as pd

sys.path.append("/Users/gd/GitHub/ECP/_code/reporting/charts")
from proc_carbonPrices import prepare_carbon_price_data
from plots_carbonPrices import plot_minMax
from plots_coverage import coverage_plots
from plots_world_sectors import plot_world_sectors
from plots_ets_tax_jur import plot_selected_jurisdictions
from plots_subnat_stacked import plot_filtered_stacked_bar
from plots_national_stacked import plot_stacked_national_bar

os.makedirs('/Users/gd/GitHub/ECP/_output/_figures/plots', exist_ok=True)

# Path to JSON config
json_path = os.path.join("/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/_dependencies/", "jurisdictions.json")

with open(json_path, 'r', encoding='utf-8') as f:
    jurisdictions = json.load(f)

canadian_provinces = jurisdictions["subnationals"]["Canada"]
us_states = jurisdictions["subnationals"]["United States"]
china_provinces = jurisdictions["subnationals"]["China"]


print("Loading carbon price data...")
carbon_df, prices_usd_max = prepare_carbon_price_data(r"/Users/gd/GitHub/ECP/_raw/wcpd_usd/CO2/constantPrices/FixedXRate/", 2024)

print("Plotting carbon price charts...")
plot_minMax(prices_usd_max, "/Users/gd/GitHub/ECP/_output/_figures/dataFig")

plot_world_sectors("/Users/gd/GitHub/ECP/_output/_dataset")

jurisdictions = ["Canada", "China", "California", "France", "Germany", "Japan", "Korea", "United Kingdom", "United States"]
plot_selected_jurisdictions("/Users/gd/GitHub/ECP/_output/_dataset", jurisdictions)

print("Plotting coverage charts...")
coverage_plots(carbon_df, '/Users/gd/GitHub/ECP/_output/_figures')


# Apply updated plotting function
# Filter data for each country’s subnational jurisdictions

df = pd.read_csv("/Users/gd/GitHub/ECP/_output/_dataset/ecp/ipcc/ecp_economy/ecp_CO2.csv")
df_national = pd.read_csv("/Users/gd/Desktop/national_stack_test.csv")

df_canada = df[df['jurisdiction'].isin(canadian_provinces)]
df_us = df[df['jurisdiction'].isin(us_states)]
df_china = df[df['jurisdiction'].isin(china_provinces)]

plot_filtered_stacked_bar(df_us, "United States")
plot_filtered_stacked_bar(df_canada, "Canada")
plot_filtered_stacked_bar(df_china, "China")

plot_stacked_national_bar(df_national)

print("✅ All charts created in _output/_figures")
