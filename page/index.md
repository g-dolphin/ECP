<!-- =============================
     ABOUT
    ============================== -->

\begin{section}{title="About the data", name="About"}

This dataset contains information about the average economy-wide emission coverage and price tag associated with carbon pricing mechanisms around the world.
* The coverage data is average economy-wide coverage as a percentage of a jurisdiction's total greenhouse gas emissions.
* The price data is expressed in 2019 USD, using 2019 USD/LCU exchange rates.

We refer to the economy-wide average price as the Emissions-weighted Carbon Price (ECP).

Note that only mechanisms placing an explicit price on CO2 emissions are taken into account. This includes carbon taxes and emissions trading systems (cap-and-trade). Hence the information presented and underlying data do not reflect the pricing mechanisms that might apply to other greenhouse gases. A few existing mechanisms apply to non-CO2 greenhouse gases such as the EU ETS, which covers some N2O emissions and the Spanish 'carbon' tax, which covers fluorinated greenhouse gases (F-gases).

It also (currently) does not include offset mechanisms such as Australia's ERF Safeguard Mechanism.

This, together with the fact that our dataset does not yet account for China's provincial ETSs, implies that the `World` coverage and average carbon price figures reported here might be lower than those reported elsewhere (e.g. on the [World Bank Carbon Pricing Dashboard](https://carbonpricingdashboard.worldbank.org/)). Note also that the exchange rate (USD/Local Currency Unit) affects the USD values calculated and reported below. The exchange rates currently used are 2019 exchange rates from the World Bank.  

\end{section}

<!-- =============================
     GETTING STARTED
     ============================== -->
\begin{section}{title="Methodology", name="Methodology"}

These economy wide averages are based on sector(-fuel) level coverage and price data. This data is available and presented [here](https://gd1989.github.io/WorldCarbonPricingDatabase/).

The methodology and data used to calculate economy-wide averages is described in detail in [Dolphin, G., Pollitt, M. and D.M. Newbery (2020), The Political Economy of Carbon Pricing: a Panel Analysis](https://academic.oup.com/oep/article-abstract/72/2/472/5530742) as well as on the companion GitHub [repository](https://github.com/gd1989/ECP) to this page. The principle of it is, however, straightforward: it consists in (i) multiplying sector(-fuel) level CO2 emissions share (in a jurisdiction's total GHG emissions) by the associated total price tag and (ii) aggregate over all sectors (and fuels).

In cases where emissions are subject to both a carbon tax and an emissions trading system, the total carbon price is the sum of the tax rate and (the yearly average of) the allowance price.

The coverage figures are based on CO2 emissions data from the International
Energy Agency and GHG emissions data from Climate Watch (CAIT Climate Data Explorer series).

\end{section}


\begin{section}{title="Country-level coverage and average carbon price", name="ECP"}

Carbon pricing mechanisms around the world vary in scope. Some have a very narrow
scope and target a single sector (e.g. electricity and heat production) or multiple
sectors. The figure below presents coverage data for a number of selected jurisdictions
over the period 1990-2017; 2017 is the last year for which the CAIT series are currently
available.

The coverage is expressed as a share of each jurisdiction's total GHG emissions (excluding Land Use and Land Use Change and Forestry) in any given year.


\figure{path="/assets/coverage_ts.png", caption="Carbon pricing coverage, 1990-2017", width="70%", style="border-radius:5px"}

The country-level average carbon price, in 2019USD/tCO2, is presented below. While some countries subject a large share of their domestic GHG emissions to a (at times substantial) price, their emissions represent a relatively small proportion of global (world) emissions. As a result, the `World` average price of carbon remains low.

\figure{path="/assets/ecp_ts.png", caption="Total (emissions-weighted) carbon price, 1990-2018", width="70%", style="border-radius:5px"}

\end{section}
