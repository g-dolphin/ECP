from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PathLike = Union[str, Path]


def get_selected_jurisdictions(
    data_dir: PathLike,
    jurisdictions: Sequence[str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load coverage and price data for a set of jurisdictions.

    Parameters
    ----------
    data_dir : str or Path
        Root directory of the ECP _output/_dataset (i.e. contains
        "coverage/tot_coverage_jurisdiction_CO2.csv" and
        "ecp/ipcc/ecp_economy/ecp_CO2.csv").
    jurisdictions : sequence of str
        Jurisdictions to retain.

    Returns
    -------
    (coverage_df, price_df, price_covered_df) : tuple of DataFrames
    """
    data_dir = Path(data_dir)

    coverage_df = pd.read_csv(
        data_dir / "coverage" / "tot_coverage_jurisdiction_CO2.csv"
    )
    price_df = pd.read_csv(
        data_dir / "ecp" / "ipcc" / "ecp_economy" / "ecp_CO2.csv"
    )
    price_covered_df = pd.read_csv(
        data_dir / "ecp" / "ipcc" / "ecp_economy" / "ecp_CO2.csv"
    )

    coverage_df = coverage_df[coverage_df["jurisdiction"].isin(jurisdictions)].copy()
    price_df = price_df[price_df["jurisdiction"].isin(jurisdictions)].copy()
    price_covered_df = price_covered_df[
        price_covered_df["jurisdiction"].isin(jurisdictions)
    ].copy()

    return coverage_df, price_df, price_covered_df


def plot_selected_jurisdictions(
    data_dir: PathLike,
    jurisdictions: Sequence[str],
    year: int = 2024,
    output_plot_path: Optional[PathLike] = None,
    output_data_path: Optional[PathLike] = None,
) -> pd.DataFrame:
    """
    Plot ETS + carbon tax coverage for selected jurisdictions (stacked bar),
    and annotate with average CO₂ prices.

    Parameters
    ----------
    data_dir : str or Path
        Root directory of the ECP _output/_dataset.
    jurisdictions : sequence of str
        Jurisdictions to include.
    year : int, default 2024
        Year to display.
    output_plot_path : str or Path, optional
        PNG/SVG path for figure. If None, figure is not written.
    output_data_path : str or Path, optional
        CSV path for underlying combined data. If None, CSV is not written.

    Returns
    -------
    DataFrame
        Combined dataset used for plotting, indexed by jurisdiction name.
    """
    coverage_df, price_df, price_covered_df = get_selected_jurisdictions(
        data_dir=data_dir,
        jurisdictions=jurisdictions,
    )

    # Kept from original script (in case you were deflating prices elsewhere)
    gdp_def = 124.16 / 107.59  # noqa: F841  # currently not used

    jurisdiction_map = {
        "USA": "United States",
        "CAN": "Canada",
        "GBR": "United Kingdom",
        "DEU": "Germany",
        "FRA": "France",
    }

    # Filter to selected year
    coverage_df_y = coverage_df[coverage_df["year"] == year].copy()
    price_df_y = price_df[price_df["year"] == year].copy()
    price_covered_df_y = price_covered_df[price_covered_df["year"] == year].copy()

    # Human-readable names
    for df in (coverage_df_y, price_df_y, price_covered_df_y):
        df["jurisdiction_name"] = df["jurisdiction"].map(jurisdiction_map).fillna(
            df["jurisdiction"]
        )

    # Coverage shares
    coverage_df_y = coverage_df_y[
        ["jurisdiction_name", "cov_ets_CO2_jurCO2", "cov_tax_CO2_jurCO2"]
    ].copy()
    coverage_df_y.rename(
        columns={
            "cov_ets_CO2_jurCO2": "ETS",
            "cov_tax_CO2_jurCO2": "Carbon tax",
        },
        inplace=True,
    )

    # Average prices (all emissions)
    price_df_y["Average CO₂ price (USD/t)"] = price_df_y["ecp_all_jurCO2_usd_k"]
    price_df_y = price_df_y[["jurisdiction_name", "Average CO₂ price (USD/t)"]].copy()

    # Average prices (covered emissions)
    price_covered_df_y[
        "Average CO₂ price (USD/t) - covered emissions"
    ] = price_covered_df_y["ecp_all_jurCO2_usd_k"]
    price_covered_df_y = price_covered_df_y[
        ["jurisdiction_name", "Average CO₂ price (USD/t) - covered emissions"]
    ].copy()

    # Combine
    combined_df = coverage_df_y.merge(
        price_df_y,
        on="jurisdiction_name",
        how="left",
    ).merge(
        price_covered_df_y,
        on="jurisdiction_name",
        how="left",
    )

    # Sort by ETS then Carbon tax share (descending)
    combined_df = combined_df.set_index("jurisdiction_name")
    combined_df = combined_df.sort_values(by=["ETS", "Carbon tax"], ascending=False)

    # Convert coverage shares to percent for plotting
    combined_df["ETS_pct"] = combined_df["ETS"] * 100
    combined_df["Carbon_tax_pct"] = combined_df["Carbon tax"] * 100

    # ------------------------------------------------------------------
    # Plot
    # ------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6))

    y_pos = np.arange(len(combined_df))

    bars_ets = ax.barh(
        y_pos,
        combined_df["ETS_pct"],
        color="navy",
        label="ETS",
    )
    bars_tax = ax.barh(
        y_pos,
        combined_df["Carbon_tax_pct"],
        left=combined_df["ETS_pct"],
        color="red",
        label="Carbon tax",
    )

    # Label inside bars (if big enough)
    for bar in bars_ets:
        width = bar.get_width()
        if width > 3:  # > 3 percentage points
            ax.text(
                width / 2,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.0f}%",
                ha="center",
                va="center",
                color="white",
                fontsize=8,
            )

    for bar in bars_tax:
        width = bar.get_width()
        if width > 3:
            ax.text(
                bar.get_x() + width / 2,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.0f}%",
                ha="center",
                va="center",
                color="white",
                fontsize=8,
            )

    # Annotate prices on the right-hand side
    xmax = (combined_df["ETS_pct"] + combined_df["Carbon_tax_pct"]).max()
    x_text = xmax * 1.05

    for i, (idx, row) in enumerate(combined_df.iterrows()):
        # All emissions price
        if not pd.isna(row["Average CO₂ price (USD/t)"]):
            ax.text(
                x_text,
                i,
                f"{row['Average CO₂ price (USD/t)']:.0f} USD/t",
                va="center",
                ha="left",
                fontsize=8,
            )

        # Covered emissions price (if available)
        if not pd.isna(row["Average CO₂ price (USD/t) - covered emissions"]):
            ax.text(
                x_text,
                i - 0.25,
                f"({row['Average CO₂ price (USD/t) - covered emissions']:.0f} on covered)",
                va="center",
                ha="left",
                fontsize=7,
                color="dimgray",
            )

    ax.set_yticks(y_pos)
    ax.set_yticklabels(combined_df.index, fontsize=10)
    ax.set_xlabel("Share of CO₂ emissions covered by pricing (%)", fontsize=11)

    title = f"ETS and carbon tax coverage and prices – {year}"
    ax.set_title(title, fontsize=13, fontweight="bold")

    ax.set_xlim(0, x_text * 1.25)

    ax.xaxis.grid(True, linestyle=":", color="gray", alpha=0.6)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(loc="upper left", frameon=False)

    fig.tight_layout()

    # Save figure
    if output_plot_path is not None:
        output_plot_path = Path(output_plot_path)
        output_plot_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_plot_path, dpi=300, bbox_inches="tight")

    plt.close(fig)

    # Save data
    if output_data_path is not None:
        output_data_path = Path(output_data_path)
        output_data_path.parent.mkdir(parents=True, exist_ok=True)
        combined_df.to_csv(output_data_path, index=True)

    return combined_df
