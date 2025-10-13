import pandas as pd
import glob
import numpy as np

# This script processes the GLORIA MRIO and satellite tables   

root = "/Users/gd/OneDrive - rff/Documents/Research/resources/data/MRIO_tables/GLORIA/"
rootI = "/Users/gd/GitHub/ecp_distrib/datamatch/1_import_&_format_raw/gloria"

# Loading labels

Regions = pd.read_excel(rootI+"/GLORIA_ReadMe_057_MM.xlsx",
                        sheet_name="Regions")
Sectors = pd.read_excel(rootI+"/GLORIA_ReadMe_057_MM.xlsx",
                        sheet_name="Sectors")
Satellites = pd.read_excel(rootI+"/GLORIA_ReadMe_057_MM.xlsx",
                            sheet_name="Satellites")


#-----------------------------------------------------------------------------

# NOTE ON UNITS: emissions are expressed in kt (or, equivalently, Gg),
#                monetary values are expressed in thousand USD current price (see GLORIA technical doc)
    

def gloria57_proc(year):
    
    # condition to choose years - needed in case some 
    if year > 2028:
        year_mrio = 2028
    else:
        year_mrio = year

    year_dir = str(year_mrio)
    gloria_path = root+"tables/"+year_dir

    # Load transactions matrix (T), value added matrix (V), final demand matrix (Y), and satellite matrices (TQ, YQ)

    # PATHS
    T_filepath = glob.glob(gloria_path+"/mrio/20230320_120secMother_AllCountries_002_T-Results_*_057_Markup001(full).csv")
    V_filepath = glob.glob(gloria_path+"/mrio/20230320_120secMother_AllCountries_002_V-Results_*_057_Markup001(full).csv")
    Y_filepath = glob.glob(gloria_path+"/mrio/20230320_120secMother_AllCountries_002_Y-Results_*_057_Markup001(full).csv")
    TQ_filepath = glob.glob(gloria_path+"/satellite/20230727_120secMother_AllCountries_002_TQ-Results_*_057_Markup001(full).csv")
    YQ_filepath = glob.glob(gloria_path+"/satellite/20230727_120secMother_AllCountries_002_YQ-Results_*_057_Markup001(full).csv")

    # specifying rows and column indices that need to be kept
    # every other column is dropped because it contains information on products (keeping industry)
    # every other 120 rows block is dropped as these contain product data
    rowIndices = [x for x in range(120, 240)]

    k = 0
    startCol = []
    for i in range(0, int(39360/(2*120))):
        startCol.append(k)
        k += 2*120

    k = 120
    endCol = []
    for i in range(0, int(39360/(2*120))):
        endCol.append(k)
        k += 2*120

    colIndices = []
    ran = [x for x in range(0, len(startCol))]
    for i in ran:
        temp = [x for x in range(startCol[i], endCol[i])]
        colIndices = colIndices+temp


    # Transactions matrix
    T = pd.DataFrame()

    for file in T_filepath: 
        with pd.read_csv(file, header=None, 
                          chunksize=240, 
                          usecols = colIndices) as reader:
            
            i = 0
            for chunk in reader:
                chunk.reset_index(inplace=True)
                chunk.drop('index', axis=1, inplace=True)
                chunk = chunk.iloc[rowIndices]

                if i == 0:
                    T = chunk
                else:
                    T = pd.concat([T, chunk])

                i+=1

    # Value-added matrix
    V = pd.read_csv(V_filepath[0], header=None,
                    usecols = colIndices)

    # Demand matrix
    Y = pd.DataFrame()

    for file in Y_filepath: 
        with pd.read_csv(file, header=None, 
                         chunksize=240) as reader:
            
            i = 0
            for chunk in reader:
                chunk.reset_index(inplace=True)
                chunk.drop('index', axis=1, inplace=True)
                chunk = chunk.iloc[rowIndices]

                if i == 0:
                    Y = chunk
                else:
                    Y = pd.concat([Y, chunk])

                i+=1

    # Satellite (emissions) matrix
    TQ = pd.read_csv(TQ_filepath[0], header=None,
                     usecols = colIndices)
    YQ = pd.read_csv(YQ_filepath[0], header=None)

    # convert monetary values to constant USD
    # cum_inf_factor = gdp_defl.loc[gdp_defl.Year==year_mrio, "cum_inf"].item()

