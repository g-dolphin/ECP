
import pandas as pd
import numpy as np
import os
from importlib.machinery import SourceFileLoader

path_dependencies = '/Users/gd/GitHub/ECP/_code/compilation/_dependencies/dep_ecp'
path_ghg = '/Users/gd/OneDrive - rff/documents/research/projects/ecp/ecp_dataset/source_data/ghg_inventory/raw'

ecp_general = SourceFileLoader('general_func', path_dependencies+'/ecp_v3_gen_func.py').load_module()

# CO2

def inventory_co2(wcpd_df, jur_names, iea_wb_map, edgar_ghg_df, edgar_wb_map):

    # Dictionary of product categories
    productCategories = {"Coal":['HARDCOAL', 'BROWN', 'ANTCOAL', 'COKCOAL', 'BITCOAL', 'SUBCOAL', 
                                    'LIGNITE', 'PATFUEL', 'OVENCOKE', 'GASCOKE', 'COALTAR', 'BKB', 
                                    'GASWKSGS', 'COKEOVGS', 'BLFURGS', 'OGASES', 'PEAT', 'PEATPROD', 'OILSHALE'],
                        "Natural gas":['NATGAS'],
                        "Oil":['CRNGFEED', 'CRUDEOIL', 'NGL', 'REFFEEDS', 'ADDITIVE', 'ORIMUL', 
                                'NONCRUDE', 'REFINGAS', 'ETHANE', 'LPG', 'NONBIOGAS', 'AVGAS', 
                                'JETGAS', 'OTHKE', 'RESFUEL', 'NAPHTA', 'WHITESP', 'LUBRIC', 
                                'BITUMEN', 'PARWAX', 'PETCOKE', 'ONONSPEC', 'NONBIOLJET'],
                        "Other":['INDWASTE', 'MUNWASTE', 'PRIMSBIO', 'BIOGASES', 'BIOGASOL',
                                'BIODIESEL', 'OBIOLIQ', 'RENEWNS', 'CHARCOAL'],
                        "Total":['TOTAL']}

    # concatenate IEA yearly emissions files
    df = pd.read_fwf(path_ghg+'/national/IEA/iea_energy_ghg_emissions/2024_edition/WORLD_BIGCO2.TXT',
                     header=None, names=["jurisdiction", "Product", "year", "FLOWname", "CO2"],
                     colspecs=[(0,12), (15, 25), (30, 38), (40,58), (58, 85)])

    df["CO2"].replace(to_replace={"..":np.nan, "x":np.nan, "c":np.nan}, 
                        inplace=True)
    df["CO2"] = df["CO2"].astype(float)
    
    memoAggregates = ['OECDAM', 'OECDAO', 'OECDEUR', 'OECDTOT', 'OTHERAFRIC' 'OTHERASIA' 'OTHERLATIN',
                      'IEATOT', 'ANNEX2NA', 'ANNEX2EU', 'ANNEX2AO', 'ANNEX2', 'MG7', 'AFRICA',
                      'UNAFRICA', 'MIDEAST', 'EURASIA', 'LATAMER', 'ASIA', 'CHINAREG', 'NOECDTOT',
                      'IEAFAMILY', 'WORLDAV', 'WORLDMAR', 'WORLD', 'UNAMERICAS', 'UNASIATOT',
                      'UNEUROPE', 'UNOCEANIA', 'EU28', 'ANNEX1', 'ANNEX1EIT', 'NONANNEX1', 'ANNEXB',
                      'MYUGO', 'MFSU15', 'MG8', 'MG20', 'OPEC', 'MASEAN', 'EU27_2020', 'MBURKINAFA',
                      'MCHAD', 'MMAURITANI', 'MPALESTINE', 'MMALI', 'MGREENLAND', 'FSUND']

    df = df.loc[~df.jurisdiction.isin(memoAggregates)]
    df["jurisdiction"] = df["jurisdiction"].apply(lambda x: x.capitalize())

    df["ProductCat"] = df["Product"].copy()

    for key in productCategories.keys():
        for product in productCategories[key]:
            df["ProductCat"].replace(to_replace={product:key}, inplace=True)

    df = df.groupby(["jurisdiction", "ProductCat", "year", "FLOWname"]).sum().reset_index()


    # Country names replacement
    df["jurisdiction"].replace(to_replace=iea_wb_map, inplace=True)

    # Add Flow codes to dataframe
    flowCodes = pd.read_csv('/Users/gd/GitHub/ECP/_raw/_aux_files/iea_ukds_FLOWcodes.csv',
                            usecols=[0,1])
    df = df.merge(flowCodes, on='FLOWname', how='left')

    # Add ipcc codes
    ipccCodes = pd.read_csv('/Users/gd/GitHub/ECP/_raw/_aux_files/ipcc2006_iea_category_codes.csv',
                            usecols=[0,3])
    ipccCodes = ipccCodes[~ipccCodes.FLOW.isna()] # remove rows with NA entries; otherwise 'NA' entries in 'FLOW' column get merged with the multiple 'NA' entries in ipccCodes
    df = df.merge(ipccCodes, on='FLOW', how='left')

    # dataframe format/labels standardization
    df.rename(columns={"FLOW":"iea_code", "ProductCat":'Product'}, inplace=True)
    df.drop("FLOWname", axis=1, inplace=True)

    combustion_nat = df.copy()
    del df

    # Data from EDGAR database (IPPU)
    # select sectors
    ippu_fug_nat = edgar_ghg_df.loc[edgar_ghg_df.ipcc_code.str.match("1B|2"), :]
    ippu_fug_nat["jurisdiction"].replace(to_replace=edgar_wb_map, inplace=True)

    # dataframe standardization
    ippu_fug_nat = ippu_fug_nat[["jurisdiction", "year", "ipcc_code", "CO2"]]
    ippu_fug_nat["year"] = ippu_fug_nat["year"].astype(int)
    ippu_fug_nat["iea_code"] = "NA"
    ippu_fug_nat["Product"] = "NA"


    # COMBINED INVENTORY

    inventory_nat = wcpd_df.loc[wcpd_df.jurisdiction.isin(jur_names), ["jurisdiction", "year", "ipcc_code", "iea_code", "Product"]]
    inventory_nat[["iea_code", "Product"]] = inventory_nat[["iea_code", "Product"]].fillna("NA")

    combined_nat = pd.concat([combustion_nat, ippu_fug_nat], axis=0)

    inventory_nat = inventory_nat.merge(combined_nat, on=["jurisdiction", "year", "ipcc_code", "iea_code", "Product"], how="left")
    
    return inventory_nat


