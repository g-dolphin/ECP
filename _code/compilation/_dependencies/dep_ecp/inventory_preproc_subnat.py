
# Ideally, need to write this so that one function can accommodate several subnational inventories.

import os
import glob
from re import sub
import pandas as pd
import numpy as np

# path to GHG data
path_ghg = "/Users/ejoiner/OneDrive - rff/ecp/ecp_dataset/source_data/ghg_inventory/raw"

# load (subnat) jurisdictions lists
stream = open("/Users/ejoiner/OneDrive - rff/Documents/RFF Organization/Research Documents/WCPD/WorldCarbonPricingDatabase/_code/_compilation/_dependencies/jurisdictions.py")
read_file = stream.read()
exec(read_file)

# load inventory sector names to IPCC 
stream = open("/Users/ejoiner/OneDrive - rff/Documents/RFF Organization/Research Documents/WCPD/ECP/_code/compilation/_dependencies/dep_ecp/ipcc_map_subnat.py")
read_file = stream.read()
exec(read_file)

# jur names mapping
stream = open("/Users/ejoiner/OneDrive - rff/Documents/RFF Organization/Research Documents/WCPD/ECP/_code/compilation/_dependencies/dep_ecp/jur_names_concordances.py")
read_file = stream.read()
exec(read_file)


# Common pre-processing
# CANADA

can = pd.read_csv(path_ghg+'/subnational/Canada/harmonized_data/ECCC/GHG_IPCC_Can_Prov_Terr_2021.csv',
            low_memory=False)

can.rename(columns={"Region":"jurisdiction", "Category":"ipcc_code"}, inplace=True)

can = can.loc[can.jurisdiction != "Canada", :]
can.drop(["Rollup", "CategoryID", "CH4", "N2O", "Unit"], axis=1, inplace=True)
can.rename(columns={"Region":"jurisdiction", "Year":"year",
                    "CH4 (CO2eq)":"CH4", "N2O (CO2eq)":"N2O", "CO2eq":"all_GHG"}, inplace=True)

can = can.loc[~can.ipcc_code.isna(), :] #keep all sectors in 'can' dataframe but assign IEA and IPCC codes so that they can be sorted
can["ipcc_code"].replace(to_replace=category_names_ipcc_can_map, inplace=True)

# eliminating 'x' entries in the columns
for col in ["CO2", "CH4", "N2O", "HFCs", "PFCs", "SF6", "NF3", "all_GHG"]:
    can[col].replace(to_replace={"x":None}, inplace=True)
    can[col] = can[col].astype(float)

can["F-GASES"] = can[["HFCs", "PFCs", "SF6", "NF3"]].sum(axis=1)
can.drop(["HFCs", "PFCs", "SF6", "NF3"], axis=1, inplace=True)

can["supra_jur"] = "Canada"

can = can[['supra_jur', 'jurisdiction', 'year', 'ipcc_code', 'CO2', 'CH4', 'N2O', 'F-GASES',
       'all_GHG']]



# CHINA

inv_jur_names_chn = pd.read_excel(path_ghg+"/subnational/China/CEADS/CEADS_provincial_emissions/Emission_inventories_for_30_provinces_1997.xlsx", 
                            sheet_name="Sum")
inv_jur_names_chn = list(inv_jur_names_chn["Unnamed: 0"])[:-2]

file_list = os.listdir(path_ghg+"/subnational/China/CEADS/CEADS_provincial_emissions/")

# file location does not have file type 

#file_list.remove('.DS_Store')

china_comb = pd.DataFrame() # df for combustion emissions
china_proc = pd.DataFrame() # df for process emissions

for file in file_list:
    for prov in inv_jur_names_chn:
        temp = pd.read_excel(path_ghg+"/subnational/China/CEADS/CEADS_provincial_emissions/"+file, 
                            sheet_name=prov, skiprows=[1,2])

        temp.rename(columns={"Unnamed: 0":"ipcc_code"}, inplace=True)
        temp["year"] = file[-9:-5]
        temp["jurisdiction"] = prov

        temp_comb = temp[["jurisdiction", "year", "ipcc_code", "Process", "Total"]].copy()
        temp_proc = temp[["jurisdiction", "year", "ipcc_code", "Process"]].copy()

        temp_comb.loc[:, "CO2"] = temp.loc[:, "Total"]-temp.loc[:, "Process"]
        temp_comb.drop(["Process", "Total"], axis=1, inplace=True)

        if china_comb.empty == True:
            china_comb = temp_comb
            china_proc = temp_proc
        else:
            china_comb = pd.concat([china_comb, temp_comb])
            china_proc = pd.concat([china_proc, temp_proc])


# From the CEADS data, we can actually recover the emissions associated with each broad fuel category (like for national jurisdictions)