#    T = T*cum_inf_factor
#    V = V*cum_inf_factor
#    Y = Y*cum_inf_factor

    #-----------------------------------------------------------------------------

    # Calculate total input from sum of 
    # 1. country-industry aggregation of transactions
    # 2. country-industry value added

    # Aggregate transactions matrix across all columns (country-industry level)

    T_agg = np.array(T.sum(axis=1)).reshape(len(T), 1)
    T_agg = pd.DataFrame(data=T_agg,
                         columns=['T'])

    T_agg_col = np.array(T.sum(axis=0)).reshape(len(T), 1)
    T_agg_col = pd.DataFrame(data=T_agg_col,
                             columns=['T'])

    Y_agg = np.array(Y.sum(axis=1)).reshape(len(Y), 1)
    Y_agg = pd.DataFrame(data=Y_agg,
                         columns=['Y'])

    V_agg = np.array(V.sum(axis=0)).reshape(19680, 1)
    V_agg = pd.DataFrame(data=V_agg,
                         columns=['V'])
    
    # Append labels to matrices
    ## create labels dataframes 
    sectorsExt = []
    sectorsMatch = []
    for i in range(0, 164):
        sectorsExt = np.append(sectorsExt, np.array(Sectors.Sector_names))
        sectorsMatch = np.append(sectorsMatch, np.array(Sectors.MM_sector_match))

    labelsT = pd.DataFrame(data={"regions":np.array(np.repeat(Regions.Region_acronyms, 120)),
                                 "sectors": sectorsExt, "MM_sector_match": sectorsMatch})
    
    aggSectorsLabels = Sectors[['MM_sector', 'MM_sector_name']]
    labelsT = labelsT.merge(aggSectorsLabels,
                            left_on=["MM_sector_match"], right_on=["MM_sector"],
                            how='left')
    labelsT = labelsT.merge(Regions[["Region_acronyms", "MM_region_match"]],
                            left_on=["regions"], right_on=["Region_acronyms"], 
                            how="left")
    labelsT = labelsT.merge(Regions[["MM_region", "MM_region_name"]],
                            left_on=["MM_region_match"], right_on=["MM_region"], 
                            how="left")

    labelsT.drop(['MM_sector_match', 'MM_sector', 
                  'Region_acronyms', 'MM_region_match', 'MM_region'], axis=1,
                  inplace=True)
    
    labelsT.rename(columns={"MM_sector_name":"sector", "MM_region_name":"regionName"}, 
                   inplace=True)

    labelsQ = Satellites[["Sat_head_indicator", "Sat_indicator"]]
    labelsQ["Sat_indicator"] = labelsQ["Sat_indicator"].apply(lambda x: x.replace("'", ""))

    #-----------------------Sectors and regions aggregation------------------------------  

    ## append labels (including region and sector aggregates)
    T_agg = pd.concat([labelsT, T_agg], axis=1)
    T_agg_col = pd.concat([labelsT, T_agg_col], axis=1)
    Y_agg = pd.concat([labelsT, Y_agg], axis=1)
    V_agg = pd.concat([labelsT, V_agg], axis=1)
    
    TQ = pd.concat([labelsQ, TQ], axis=1)
    YQ = pd.concat([labelsQ, YQ], axis=1)

    T_agg = T_agg.groupby(["regionName", "sector"]).sum()
    T_agg.reset_index(inplace=True)

    T_agg_col = T_agg_col.groupby(["regionName", "sector"]).sum()
    T_agg_col.reset_index(inplace=True)

    Y_agg = Y_agg.groupby(["regionName", "sector"]).sum()
    Y_agg.reset_index(inplace=True)

    V_agg = V_agg.groupby(["regionName", "sector"]).sum()
    V_agg.reset_index(inplace=True)

    # Sum country-industry demand matrix (Y) and aggregated transactions matrix (T_agg) to obtain 'total output'
    # In the IO framework, total output is the sum of intermediary transactions and final demand
    
    tot_out = pd.concat([T_agg, Y_agg[["Y"]]], axis=1)
    tot_out.columns = ["regionName", "sector", "tot_int_demand", "Y"] 
    tot_out["tot_out"] = tot_out.loc[:, "tot_int_demand"] + tot_out.loc[:, "Y"]
        
    tot_inp = pd.concat([T_agg_col, V_agg[["V"]]], axis=1)
    tot_inp.columns = ["regionName", "sector", "tot_int_input", "V"] 
    tot_inp["tot_inp"] = tot_inp.loc[:, "tot_int_input"] + tot_inp.loc[:, "V"]

    #-----------------------------------------------------------------------------   
 
    # Emissions from Satellite accounts - EDGAR
    # !! need to check that accounts are loaded correctly because data for Italy is 0 for all sectors in 2021...

    ## select satellite indicator labels and corresponding rows in satellite matrix
    CO2emissionsSatIndicators = [x for x in labelsQ.Sat_indicator if "co2_excl" in x]
    
    TQ_co2 = TQ.loc[(TQ["Sat_indicator"].isin(CO2emissionsSatIndicators)) & (TQ["Sat_head_indicator"]=="Emissions (EDGAR)"), :]
    TQ_co2 = TQ_co2.drop(["Sat_head_indicator"], axis=1)
    
    # Selection of emissions sectors
    # this step is optional, use only if interested in a subset of emissions (e.g., IPCC: ENERGY)
