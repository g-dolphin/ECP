## PACKAGES / LIBRARIES

import pandas as pd

# OTHER
isoA3 = ['ALB', 'AUT', 'BIH', 'BEL', 'BGR', 
         'CHE', 'CYP', 'CZE', 'DEU', 'DNK', 
         'EST', 'GRC', 'ESP', 'EU27', 
         'FIN', 'FRA', 'GEO', 'HRV', 'HUN', 
         'IRL', 'ISL', 'ITA', 'LTU', 'LUX', 
         'LVA', 'MDA', 'MNE', 'MKD', 'MLT', 
         'NLD', 'NOR', 'POL', 'PRT', 'ROU', 
         'RUS', 'SWE', 'SVN', 'SVK', 'TUR', 
         'UKR', 'GBR', 'XXK']

estat = ['AL', 'AT', 'BA', 'BE', 'BG', 
         'CH', 'CY', 'CZ', 'DE', 'DK', 
         'EE', 'EL', 'ES', 'EU27_2020', 
         'FI', 'FR', 'GE', 'HR', 'HU', 
         'IE', 'IS', 'IT', 'LT', 'LU', 
         'LV', 'MD', 'ME', 'MK', 'MT', 
         'NL', 'NO', 'PL', 'PT', 'RO', 
         'RS', 'SE', 'SI', 'SK', 'TR', 
         'UA', 'UK', 'XK']

isoA2 = ['AL', 'AT', 'BA', 'BE', 'BG', 
         'CH', 'CY', 'CZ', 'DE', 'DK', 
         'EE', 'EL', 'ES', 'EU27_2020', 
         'FI', 'FR', 'GE', 'HR', 'HU', 
         'IE', 'IS', 'IT', 'LT', 'LU', 
         'LV', 'MD', 'ME', 'MK', 'MT', 
         'NL', 'NO', 'PL', 'PT', 'RO', 
         'RS', 'SE', 'SI', 'SK', 'TR', 
         'UA', 'UK', 'XK']

weoNames = ['Albania', 'Austria', 'Bosnia and Herzegovina', 'Belgium', 'Bulgaria',
            'Switzerland', 'Cyprus', 'Czechia', 'Germany', 'Denmark', 
            'Estonia', "Greece", "Spain", 'EU27', 
            "Finland", "France", "Georgia", "Croatia", "Hungary", 
            "Ireland", "Iceland", "Italy", "Lithuania", "Luxemburg", 
            "Latvia", "Moldova", "Montenegro", "North Macedonia", "Malta", 
            "Netherlands", "Norway", "Poland", "Portugal", "Romania", 
            "Russia", "Sweden", "Slovenia", "Slovakia", "Turkiye", 
            "Ukraine", "United Kingdom", "Kosovo"]

estattoISOa3Map = dict(zip(estat, isoA3)) 
ISOa3toNameMap = dict(zip(isoA3, weoNames))
NametoISOa3NameMap = dict(zip(weoNames, isoA3))
ISOa2toISOa3Map = dict(zip(isoA2, isoA3))

# COUNTRY SELECTION
ctrySel = ['ALB', 'AUT', 'BIH', 'BEL', 'BGR',
          'CHE', 'CYP', 'CZE', 'DEU', 'DNK', 
          'EST', 'GRC', 'ESP', 'EU27',
          'FIN', 'FRA', 'GEO', 'HRV', 'HUN', 
          'IRL', 'ISL', 'ITA', 'LTU', 'LUX', 
          'LVA', 'MDA', 'MNE', 'MKD', 'MLT', 
          'NLD', 'NOR', 'POL', 'PRT', 'ROU', 
          'RUS', 'SWE', 'SVN', 'SVK', 'TUR', 
          'UKR', 'GBR', 'XXK']

