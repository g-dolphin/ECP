

# UNITED STATES

us = pd.DataFrame()

os.chdir(path_ghg+'/subnational/United_States/Rhodium/')
file_list = glob.glob('*.csv')

for file in file_list:
    temp = pd.read_csv(path_ghg+'/subnational/United_States/Rhodium/'+file, decimal=',')
    #extract US state name from file name
    state_name = file[len("DetailedGHGinventory_"):-4]
    #add state name as key column
    temp.loc[:, "jurisdiction"] = state_name
    #concat
    us = pd.concat([us, temp])

# excluding LULUCF emissions - excluded from emissions total calculations to be consistent with chosen total
us = us.loc[~us.Subsector.str.match("LULUCF"), :]
us = us.drop(["Ranking"], axis=1)
us.loc[:, "jurisdiction"] = us.loc[:, "jurisdiction"].apply(lambda x: x.replace('_', ' ').title())

us_tot_ghg = us.groupby(["jurisdiction", "Year"]).sum()
us_tot_ghg = us_tot_ghg.reset_index()
us_tot_ghg.columns = ["jurisdiction", "Year", "Total_GHG_Emissions_Excluding_LUCF_MtCO2e"]

us = us.loc[us.Gas.isin(['CO2 (combustion)', 'CO2 (non-combustion)'])]
us_tot_co2 = us.groupby(["jurisdiction", "Year"]).sum()
us_tot_co2 = us_tot_co2.reset_index()
us_tot_co2.columns = ["jurisdiction", "Year", "Total_CO2_Emissions_Excluding_LUCF_MtCO2e"]

us_tot = us_tot_ghg.merge(us_tot_co2, on=["jurisdiction", "Year"])
us_tot.rename(columns={"Year":"year"}, inplace=True)

#add ipcc_code

sector_names_map_us = {'Wastewater Treatment':'4D',
       'Rice Cultivation':'3C7', 'Manure Management':'3A2', 'Landfills':'4A',
       'Incineration of Waste':'4C1', 'Field Burning of Agricultural Residues':'3C1',
       'Enteric Fermentation':'3A1', 'Composting':'4B', 'Ferroalloy Production':'2C2',
#       'Iron and Steel Production & Metallurgical Coke Production':'1A2A', TEMPORARY FIX
       'Petrochemical Production':'2B8',
       'Stationary Combustion':'1A5A', 'Mobile Combustion':'1A5B',
       'Carbide Production and Consumption':'2B5',
       'Abandoned Underground Coal Mines':'1B1A13', 'Industry - All combustion':'1A2A',# CODE ATTRIBUTION IS TEMPORARY FIX
       'Transport - Other':'1A3E', 
       'Transport - LDVs':'1A3B', 'Transport - Freight (trucks)':'1A3B',
       'Transport - Air':'1A3A', 'Transport - Rail':'1A3C', 'Commercial':'1A4A',
       'Power - All Fuels':'1A1A1', 'Residential':'1A4B', 'Liming':'3C2', 'Urea Fertilization':'3C3',
       'Aluminum Production':'2C3', 'Ammonia Production':'2B1',
       'Glass Production':'2A3',
       'Lead Production':'2C5', 'Lime Production':'2A2',
       'Magnesium Production and Processing':'2C4', 'Non-Energy Use of Fuels':'2D',
       'Other Process Uses of Carbonates':'2A4',
       'Soda Ash Production':'2B7', 'Titanium Dioxide Production':'2B6',
       'Zinc Production':'2C6', 'Cement Production':'2A1', 
       'Substitution of Ozone Depleting Substances':'2F', 
       'Electronics Industry':'2E', 
       'Adipic Acid Production':'2B3', 'N2O from Product Uses':'2G3',
       'Nitric Acid Production':'2B2', 'Agricultural Soil Management':'3C4',
       'Coal Mining':'1B1A', 'Caprolactam, Glyoxal, and Glyoxylic Acid Production':'2B4'}

#'Abandoned Oil and Gas Wells', 'MVAC', 'Petroleum Systems', 'Electrical Transmission and Distribution',
# 'LULUCF Carbon Stock Change', 'LULUCF N2O Emissions', 'LULUCF CH4 Emissions', 'Natural Gas Systems',
#'Urea Consumption for Non-Agricultural Purposes':'', 'HCFC-22 Production', 'Phosphoric Acid Production',
# 'Transport - Natural gas pipeline', 'Carbon Dioxide Consumption',

us.loc[:, "ipcc_code"] = us.loc[:, "Subsector"]
us.loc[:, "ipcc_code"] = us.loc[:, "ipcc_code"].replace(to_replace=sector_names_map_us)

