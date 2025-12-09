from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PathLike = Union[str, Path]


def plot_ccost_gdp(
    df: pd.DataFrame,
    jurisdiction_col: str = "jurisdiction",
    ccost_col: str = "ccost_int",
    emissions_col: str = "co2_int",
    output_plot_path: Optional[PathLike] = None,
    output_data_path: Optional[PathLike] = None,
    title: str = "Carbon cost and CO₂ emissions per unit of GDP",
    x_label: str = "Carbon cost (% of GDP)",
) -> pd.DataFrame:
    """
    Plot a horizontal bar chart of carbon cost intensity vs CO₂ intensity of GDP.

    Parameters
    ----------
    df : DataFrame
        Input data, typically one year of carbonCostTot.
    jurisdiction_col : str
        Column with jurisdiction names.
    ccost_col : str
        Column with carbon cost intensity (share of GDP, 0–1).
    emissions_col : str
        Column with CO₂ emissions intensity (e.g. tCO₂ per USD).
    output_plot_path : str or Path, optional
        PNG/PDF path for the figure.
    output_data_path : str or Path, optional
        CSV path for underlying data.
    title : str
        Figure title.
    x_label : str
        X-axis label.

    Returns
    -------
    DataFrame
        Filtered and sorted DataFrame used in the plot.
    """
    df_plot = df[df[ccost_col] > 0].copy()
    df_plot[ccost_col] = df_plot[ccost_col] * 100.0  # convert to percent

    df_plot.sort_values(by=ccost_col, ascending=True, inplace=True)

    fig, ax = plt.subplots(figsize=(12, 10))

    y_pos = np.arange(len(df_plot))
    values = df_plot[ccost_col].to_numpy()
    labels = df_plot[jurisdiction_col].tolist()

    bar_color = "#1f77b4"
    ax.barh(y_pos, values, color=bar_color)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)

    ax.set_xlabel(x_label, fontsize=11)
    ax.set_title(title, fontsize=13, weight="bold")

    max_value = values.max() if len(values) else 0.0

    # Annotate bars with CO₂ intensity
    if emissions_col in df_plot.columns:
        for i, (value, co2_int) in enumerate(
            zip(values, df_plot[emissions_col].to_numpy())
        ):
            ax.text(
                value + max_value * 0.02,
                i,
                f"{co2_int:.2f} tCO₂ per unit GDP",
                va="center",
                ha="left",
                fontsize=8,
            )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.grid(True, linestyle=":", alpha=0.6)
    ax.set_axisbelow(True)

    fig.tight_layout()

    if output_plot_path is not None:
        output_plot_path = Path(output_plot_path)
        output_plot_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_plot_path, dpi=300, bbox_inches="tight")

    plt.close(fig)

    if output_data_path is not None:
        output_data_path = Path(output_data_path)
        output_data_path.parent.mkdir(parents=True, exist_ok=True)

        cols_to_save = [jurisdiction_col, ccost_col]
        if emissions_col in df_plot.columns:
            cols_to_save.append(emissions_col)
        df_plot[cols_to_save].to_csv(output_data_path, index=False)

    return df_plot
