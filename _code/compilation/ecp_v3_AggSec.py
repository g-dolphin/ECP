# script for calculating price series at the level of aggregate IPCC categories

import pandas as pd

#Adjustments to calculate prices at aggregate sector level:
#- create list of (aggregate) IPCC codes for which price series have to be created

sectAgg = ["1A1A", "1A3A", "1A3D", "1B1", "1B2A", "1B2B",
           "2A4", "2B", "2C", "2D", "2E", "2F", "2G", 
           "3B1", "3B2", "3B3", "3B5", 
           "4A", "4C", "4D",
           "5"]

#- extract/calculate emissions figures for those codes (using emissions inventories)
# need to specify which inventory one is drawing from (national or subnational) and specify the corresponding path
# recall that (i) the inventory is constructed from different sources and (ii) for non-combustion emissions, the "Product" disaggregation does not exist

inventory = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/source_data/ghg_inventory/processed/inventory_nat_"+gas+".csv")

#- calculate emissions of sub-categories as a share of aggregate category total
# figures for some (most) aggregate categories are not in the inventory per se and have to calculated

#- aggregate dataframe at aggregate category level