
# ----------------------------------------------------------------------------
# Convert monetary values to constant USD

#gdp_defl = pd.read_csv("/Users/gd/OneDrive - rff/Documents/Research/projects/embedded_carbon_price/data/wb_deflator/wb_deflator.csv")
#gdp_defl.drop(['Country Code', 'Series Name'], axis=1, inplace=True)

#gdp_defl = gdp_defl.melt(id_vars=["Series Code", "Country Name"])
#gdp_defl = gdp_defl.loc[gdp_defl["Series Code"]=="NY.GDP.DEFL.KD.ZG", :]

#gdp_defl["variable"] = gdp_defl["variable"].apply(lambda x: x[:-9])
#gdp_defl.rename(columns={"variable":"Year"}, inplace=True)
#gdp_defl.drop(["Series Code", "Country Name"], axis=1, inplace=True)

#gdp_defl["Year"] = gdp_defl["Year"].astype(int)

#price_year = 2019

#for yr in gdp_defl.Year.unique():
#    x = 1
#    
#    for i in range(yr, price_year):
#        inflation = gdp_defl.loc[gdp_defl.Year==i, "value"].item()
#        x = x*(1+inflation/100)
    
#    gdp_defl.loc[gdp_defl.Year==yr, "cum_inf"] = x