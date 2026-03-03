import numpy as np
import pandas as pd
import xarray as xr

def pick_data_var(ds: xr.Dataset) -> str:
    """Pick first numeric data variable."""
    for v in ds.data_vars:
        if np.issubdtype(ds[v].dtype, np.number):
            return v
    raise RuntimeError("No numeric data variable found in dataset")

def normalize_lon(ds: xr.Dataset) -> xr.Dataset:
    """Convert 0..360 longitudes to -180..180 if needed."""
    if "lon" in ds.coords:
        lon = ds["lon"].values
        if np.nanmin(lon) >= 0 and np.nanmax(lon) > 180:
            ds = ds.assign_coords(lon=(((ds["lon"] + 180) % 360) - 180)).sortby("lon")
    return ds

def years_in_dataset(ds: xr.Dataset) -> list[int]:
    if "time" not in ds.dims:
        return []
    t = pd.to_datetime(ds["time"].values)
    return sorted(set(t.year.tolist()))

def slice_year(ds: xr.Dataset, var: str, year: int) -> xr.DataArray:
    if "time" not in ds.dims:
        return ds[var]
    t = pd.to_datetime(ds["time"].values)
    idx = np.where(t.year == year)[0]
    if len(idx) != 1:
        raise RuntimeError(f"Year {year} not uniquely found in time dimension")
    return ds[var].isel(time=int(idx[0]))
