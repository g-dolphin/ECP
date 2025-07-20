import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
from matplotlib.cm import get_cmap
import matplotlib.image as mpimg
import os

def plot_stacked_national_bar(df_country):
    # Filter years
    df_country_filtered = df_country[(df_country['year'] >= 1990) & (df_country['year'] <= 2024)]

    # Keep only jurisdictions with any non-zero CO₂ price
    jurisdictions_to_keep = df_country_filtered.groupby('jurisdiction')['ecp_all_wldCO2_usd_k'].max()
    jurisdictions_to_keep = jurisdictions_to_keep[jurisdictions_to_keep > 0].index.tolist()
    df_country_filtered = df_country_filtered[df_country_filtered['jurisdiction'].isin(jurisdictions_to_keep)]

    # Pivot for plotting
    df_pivot = df_country_filtered.pivot_table(
        index='year',
        columns='jurisdiction',
        values='ecp_all_wldCO2_usd_k',
        aggfunc='sum',
        fill_value=0
    )

    # Sort columns by total contribution (descending)
    total_contributions = df_pivot.sum(axis=0)
    sorted_jurisdictions = total_contributions.sort_values(ascending=False).index
    df_pivot = df_pivot[sorted_jurisdictions]

    # Get distinct colors
    def get_distinct_colors(n):
        base_maps = ['tab20', 'tab20b', 'tab20c']
        colors = []
        for cmap_name in base_maps:
            cmap = get_cmap(cmap_name)
            colors.extend([to_hex(cmap(i)) for i in range(cmap.N)])
            if len(colors) >= n:
                break
        return colors[:n]

    jurisdictions = df_pivot.columns
    n_jurisdictions = len(jurisdictions)
    colors = get_distinct_colors(n_jurisdictions)

    # Custom local style
    custom_style = {
        'figure.figsize': (12, 6),
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 9,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linestyle': '--',
        'lines.linewidth': 1,
        'patch.linewidth': 0.5,
        'savefig.dpi': 300,
        'figure.autolayout': False
    }

    note_text = (
        "Note: This figure shows the contribution of each country to the global average price of CO₂. "
        "Countries' contribution relects all carbon pricing mechanisms in place, including subnational ones (except subnational mechanisms in Mexico and Japan). " 
        "Prices are expressed in 2021 USD. National prices are weighted by their share of global emissions. " 
        "Countries are ranked in ascending order, starting from the bottom."
    )
    footer_text = (
        "© Geoffroy Dolphin, 2025. All rights reserved. "
        "Data source: World Carbon Pricing Database. " #| Visualization by Geoffroy Dolphin. "
        "Licensed under CC BY-NC 4.0. Reuse permitted with attribution for non-commercial use."
    )

    with plt.style.context(['seaborn-v0_8-muted', custom_style]):
        fig, ax = plt.subplots()
        df_pivot.plot(kind='bar', stacked=True, ax=ax, color=colors)

        ax.set_title('Countries contributions to global CO₂ price (1990–2024)')
        ax.set_ylabel('Average CO₂ Price (USD/tCO₂)')
        ax.set_xlabel('')
        ax.grid(True, axis='y')

        # Legend placement (slightly higher to make space below)
        ax.legend(
            bbox_to_anchor=(0.5, -0.18),
            loc='upper center',
            ncol=6,
        )

        # Adjust layout to make space below the plot
        fig.subplots_adjust(bottom=0.38)

        # Add explanatory note and footer
        plt.figtext(0.5, 0.01, note_text, wrap=True, ha='center', fontsize=9)
        plt.figtext(0.5, -0.025, footer_text, wrap=True, ha='center', fontsize=8)

        plt.tight_layout(rect=[0, 0.06, 1, 1])  # Ensure plot area doesn't squeeze bottom text

        plt.savefig(
            "/Users/gd/GitHub/ECP/_output/_figures/plots/national_stacked_world.png",
            bbox_inches='tight'
        )
        plt.show()





