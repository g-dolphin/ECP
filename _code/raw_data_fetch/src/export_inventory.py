import os
from pathlib import Path
import pandas as pd

# Map EDGAR sector codes to your preferred WCPD sector names (edit as needed)
SECTOR_MAP = {
    "TOTALS": "All sectors",
    "ENE": "Power",
    "IND": "Industry combustion",
    "RCO": "Buildings",
    "TRO": "Road transport",
    "TNR_Other": "Other transport",
    "AGS": "Agriculture",
    "WWT": "Wastewater",
    "SWD": "Solid waste",
    "CHE": "Chemical processes",
    "NMM": "Mineral processes",
    "PRU_SOL": "Solvents/products use",
    "NEU": "Non-energy use of fuels",
}

def export_pair(pair_dir: Path):
    df = pd.read_parquet(pair_dir / "adm1_inventory_long.parquet")
    df["sector_wcpd"] = df["sector_code"].map(SECTOR_MAP).fillna(df["sector"])

    out = df[
        [
            "country",
            "iso3",
            "adm1_code",
            "adm1_name",
            "year",
            "ipcc_category",
            "sector_wcpd",
            "sector_code",
            "gas",
            "emissions",
            "emissions_unit",
        ]
    ]
    out.to_parquet(pair_dir / "adm1_inventory_country_adm1_year_sector.parquet", index=False)
    out.to_csv(pair_dir / "adm1_inventory_country_adm1_year_sector.csv", index=False)


def main():
    data_root = Path(
        os.environ.get(
            "EDGAR_DATA_ROOT",
            "/Users/geoffroydolphin/GitHub/ECP/_raw/ghg_inventory/raw/subnational/jrc_edgar_gridded",
        )
    )
    base = data_root / "output" / "by_gas_sector"
    if not base.exists():
        raise SystemExit(f"Missing {base}; run aggregate_adm1 first.")

    pair_dirs = [p for p in base.glob("*/*") if (p / "adm1_inventory_long.parquet").exists()]
    if not pair_dirs:
        raise SystemExit(f"No per-pair outputs found under {base}.")

    for pair_dir in sorted(pair_dirs):
        export_pair(pair_dir)

if __name__ == "__main__":
    main()
