from pathlib import Path
import os
import re

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
import yaml
from exactextract import exact_extract

from src.utils import pick_data_var, normalize_lon, years_in_dataset, slice_year

def load_edgar_ipcc_map(map_path: Path) -> dict[str, str]:
    df = pd.read_csv(map_path)
    df.columns = [c.lstrip("\ufeff").strip() for c in df.columns]
    edgar_col = "edgar_id"
    ipcc_col = "ipcc_code"
    if edgar_col not in df.columns or ipcc_col not in df.columns:
        raise ValueError(f"Expected columns {edgar_col} and {ipcc_col} in {map_path}")
    return {
        str(k).strip(): str(v).strip()
        for k, v in zip(df[edgar_col], df[ipcc_col])
        if pd.notna(k) and pd.notna(v)
    }

def exact_zonal_sum(da: xr.DataArray, polygons: gpd.GeoDataFrame) -> np.ndarray:
    import rioxarray  # noqa: F401

    # EDGAR typically uses (lat, lon)
    if set(da.dims) >= {"lat", "lon"}:
        da2 = da.rename({"lat": "y", "lon": "x"})
    else:
        da2 = da

    da2 = da2.rio.write_crs(4326, inplace=False)

    stats = exact_extract(da2, polygons, ["sum"])
    # exactextract returns GeoJSON-like features with properties
    return np.array([s.get("properties", {}).get("sum", np.nan) for s in stats], dtype=float)

def infer_year_from_filename(name: str) -> list[int]:
    ys = re.findall(r"(19\d{2}|20\d{2})", name)
    return [int(ys[-1])] if ys else []

def main():
    min_year = int(os.environ.get("EDGAR_MIN_YEAR", "2010"))
    data_root = Path(
        os.environ.get(
            "EDGAR_DATA_ROOT",
            "/Users/geoffroydolphin/GitHub/ECP/_raw/ghg_inventory/raw/subnational/jrc_edgar_gridded",
        )
    )
    manifest = pd.read_csv("config/edgar_v80_manifest.csv")
    ipcc_map_path = Path(
        os.environ.get("EDGAR_IPCC_MAP", "/Users/geoffroydolphin/GitHub/ECP/_raw/_aux_files/edgar_ipcc_map.csv")
    )
    if ipcc_map_path.exists():
        ipcc_map = load_edgar_ipcc_map(ipcc_map_path)
        manifest["ipcc_category"] = (
            manifest["sector_code"].map(ipcc_map).fillna(manifest.get("ipcc_category"))
        )
    cfg = yaml.safe_load(open("config/countries.yml", "r", encoding="utf-8"))

    boundaries_dir = data_root / "interim" / "boundaries"
    base = data_root / "raw" / "edgar"

    # Load boundaries
    adm1 = {}
    for iso3, meta in cfg["countries"].items():
        gdf = gpd.read_file(boundaries_dir / f"adm1_{iso3}.gpkg", layer="adm1")
        adm1[iso3] = gdf

    out_base = data_root / "output" / "by_gas_sector"
    out_base.mkdir(parents=True, exist_ok=True)

    for _, m in manifest.iterrows():
        release = m["release"]
        gas = m["gas"]
        sector = m["sector_code"]
        sector_label = m.get("sector_label", sector)
        ipcc_category = m.get("ipcc_category", None)

        nc_dir = base / release / gas / sector / "netcdf"
        nc_files = sorted(nc_dir.glob("*.nc"))
        if not nc_files:
            raise FileNotFoundError(f"No .nc files found in {nc_dir}")

        processed_years: set[int] = set()
        out_rows = []

        for nc_path in nc_files:
            ds = xr.open_dataset(nc_path, decode_times=True)
            ds = normalize_lon(ds)
            var = pick_data_var(ds)

            years = years_in_dataset(ds)
            if not years:
                years = infer_year_from_filename(nc_path.name)

            if not years:
                ds.close()
                raise RuntimeError(f"Could not infer years for {nc_path}")

            unit = ds[var].attrs.get("units", "unknown")

            for year in years:
                if int(year) < min_year:
                    continue
                if int(year) in processed_years:
                    continue
                da = slice_year(ds, var, year)

                for iso3, meta in cfg["countries"].items():
                    gdf = adm1[iso3]
                    sums = exact_zonal_sum(da, gdf)

                    gdf2 = gdf.reset_index(drop=True)
                    for i, row in gdf2.iterrows():
                        out_rows.append({
                            "iso3": iso3,
                            "country": meta["name"],
                            "adm1_code": row["adm1_code"],
                            "adm1_name": row["adm1_name"],
                            "year": int(year),
                            "ipcc_category": ipcc_category,
                            "sector_code": sector,
                            "sector": sector_label,
                            "gas": gas,
                            "emissions": float(sums[i]),
                            "emissions_unit": unit,
                        })

                processed_years.add(int(year))

            ds.close()

        # write per gas-sector pair to keep outputs small
        if out_rows:
            out_df = pd.DataFrame(out_rows)
            pair_dir = out_base / gas / sector
            pair_dir.mkdir(parents=True, exist_ok=True)
            out_df.to_parquet(pair_dir / "adm1_inventory_long.parquet", index=False)
            out_df.to_csv(pair_dir / "adm1_inventory_long.csv", index=False)
    # no single combined output here; outputs are written per gas-sector pair

if __name__ == "__main__":
    main()
