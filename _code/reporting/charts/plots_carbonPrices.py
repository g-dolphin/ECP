## PATHS

# CHART-SPECIFIC PLOT FEATURES

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

def plot_minMax(prices_usd_max, path):
    prices_usd_max = pd.read_csv(path+r"/carbonPrices_usd_max_2024.csv")

    # Get the world average
    wld_avg = prices_usd_max.loc[
        (prices_usd_max.jurisdiction == "World") & (prices_usd_max.year == 2024),
        "ecp_all_jurCO2_usd_k"
    ].item()

    # Sort by max_price instead for consistent outlines
    sorted_data = (
        prices_usd_max
        .query("ecp_all_jurCO2_usd_k != 0 and jurisdiction != 'Malta'")
        .sort_values(by="max_price", ascending=True)
    )

    labels = sorted_data['jurisdiction']
    y_pos = np.arange(len(labels))
    prices = sorted_data['ecp_all_jurCO2_usd_k']
    max_prices = sorted_data['max_price']

    # Optional: detect if any average > max
    if any(prices > max_prices):
        print("⚠️ Warning: Some average prices exceed the maximum price!")

    # Style
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 16))

    bar_color = "#4682B4"
    edge_color = "#333333"

    # Plot max outline bars FIRST
    ax.barh(y_pos, max_prices, height=0.6, facecolor='none',
            edgecolor=edge_color, linewidth=1.8, label="Maximum price")

    # Plot average bars ON TOP
    ax.barh(y_pos, prices, color=bar_color, height=0.4,
            label="Average (emissions-weighted)")

    # World average line
    ax.axvline(x=wld_avg, color="firebrick", linestyle="--", linewidth=2, label="World average")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=12)
    ax.set_xlabel("2021 USD/tCO$_2$", fontsize=14)
    ax.set_title("Emissions-weighted Average and Maximum CO₂ Prices by Jurisdiction (2024)",
                 fontsize=18, weight='bold', pad=20)

    ax.tick_params(axis='x', labelsize=12)
    ax.legend(loc="lower right", fontsize=12, title_fontsize=13, frameon=False)

    ax.xaxis.grid(True, linestyle='--', alpha=0.6)
    ax.yaxis.grid(False)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    fig.tight_layout()

    output_path = "/Users/gd/GitHub/ECP/_output/_figures/plots/max_price_ecp_2024.png"
    fig.savefig(output_path, dpi=400, bbox_inches="tight")
    plt.close()

    print(f"Chart saved to: {output_path}")

    return