excl_sectors = ['Transport - Natural gas pipeline', 'Carbon Dioxide Consumption', 'Abandoned Oil and Gas Wells', 'Phosphoric Acid Production',
                'Natural Gas Systems', 'Petroleum Systems', 'Urea Consumption for Non-Agricultural Purposes']

us = us.loc[~us.ipcc_code.isin(excl_sectors), :]

us = us.drop(["Gas", "Subsector", "Sector"], axis=1)
us = us.rename(columns={"Emission (mmt CO2e)":"CO2_emissions", "Year":"year"})
us = us[["jurisdiction", "year", "ipcc_code", "CO2_emissions"]]

us = us.loc[us.year<=2020, :]
us = us.sort_values(by=["jurisdiction", "year", "ipcc_code"])

#needed to aggregate over IPCC sectors as I have attributed same ipcc_code to multiple Rhodium categories
us = us.groupby(by=["jurisdiction", "year", "ipcc_code"]).sum()
us = us.reset_index()

us["supra_jur"] = "United States"

# replace name of Georgia state to avoid clash with Georgia country
us["jurisdiction"].replace(to_replace={"Georgia":"Georgia_US"}, inplace=True)


# CANADA

can = pd.read_csv(path_ghg+'/subnational/Canada/harmonized_data/ECCC/GHG_IPCC_Can_Prov_Terr.csv',
                  low_memory=False)
can_map = pd.read_csv(path_ghg+'/subnational/Canada/harmonized_data/ECCC/ipcc_code_name_map.csv')

map_ipcc_can = dict(zip(list(can_map['category'].values), list(can_map['IPCC_CODE'].values)))

can = can.loc[can.Region != "Canada", :]
can = can[["Region", "Year", "Category", "CO2", "CO2eq"]]
can.rename(columns={"Region":"jurisdiction", "Category":"ipcc_code", "CO2eq":"tot_ghg"}, inplace=True)

for col in ["CO2", "tot_ghg"]:
    can[col].replace(to_replace={"x":None}, inplace=True)
    can[col] = can[col].astype(float)
    can[col] = can[col].divide(1000, fill_value=None)

can_tot = can.loc[can.ipcc_code.isin(["TOTAL"]), ["jurisdiction", "Year", "CO2", "tot_ghg"]]
can_lulucf = can.loc[can.ipcc_code.isin(["LAND USE, LAND-USE CHANGE AND FORESTRY"]), ["jurisdiction", "Year", "CO2", "tot_ghg"]]
can_tot = can_tot.merge(can_lulucf, on=["jurisdiction", "Year"])

#Calculating totals excluding LULUCF
can_tot["CO2_x"] = can_tot.CO2_x - can_tot.CO2_y
can_tot["tot_ghg_x"] = can_tot.tot_ghg_x - can_tot.tot_ghg_y
can_tot.drop(["CO2_y", "tot_ghg_y"], axis=1, inplace=True)
can_tot.rename(columns={"CO2_x":"Total_GHG_Emissions_Excluding_LUCF_MtCO2e", "tot_ghg_x":"Total_CO2_Emissions_Excluding_LUCF_MtCO2e"}, inplace=True)
can_tot.rename(columns={"Year":"year"}, inplace=True)

can["ipcc_code"].replace(to_replace=map_ipcc_can, inplace=True)
can = can[["jurisdiction", "Year", "ipcc_code", "CO2"]]
can.columns = ["jurisdiction", "year", "ipcc_code", "CO2_emissions"]
can = can.loc[~can.ipcc_code.isna(), :] #keep all sectors in 'can' dataframe but assign IEA and IPCC codes so that they can be sorted

can["supra_jur"] = "Canada"


# CHINA

chn_prov_names = pd.read_excel(path_ghg+"/subnational/China/CEADS/CEADS_provincial_emissions/Emission_inventories_for_30_provinces_1997.xlsx", 
                           sheet_name="Sum")
chn_prov_names = list(chn_prov_names["Unnamed: 0"])[:-2]

file_list = os.listdir(path_ghg+"/subnational/China/CEADS/CEADS_provincial_emissions/")
#file_list.remove('.DS_Store')

china_comb = pd.DataFrame()
china_proc = pd.DataFrame()

for file in file_list:
    for prov in chn_prov_names:
        temp = pd.read_excel(path_ghg+"/subnational/China/CEADS/CEADS_provincial_emissions/"+file, 
                           sheet_name=prov, skiprows=[1,2])

        temp.rename(columns={"Unnamed: 0":"ipcc_code"}, inplace=True)
        temp["year"] = file[-9:-5]
        temp["jurisdiction"] = prov
        
        temp_comb = temp[["jurisdiction", "year", "ipcc_code", "Process", "Total"]].copy()
        temp_proc = temp[["jurisdiction", "year", "ipcc_code", "Process"]].copy()
        
        temp_comb.loc[:, "CO2_emissions"] = temp.loc[:, "Total"]-temp.loc[:, "Process"]
        temp_comb.drop(["Process", "Total"], axis=1, inplace=True)
        
        if china_comb.empty == True:
            china_comb = temp_comb
            china_proc = temp_proc
        else:
            china_comb = pd.concat([china_comb, temp_comb])
            china_proc = pd.concat([china_proc, temp_proc])


            # From the CEADS data, we can acutally recover the emissions associated with each broad fuel category (like for national jurisdictions)

