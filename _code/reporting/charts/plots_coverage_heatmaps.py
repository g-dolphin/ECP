from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PathLike = Union[str, Path]


def plot_coverage_heatmap(
    df: pd.DataFrame,
    index_col: str,
    column_col: str,
    value_col: str,
    title: str,
    output_plot_path: PathLike,
    output_data_path: PathLike,
    cmap: str = "Blues",
    sort_index: bool = True,
    sort_columns: bool = True,
) -> pd.DataFrame:
    """
    Plot a coverage heatmap and save both the figure and the pivoted data.

    Parameters
    ----------
    df : DataFrame
        Long-format coverage data.
    index_col : str
        Column to use as rows (e.g. jurisdiction or sector).
    column_col : str
        Column to use as columns (typically year).
    value_col : str
        Column with coverage values (0–1 or 0–100).
    title : str
        Title for the heatmap.
    output_plot_path : str or Path
        Path for the saved heatmap image.
    output_data_path : str or Path
        Path for the saved pivoted data CSV.
    cmap : str
        Matplotlib/seaborn colormap name.
    sort_index : bool
        If True, sort index (rows) alphabetically.
    sort_columns : bool
        If True, sort columns (e.g. years) ascending.

    Returns
    -------
    DataFrame
        Pivoted table used in the heatmap.
    """
    pivot = df.pivot(index=index_col, columns=column_col, values=value_col)

    if sort_index:
        pivot = pivot.sort_index()
    if sort_columns:
        pivot = pivot.reindex(sorted(pivot.columns), axis=1)

    # If values are in 0–1, convert to % just for display
    if pivot.max().max() <= 1.0:
        pivot_display = pivot * 100.0
        value_label = "Coverage (%)"
    else:
        pivot_display = pivot
        value_label = "Coverage"

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(
        pivot_display,
        cmap=cmap,
        linewidths=0.3,
        linecolor="white",
        cbar_kws={"label": value_label},
        ax=ax,
    )
    ax.set_title(title, fontsize=13, weight="bold")
    ax.set_xlabel(column_col.capitalize())
    ax.set_ylabel(index_col.capitalize())

    fig.tight_layout()

    output_plot_path = Path(output_plot_path)
    output_plot_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_plot_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    output_data_path = Path(output_data_path)
    output_data_path.parent.mkdir(parents=True, exist_ok=True)
    pivot.to_csv(output_data_path)

    return pivot


def prepare_subnational_subset(
    df: pd.DataFrame,
    jurisdictions: Iterable[str],
    jurisdiction_col: str = "jurisdiction",
) -> pd.DataFrame:
    """
    Helper to subset an ECP coverage dataset to a given list of subnational jurisdictions.

    Parameters
    ----------
    df : DataFrame
        Input data.
    jurisdictions : iterable of str
        Jurisdiction names to keep.
    jurisdiction_col : str
        Column name for jurisdiction identifier.

    Returns
    -------
    DataFrame
        Subset of df containing only the requested jurisdictions.
    """
    return df[df[jurisdiction_col].isin(jurisdictions)].copy()
