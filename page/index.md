<!-- =============================
     ABOUT
    ============================== -->

\begin{section}{title="About the data", name="About"}

This dataset contains information about the average economy-wide emission coverage and price tag associated with carbon pricing mechanisms around the world.
* The coverage data is average economy-wide coverage as a percentage of a jurisdiction's total greenhouse gas emissions.
* The price data is expressed in 2019 USD, using 2019 USD/LCU exchange rates.

We refer to the economy-wide average price as the Emissions-weighted Carbon Price (ECP).

Note that only mechanisms placing an explicit price on CO2 emissions are taken into account. This includes carbon taxes and emissions trading systems (cap-and-trade). Hence the information presented and underlying data do not reflect the pricing mechanisms that might apply to other greenhouse gases. A few existing mechanisms apply to non-CO2 greenhouse gases such as the EU ETS, which covers some N2O emissions and the Spanish 'carbon' tax, which covers fluorinated greenhouse gases (F-gases).

\end{section}

<!-- =============================
     GETTING STARTED
     ============================== -->
\begin{section}{title="Methodology", name="Methodology"}

These economy wide averages are based on sector(-fuel) level coverage and price data. This data is available and presented [here](https://gd1989.github.io/WorldCarbonPricingDatabase/).

The methodology and data used to calculate economy-wide averages is described in detail in [Dolphin, G., Pollitt, M. and D.M. Newbery (2020), The Political Economy of Carbon Pricing: a Panel Analysis](https://academic.oup.com/oep/article-abstract/72/2/472/5530742) as well as on the companion GitHub [repository](https://github.com/gd1989/ECP) to this page. The principle of it is, however, straightforward: it consists in (i) multiplying sector(-fuel) level CO2 emissions share (in a jurisdiction's total GHG emissions) by the associated total price tag and
(ii) aggregate over all sectors (and fuels).

In cases where emissions are subject to both a carbon tax and an emissions trading system, the total carbon price is the sum of the tax rate and (the yearly average of) the allowance price .

\end{section}


\begin{section}{title="The ECP", name="ECP"}

\figure{path="/assets/coverageTS.png", caption="Carbon pricing coverage, 1990-2016"}

\figure{path="/assets/coverageHIST.png", caption="Coverage distribution, 2016"}

\figure{path="/assets/ecpTS.png", caption="Total (emissions-weighted) carbon price, 1990-2018"}



\end{section}
