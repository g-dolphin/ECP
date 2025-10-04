## PATHS

# CHART-SPECIFIC PLOT FEATURES

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def plot_minMax(prices_usd_max_path, output_path):
    # Load data
    prices_usd_max = pd.read_csv(prices_usd_max_path)

    # Filter data
    data = (
        prices_usd_max
        .query("ecp_all_jurCO2_usd_k != 0 and jurisdiction != 'Malta'")
        .copy()
    )

    # Sort by average price (to match bar heights)
    data = data.sort_values(by="ecp_all_jurCO2_usd_k", ascending=True)

    # Extract values
    labels = data['jurisdiction']
    avg_prices = data['ecp_all_jurCO2_usd_k']
    max_prices = data['max_price']
    y_pos = np.arange(len(labels))

    # World average price
    wld_avg = prices_usd_max.query("jurisdiction == 'World' and year == 2024")["ecp_all_jurCO2_usd_k"].item()

    # === Plot ===
    plt.style.use("seaborn-v0_8-white")
    fig, ax = plt.subplots(figsize=(10, len(labels) * 0.45))

    # Colors and styling
    bar_color = "#003f5c"     # dark blue
    edge_color = "#ffa600"    # warm orange outline

    # Plot maximum prices (outline bars)
    ax.barh(y_pos, max_prices, height=0.6, facecolor='none',
            edgecolor=edge_color, linewidth=2.0, label="Maximum price")

    # Plot average prices (filled bars)
    ax.barh(y_pos, avg_prices, height=0.4, color=bar_color, label="Average price (emissions-weighted)")

    # Add world average line
    ax.axvline(x=wld_avg, linestyle="--", color="black", linewidth=1.5, label="World average")

    # Format axes
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel("2021 USD/tCO$_2$", fontsize=12)
    ax.set_title("Average and Maximum CO₂ Prices by Jurisdiction (2024)",
                 fontsize=14, fontweight='bold', pad=15)

    ax.tick_params(axis='x', labelsize=10)
    ax.xaxis.grid(True, linestyle=":", alpha=0.6)
    ax.yaxis.grid(False)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Legend
    ax.legend(loc="lower right", fontsize=9, frameon=False)

    plt.tight_layout()

    output_path = "/Users/gd/GitHub/ECP/_output/_figures/plots/max_price_ecp_2024.png"
    fig.savefig(output_path, dpi=400, bbox_inches="tight")
    plt.close()

    print(f"Chart saved to: {output_path}")
