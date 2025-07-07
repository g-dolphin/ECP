import os
import sys

sys.path.append("/Users/gd/GitHub/ECP/_code/reporting")
from proc_carbonPrices import prepare_carbon_price_data
from plots_carbonPrices import plot_carbon_prices
from plots import plot_coverage
from world_sectors import get_world_sectors

os.makedirs('/Users/gd/GitHub/ECP/_output/_figures', exist_ok=True)

print("Loading carbon price data...")
carbon_df = prepare_carbon_price_data(r"/Users/gd/GitHub/ECP/_raw/wcpd_usd/CO2/constantPrices/FixedXRate/")

print("Plotting carbon price charts...")
plot_carbon_prices(carbon_df, '/Users/gd/GitHub/ECP/_output/_figures')

print("Plotting coverage charts...")
plot_coverage(carbon_df, '/Users/gd/GitHub/ECP/_output/_figures')

print("Loading world sectors data...")
coverage_df, price_df, price_covered_df = get_world_sectors('../_dataset/ecp/ipcc')

print("✅ All charts created in _output/charts")