ctrySelEU = ['AUT', 'BEL', 'BGR', 'CYP', 'CZE', 
            'DEU', 'DNK', 'EST', 'GRC', 'ESP', 
            'FIN', 'FRA', 'HRV', 'HUN', 'IRL',
            'ITA', 'LTU', 'LUX', 'LVA', 'MLT', 
            'NLD', 'POL', 'PRT', 'ROU', 'SWE', 
            'SVN', 'SVK']

ctrySelnEU = ['ALB', 'BIH', 'CHE', 'GEO', 'ISL', 'ITA', 
             'MDA', 'MNE', 'MKD', 'NOR', 'POL', 'RUS', 
             'TUR', 'UKR', 'GBR', 'XXK']

#######################################################################################
################################### START CODE HERE ###################################
#######################################################################################

#Some code to download and concatenate files for specific jurisdictions

# DOWNLOAD DATA

def concatenate(indir):

    fileList = ['prices_usd_kFixRate_CO2_Afghanistan.csv', 'prices_usd_kFixRate_CO2_Albania.csv', 'prices_usd_kFixRate_CO2_Algeria.csv', 'prices_usd_kFixRate_CO2_Andorra.csv', 
                'prices_usd_kFixRate_CO2_Angola.csv', 'prices_usd_kFixRate_CO2_Antigua_and_Barbuda.csv', 'prices_usd_kFixRate_CO2_Argentina.csv', 'prices_usd_kFixRate_CO2_Armenia.csv', 
                'prices_usd_kFixRate_CO2_Australia.csv', 'prices_usd_kFixRate_CO2_Austria.csv', 'prices_usd_kFixRate_CO2_Azerbaijan.csv', 'prices_usd_kFixRate_CO2_Bahamas_The.csv', 
                'prices_usd_kFixRate_CO2_Bahrain.csv', 'prices_usd_kFixRate_CO2_Bangladesh.csv', 'prices_usd_kFixRate_CO2_Barbados.csv', 'prices_usd_kFixRate_CO2_Belarus.csv', 
                'prices_usd_kFixRate_CO2_Belgium.csv', 'prices_usd_kFixRate_CO2_Belize.csv', 'prices_usd_kFixRate_CO2_Benin.csv', 'prices_usd_kFixRate_CO2_Bhutan.csv', 
                'prices_usd_kFixRate_CO2_Bolivia.csv', 'prices_usd_kFixRate_CO2_Bosnia_and_Herzegovina.csv', 'prices_usd_kFixRate_CO2_Botswana.csv', 'prices_usd_kFixRate_CO2_Brazil.csv', 
                'prices_usd_kFixRate_CO2_Brunei_Darussalam.csv', 'prices_usd_kFixRate_CO2_Bulgaria.csv', 'prices_usd_kFixRate_CO2_Burkina_Faso.csv', 'prices_usd_kFixRate_CO2_Burundi.csv', 
                'prices_usd_kFixRate_CO2_Cabo_Verde.csv', 'prices_usd_kFixRate_CO2_Cambodia.csv', 'prices_usd_kFixRate_CO2_Cameroon.csv', 'prices_usd_kFixRate_CO2_Canada.csv', 
                'prices_usd_kFixRate_CO2_Central_African_Republic.csv', 'prices_usd_kFixRate_CO2_Chad.csv', 'prices_usd_kFixRate_CO2_Chile.csv', 'prices_usd_kFixRate_CO2_China.csv', 
                'prices_usd_kFixRate_CO2_Colombia.csv', 'prices_usd_kFixRate_CO2_Comoros.csv', 'prices_usd_kFixRate_CO2_Congo_Dem_Rep.csv', 'prices_usd_kFixRate_CO2_Congo_Rep.csv', 
                'prices_usd_kFixRate_CO2_Costa_Rica.csv', "prices_usd_kFixRate_CO2_Cote_d'Ivoire.csv", 'prices_usd_kFixRate_CO2_Croatia.csv', 'prices_usd_kFixRate_CO2_Cuba.csv', 
                'prices_usd_kFixRate_CO2_Cyprus.csv', 'prices_usd_kFixRate_CO2_Czech_Republic.csv', 'prices_usd_kFixRate_CO2_Denmark.csv', 'prices_usd_kFixRate_CO2_Djibouti.csv', 
                'prices_usd_kFixRate_CO2_Dominica.csv', 'prices_usd_kFixRate_CO2_Dominican_Republic.csv', 'prices_usd_kFixRate_CO2_Ecuador.csv', 'prices_usd_kFixRate_CO2_Egypt_Arab_Rep.csv', 
                'prices_usd_kFixRate_CO2_El_Salvador.csv', 'prices_usd_kFixRate_CO2_Equatorial_Guinea.csv', 'prices_usd_kFixRate_CO2_Eritrea.csv', 'prices_usd_kFixRate_CO2_Estonia.csv', 
                'prices_usd_kFixRate_CO2_Ethiopia.csv', 'prices_usd_kFixRate_CO2_Federated_States_of_Micronesia.csv', 'prices_usd_kFixRate_CO2_Fiji.csv', 'prices_usd_kFixRate_CO2_Finland.csv', 
                'prices_usd_kFixRate_CO2_France.csv', 'prices_usd_kFixRate_CO2_Gabon.csv', 'prices_usd_kFixRate_CO2_Gambia_The.csv', 'prices_usd_kFixRate_CO2_Georgia.csv', 'prices_usd_kFixRate_CO2_Germany.csv', 
                'prices_usd_kFixRate_CO2_Ghana.csv', 'prices_usd_kFixRate_CO2_Greece.csv', 'prices_usd_kFixRate_CO2_Grenada.csv', 'prices_usd_kFixRate_CO2_Guatemala.csv', 'prices_usd_kFixRate_CO2_Guinea-Bissau.csv', 
                'prices_usd_kFixRate_CO2_Guinea.csv', 'prices_usd_kFixRate_CO2_Guyana.csv', 'prices_usd_kFixRate_CO2_Haiti.csv', 'prices_usd_kFixRate_CO2_Honduras.csv', 'prices_usd_kFixRate_CO2_Hong_Kong_SAR_China.csv', 
                'prices_usd_kFixRate_CO2_Hungary.csv', 'prices_usd_kFixRate_CO2_Iceland.csv', 'prices_usd_kFixRate_CO2_India.csv', 'prices_usd_kFixRate_CO2_Indonesia.csv', 'prices_usd_kFixRate_CO2_Iran_Islamic_Rep.csv', 
                'prices_usd_kFixRate_CO2_Iraq.csv', 'prices_usd_kFixRate_CO2_Ireland.csv', 'prices_usd_kFixRate_CO2_Israel.csv', 'prices_usd_kFixRate_CO2_Italy.csv', 'prices_usd_kFixRate_CO2_Jamaica.csv', 
                'prices_usd_kFixRate_CO2_Japan.csv', 'prices_usd_kFixRate_CO2_Jordan.csv', 'prices_usd_kFixRate_CO2_Kazakhstan.csv', 'prices_usd_kFixRate_CO2_Kenya.csv', 'prices_usd_kFixRate_CO2_Kiribati.csv', 
                'prices_usd_kFixRate_CO2_Korea_Dem_Rep.csv', 'prices_usd_kFixRate_CO2_Korea_Rep.csv', 'prices_usd_kFixRate_CO2_Kosovo.csv', 'prices_usd_kFixRate_CO2_Kuwait.csv', 'prices_usd_kFixRate_CO2_Kyrgyz_Republic.csv', 
                'prices_usd_kFixRate_CO2_Lao_PDR.csv', 'prices_usd_kFixRate_CO2_Latvia.csv', 'prices_usd_kFixRate_CO2_Lebanon.csv', 'prices_usd_kFixRate_CO2_Lesotho.csv', 'prices_usd_kFixRate_CO2_Liberia.csv', 
                'prices_usd_kFixRate_CO2_Libya.csv', 'prices_usd_kFixRate_CO2_Liechtenstein.csv', 'prices_usd_kFixRate_CO2_Lithuania.csv', 'prices_usd_kFixRate_CO2_Luxembourg.csv', 'prices_usd_kFixRate_CO2_Macao_SAR_China.csv', 
                'prices_usd_kFixRate_CO2_Madagascar.csv', 'prices_usd_kFixRate_CO2_Malawi.csv', 'prices_usd_kFixRate_CO2_Malaysia.csv', 'prices_usd_kFixRate_CO2_Maldives.csv', 'prices_usd_kFixRate_CO2_Mali.csv', 
                'prices_usd_kFixRate_CO2_Malta.csv', 'prices_usd_kFixRate_CO2_Marshall_Islands.csv', 'prices_usd_kFixRate_CO2_Mauritania.csv', 'prices_usd_kFixRate_CO2_Mauritius.csv', 'prices_usd_kFixRate_CO2_Mexico.csv', 
                'prices_usd_kFixRate_CO2_Moldova.csv', 'prices_usd_kFixRate_CO2_Monaco.csv', 'prices_usd_kFixRate_CO2_Mongolia.csv', 'prices_usd_kFixRate_CO2_Montenegro.csv', 'prices_usd_kFixRate_CO2_Morocco.csv', 
                'prices_usd_kFixRate_CO2_Mozambique.csv', 'prices_usd_kFixRate_CO2_Myanmar.csv', 'prices_usd_kFixRate_CO2_Namibia.csv', 'prices_usd_kFixRate_CO2_Nauru.csv', 'prices_usd_kFixRate_CO2_Nepal.csv', 
                'prices_usd_kFixRate_CO2_Netherlands.csv', 'prices_usd_kFixRate_CO2_New_Zealand.csv', 'prices_usd_kFixRate_CO2_Nicaragua.csv', 'prices_usd_kFixRate_CO2_Niger.csv', 'prices_usd_kFixRate_CO2_Nigeria.csv', 
                'prices_usd_kFixRate_CO2_North_Macedonia.csv', 'prices_usd_kFixRate_CO2_Norway.csv', 'prices_usd_kFixRate_CO2_Oman.csv', 'prices_usd_kFixRate_CO2_Pakistan.csv', 'prices_usd_kFixRate_CO2_Palau.csv', 
                'prices_usd_kFixRate_CO2_Panama.csv', 'prices_usd_kFixRate_CO2_Papua_New_Guinea.csv', 'prices_usd_kFixRate_CO2_Paraguay.csv', 'prices_usd_kFixRate_CO2_Peru.csv', 'prices_usd_kFixRate_CO2_Philippines.csv', 
                'prices_usd_kFixRate_CO2_Poland.csv', 'prices_usd_kFixRate_CO2_Portugal.csv', 'prices_usd_kFixRate_CO2_Puerto_Rico.csv', 'prices_usd_kFixRate_CO2_Qatar.csv', 'prices_usd_kFixRate_CO2_Romania.csv', 
                'prices_usd_kFixRate_CO2_Russian_Federation.csv', 'prices_usd_kFixRate_CO2_Rwanda.csv', 'prices_usd_kFixRate_CO2_Samoa.csv', 'prices_usd_kFixRate_CO2_San_Marino.csv', 
                'prices_usd_kFixRate_CO2_Sao_Tome_and_Principe.csv', 'prices_usd_kFixRate_CO2_Saudi_Arabia.csv', 'prices_usd_kFixRate_CO2_Senegal.csv', 'prices_usd_kFixRate_CO2_Serbia.csv', 
                'prices_usd_kFixRate_CO2_Seychelles.csv', 'prices_usd_kFixRate_CO2_Sierra_Leone.csv', 'prices_usd_kFixRate_CO2_Singapore.csv', 'prices_usd_kFixRate_CO2_Slovak_Republic.csv', 'prices_usd_kFixRate_CO2_Slovenia.csv', 
                'prices_usd_kFixRate_CO2_Solomon_Islands.csv', 'prices_usd_kFixRate_CO2_Somalia.csv', 'prices_usd_kFixRate_CO2_South_Africa.csv', 'prices_usd_kFixRate_CO2_South_Sudan.csv', 'prices_usd_kFixRate_CO2_Spain.csv', 
                'prices_usd_kFixRate_CO2_Sri_Lanka.csv', 'prices_usd_kFixRate_CO2_St_Kitts_and_Nevis.csv', 'prices_usd_kFixRate_CO2_St_Lucia.csv', 'prices_usd_kFixRate_CO2_St_Vincent_and_the_Grenadines.csv', 
                'prices_usd_kFixRate_CO2_Sudan.csv', 'prices_usd_kFixRate_CO2_Suriname.csv', 'prices_usd_kFixRate_CO2_Swaziland.csv', 'prices_usd_kFixRate_CO2_Sweden.csv', 'prices_usd_kFixRate_CO2_Switzerland.csv',
                'prices_usd_kFixRate_CO2_Timor-Leste.csv', 
                'prices_usd_kFixRate_CO2_Togo.csv', 'prices_usd_kFixRate_CO2_Tonga.csv', 'prices_usd_kFixRate_CO2_Trinidad_and_Tobago.csv', 'prices_usd_kFixRate_CO2_Tunisia.csv', 'prices_usd_kFixRate_CO2_Turkey.csv', 
                'prices_usd_kFixRate_CO2_Turkmenistan.csv', 'prices_usd_kFixRate_CO2_Tuvalu.csv', 'prices_usd_kFixRate_CO2_Uganda.csv', 'prices_usd_kFixRate_CO2_Ukraine.csv', 
                'prices_usd_kFixRate_CO2_United_Arab_Emirates.csv', 'prices_usd_kFixRate_CO2_United_Kingdom.csv', 'prices_usd_kFixRate_CO2_United_States.csv', 'prices_usd_kFixRate_CO2_Uruguay.csv', 
                'prices_usd_kFixRate_CO2_Uzbekistan.csv', 'prices_usd_kFixRate_CO2_Vanuatu.csv', 'prices_usd_kFixRate_CO2_Vatican_City.csv', 'prices_usd_kFixRate_CO2_Venezuela_RB.csv', 
                'prices_usd_kFixRate_CO2_Vietnam.csv', 'prices_usd_kFixRate_CO2_Western_Sahara.csv', 'prices_usd_kFixRate_CO2_West_Bank_and_Gaza.csv', 'prices_usd_kFixRate_CO2_Yemen_Rep.csv', 
                'prices_usd_kFixRate_CO2_Zambia.csv', 'prices_usd_kFixRate_CO2_Zimbabwe.csv']
    dfList = []

    #each iteration of the loop will add a dataframe to the list
    for filename in fileList:
        path = indir+filename
        print(filename)
        df=pd.read_csv(path, keep_default_na=False, header=0)
        dfList.append(df)

    #'axis=0' ensures that we are concatenating vertically,
    concatDf=pd.concat(dfList,axis=0)

    #    concatDf.to_csv(outfile,index=None)
    return concatDf

#indir = r"https://raw.githubusercontent.com/g-dolphin/ECP/master/_raw/wcpd_usd/CO2/constantPrices/FixedXRate/"
#pathECP = r"https://raw.githubusercontent.com/g-dolphin/ECP/master/_dataset/ecp/ipcc/ecp_economy/ecp_CO2.csv"
#pathCoverage = r"https://raw.githubusercontent.com/g-dolphin/ECP/master/_dataset/coverage/tot_coverage_jurisdiction_CO2.csv"

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
