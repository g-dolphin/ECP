# Emissions-weighted Carbon Price
 
The Emissions-weighted Carbon Price (ECP) is an economy-wide average price on CO2 emissions. It is calculated from sector-fuel level data, which is aggregated back to the economy level using the share of each sector-fuel CO2 emissions in total GHG emissions as weights. The full methodology is described in [Dolphin, G., Pollitt, M. and D.M. Newbery (2020), The Political Economy of Carbon Pricing: a Panel Analysis](https://academic.oup.com/oep/article-abstract/72/2/472/5530742).

It is currently calculated for [123] national jurisdictions and 63 (North American) sub-national jurisdictions over the period 1990-2018.

Its calculation requires the combination of information about:
 1. Carbon pricing mechanisms' coverage
 2. Carbon pricing mechanisms' associated price
 3. CO2 emissions from the covered sectors and total GHG emissions

Information about 1. and 2. have been collected as part of a project developed within the Energy Policy Research Group at the University of Cambridge. The full dataset is available [here](https://github.com/gd1989/WorldCarbonPricingDatabase). CO2 and GHG emissions data come from various sources. For national jurisdictions, the main sources are the [International Energy Agency's CO2 Emissions from Fuel Combustion](https://www.iea.org/reports/co2-emissions-from-fuel-combustion-overview) and the CAIT Country Greenhouse Gas Emissions Data (1990-2016) available on the [Climate Watch platform](https://www.climatewatchdata.org/ghg-emissions). For subnational jurisdictions, information is taken from their respective IPCC GHG Inventories.

Note: The ECP currently does not account for coverage (exemptions) *within* sectors. For instance, it currently does not account for sector-specific exemptions in the tax base or the exclusion of some emissions plants below rated power threshold levels in ETSs. As a result, the ECP is, in some cases, a slight overestimate of the average carbon price in a sector or an economy.
  - The best approach I could think of so far (but not yet implemented) is to collect information on these 'within-sector’ tax base exemptions, estimate the percentage of sector-level emissions that they affect, and use it to introduce an adjustment in the calculation of the sector-level prices.
  - [tesssssst]
