
import pandas as pd

ecp_general = SourceFileLoader('general', path_dependencies+'/ecp_v3_gen_func.py').load_module()

ecp_general.concat_iea() # Concatenate IEA yearly emissions files

# CO2
## COMBUSTION (1A)

result = {}

with open(path_ghg+'/national/IEA/iea_energy_combustion_emissions/detailed_figures/emissions_allyears/iea_CO2em_ally.csv', 'r',
         encoding = 'latin-1') as csvfile:
    data_reader = csv.reader(csvfile)
    next(data_reader, None)  # skip the headers

    for row in data_reader:
        #extract column value based on column index
        year = row[6]
        location = row[1]
        product_code = row[2]
        flow = row[4]
        sector_name = row[5]
        value = ecp_general.convert_value(row[8]) #uses the convert_value function created above
        
        #'product_code' function defined above; assigns a 'product category' to each of the sub-products based on its product code
        product_category = ecp_general.get_product_category(product_code)

        #initialise container of year key
        if year not in result:
            result[year] = {}
            
        #initialise container of location key
        if location not in result[year]:
                result[year][location] = {}
            
        # initialise container of product_category key if not present; that is, if the product category key is NOT already present in result, it will be addded to it
        if product_category not in result[year][location]:
            result[year][location][product_category] =  {}

        #initialise container of flow-sector names if not present
        if sector_name not in result[year][location][product_category]:
            result[year][location][product_category][sector_name] = {}

        # initialise container of flow codes if not present
        if flow not in result[year][location][product_category][sector_name]:
            result[year][location][product_category][sector_name][flow] = 0

        # perform the aggregation (in the present case, for each row, the code adds the value of 'value' to the container)
        result[year][location][product_category][sector_name][flow] += value
        
