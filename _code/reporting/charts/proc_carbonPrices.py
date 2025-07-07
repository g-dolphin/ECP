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

def prepare_carbon_price_data(data_dir):
    """Load and combine all carbon price CSVs in given folder."""
    from glob import glob
    files = glob(f"{data_dir}/*.csv")
    dfs = [pd.read_csv(f) for f in files]
    df = pd.concat(dfs, ignore_index=True)
    return df
