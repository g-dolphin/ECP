import pandas as pd

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

def prepare_carbon_price_data(data_dir, year):
    """Load and combine all carbon price CSVs in given folder."""
    from glob import glob
    files = glob(f"{data_dir}/*.csv")
    dfs = [pd.read_csv(f) for f in files]
    df = pd.concat(dfs, ignore_index=True)

    pathECP = r"/Users/gd/GitHub/ECP/_output/_dataset/ecp/ipcc/ecp_economy/ecp_CO2.csv"
    pathCoverage = r"/Users/gd/GitHub/ECP/_output/_dataset/coverage/tot_coverage_jurisdiction_CO2.csv"

    prices_usd = df.copy()
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

    prices_usd_max.drop(["ipcc_code"], axis=1, inplace=True)
    prices_usd_max.reset_index(inplace=True)

    world_row = pd.DataFrame({"jurisdiction":"World", "year":year, "max_price":prices_usd_max.max_price.max()}, index=[0])
    prices_usd_max = pd.concat([prices_usd_max, world_row], ignore_index=True)

    # filling 'max_price' column with 0

    prices_usd_max["max_price"] = prices_usd_max["max_price"].fillna(0)

    # Add ecp column

    prices_usd_max = prices_usd_max.merge(ecp[["jurisdiction", "year", "ecp_all_jurCO2_usd_k"]], 
                    on=["jurisdiction", "year"], how="left")


    prices_usd_max["pct_difference"] = 1-(prices_usd_max.ecp_all_jurCO2_usd_k/prices_usd_max.max_price)

    # SAVE INPUT & OUTPUT FILES
    #prices_usd.to_csv(path_input+r"_usd.csv", index = False)
    #ecp.to_csv(path_input+r"_ecp.csv", index = False)
    #coverage.to_csv(path_input+r"_coverage.csv", index = False)

    prices_usd_max.to_csv(r"/Users/gd/GitHub/ECP/_output/_figures/dataFig/carbonPrices_usd_max_"+str(year)+".csv", index = False)
    #prices_economy.to_csv(path_output+r"_economy.csv", index = False)

    return df, prices_usd_max