import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
from matplotlib.cm import get_cmap
import matplotlib.image as mpimg
import os
import os

def plot_stacked_national_bar(df_country):
    # Filter years
    df_country_filtered = df_country[(df_country['year'] >= 1990) & (df_country['year'] <= 2024)]

    # Keep only jurisdictions with any non-zero CO₂ price
    jurisdictions_to_keep = df_country_filtered.groupby('jurisdiction')['ecp_all_wldCO2_usd_k'].max()
    jurisdictions_to_keep = jurisdictions_to_keep[jurisdictions_to_keep > 0].index.tolist()
    df_country_filtered = df_country_filtered[df_country_filtered['jurisdiction'].isin(jurisdictions_to_keep)]

    # Keep years > 2005
    df_country_filtered = df_country_filtered[df_country_filtered["year"] >= 2005]

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

    threshold = 0.1  # USD/tCO₂
    df_major = df_pivot.copy()

    # Identify minor values per year
    mask_minor = df_major < threshold

    # Compute "Other" series *before* modifying df_major
    other_series = df_major.where(mask_minor).sum(axis=1)

    # Set minor values to 0 so they don't plot twice
    df_major = df_major.mask(mask_minor, 0)

    # Add "Other" as a new column (after masking)
    df_major['Other'] = other_series

    # Drop all-zero columns (those that are only under threshold and not "Other")
    df_major = df_major.loc[:, (df_major != 0).any(axis=0)]

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

    jurisdictions = df_major.columns
    n_jurisdictions = len(jurisdictions)
    colors = get_distinct_colors(n_jurisdictions)

    if 'Other' in jurisdictions:
        other_index = jurisdictions.get_loc('Other')
        colors[other_index] = '#999999'

    custom_style = {
        'figure.figsize': (10, 8),
        'axes.titlesize': 16,
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
        "Note: This chart shows the contribution of each country to the global average price of CO$_2$ (stacked bottom to top by contribution). "
        "Values reflect national and subnational carbon pricing mechanisms, except subnational mechanisms in Mexico and Japan. "
        "Prices are expressed in 2021 USD. National prices are weighted by their share of global emissions. "
        "For readability, the category 'Other' collects countries that contributed < USD 0.1/tCO$_2$ to the global average in any year."
    )
    footer_text = (
        "© Geoffroy Dolphin, 2025. All rights reserved. "
        "Data source: World Carbon Pricing Database. "
        "Licensed under CC BY-NC 4.0. Reuse permitted with attribution for non-commercial use."
    )

    with plt.style.context(['seaborn-v0_8-muted', custom_style]):
        fig, ax = plt.subplots()
        df_major.plot(kind='bar', stacked=True, ax=ax, color=colors)

        ax.set_title("Country contributions to the global price of CO₂ emissions, 2005-2024")
        ax.set_ylabel('Average CO₂ Price (USD/tCO₂)')
        ax.set_xlabel('')
        ax.grid(True, axis='y')

        ax.legend(
            bbox_to_anchor=(0.5, -0.1),
            loc='upper center',
            ncol=6,
        )

        fig.subplots_adjust(bottom=0.38)
        plt.figtext(0.5, -0.03, note_text, wrap=True, ha='center', fontsize=9)
        plt.figtext(0.5, -0.07, footer_text, wrap=True, ha='center', fontsize=8)
        plt.tight_layout(rect=[0, 0.06, 1, 1])

        # Save figure
        fig_path = "/Users/gd/GitHub/ECP/_output/_figures/plots/national_stacked_world.png"
        plt.savefig(fig_path, bbox_inches='tight')
        plt.show()

    # Save data to CSV
    csv_path = "/Users/gd/GitHub/ECP/_output/_figures/dataFig/national_stacked_world.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df_major.to_csv(csv_path)






