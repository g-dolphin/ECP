import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to create a filtered stacked bar chart
# Updated function using style context for local styling
def plot_filtered_stacked_bar(df_country, country_name):
    # Filter years
    df_country_filtered = df_country[(df_country['year'] >= 1990) & (df_country['year'] <= 2024)]

    # Keep only jurisdictions with any non-zero CO₂ price
    jurisdictions_to_keep = df_country_filtered.groupby('jurisdiction')['ecp_all_supraCO2_usd_k'].max()
    jurisdictions_to_keep = jurisdictions_to_keep[jurisdictions_to_keep > 0].index.tolist()
    df_country_filtered = df_country_filtered[df_country_filtered['jurisdiction'].isin(jurisdictions_to_keep)]

    # Pivot for plotting
    df_pivot = df_country_filtered.pivot_table(
        index='year',
        columns='jurisdiction',
        values='ecp_all_supraCO2_usd_k',
        aggfunc='sum',
        fill_value=0
    )

    # Custom local style
    custom_style = {
        'figure.figsize': (12, 6),
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'legend.loc': 'best',
        'axes.grid': True,
        'grid.alpha': 0.3,
        'grid.linestyle': '--',
        'lines.linewidth': 1,
        'patch.linewidth': 0.5,
        'savefig.dpi': 300,
        'figure.autolayout': True,
    }

    # Plot with local style context
    with plt.style.context(['seaborn-v0_8-muted', custom_style]):
        ax = df_pivot.plot(kind='bar', stacked=True)
        ax.set_title(f'{country_name} - Stacked CO₂ Price by Subnational Jurisdiction (1990–2024)')
        ax.set_ylabel('Average CO₂ Price (USD/tCO₂)')
        ax.set_xlabel('Year')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, axis='y')
        plt.tight_layout()

    plt.savefig("/Users/gd/GitHub/ECP/_output/_figures/plots/subnat_stacked_"+country_name+".png")

    plt.show()