# Replace province names by those in dataset
province_names_map = {'Beijing': 'Beijing Municipality', 'Tianjin': 'Tianjin Municipality', 'Hebei':'Hebei Province', 
                      'Shanxi':'Shanxi Province', 'InnerMongolia':'Inner Mongolia Autonomous Region',
                      'Liaoning':'Liaoning Province', 'Jilin':'Jilin Province', 'Heilongjiang':'Heilongjiang Province', 
                      'Shanghai':'Shanghai Municipality', 'Jiangsu':'Jiangsu Province',
                      'Zhejiang':'Zhejiang Province', 'Anhui':'Anhui Province', 'Fujian':'Fujian Province', 'Jiangxi':'Jiangxi Province', 
                      'Shandong':'Shandong Province', 'Henan':'Henan Province', 'Hubei':'Hubei Province', 'Hunan':'Hunan Province', 
                      'Guangdong':'Guangdong Province', 'Guangxi':"Guangxi Zhuang Autonomous Region", 'Hainan':'Hainan Province', 'Chongqing':'Chongqing Municipality',
                      'Sichuan':'Sichuan Province', 'Guizhou':'Guizhou Province', 'Yunnan':'Yunnan Province', 'Shaanxi':'Shaanxi Province', 
                      'Gansu':'Gansu Province', 'Qinghai':'Qinghai Province', 'Ningxia':'Ningxia Hui Autonomous Region', 
                      'Xinjiang':'Xinjiang Uyghur Autonomous Region'}

# Associate IPCC sector names with sector codes
sector_names_map_china = {'Farming, Forestry, Animal Husbandry, Fishery and Water Conservancy      ':'1A4C',
                          'Coal Mining and Dressing                                 ':'1A1C',
                          'Petroleum and Natural Gas Extraction                     ':'1B2',
                          'Ferrous Metals Mining and Dressing                       ':'1A2I',
                          'Nonferrous Metals Mining and Dressing                    ':'1A2I',
                          'Nonmetal Minerals Mining and Dressing                    ':'1A2I',
                          'Other Minerals Mining and Dressing                       ':'1A2I',
                          'Logging and Transport of Wood and Bamboo                 ':'1A2J',
                          'Food Processing                                          ':'1A2E',
                          'Food Production                                          ':'1A2E',
                          'Beverage Production':'1A2E',
                          'Tobacco Processing                                       ':'1A2E',
                          'Textile Industry                                         ':'1A2L',
                          'Garments and Other Fiber Products                        ':'1A2L',
                          'Leather, Furs, Down and Related Products                 ':'1A2L',
                          'Timber Processing, Bamboo, Cane, Palm Fiber & Straw Products':'1A2J',
                          'Furniture Manufacturing                                  ':'1A2J',
                          'Papermaking and Paper Products                           ':'1A2D',
                          'Printing and Record Medium Reproduction                  ':'1A2D',
                          'Cultural, Educational and Sports Articles                ':'1A2D',
                          'Petroleum Processing and Coking                          ':'1A1B',
                          'Raw Chemical Materials and Chemical Products             ':'1A2C',
                          'Medical and Pharmaceutical Products                      ':'1A2C',
                          'Chemical Fiber                                           ':'1A2C',
                          'Rubber Products                                          ':'1A2C',
                          'Plastic Products                                         ':'1A2C',
                          'Nonmetal Mineral Products                                ':'1A2F',
                          'Smelting and Pressing of Ferrous Metals                  ':'1A2A',
                          'Smelting and Pressing of Nonferrous Metals               ':'1A2B',
                          'Metal Products                                           ':'1A2A',
                          'Ordinary Machinery                                       ':'1A2H',
                          'Equipment for Special Purposes                           ':'1A2H',
                          'Transportation Equipment                                 ':'1A2G',
                          'Electric Equipment and Machinery                         ':'1A2H',
                          'Electronic and Telecommunications Equipment              ':'1A2H',
                          'Instruments, Meters, Cultural and Office Machinery         ':'1A2H',
                          'Other Manufacturing Industry                             ':'1A2M',
                          'Scrap and waste':'1A2M',
                          'Production and Supply of Electric Power, Steam and Hot Water   ':'1A1A',
                          'Production and Supply of Gas                             ':'1B2B',
                          'Production and Supply of Tap Water                       ':'1A4A', # to be verified
                          'Construction                                             ':'1A2K',
                          'Transportation, Storage, Post and Telecommunication Services    ':'1A3',
                          'Wholesale, Retail Trade and Catering Services            ':'1A4A',
                          'Others                                                   ':'1A5',
                          'Urban':'1A4B', 
                          'Rural':'1A4B'}

