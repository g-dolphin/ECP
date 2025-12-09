from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence, Union

import matplotlib.pyplot as plt
import pandas as pd

PathLike = Union[str, Path]


def plot_cp_regional(
    df: pd.DataFrame,
    region_col: str = "region",
    year_col: str = "year",
    value_col: str = "ecp_regional_CO2_usd_k",
    regions: Optional[Sequence[str]] = None,
    output_plot_path: Optional[PathLike] = None,
    output_data_path: Optional[PathLike] = None,
    title: Optional[str] = None,
) -> pd.DataFrame:
    """
    Plot time series of regional average carbon prices.

    Parameters
    ----------
    df : DataFrame
        Regional ECP dataset with columns [region_col, year_col, value_col].
    region_col : str
        Column for region names.
    year_col : str
        Column for year.
    value_col : str
        Column for price (USD/tCO₂).
    regions : sequence of str, optional
        Regions to include. If None, all unique regions in df are used.
    output_plot_path : str or Path, optional
        PNG/PDF path for figure.
    output_data_path : str or Path, optional
        CSV path for underlying data.
    title : str, optional
        Figure title; if None, a default is constructed.

    Returns
    -------
    DataFrame
        Long-format data actually plotted.
    """
    if regions is not None:
        df_plot = df[df[region_col].isin(regions)].copy()
    else:
        df_plot = df.copy()

    df_plot = df_plot[[year_col, region_col, value_col]].dropna()

    fig, ax = plt.subplots(figsize=(11, 6))

    for region, sub in df_plot.groupby(region_col):
        sub = sub.sort_values(year_col)
        ax.plot(
            sub[year_col],
            sub[value_col],
            label=str(region),
            linewidth=2,
        )

    ax.set_xlabel("Year", fontsize=11)
    ax.set_ylabel("Carbon price (USD/tCO₂)", fontsize=11)

    if title is None:
        title = "Regional average carbon prices over time"
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
        df_plot.to_csv(output_data_path, index=False)

    return df_plot
