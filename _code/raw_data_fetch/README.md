# EDGAR v8.0 → ADM1 annual sector inventories (Mexico/Japan/China)

This scaffold reconstructs **annual sector-specific GHG emissions inventories** at ADM1 level
using **EDGAR v8.0 GHG sector-specific gridmaps (0.1°)** and polygon boundaries (e.g., GADM).

Output format (long):
`country, iso3, adm1_code, adm1_name, year, sector_code, sector, gas, emissions, emissions_unit`

## 0) Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 1) Provide ADM1 boundaries

Put boundary files at the paths in `config/countries.yml`.
Recommended: **GADM** ADM1 as GeoPackage (or Shapefile). GADM downloads: https://gadm.org/download_country.html

Ensure the layer contains fields for ADM1 id and name (default in GADM: `GID_1`, `NAME_1`).

## 2) Choose sectors & gases

Edit `config/edgar_v80_manifest.csv`:
- `release` should remain `v80ghg`
- `gas`: typically `CO2`, `CH4`, `N2O`
- `sector_code`: EDGAR gallery sector code (e.g. `IND`, `RCO`, `TRO` …)
- `download_kind`: keep `emi_nc` unless you explicitly want fluxes

Sector codes are taken from the EDGAR v8.0 gallery (examples):
- `IND` (manufacturing combustion), `RCO` (buildings), `TRO` (road transport),
  `AGS` (agricultural soils), `WWT` (wastewater), `TOTALS` (all sectors), etc.

## 3) Run the full pipeline

```bash
bash run_pipeline.sh
```

This will:
1. Download EDGAR NetCDF ZIPs via the EDGAR gallery pages (sector-specific gridmaps)
2. Standardize ADM1 boundaries to EPSG:4326
3. Zonal-sum each annual gridmap to ADM1 polygons
4. Export a long-form inventory table to `data/output/` (under `EDGAR_DATA_ROOT`) as CSV + Parquet

## Data Root

By default, scripts write to:
`/Users/geoffroydolphin/GitHub/ECP/_raw/ghg_inventory/raw/subnational/jrc_edgar_gridded`

Override with:
`EDGAR_DATA_ROOT=/path/to/jrc_edgar_gridded`

## Notes & QA

- EDGAR gridmaps are provided as **annual emissions** and also as **fluxes**. This scaffold downloads `NETCDF emissions`.
- Units are stored from NetCDF metadata; you can add a unit conversion step if desired.
- Start small (e.g., 1 gas × 3 sectors × 1 country), then scale up / parallelize.
