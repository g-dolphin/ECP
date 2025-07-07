## PACKAGES / LIBRARIES

import pandas as pd


indir = r"/Users/gd/GitHub/ECP/_raw/wcpd_usd/CO2/constantPrices/FixedXRate/"
pathECP = r"/Users/gd/Library/CloudStorage/OneDrive-rff/Documents/Research/projects/ecp/ecp_dataset/data/ecp/ecp_economy/ecp_vw/ecp_tv_CO2_May-02-2025.csv"
pathCoverage = r"/Users/gd/Library/CloudStorage/OneDrive-rff/Documents/Research/projects/ecp/ecp_dataset/data/coverage/jurisdictions/tot_coverage_jurisdiction_CO2_May-02-2025.csv"

prices_usd = concatenate(indir)
ecp = pd.read_csv(pathECP)
coverage = pd.read_csv(pathCoverage)

## ADDING ISOa3 CODES
coverage["ISO-a3"] = coverage["jurisdiction"]
coverage["ISO-a3"] = coverage["ISO-a3"].replace(to_replace=NametoISOa3NameMap)

prices_usd["ISO-a3"] = prices_usd["jurisdiction"]
prices_usd["ISO-a3"] = prices_usd["ISO-a3"].replace(to_replace=NametoISOa3NameMap)

## AD HOC ISOa3 CODES mapping

## JURISDICTION SELECTION

coverage = coverage.loc[coverage["ISO-a3"].isin(ctrySel+["World"])]

year = 2024

#-------------------END OF INPUTS---------------------------

#------------------------------------ Coverage ------------------------------------#

coverage = coverage.loc[(coverage.year==year)]

wldAvgCov = coverage.loc[coverage.jurisdiction=="World", 'cov_all_CO2_jurCO2'].item()

#------------------------------------ Average vs. Max carbon prices plot ------------------------------------#
# Find the highest recorded nominal price

prices_usd["tax_rate_incl_ex_usd_k"] = pd.to_numeric(prices_usd["tax_rate_incl_ex_usd_k"], errors='coerce')
prices_usd["ets_price_usd_k"] = pd.to_numeric(prices_usd["ets_price_usd_k"], errors='coerce')

prices_usd["max_price"] = prices_usd[['tax_rate_incl_ex_usd_k', 'ets_price_usd_k']].max(axis=1)

prices_usd_max = prices_usd[['jurisdiction', 'year', 'ipcc_code', 'Product', "max_price", "ISO-a3"]]
prices_usd_max = prices_usd_max.loc[(prices_usd_max["ISO-a3"].isin(ctrySel)) & (prices_usd_max.year==year)]

prices_usd_max = prices_usd_max.groupby(["jurisdiction", "year"]).max()

prices_usd_max.drop(["ipcc_code", "Product"], axis=1, inplace=True)
prices_usd_max.reset_index(inplace=True)

world_row = pd.DataFrame({"jurisdiction":"World", "year":2024, "max_price":prices_usd_max.max_price.max()}, index=[0])
prices_usd_max = pd.concat([prices_usd_max, world_row], ignore_index=True)

# filling 'max_price' column with 0

prices_usd_max["max_price"] = prices_usd_max["max_price"].fillna(0)

# Add ecp column

prices_usd_max = prices_usd_max.merge(ecp[["jurisdiction", "year", "ecp_all_jurCO2_usd_k"]], 
                  on=["jurisdiction", "year"], how="left")


prices_usd_max["pct_difference"] = 1-(prices_usd_max.ecp_all_jurCO2_usd_k/prices_usd_max.max_price)

wld_avg = ecp.loc[(ecp.jurisdiction=="World") & (ecp.year==2024), "ecp_all_jurCO2_usd_k"].item()

# SAVE INPUT & OUTPUT FILES
#prices_usd.to_csv(path_input+r"_usd.csv", index = False)
#ecp.to_csv(path_input+r"_ecp.csv", index = False)
#coverage.to_csv(path_input+r"_coverage.csv", index = False)

prices_usd_max.to_csv(r"/Users/gd/GitHub/ECP/_figures/dataFig/carbonPrices_usd_max_"+str(year)+".csv", index = False)
#prices_economy.to_csv(path_output+r"_economy.csv", index = False)
