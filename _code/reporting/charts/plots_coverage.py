from pathlib import Path
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


PathLike = Union[str, Path]

# define these at module level as before
countries_eur = [...]        # your existing list
color_bars = "#1f77b4"       # whatever you used


def coverage_plots(
    coverage: pd.DataFrame,
    year: int,
    output_plot_path: PathLike,
    output_data_path: PathLike,
) -> None:
    """
    Plot coverage (share of CO₂ emissions priced) for selected European countries
    vs the world average, and save both PNG + CSV.

    Parameters
    ----------
    coverage : DataFrame
        Coverage dataset with columns ['jurisdiction', 'year', 'cov_all_CO2_jurCO2', ...]
    year : int
        Year to filter.
    output_plot_path : str or Path
        Path for the PNG output.
    output_data_path : str or Path
        Path for the CSV with the underlying plotted data.
    """
    wldAvgCov = coverage.loc[
        (coverage["jurisdiction"] == "World") & (coverage["year"] == year),
        "cov_all_CO2_jurCO2",
    ].item()

    coverage_filtered = coverage[
        (coverage["year"] == year) & (coverage["jurisdiction"].isin(countries_eur))
    ].copy()

    coverage_filtered = coverage_filtered.sort_values(by="jurisdiction")
    y_pos = np.arange(len(coverage_filtered["jurisdiction"]))
    labels = coverage_filtered["jurisdiction"].tolist()

    plt.figure(figsize=(10, 16))
    ax1 = plt.barh(
        y_pos,
        coverage_filtered["cov_all_CO2_jurCO2"] * 100,
        color=color_bars,
    )
    plt.axvline(
        x=wldAvgCov * 100,
        color="firebrick",
        linestyle="--",
        label="World average",
    )

    plt.yticks(y_pos, labels, fontsize=12)
    plt.xlabel("Percent of total CO₂ emissions", size=18, color="gray")
    plt.legend(loc="upper right", fontsize=16)
    plt.tight_layout()

    output_plot_path = Path(output_plot_path)
    output_plot_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_plot_path, dpi=300, bbox_inches="tight")
    plt.close()

    # Underlying data
    output_data_path = Path(output_data_path)
    output_data_path.parent.mkdir(parents=True, exist_ok=True)

    coverage_csv = coverage_filtered[["jurisdiction", "cov_all_CO2_jurCO2"]].copy()
    coverage_csv["coverage_percent"] = coverage_csv["cov_all_CO2_jurCO2"] * 100
    coverage_csv.drop(columns=["cov_all_CO2_jurCO2"], inplace=True)
    coverage_csv.to_csv(output_data_path, index=False)
