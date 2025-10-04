# Emissions-weighted Carbon Price

The present dataset constitutes an extension of a dataset initially developed while pursuing my PhD within the Energy Policy Research Group at the University of Cambridge. Its existence owes much to its support as well as that of the Cambridge Judge Business School and the UK Economic and Social Research Council. Its most recent updates are supported by Resources for the Future.

The Emissions-weighted Carbon Price (ECP) is an economy-wide average price on CO2 emissions. It is calculated from sector-fuel level data, which is aggregated back to the economy level using the share of each sector-fuel CO2 emissions in total GHG emissions as weights. The full methodology is described in [Dolphin and Merkle (2025)](https://www.nature.com/articles/s41597-024-03121-6)

If this dataset has been useful to you or simply think it's cool, feel free to give it a ⭐!

## Jurisdiction average

It is calculated for 198 national and 75 subnational jurisdictions (13 Canadian provinces and territories, 50 US states, and 22 Chinese provinces) over 1990–2024. The average World CO2 price is also calculated. For national jurisdictions, the emissions-weighted price accounts for the prices arising from carbon pricing instruments introduced in their respective subnational jurisdictions. For instance, the emissions-weighted price for the United States includes the prices arising from state-level carbon pricing mechanisms.

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

[Dolphin, G., Merkle, M. (2024). Emissions-weighted Carbon Price: Source and Methods. Scientific Data.](https://www.nature.com/articles/s41597-024-03121-6)

# License

This work is licensed under a [Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/) license. "Work" in the above sentence refers to all material available on this repository.

