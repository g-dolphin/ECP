# Data pipeline

This repository builds the ECP dataset from raw pricing, emissions, and macroeconomic data, then produces figures and reports. The core flow is:

- Raw inputs live in `_raw`.
- Compilation scripts in `_code/compilation` harmonize prices, coverage, and emissions.
- Final datasets are written to `_output/_dataset`.
- Reporting scripts in `_code/reporting` generate charts and reports in `_output/_figures`, `_output/_tables`, and `_output/_reports`.

## Mermaid overview

<div class="mermaid">
flowchart LR
  subgraph "Raw Inputs"
    WCPD["_raw/wcpd_usd - World Carbon Pricing Database"]
    WCPD_CF["_raw/wcpd_cfWeightedPrices_usd - coverage-weighted prices"]
    WB["_raw/wb_rates - World Bank and BIS rates"]
    INV["_raw/ghg_inventory - inventory sources and GWP"]
    AUX["_raw/_aux_files - mapping and concordances"]
  end

  subgraph "Compilation"
    UTIL["_code/compilation/_utils/dep_ecp - Python utilities"]
    IPCC["_code/compilation/ecp/ipcc - notebooks"]
    IND["_code/compilation/ecp/industry - R pipeline"]
    CCOST["_code/compilation/ccost - carbon cost scripts"]
  end

  subgraph "Outputs"
    ECP[_output/_dataset/ecp]
    COV[_output/_dataset/coverage]
    CC[_output/_dataset/carbonCost]
  end

  subgraph "Reporting"
    CHARTS[_code/reporting/charts]
    REPORTS["_code/reporting/reports - Quarto"]
    FIGS[_output/_figures]
    TABLES[_output/_tables]
    PDFHTML[_output/_reports]
  end

  WCPD --> UTIL
  WCPD_CF --> UTIL
  WB --> UTIL
  INV --> UTIL
  AUX --> UTIL

  UTIL --> IPCC
  UTIL --> IND
  UTIL --> CCOST

  IPCC --> ECP
  IND --> ECP
  UTIL --> COV
  CCOST --> CC

  ECP --> CHARTS
  COV --> CHARTS
  CC --> CHARTS
  CHARTS --> FIGS
  CHARTS --> TABLES
  REPORTS --> PDFHTML
  FIGS --> REPORTS
  TABLES --> REPORTS
</div>

## Compilation highlights

- `dep_ecp` in `_code/compilation/_utils` hosts shared Python utilities for coverage factors, currency conversion, inventory processing, and weighted averages.
- IPCC notebooks in `_code/compilation/ecp/ipcc` generate national and sector ECP calculations from harmonized inputs.
- Industry-level processing in `_code/compilation/ecp/industry` uses R scripts to import, match, and check sectoral concordances.

## Reporting highlights

- `generate_charts.py` orchestrates chart builds from the datasets in `_output/_dataset`.
- `report.qmd` assembles figures and tables into HTML/PDF deliverables via Quarto.
