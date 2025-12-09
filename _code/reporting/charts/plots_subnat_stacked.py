from __future__ import annotations

from pathlib import Path
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PathLike = Union[str, Path]


def plot_filtered_stacked_bar(
    df_country: pd.DataFrame,
    country_name: str,
    output_plot_path: PathLike,
    output_data_path: PathLike,
) -> pd.DataFrame:
    """
    Create a stacked bar chart of CO₂ prices by subnational jurisdiction
    for a given country, and save both the figure and the underlying data.

    Parameters
    ----------
    df_country : DataFrame
        ECP data for the country, with columns including:
        - 'year'
        - 'jurisdiction'
        - 'ecp_all_supraCO2_usd_k' (average CO₂ price, USD/tCO₂)
    country_name : str
        Name to use in the plot title ("United States", "Canada", "China", ...).
    output_plot_path : str or Path
        Path to save the figure (PNG, PDF, etc.).
    output_data_path : str or Path
        Path to save the underlying pivot data (CSV).

    Returns
    -------
    DataFrame
        Pivot table used for plotting (rows = year, columns = jurisdiction).
    """
    # ------------------------------------------------------------------
    # Filter years
    # ------------------------------------------------------------------
    df_country_filtered = df_country[
        (df_country["year"] >= 1990) & (df_country["year"] <= 2024)
    ].copy()

    # Ensure the price column is numeric
    df_country_filtered["ecp_all_supraCO2_usd_k"] = pd.to_numeric(
        df_country_filtered.get("ecp_all_supraCO2_usd_k"), errors="coerce"
    )

    # Keep only jurisdictions with any non-zero CO₂ price
    jurisdictions_to_keep = (
        df_country_filtered.groupby("jurisdiction")["ecp_all_supraCO2_usd_k"]
        .max()
        .fillna(0.0)
    )
    jurisdictions_to_keep = jurisdictions_to_keep[jurisdictions_to_keep > 0].index.tolist()

    df_country_filtered = df_country_filtered[
        df_country_filtered["jurisdiction"].isin(jurisdictions_to_keep)
    ].copy()

    # ------------------------------------------------------------------
    # Pivot for plotting: rows = year, columns = jurisdiction
    # ------------------------------------------------------------------
    df_pivot = df_country_filtered.pivot_table(
        index="year",
        columns="jurisdiction",
        values="ecp_all_supraCO2_usd_k",
        aggfunc="sum",
        fill_value=0.0,
    )

    # If nothing left after filtering, just save empty CSV and skip plotting
    output_data_path = Path(output_data_path)
    output_data_path.parent.mkdir(parents=True, exist_ok=True)
    df_pivot.to_csv(output_data_path)

    if df_pivot.empty:
        # nothing to plot, but don't crash the batch
        return df_pivot

    # ------------------------------------------------------------------
    # Local plotting style
    # ------------------------------------------------------------------
    custom_style = {
        "figure.figsize": (12, 6),
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "legend.loc": "best",
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": "--",
        "lines.linewidth": 1,
        "patch.linewidth": 0.5,
        "savefig.dpi": 300,
        "figure.autolayout": True,
    }

    output_plot_path = Path(output_plot_path)
    output_plot_path.parent.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Plot with local style context
    # ------------------------------------------------------------------
    with plt.style.context(["seaborn-v0_8-muted", custom_style]):
        ax = df_pivot.plot(kind="bar", stacked=True)

        ax.set_title(
            f"{country_name} - Stacked CO₂ Price by Subnational Jurisdiction (1990–2024)"
        )
        ax.set_ylabel("Average CO₂ Price (USD/tCO₂)")
        ax.set_xlabel("Year")

        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True, axis="y")
        plt.tight_layout()

        # Save figure
        plt.savefig(output_plot_path)

    # Do NOT plt.show() in batch generation
    plt.close("all")

    return df_pivot
