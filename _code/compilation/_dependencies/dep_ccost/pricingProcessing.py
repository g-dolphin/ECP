import pandas as pd
import numpy as np

cpricesGLORIApath = "/Users/gd/GitLab/spc/econometrics"

# ----------------------------- MATCHING EMISSIONS WITH PRICES ---------------

# Load carbon price data and select year subsample
# Use matched and re-weighted price data from pricing incidence project
# co2 price is expressed in 2021USD/tCO2

def carbonPrices(year):

    # in case analysis extends beyond last year of carbon pricing dataset
    if year > 2021:
        year_cp = 2021
    else:
        year_cp = year    

    cpricesGLORIA = pd.read_csv(cpricesGLORIApath+"/spc_data.csv")
    cpricesGLORIA = cpricesGLORIA[['country', 'sector', 'year', 'carbon_price']]

    # creating binary variable encoding whether or not a positive price exists for the sector
    cpricesGLORIA["pricing"] = np.nan
    cpricesGLORIA.loc[cpricesGLORIA['carbon_price']>0, "pricing"] = 1

    cpricesGLORIA = cpricesGLORIA.loc[cpricesGLORIA.year==year_cp]

    cpricesGLORIA["country"] = cpricesGLORIA["country"].apply(lambda x: x.replace(".", " "))
    # need to create region aggregate prices that correspond to GLORIA regions

    return cpricesGLORIA