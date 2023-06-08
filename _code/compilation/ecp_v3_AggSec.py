# script for calculating price series at the level of aggregate IPCC categories

import pandas as pd

#Adjustments to calculate prices at aggregate sector level:
# 1. create list of (aggregate) IPCC codes for which price series have to be created

sectAgg = ["1A1A", "1A3A", "1A3D", "1B1", "1B2A", "1B2B",
           "2A4", "2B", "2C", "2D", "2E", "2F", "2G", 
           "3B1", "3B2", "3B3", "3B5", 
           "4A", "4C", "4D",
           "5"]

# for each category in sectAgg:

    # a. extract/calculate emissions (using emissions inventories)
    # need to specify which inventory one is drawing from (national or subnational) and specify the corresponding path
    # recall that (i) the inventory is constructed from different sources and (ii) for non-combustion emissions, the "Product" disaggregation does not exist
    # figures for some (most) aggregate categories are not in the inventory per se and have to calculated

    inventory = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/source_data/ghg_inventory/processed/inventory_nat_"+gas+".csv")

    # b. use the matrix of parent/child relations between ipcc sectors to identify from 
    # which subcategories the aggregate price has to be calculated
    # create a dictionary where keys are each aggregate sector and values are a list of category codes

    # if inventory contains figure for that aggregate category, use it
    # if inventory does not contain figure for that aggregate category, then
    #       if data available for ALL IMMEDIATE subcategories:
    #           calculate aggregate emissions figure
    #       else:
    #           assign np.nan value

    # c. for each subcategory, calculate emissions as share of emissions of its parent category

    # d. calculate weighted average price
    # if emissions share data:
    #    calculate emissions-weighted average
    # if not:
    #    calculate simple average