# Replace province names by those in dataset
china_comb.replace(to_replace=subnat_names_map_chn, inplace=True)
china_comb.replace(to_replace=category_names_ipcc_chn_map, inplace=True)

china_proc.replace(to_replace=subnat_names_map_chn, inplace=True)
china_proc = china_proc.loc[china_proc.ipcc_code=='Nonmetal Mineral Products                                ', :]
china_proc.replace(to_replace={'Nonmetal Mineral Products                                ':"2A"}, inplace=True)
china_proc.rename(columns={"Process":"CO2"}, inplace=True)

# concatenate combustion and process emissions dataframes

china = pd.concat([china_comb, china_proc])
china = china.loc[china.ipcc_code!="Total Consumption"] # remove total category from dataframe

# sum at the (aggregate) sector level - since some sectors have been assigned the same IPCC code

chn = china.groupby(["jurisdiction", "year", "ipcc_code"]).sum()
chn = chn.reset_index()
chn["year"] = chn.year.astype(int)

# generating empty columns for greenhouse gases that are not in China's source data
for col in ["CH4", "N2O", "F-GASES", "all_GHG"]:
    chn[col] = np.nan

# convert from mmt to kt
for col in ['CO2', 'CH4', 'N2O', 'F-GASES', 'all_GHG']:
    chn[col] = chn[col]*1000

chn["supra_jur"] = "China"

chn = chn[['supra_jur', 'jurisdiction', 'year', 'ipcc_code', 'CO2', 'CH4', 'N2O', 'F-GASES',
       'all_GHG']]



# UNITED STATES

usa = pd.DataFrame()

os.chdir(path_ghg+'/subnational/United_States/Rhodium/2024')
file_list = glob.glob('*.csv')

for file in file_list:
    temp = pd.read_csv(path_ghg+'/subnational/United_States/Rhodium/2024/'+file, decimal=',')
    #extract US state name from file name
    state_name = file[len("DetailedGHGinventory_"):-4].replace("_", " ").title()
    #add state name as key column
    temp.loc[:, "jurisdiction"] = state_name
    #drop unused columns
    temp.drop(["Ranking", "Sector"], axis=1, inplace=True)
    #concat
    usa = pd.concat([usa, temp])

sub_ind = pd.read_csv(path_ghg+'/subnational/United_States/Rhodium/2022/industry/TS2022_central_subind_ghg.csv')
sub_ind.rename(columns={"StateName":"jurisdiction", "Industry":"Subsector"}, inplace=True)
sub_ind = sub_ind.loc[sub_ind.Gas=="CO2 (combustion)"] # keeping only the more detailed data for CO2 combustion

usa = usa.loc[usa.Subsector!='Industry - All combustion'] # excluding this category because we have disaggregated data for the sub-industries

# concatenate inventory categories

usa = pd.concat([usa, sub_ind])

#add ipcc_code
usa.loc[:, "ipcc_code"] = usa.loc[:, "Subsector"]
usa.loc[:, "ipcc_code"] = usa.loc[:, "ipcc_code"].replace(to_replace=category_names_ipcc_usa_map)

excl_sectors = ['Transport - Natural gas pipeline', 'Carbon Dioxide Consumption', 'Abandoned Oil and Gas Wells', 'Phosphoric Acid Production',
                'Natural Gas Systems', 'Petroleum Systems', 'Urea Consumption for Non-Agricultural Purposes', 
                "LULUCF CH4 Emissions", "LULUCF Carbon Stock Change", "LULUCF N2O Emissions"]
                # excluding LULUCF emissions because we want totals that exclude those

usa = usa.loc[~usa.ipcc_code.isin(excl_sectors), :]
usa.drop(["Subsector"], axis=1, inplace=True)

# combustion and non-combustion CO2 sectors are different IPCC categories so it's ok to replace the label
usa["Gas"].replace(to_replace={"CO2 (combustion)":"CO2", "CO2 (non-combustion)":"CO2"}, inplace=True)

# rename and limit to 2021
usa.rename(columns={"Year":"year"}, inplace=True)
usa = usa.loc[usa.year<=2021, :]

usa[["Total Emission(mmt CO2)"]] = usa[["Total Emission(mmt CO2)"]].astype(float)
usa.fillna(0, inplace=True) # needed to otherwise the sum across columns won't work

# aggregate to keep a single entry per jurisdiction/year/gas/ipcc_code - identical IPCC codes are assigned to multiple Rhodium sectors
usa = usa.groupby(["jurisdiction", "year", "Gas", "ipcc_code"]).sum()
usa.reset_index(inplace=True)

