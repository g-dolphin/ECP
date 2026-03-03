import argparse
import io
import os
import re
import zipfile
from pathlib import Path

import pandas as pd
import xarray as xr


GAS_RE = re.compile(r"_GHG_([A-Z0-9-]+)_", re.IGNORECASE)
SECTOR_RE_ZIP = re.compile(r"^([^_]+)_emi_", re.IGNORECASE)
GAS_DIRS = {"CO2", "CH4", "N2O", "CO2BIO"}


def infer_gas(nc_names: list[str]) -> str:
    gases = set()
    for name in nc_names:
        m = GAS_RE.search(name)
        if m:
            gases.add(m.group(1).upper())
    if not gases:
        raise RuntimeError("Could not infer gas from NetCDF names")
    if len(gases) > 1:
        raise RuntimeError(f"Multiple gases found in one ZIP: {sorted(gases)}")
    return next(iter(gases))


def sector_from_nc_name(name: str) -> str | None:
    stem = Path(name).name
    if stem.lower().endswith(".nc"):
        stem = stem[:-3]
    parts = stem.split("_")
    if len(parts) < 2:
        return None
    # Expect ..._<SECTOR>_emi
    if parts[-1].lower() == "emi":
        return parts[-2].upper()
    return None


def infer_sector(zip_name: str, nc_names: list[str]) -> str:
    m = SECTOR_RE_ZIP.search(zip_name)
    if m:
        return m.group(1).upper()
    sectors = set()
    for name in nc_names:
        s = sector_from_nc_name(name)
        if s:
            sectors.add(s)
    if not sectors:
        raise RuntimeError("Could not infer sector from ZIP or NetCDF names")
    if len(sectors) > 1:
        raise RuntimeError(f"Multiple sectors found in one ZIP: {sorted(sectors)}")
    return next(iter(sectors))


def sector_meta_from_nc(nc_path: Path) -> dict:
    try:
        ds = xr.open_dataset(nc_path, decode_times=False)
        for v in ds.data_vars:
            attrs = ds[v].attrs
            long_name = attrs.get("long_name")
            description = attrs.get("description")
            title = attrs.get("title")
            standard_name = attrs.get("standard_name")
            return {
                "nc_long_name": long_name.strip() if isinstance(long_name, str) else None,
                "nc_description": description.strip() if isinstance(description, str) else None,
                "nc_title": title.strip() if isinstance(title, str) else None,
                "nc_standard_name": standard_name.strip() if isinstance(standard_name, str) else None,
            }
    finally:
        try:
            ds.close()
        except Exception:
            pass
    return {
        "nc_long_name": None,
        "nc_description": None,
        "nc_title": None,
        "nc_standard_name": None,
    }


def iter_ipcc_dirs(root: Path) -> list[Path]:
    ipcc_dirs = []
    for p in sorted(root.iterdir()):
        if not p.is_dir():
            continue
        if p.name in GAS_DIRS:
            continue
        if list(p.glob("*.zip")):
            ipcc_dirs.append(p)
    return ipcc_dirs


def process_zip(
    zip_name: str,
    zf: zipfile.ZipFile,
    release: str,
    out_base: Path,
    dry_run: bool,
    out_rows: list[dict],
    ipcc_category: str | None,
):
    nc_names = [n for n in zf.namelist() if n.lower().endswith(".nc")]
    if nc_names:
        gas = infer_gas(nc_names)
        sector = infer_sector(zip_name, nc_names)

        out_dir = out_base / release / gas / sector / "netcdf"
        out_dir.mkdir(parents=True, exist_ok=True)

        if not dry_run:
            for name in nc_names:
                out_path = out_dir / Path(name).name
                if out_path.exists():
                    continue
                with zf.open(name) as src, open(out_path, "wb") as dst:
                    dst.write(src.read())

        out_rows.append(
            {
                "zip": zip_name,
                "gas": gas,
                "sector_code": sector,
                "nc_files": len(nc_names),
                "out_dir": str(out_dir),
                "ipcc_category": ipcc_category,
            }
        )
        return

    nested = [n for n in zf.namelist() if n.lower().endswith(".zip")]
    if nested:
        for name in nested:
            with zf.open(name) as src:
                data = src.read()
            with zipfile.ZipFile(io.BytesIO(data), "r") as inner:
                process_zip(
                    Path(name).name,
                    inner,
                    release,
                    out_base,
                    dry_run,
                    out_rows,
                    ipcc_category,
                )
        return

    print(f"Warning: no .nc or nested .zip files in {zip_name}")


