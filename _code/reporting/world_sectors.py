import pandas as pd

def get_world_sectors(data_dir):
    coverage_df = pd.read_csv(f"{data_dir}/tot_coverage_world_sectors_CO2.csv")
    price_df = pd.read_csv(f"{data_dir}/ecp_world_sectors/world_sectoral_ecp_CO2.csv")
    price_covered_df = pd.read_excel(f"{data_dir}/ecp_world_sectors/world_sectoral_ecp_covered_CO2.xlsx")
    return coverage_df, price_df, price_covered_df