#    emissions_sectors = []
#    Q_co2 = Q_co2.loc[Q_co2.stressor_source.isin(emissions_sectors), :]

    # Add IPCC category code column and format strings
    
    TQ_co2["ipcc_cat"] = TQ_co2.Sat_indicator.apply(lambda x: x.replace("co2_excl_short_cycle_org_c_", ""))
    TQ_co2["ipcc_cat"] = TQ_co2.ipcc_cat.apply(lambda x: x.replace("_EDGAR_consistent", ""))
   
    TQ_co2["ipcc_cat"] = TQ_co2["ipcc_cat"].apply(lambda x: x.upper())
    TQ_co2.drop(["Sat_indicator"], axis=1, inplace=True)

    # Transpose TQ matrix 
    TQ_co2.set_index("ipcc_cat", inplace=True)
    TQ_co2 = TQ_co2.transpose()
    TQ_co2.reset_index(inplace=True)
    TQ_co2.drop(["index", "TOTAL"], axis=1, inplace=True)

    # Emissions matrix needs to be kept disaggregated by ipcc sector because price applicable to emissions originating in each sector varies
    # That is, 'direct' emissions from one industry arise from several emissions sources. Emissions are priced at different levels
    # calculations of carbon price in country of origin need to account for that, at least if the calculation is made at the industry level and not the 'energy sector' level
    
    TQ_co2 = pd.concat([labelsT, TQ_co2], axis=1)

    TQ_co2 = TQ_co2.groupby(["regionName", "sector"]).sum()
    TQ_co2.reset_index(inplace=True)

    # 'Melt' dataframe to keep a single value (co2 emissions) column
    TQ_co2 = TQ_co2.melt(id_vars=["regionName", "sector"])
    TQ_co2.rename(columns={'value':'co2_emissions'}, inplace=True)

    # remove all unused files
    del TQ, YQ
    
    return TQ_co2, tot_out, tot_inp