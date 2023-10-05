# Mapping of subnational inventory sector names with IPCC category codes

# Canada

can_map = pd.read_csv('/Users/gd/OneDrive - rff/Documents/Research/projects/ecp/ecp_dataset/source_data/ghg_inventory/raw/subnational/Canada/harmonized_data/ECCC/ipcc_code_name_map.csv')

sector_names_ipcc_map_can = dict(zip(list(can_map['category'].values), list(can_map['IPCC_CODE'].values)))



# China

sector_names_ipcc_map_chn = {'Farming, Forestry, Animal Husbandry, Fishery and Water Conservancy      ':'1A4C',
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



# United States

sector_names_ipcc_map_usa = {'Wastewater Treatment':'4D',
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



