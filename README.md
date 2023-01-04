# Emissions-weighted Carbon Price
 
## Jurisdiction average

The Emissions-weighted Carbon Price (ECP) is an economy-wide average price on CO2 emissions. It is calculated from sector-fuel level data, which is aggregated back to the economy level using the share of each sector-fuel CO2 emissions in total GHG emissions as weights. The full methodology is described in the Resources for the Future Working Paper 22-6 [Emissions-weighted carbon price: Sources and Methods](https://www.rff.org/publications/working-papers/emissions-weighted-carbon-price-sources-and-methods/).

It is calculated for 46 national and 31 subnational jurisdictions (13 Canadian provinces and territories, 11 US states, and 7 Chinese provinces) over 1990–2020. The average World CO2 price is also calculated. For national jurisdictions, the emissions-weighted price accounts for the prices arising from carbon pricing instruments introduced in their respective subnational jurisdictions. For instance, the emissions-weighted price for the United States includes the prices arising from state-level carbon pricing mechanisms.

Its calculation requires the combination of information about:
 1. Carbon pricing mechanisms' coverage
 2. Carbon pricing mechanisms' associated price
 3. CO2 emissions from the covered sectors and total GHG emissions

Information about 1. and 2. have been collected as part of a project developed within the Energy Policy Research Group at the University of Cambridge. The full dataset is available [here](https://github.com/gd1989/WorldCarbonPricingDatabase). In cases where emissions are subject to both a carbon tax and an emissions trading system, the total carbon price is the sum of the tax rate and (the yearly average of) the allowance price. All prices in this repository are expressed in 2021USD/tCO2. The conversion from current local currency units (LCU) uses the 2019 LCU/USD x-rate and the cumulative rates of inflation (based on the GDP deflator of each jurisdiction). Both are obtained or calculated from [the World Bank](https://databank.worldbank.org/reports.aspx?source=World-Development-Indicators).

The coverage is expressed as a share of each jurisdiction's total CO2 emissions (excluding Land Use and Land Use Change and Forestry) in any given year. These  figures are based on CO2 emissions data from various sources. For national jurisdictions, the main sources are the [International Energy Agency's CO2 Emissions from Fuel Combustion](https://www.iea.org/reports/co2-emissions-from-fuel-combustion-overview) and the CAIT Country Greenhouse Gas Emissions Data (1990-2018) available on the [Climate Watch platform](https://www.climatewatchdata.org/ghg-emissions). For subnational jurisdictions, information is taken from their respective IPCC GHG Inventories.

## Sector average

Next to the jurisdiction-level average price, I also calculate sector-level averages for IPCC Energy sectors using IEA CO2 emissions data.

# Citation

If you use the dataset in scientific publication, we would appreciate a reference to the following paper:

Dolphin, G., Pollitt, M. and Newbery, D. 2020. The political economy of carbon pricing: a panel analysis. Oxford Economic Papers 72(2): 472-500.

# License

This work is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/)

