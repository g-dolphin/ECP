import os
from pathlib import Path
import yaml
import geopandas as gpd

DATA_ROOT = Path(
    os.environ.get("EDGAR_DATA_ROOT", "/Users/geoffroydolphin/GitHub/ECP/_raw/ghg_inventory/edgar")
)

def main():
    cfg = yaml.safe_load(open("config/countries.yml", "r", encoding="utf-8"))
    out_dir = DATA_ROOT / "interim" / "boundaries"
    out_dir.mkdir(parents=True, exist_ok=True)

    for iso3, meta in cfg["countries"].items():
        path = Path(meta["boundary_path"])
        if not path.is_absolute():
            path = DATA_ROOT / path
        gdf = gpd.read_file(path).to_crs(4326)

        adm1_id = meta["adm1_id_field"]
        adm1_name = meta["adm1_name_field"]

        keep = gdf[[adm1_id, adm1_name, "geometry"]].copy()
        keep = keep.rename(columns={adm1_id: "adm1_code", adm1_name: "adm1_name"})
        keep["iso3"] = iso3

        keep.to_file(out_dir / f"adm1_{iso3}.gpkg", layer="adm1", driver="GPKG")

if __name__ == "__main__":
    main()