def process_ipcc_dir(ipcc_dir: Path, release: str, out_base: Path, dry_run: bool) -> list[dict]:
    out_rows: list[dict] = []
    for zip_path in sorted(ipcc_dir.glob("*.zip")):
        with zipfile.ZipFile(zip_path, "r") as zf:
            process_zip(
                zip_path.name,
                zf,
                release,
                out_base,
                dry_run,
                out_rows,
                ipcc_dir.name,
            )
    return out_rows


def build_manifest(rows: list[dict], release: str, out_path: Path | None, out_base: Path) -> pd.DataFrame:
    pairs = {}
    for r in rows:
        key = (r["gas"], r["sector_code"])
        if key in pairs:
            continue
        # infer sector label from one extracted NC file
        nc_dir = Path(r["out_dir"])
        label = None
        meta = {
            "nc_long_name": None,
            "nc_description": None,
            "nc_title": None,
            "nc_standard_name": None,
        }
        if nc_dir.exists():
            nc_files = sorted(nc_dir.glob("*.nc"))
            if nc_files:
                meta = sector_meta_from_nc(nc_files[0])
                label = meta.get("nc_long_name") or meta.get("nc_description")
        pairs[key] = {
            "sector_label": label or r["sector_code"],
            "ipcc_category": r.get("ipcc_category"),
            **meta,
        }

    manifest = pd.DataFrame(
        [
            {
                "release": release,
                "gas": gas,
                "sector_code": sector,
                "sector_label": meta["sector_label"],
                "ipcc_category": meta.get("ipcc_category"),
                "nc_long_name": meta.get("nc_long_name"),
                "nc_description": meta.get("nc_description"),
                "nc_title": meta.get("nc_title"),
                "nc_standard_name": meta.get("nc_standard_name"),
                "download_kind": "emi_nc",
            }
            for (gas, sector), meta in sorted(pairs.items())
        ]
    )

    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        manifest.to_csv(out_path, index=False)

    return manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ipcc-dir", help="Path to IPCC category folder with ZIPs")
    ap.add_argument("--root", help="Root folder with IPCC category subfolders")
    ap.add_argument("--release", default="v80ghg")
    ap.add_argument("--out-base")
    ap.add_argument("--manifest-out", default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    data_root = Path(
        os.environ.get("EDGAR_DATA_ROOT", "/Users/geoffroydolphin/GitHub/ECP/_raw/ghg_inventory/edgar")
    )
    out_base = Path(args.out_base) if args.out_base else (data_root / "raw" / "edgar")
    if args.root is None and args.ipcc_dir is None:
        args.root = str(data_root / "raw" / "edgar")

    if bool(args.ipcc_dir) == bool(args.root):
        raise SystemExit("Provide exactly one of --ipcc-dir or --root.")

    rows = []
    if args.ipcc_dir:
        ipcc_dir = Path(args.ipcc_dir)
        if not ipcc_dir.exists():
            raise FileNotFoundError(ipcc_dir)
        rows.extend(process_ipcc_dir(ipcc_dir, args.release, out_base, args.dry_run))
    else:
        root = Path(args.root)
        if not root.exists():
            raise FileNotFoundError(root)
        for ipcc_dir in iter_ipcc_dirs(root):
            rows.extend(process_ipcc_dir(ipcc_dir, args.release, out_base, args.dry_run))

    summary = pd.DataFrame(rows)
    if summary.empty:
        print("No ZIP files found.")
    else:
        print(summary.to_string(index=False))

    if args.manifest_out:
        manifest = build_manifest(rows, args.release, Path(args.manifest_out), out_base)
        print(f"Wrote manifest: {args.manifest_out} ({len(manifest)} rows)")


if __name__ == "__main__":
    main()
