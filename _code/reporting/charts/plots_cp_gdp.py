from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import matplotlib.pyplot as plt
import pandas as pd

PathLike = Union[str, Path]


def plot_cp_gdp(
    df: pd.DataFrame,
    year: Optional[int] = None,
    coverage_col: str = "cpCoverage",
    jurisdiction_col: str = "jurisdiction",
    year_col: str = "year",
    output_plot_path: Optional[PathLike] = None,
    output_data_path: Optional[PathLike] = None,
    title: Optional[str] = None,
) -> pd.DataFrame:
    """
    Plot a horizontal bar chart of GDP coverage by carbon pricing for a given year.

    Parameters
    ----------
    df : DataFrame
        Input data with at least [jurisdiction_col, year_col, coverage_col].
        coverage_col is expected to be a share in [0, 1] (will be converted to %).
    year : int, optional
        Year to filter to. If None, use the max value of df[year_col].
    coverage_col : str
        Column name for GDP coverage share (0–1).
    jurisdiction_col : str
        Column name for jurisdiction names.
    year_col : str
        Column name for year.
    output_plot_path : str or Path, optional
        Where to save the figure (PNG/PDF, etc.). If None, the figure is not saved.
    output_data_path : str or Path, optional
        Where to save the underlying plotted data CSV. If None, no CSV is saved.
    title : str, optional
        Figure title; if None, a default is constructed.

    Returns
    -------
    DataFrame
        The filtered and sorted DataFrame actually plotted (with added column
        `coverage_percent`).
    """
    if year is None:
        if year_col not in df.columns:
            raise ValueError(
                "year is None and year_col not in df; either pass a year "
                "explicitly or ensure the DataFrame has a year column."
            )
        year = int(df[year_col].max())

    if year_col in df.columns:
        df_plot = df[df[year_col] == year].copy()
    else:
        df_plot = df.copy()

    # Keep non-missing coverage
    df_plot = df_plot.dropna(subset=[coverage_col]).copy()

    # Convert to percentage
    df_plot["coverage_percent"] = df_plot[coverage_col] * 100

    # Sort by coverage
    df_plot.sort_values("coverage_percent", ascending=True, inplace=True)

    # Figure
    fig, ax = plt.subplots(figsize=(10, 12))

    y_pos = range(len(df_plot))
    labels = df_plot[jurisdiction_col].tolist()
    values = df_plot["coverage_percent"].to_numpy()

    ax.barh(y_pos, values, color="#1f77b4")

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Share of GDP covered by carbon pricing (%)", fontsize=11)

    if title is None:
        title = f"GDP coverage by carbon pricing – {year}"
    ax.set_title(title, fontsize=13, weight="bold")

    # Grid and spines
    ax.xaxis.grid(True, linestyle=":", color="gray", alpha=0.5)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    # Save figure
    if output_plot_path is not None:
        output_plot_path = Path(output_plot_path)
        output_plot_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_plot_path, dpi=300, bbox_inches="tight")

    plt.close(fig)

    # Save underlying data
    if output_data_path is not None:
        output_data_path = Path(output_data_path)
        output_data_path.parent.mkdir(parents=True, exist_ok=True)
        cols_to_save = [jurisdiction_col, coverage_col, "coverage_percent"]
        cols_to_save = [c for c in cols_to_save if c in df_plot.columns]
        df_plot[cols_to_save].to_csv(output_data_path, index=False)

    return df_plot