china_comb.replace(to_replace=province_names_map, inplace=True)
china_comb.replace(to_replace=sector_names_map_china, inplace=True)

china_proc.replace(to_replace=province_names_map, inplace=True)
china_proc = china_proc.loc[china_proc.ipcc_code=='Nonmetal Mineral Products                                ', :]
china_proc.replace(to_replace={'Nonmetal Mineral Products                                ':"2A"}, inplace=True)
china_proc.rename(columns={"Process":"CO2_emissions"}, inplace=True)

# concatenate combustion and process emissions dataframes

china = pd.concat([china_comb, china_proc])
china = china.loc[china.ipcc_code!="Total Consumption"] # remove total category from dataframe

# sum at the (aggregate) sector level - since some sectors have been assigned the same IPCC code

china = china.groupby(["jurisdiction", "year", "ipcc_code"]).sum()
china = china.reset_index()
china["year"] = china.year.astype(int)

china["supra_jur"] = "China"

# retrieve total province emissions

china_tot = china.groupby(["jurisdiction", "year"]).sum()
china_tot = china_tot.reset_index()

china_tot["Total_GHG_Emissions_Excluding_LUCF_MtCO2e"] = np.nan
china_tot.rename(columns={"CO2_emissions":"Total_CO2_Emissions_Excluding_LUCF_MtCO2e"}, inplace=True)


# -------------------------------

# Inventory structure
inventory_subnat = wcpd_all.loc[wcpd_all.jurisdiction.isin(subnat_names), ["jurisdiction", "year", "ipcc_code", "iea_code"]]

us_states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Dc', 'Delaware', 'Florida', 'Georgia_US',
            'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts',
            'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico',
            'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
            'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']

can_prov = ['Alberta', 'British Columbia', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Northwest Territories',
            'Northwest Territories and Nunavut', 'Nova Scotia', 'Nunavut', 'Ontario', 'Prince Edward Island', 'Quebec', 'Saskatchewan', 'Yukon']

chn_prov = ['Anhui Province', 'Beijing Municipality', 'Chongqing Municipality', 'Fujian Province', 'Gansu Province', 'Guangdong Province',
            'Guangxi Zhuang Autonomous Region', 'Guizhou Province', 'Hainan Province', 'Hebei Province', 'Heilongjiang Province', 'Henan Province',
            'Hubei Province', 'Hunan Province', 'Inner Mongolia Autonomous Region', 'Jiangsu Province', 'Jiangxi Province', 'Jilin Province',
            'Liaoning Province', 'Ningxia Hui Autonomous Region', 'Qinghai Province', 'Shaanxi Province', 'Shandong Province', 'Shanghai Municipality',
            'Shanxi Province', 'Sichuan Province', 'Tianjin Municipality', 'Xinjiang Uyghur Autonomous Region', 'Yunnan Province', 'Zhejiang Province',
            "Hong Kong Special Administrative Region", "Tibet Autonomous Region", "Macau Special Administrative Region"]

jpn_pref = ["Tokyo", "Saitama", "Kyoto"]

# we don't have fuel level information for subnational jurisdictions so we drop the Product column and delete duplicate/redundant rows 
inventory_subnat.drop_duplicates(subset=["jurisdiction", "year", "ipcc_code", "iea_code"], inplace=True)
inventory_subnat[["iea_code"]] = inventory_subnat[["iea_code"]].fillna("NA")


# COMBINED data
combined_subnat = pd.concat([us, can, china])
combined_subnat = combined_subnat.merge(ipcc_iea_map, on=["ipcc_code"], how="left")
combined_subnat[["iea_code"]] = combined_subnat[["iea_code"]].fillna("NA")

inventory_subnat.loc[inventory_subnat.jurisdiction.isin(us_states), "supra_jur"] = "United States"
inventory_subnat.loc[inventory_subnat.jurisdiction.isin(can_prov), "supra_jur"] = "Canada"
inventory_subnat.loc[inventory_subnat.jurisdiction.isin(chn_prov), "supra_jur"] = "China"
inventory_subnat.loc[inventory_subnat.jurisdiction.isin(jpn_pref), "supra_jur"] = "Japan"

inventory_subnat = inventory_subnat.merge(combined_subnat, on=["supra_jur", "jurisdiction", "year", "ipcc_code", "iea_code"], how="left")
inventory_subnat = inventory_subnat[['supra_jur', 'jurisdiction', 'year', 'ipcc_code', "iea_code", 'CO2_emissions']]