with open(path_ghg+'/national/IEA/iea_energy_combustion_emissions/detailed_figures/agg_product/iea_aggprod.csv', "w", encoding = 'utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(('Country','year','Flow','Sector','Product','CO2_emissions'))

    for year in result:
        for location in result[year]:
            for product_category in result[year][location]:
                for sector_name in result[year][location][product_category]:
                    for flow in result[year][location][product_category][sector_name]:
                        writer.writerow((location, year, flow, sector_name, product_category, result[year][location][product_category][sector_name][flow]))
                        
os.remove(path_ghg+'/national/IEA/iea_energy_combustion_emissions/detailed_figures/emissions_allyears/iea_CO2em_ally.csv')                


data = pd.read_csv(path_ghg+"/national/IEA/iea_energy_combustion_emissions/detailed_figures/agg_product/iea_aggprod.csv",
                  encoding = "utf-8") #specify encoding
data = pd.DataFrame(data)

map_iea_wb = {"CÃ\x83Â´te d'Ivoire": "Cote d'Ivoire", "CÃ´te d'Ivoire": "Cote d'Ivoire",
              '"China (P.R. of China and Hong Kong, China)"': 'China (P.R. of China and Hong Kong, China)',
              "People's Republic of China": 'China', 'CuraÃ\x83Â§ao/Netherlands Antilles': 'Curacao/Netherlands Antilles',
              'CuraÃ§ao': 'Curacao', 'CuraÃ§ao/Netherlands Antilles': 'Curacao/Netherlands Antilles',
              'Democratic Republic of Congo': 'Congo, Dem. Rep.', 'Democratic Republic of the Congo': 'Congo, Dem. Rep.',
              'Republic of the Congo': 'Congo, Rep.', 'Egypt': 'Egypt, Arab Rep.', 'Hong Kong (China)': 'Hong Kong SAR, China',
              'Islamic Republic of Iran': 'Iran, Islamic Rep.', "Democratic People's Republic of Korea": 'Korea, Dem. Rep.',
              'Korea': 'Korea, Rep.', 'Kyrgyzstan': 'Kyrgyz Republic', 'Republic of North Macedonia': 'North Macedonia',
              'Republic of Moldova':'Moldova', 'Chinese Taipei':'Taiwan, China',
              'Venezuela': 'Venezuela, RB', 'Plurinational State of Bolivia':'Bolivia',
              'United Republic of Tanzania':'Tanzania',
              'Bolivarian Republic of Venezuela': 'Venezuela, RB', 'Viet Nam': 'Vietnam', 'Yemen': 'Yemen, Rep.'}
                   
data['Country'] = data['Country'].replace(to_replace=map_iea_wb) # standardize country names to WB country names list

data.to_csv(path_ghg+'/national/IEA/iea_energy_combustion_emissions/detailed_figures/agg_product/iea_aggprod.csv',index=None)


## FUGITIVE EMISSIONS


## INDUSTRIAL PROCESSES AND PRODUCT USE

ippu_nat = pd.read_excel(path_ghg+"/national/EDGAR/v60_CO2_excl_short-cycle_org_C_1970_2018.xls",
                          sheet_name="v6.0_EM_CO2_fossil_IPCC2006", skiprows=9)

ippu_nat.drop(['IPCC_annex', 'C_group_IM24_sh', 'Country_code_A3', 'ipcc_code_2006_for_standard_report_name', 'fossil_bio'], axis=1, inplace=True)

ippu_nat = ippu_nat.loc[~ippu_nat.Name.isin(["Int. Shipping", "Int. Aviation"]), :]
ippu_nat = ippu_nat.melt(id_vars=["Name", "ipcc_code_2006_for_standard_report"])

ippu_nat.rename(columns={"Name":"jurisdiction", "ipcc_code_2006_for_standard_report":"ipcc_code", "variable":"year", "value":"CO2_emissions"}, 
                 inplace=True)
ippu_nat["ipcc_code"] = ippu_nat["ipcc_code"].apply(lambda x: x.replace('.', '').upper())
ippu_nat["year"] = ippu_nat["year"].apply(lambda x: x.replace('Y_', '').upper())
ippu_nat["ipcc_code"] = ippu_nat["ipcc_code"].apply(lambda x: x.replace('_NORES', '').upper())
ippu_nat["year"] = ippu_nat["year"].astype(int)

ippu_nat["CO2_emissions"] = ippu_nat["CO2_emissions"]/1000

# select only IPCC 2 Industrial Processes and Product Use categories
ippu_nat = ippu_nat.loc[ippu_nat.ipcc_code.str.match("2"), :]


# need to change names of countries to match names in inventory dataframe

map_edgar_wb = {'Bahamas':'Bahamas, The', 'Cape Verde':'Cabo Verde', 'Congo_the Democratic Republic of the':'Congo, Dem. Rep.',
                'Congo':'Congo, Rep.', "Egypt":'Egypt, Arab Rep.', 'Micronesia, Federated States of':'Federated States of Micronesia',
                'Gambia':'Gambia, The', 'Hong Kong':'Hong Kong SAR, China', 'Iran, Islamic Republic of':'Iran, Islamic Rep.',
                "Korea, Democratic People's Republic of":'Korea, Dem. Rep.', 'Korea, Republic of':'Korea, Rep.', 'Kyrgyzstan':'Kyrgyz Republic',
                "Lao People's Democratic Republic":'Lao PDR', 'Libyan Arab Jamahiriya':'Libya', 'Macao':'Macao SAR, China', 
                'Moldova, Republic of':'Moldova', 'Macedonia, the former Yugoslav Republic of':'North Macedonia', 'Slovakia':'Slovak Republic', 
                'Saint Kitts and Nevis':'St. Kitts and Nevis', 'Saint Lucia':'St. Lucia', 
                'Saint Vincent and the Grenadines':'St. Vincent and the Grenadines', 'Taiwan_Province of China':'Taiwan, China',
                'Tanzania_United Republic of':'Tanzania', 'Venezuela':'Venezuela, RB', 'Viet Nam':'Vietnam', 'Yemen':'Yemen, Rep.'} #'Serbia and Montenegro':'Serbia'

ippu_nat["jurisdiction"] = ippu_nat["jurisdiction"].replace(to_replace=map_edgar_wb)



# DATA FORMATTING (common inventory reporting format)

# 1A Fuel Combustion Activities
combustion_nat = pd.read_csv(path_ghg+"/national/IEA/iea_energy_combustion_emissions/detailed_figures/agg_product/iea_aggprod.csv",
                  encoding = "utf-8") #specify encoding
combustion_nat.rename(columns={"Country":"jurisdiction", "Year":"year", "Flow":"iea_code"}, inplace=True)
combustion_nat.drop("Sector", axis=1, inplace=True)

combustion_nat = combustion_nat.merge(ipcc_iea_map, on=["iea_code"], how="left")
combustion_nat["CO2_emissions"] = combustion_nat["CO2_emissions"]/1000

# 2 Industrial Processes and Product Use
ippu_nat = ippu_nat[["jurisdiction", "year", "ipcc_code", "CO2_emissions"]]
ippu_nat["year"] = ippu_nat["year"].astype(int)
ippu_nat["iea_code"] = "NA"
ippu_nat["Product"] = "NA"


# COMBINED INVENTORY

inventory_nat = wcpd_all.loc[wcpd_all.jurisdiction.isin(ctry_names), ["jurisdiction", "year", "ipcc_code", "iea_code", "Product"]]
inventory_nat[["iea_code", "Product"]] = inventory_nat[["iea_code", "Product"]].fillna("NA")

combined_nat = pd.concat([combustion_nat, ippu_nat])

inventory_nat = inventory_nat.merge(combined_nat, on=["jurisdiction", "year", "ipcc_code", "iea_code", "Product"], how="left")