# OTHER GHGs
def inventory_non_co2(gas, edgar_ghg):

    # format ipcc_code and year columns
    edgar_ghg["ipcc_code"] = edgar_ghg["ipcc_code"].apply(lambda x: x.replace('.', '').upper())
    edgar_ghg["ipcc_code"] = edgar_ghg["ipcc_code"].apply(lambda x: x.replace('_NORES', '').upper())

    df = edgar_ghg[["jurisdiction", "year", "ipcc_code", gas]]

    return df

# Other GHGs - iea
# NB: for fugitive emissions, EDGAR is more granular
def inventory_non_co2_iea():
    df = pd.read_fwf(path_ghg+'/national/IEA/iea_energy_ghg_emissions/2024_edition/WORLD_GHG.TXT',
                        header=None, names=["jurisdiction", "Product", "year", "FLOWname", "gas", "Value"],
                        colspecs=[(0,12), (15, 25), (30, 38), (40,58), (58, 75), (75, 95)])

    df = df.loc[~df.gas.isin(["CO2", "TOTAL"])]

    df = df.loc[~df.jurisdiction.isin(memoAggregates)]
    df["jurisdiction"] = df["jurisdiction"].apply(lambda x: x.capitalize())

    # Country names replacement
    df["jurisdiction"].replace(to_replace=iea_wb_map, inplace=True)

    # Add Flow codes to dataframe
    flowCodes = pd.read_csv('/Users/gd/GitHub/ECP/_raw/_aux_files/iea_ukds_FLOWcodes.csv',
                            usecols=[0,1])
    df = df.merge(flowCodes, on='FLOWname', how='left')

    # Add ipcc codes
    ipccCodes = pd.read_csv('/Users/gd/GitHub/ECP/_raw/_aux_files/ipcc2006_iea_category_codes.csv',
                            usecols=[0,3])
    df = df.merge(ipccCodes, on='FLOW', how='left')
