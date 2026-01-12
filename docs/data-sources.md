# Data sources

This project combines jurisdiction-level carbon pricing data with emissions inventories and macroeconomic conversion factors. The files in `_raw` are the local inputs used to build the compiled datasets.

## Pricing and coverage

- World Carbon Pricing Database (WCPD)
  - Local snapshots in `_raw/wcpd_usd` (prices) and `_raw/wcpd_cfWeightedPrices_usd` (coverage-weighted prices).
  - Original repository: https://github.com/gd1989/WorldCarbonPricingDatabase

## Emissions inventories

- National and subnational inventories, documented in `_raw/ghg_inventory`.
- Source list is captured in `_raw/ghg_inventory/ghg_data_sources_list.csv`.

## Exchange rates and deflators

- World Bank GDP deflators and exchange rates in `_raw/wb_rates`.
- BIS exchange rates in `_raw/wb_rates/xRate_bis.csv`.

## Mapping and concordances

- Harmonization resources in `_raw/_aux_files`.
- Includes ISO mappings, IPCC/IEA concordances, and inventory update files.

## External reference summary

- IEA CO2 emissions from fuel combustion (national sectoral emissions).
- CAIT / Climate Watch historical emissions.
- IPCC national inventory reports for subnational data.
- World Bank WDI for deflators and FX rates.

These sources feed the compilation utilities and notebooks in `_code/compilation` to produce ECP estimates.
