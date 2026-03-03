import os
import re
import zipfile
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

GALLERY_URL = "https://edgar.jrc.ec.europa.eu/gallery"
DATA_ROOT = Path(
    os.environ.get("EDGAR_DATA_ROOT", "/Users/geoffroydolphin/GitHub/ECP/_raw/ghg_inventory/edgar")
)

def find_netcdf_zip_url(release: str, gas: str, sector: str, download_kind: str = "emi_nc") -> str:
    params = {"release": release, "sector": sector, "substance": gas}
    r = requests.get(GALLERY_URL, params=params, timeout=60)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")

    zip_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.lower().endswith(".zip"):
            if href.startswith("/"):
                href = "https://edgar.jrc.ec.europa.eu" + href
            zip_links.append(href)

    # Prefer links that match <sector>_<download_kind>.zip
    pat = re.compile(rf"{re.escape(sector)}.*{re.escape(download_kind)}.*\.zip", re.IGNORECASE)
    for link in zip_links:
        if pat.search(link):
            return link

    if zip_links:
        return zip_links[0]
    raise RuntimeError(f"No ZIP download found for release={release} gas={gas} sector={sector}")

def download_file(url: str, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(out_path, "wb") as f, tqdm(total=total, unit="B", unit_scale=True, desc=out_path.name) as pbar:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))

def unzip(zip_path: Path, extract_dir: Path):
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_dir)

def main():
    manifest = pd.read_csv("config/edgar_v80_manifest.csv")
    base = DATA_ROOT / "raw" / "edgar"

    for _, row in manifest.iterrows():
        release = row["release"]
        gas = row["gas"]
        sector = row["sector_code"]
        kind = row.get("download_kind", "emi_nc")

        url = find_netcdf_zip_url(release, gas, sector, kind)

        out_dir = base / release / gas / sector
        zip_path = out_dir / f"{sector}_{kind}.zip"
        nc_dir = out_dir / "netcdf"

        if not zip_path.exists():
            download_file(url, zip_path)

        if not any(nc_dir.glob("*.nc")):
            unzip(zip_path, nc_dir)

if __name__ == "__main__":
    main()
