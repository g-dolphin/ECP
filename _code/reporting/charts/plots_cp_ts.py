from __future__ import annotations

from pathlib import Path
from typing import Dict, Mapping, Optional, Sequence, Union

import matplotlib.pyplot as plt
import pandas as pd

PathLike = Union[str, Path]


def _save_ts_figure_and_data(
    df_long: pd.DataFrame,
    group_col: str,
    year_col: str,
    value_col: str,
    output_plot_path: Optional[PathLike],
    output_data_path: Optional[PathLike],
    title: str,
) -> pd.DataFrame:
    """Internal helper to plot time series and save figure + data."""
    fig, ax = plt.subplots(figsize=(11, 6))

    for label, sub in df_long.groupby(group_col):
        sub = sub.sort_values(year_col)
        ax.plot(
            sub[year_col],
            sub[value_col],
            label=str(label),
            linewidth=2,
        )

    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("Carbon price (USD/tCO₂)", fontsize=11)
    ax.set_title(title, fontsize=13, weight="bold")

    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), borderaxespad=0.0)
    ax.grid(True, linestyle=":", alpha=0.4)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    if output_plot_path is not None:
        output_plot_path = Path(output_plot_path)
        output_plot_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_plot_path, dpi=300, bbox_inches="tight")

    plt.close(fig)

    if output_data_path is not None:
        output_data_path = Path(output_data_path)
        output_data_path.parent.mkdir(parents=True, exist_ok=True)
        df_long.to_csv(output_data_path, index=False)

    return df_long


def plot_cp_ts_jurisdictions(
    df: pd.DataFrame,
    jurisdictions: Sequence[str],
    year_col: str = "year",
    jurisdiction_col: str = "jurisdiction",
    value_col: str = "ecp_all_jurCO2_usd_k",
    output_plot_path: Optional[PathLike] = None,
    output_data_path: Optional[PathLike] = None,
    title: Optional[str] = None,
) -> pd.DataFrame:
    """
    Plot time series of carbon prices for selected jurisdictions.

    Parameters
    ----------
    df : DataFrame
        Input ECP dataset at the jurisdiction level.
    jurisdictions : sequence of str
        Jurisdictions to plot.
    year_col : str
        Column name for year.
    jurisdiction_col : str
        Column for jurisdiction names.
    value_col : str
        Column for price (USD/tCO₂).
    output_plot_path : str or Path, optional
        PNG/PDF path for the figure.
    output_data_path : str or Path, optional
        CSV path for underlying data.
    title : str, optional
        Figure title; if None, a default is constructed.

    Returns
    -------
    DataFrame
        Long-format data actually plotted, with columns
        [year_col, jurisdiction_col, value_col].
    """
    df_plot = df[df[jurisdiction_col].isin(jurisdictions)].copy()
    df_plot = df_plot[[year_col, jurisdiction_col, value_col]].dropna()

    if title is None:
        title = "Carbon price time series – selected jurisdictions"

    return _save_ts_figure_and_data(
        df_long=df_plot,
        group_col=jurisdiction_col,
        year_col=year_col,
        value_col=value_col,
        output_plot_path=output_plot_path,
        output_data_path=output_data_path,
        title=title,
    )


def plot_cp_ts_world_sectors(
    df_world_sec: pd.DataFrame,
    sector_map: Mapping[str, str],
    year_col: str = "year",
    sector_col: str = "ipcc_code",
    value_col: str = "ecp_world_ipcc_CO2_usd_k",
    output_plot_path: Optional[PathLike] = None,
    output_data_path: Optional[PathLike] = None,
    title: Optional[str] = None,
) -> pd.DataFrame:
    """
    Plot time series of world average carbon prices by sector.

    Parameters
    ----------
    df_world_sec : DataFrame
        World-sector data with columns [year_col, sector_col, value_col].
    sector_map : dict
        Mapping from IPCC code (sector_col) to human-readable sector name.
    year_col : str
        Column for year.
    sector_col : str
        Column for sector code.
    value_col : str
        Column for price (USD/tCO₂).
    output_plot_path : str or Path, optional
        PNG/PDF path for the figure.
    output_data_path : str or Path, optional
        CSV path for underlying data.
    title : str, optional
        Figure title; if None, a default is constructed.

    Returns
    -------
    DataFrame
        Long-format data actually plotted, with columns
        [year_col, "sector", value_col].
    """
    df_plot = df_world_sec[df_world_sec[sector_col].isin(sector_map.keys())].copy()
    df_plot["sector"] = df_plot[sector_col].map(sector_map)
    df_plot = df_plot[[year_col, "sector", value_col]].dropna()

    if title is None:
        title = "Carbon price time series – world sectors"

    return _save_ts_figure_and_data(
        df_long=df_plot.rename(columns={"sector": sector_col}),
        group_col=sector_col,
        year_col=year_col,
        value_col=value_col,
        output_plot_path=output_plot_path,
        output_data_path=output_data_path,
        title=title,
    )
