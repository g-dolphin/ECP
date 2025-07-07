import os
import sys

sys.path.append("/Users/gd/GitHub/ECP/_code/reporting/charts")
from proc_carbonPrices import prepare_carbon_price_data
from plots_carbonPrices import plot_minMax
from plots_coverage import coverage_plots
from plots_world_sectors import plot_world_sectors

os.makedirs('/Users/gd/GitHub/ECP/_output/_figures/plots', exist_ok=True)

print("Loading carbon price data...")
carbon_df, prices_usd_max = prepare_carbon_price_data(r"/Users/gd/GitHub/ECP/_raw/wcpd_usd/CO2/constantPrices/FixedXRate/", 2024)

print("Plotting carbon price charts...")
plot_minMax(prices_usd_max, "/Users/gd/GitHub/ECP/_output/_figures/dataFig")

plot_world_sectors("/Users/gd/GitHub/ECP/_output/_dataset")

#print("Plotting coverage charts...")
#coverage_plots(carbon_df, '/Users/gd/GitHub/ECP/_output/_figures')


print("✅ All charts created in _output/_figures")
