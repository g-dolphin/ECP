import pandas as pd
import numpy as np

colList = {"ets_price_usd_k":"ecp_ets_supraSec_CO2_usd_k",	
           "tax_rate_incl_ex_usd_k":"ecp_tax_supraSec_CO2_usd_k",
           "all_inst_usd_k":"ecp_all_supraSec_CO2_usd_k"}


# function description: adds sector-level prices from subnational pricing mechanisms to national sector-level prices
# NB: current isssue: emissions inventories for subnational jurisdictions are missing data for some IPCC categories for which prices are in force

def secNat_from_secSubnat(prices, dfSecPriceNat, gas):

   inventories_subnat_ctrySect = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/source_data/ghg_inventory/processed/subnational/"+gas+"/sector_level/inventory_"+gas+".csv")

   # 1. get subnational sector-level ecp (wcpd_usd.csv)
   # ==> done; in dataframe `cfWprices_usd`
   # 2. multiply these prices by shares calculated in ecp_v3.ipynb; dataframe `inventories_subnat_ctrySect[gas]`
   for nat_jur in ["Canada"]:#subnat_lists.keys():
      print(nat_jur)
      temp = prices.loc[prices.jurisdiction.isin(subnat_lists[nat_jur])]
      temp_subnat = temp.merge(inventories_subnat_ctrySect, how='left',
                              on=["jurisdiction", "year", "ipcc_code", "iea_code"])
      
      for price in ["ets_price_usd_k", "tax_rate_incl_ex_usd_k", "all_inst_usd_k"]:
          temp_subnat[colList[price]] = temp_subnat[price]*temp_subnat.CO2_ctry_sect_ctryCO2
          temp_subnat.drop(price, axis=1, inplace=True)
            
      temp_subnat = temp_subnat.groupby(["year", "ipcc_code"]).sum()
      temp_subnat.reset_index(inplace=True)
      temp_subnat["jurisdiction"] = nat_jur+"sub" #

      temp_subnat.rename(columns={"ecp_ets_supraSec_CO2_usd_k":"ecp_ets_usd_k", 
                                  "ecp_tax_supraSec_CO2_usd_k":"ecp_tax_usd_k", 
                                  "ecp_all_supraSec_CO2_usd_k":"ecp_all_usd_k"}, inplace=True)

      #   3. add resulting product to national sector-level values
      #   National-sector-level ecp from subnational schemes      

      temp_nat = dfSecPriceNat.loc[dfSecPriceNat.jurisdiction == nat_jur, :]

      temp_nat_subnat = pd.concat([temp_nat, temp_subnat])
      temp_nat_subnat = temp_nat_subnat.groupby(["year", "ipcc_code"]).sum() # summing country-level ecp from country-level and subnational mechanisms
      temp_nat_subnat.reset_index(inplace=True)

      temp_nat_subnat["jurisdiction"] = nat_jur

      # replacing rows jurisdiction==nat_jur with updated ones
      dfSecPriceNat = dfSecPriceNat.loc[dfSecPriceNat.jurisdiction != nat_jur, :]
      dfSecPriceNat = pd.concat([dfSecPriceNat, temp_nat_subnat])

      return dfSecPriceNat