usa = usa.pivot(index=['jurisdiction', 'year', 'ipcc_code'], values = "Total Emission(mmt CO2)", columns="Gas")
usa.reset_index(inplace=True)

usa["F-GASES"] = usa[["HFCs", "PFCs", "NF3", "SF6"]].sum(axis=1)
usa["all_GHG"] = usa[["CO2", "CH4", "N2O", "F-GASES"]].sum(axis=1)

usa.drop(["NF3", "SF6", "PFCs", "HFCs"], axis=1, inplace=True)

# replace name of Georgia State to avoid clash with Georgia country
usa["jurisdiction"].replace(to_replace={"Georgia":"Georgia_US"}, inplace=True)

# convert from mmt to kt
for col in ['CO2', 'CH4', 'N2O', 'F-GASES', 'all_GHG']:
    usa[col] = usa[col]*1000

# add supra jurisdiction column
usa["supra_jur"] = "United States"

usa = usa[['supra_jur', 'jurisdiction', 'year', 'ipcc_code', 'CO2', 'CH4', 'N2O', 'F-GASES',
       'all_GHG']]



def subnat_total():

    #CANADA 
    can_tot = can.loc[can.ipcc_code=="0"]
    can_tot = can_tot.drop("ipcc_code", axis=1)

    can_lulucf = can.loc[can.ipcc_code.isin(["3B"]), :]
    can_lulucf = can_lulucf.drop(["ipcc_code", "supra_jur"], axis=1)

    #Calculating totals excluding LULUCF
    temp = can_tot.merge(can_lulucf, on=["jurisdiction", "year"], how="left")

    for gas in ["CO2", "CH4", "N2O", "F-GASES", "all_GHG"]:
        temp[gas+"_x"] = temp[gas+"_x"]-temp[gas+"_y"]
        temp.rename(columns={gas+"_x":gas}, inplace=True)
        temp.drop([gas+"_y"], axis=1, inplace=True)

    can_tot = temp

    # CHINA

    chn_tot = chn.groupby(["supra_jur", "jurisdiction", "year"]).sum()
    chn_tot = chn_tot.reset_index()

    # USA

    usa_tot = usa.groupby(["supra_jur", "jurisdiction", "year"]).sum()
    usa_tot = usa_tot.reset_index()

    # COMBINED

    subnat_total = pd.concat([can_tot, chn_tot, usa_tot])

    return subnat_total


def inventory_subnat(wcpd_df, subnat_names, mapping_ipcc_iea, gas, subnat_lists):

    # Inventory structure
    inventory_subnat = wcpd_df.loc[wcpd_df.jurisdiction.isin(subnat_names), ["jurisdiction", "year", "ipcc_code", "iea_code"]]

    # we don't have fuel level GHG data for subnational jurisdictions so we drop the Product column and delete duplicate/redundant rows 
    inventory_subnat.drop_duplicates(subset=["jurisdiction", "year", "ipcc_code", "iea_code"], inplace=True)
    inventory_subnat[["iea_code"]] = inventory_subnat[["iea_code"]].fillna("NA")


    # CANADA

    can_inv = can[["supra_jur", "jurisdiction", "year", "ipcc_code", gas]]

    # CHINA

    chn_inv = chn[["supra_jur", "jurisdiction", "year", "ipcc_code", gas]]

    # UNITED STATES

    usa_inv = usa[["supra_jur", "jurisdiction", "year", "ipcc_code", gas]]


    # -------------------------------Combined inventory df-----------------------------------
    # This part of the code needs adjustment as and when new GHG inventories are added to the 


    # COMBINED data
    combined_subnat = pd.concat([can_inv, chn_inv, usa_inv])
    combined_subnat = pd.merge(combined_subnat, mapping_ipcc_iea, on=["ipcc_code"], how="left")
    combined_subnat[["iea_code"]] = combined_subnat[["iea_code"]].fillna("NA")

    inventory_subnat.loc[inventory_subnat.jurisdiction.isin(subnat_lists["United States"]), "supra_jur"] = "United States"
    inventory_subnat.loc[inventory_subnat.jurisdiction.isin(subnat_lists["Canada"]), "supra_jur"] = "Canada"
    inventory_subnat.loc[inventory_subnat.jurisdiction.isin(subnat_lists["China"]), "supra_jur"] = "China"
    #inventory_subnat.loc[inventory_subnat.jurisdiction.isin(subnat_jpn), "supra_jur"] = "Japan"

    inventory_subnat = inventory_subnat.merge(combined_subnat, on=["supra_jur", "jurisdiction", "year", "ipcc_code", "iea_code"], how="left")
    inventory_subnat = inventory_subnat[['supra_jur', 'jurisdiction', 'year', 'ipcc_code', "iea_code", gas]]
    
    return inventory_subnat