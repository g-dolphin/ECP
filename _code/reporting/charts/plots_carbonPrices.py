import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Union


PathLike = Union[str, Path]


def plot_minMax(prices_usd_max: pd.DataFrame, output_path: PathLike) -> None:
    """
    Plot min/max and average carbon prices by jurisdiction.

    Parameters
    ----------
    prices_usd_max : DataFrame
        Output of `prepare_carbon_price_data()[1]`, with columns including:
        jurisdiction, max_price, ecp_all_jurCO2_usd_k, etc.
    output_path : str or Path
        Where to save the PNG (full path).
    """
    data = (
        prices_usd_max
        .query("ecp_all_jurCO2_usd_k != 0 and jurisdiction != 'Malta'")
        .copy()
    )

    # Sort, compute y positions, labels, etc. (your existing code)
    data = data.sort_values("ecp_all_jurCO2_usd_k")
    labels = data["jurisdiction"].tolist()
    y_pos = np.arange(len(labels))
    max_prices = data["max_price"].to_numpy()
    avg_prices = data["ecp_all_jurCO2_usd_k"].to_numpy()
    wld_avg = data.loc[data["jurisdiction"] == "World", "ecp_all_jurCO2_usd_k"].iloc[0]

    fig, ax = plt.subplots(figsize=(10, 14))
    bar_color = "#1f77b4"
    edge_color = "#333333"

    ax.barh(y_pos, max_prices, height=0.6, facecolor="none",
            edgecolor=edge_color, linewidth=2.0, label="Maximum price")
    ax.barh(y_pos, avg_prices, height=0.4, color=bar_color,
            label="Average price (emissions-weighted)")

    ax.axvline(x=wld_avg, linestyle="--", color="black",
               linewidth=1.5, label="World average")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel("Carbon price (USD/tCO₂)", fontsize=12)
    ax.legend(loc="lower right", fontsize=9, frameon=False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=400, bbox_inches="tight")
    plt.close()
