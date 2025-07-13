import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import pandas as pd

df = pd.read_csv("/Users/gd/GitHub/ECP/_output/_dataset/ecp/ipcc/ecp_economy/ecp_CO2.csv")
df_world_sec = pd.read_csv("/Users/gd/GitHub/ECP/_output/_dataset/ecp/ipcc/ecp_world_sectors/world_sectoral_ecp_CO2.csv")

# Define sector mapping
sector_map = {
    "1A1A1": "Electricity Generation",
    "1A1C": "Other Energy Industries",
    "1A2A": "Iron and Steel",
    "1A2B": "Non-Ferrous Metals",
    "1A2C": "Chemicals",
    "1A2D": "Pulp, Paper, Print",
#    "1A2E": "Food Processing",
    "1A2F": "Non-Metallic Minerals",
#    "1A2G": "Transport Equipment",
#    "1A2H": "Machinery",
    "1A2I": "Mining and Quarrying",
    "1A2J": "Wood and Wood Products",
    "1A2L": "Textile and Leather",
    "1A3A1": "International Aviation",
    "1A3B": "Road Transport",
    "1A4A": "Buildings - Commercial and Institutional",
    "1A4B": "Buildings - Residential",
    "1A4C": "Agriculture, Forestry, Fishing"
}

jurisdictions = ["Canada", "China", "France", "Germany", "Italy", "United Kingdom", "United States", "World"]

def plot_cp_time_series(df, selec_list, label):
    # Apply a clean, publication-ready style
    plt.style.use('seaborn-whitegrid')

    # Set up figure
    fig, ax = plt.subplots(figsize=(12, 6))

    # Define a consistent color cycle
    colors = plt.get_cmap("tab10")

    if label == "jurisdictions":
        field = "jurisdiction"
        variable = 'ecp_all_jurCO2_usd_k'
        legend_title = "Jurisdiction"
        chart_title = "Emissions-weighted CO$_2$ Price, by jurisdiction"
    else:
        field = "ipcc_code"
        variable = "ecp_all_sectCO2_usd_k"
        legend_title = "Sector"
        chart_title = "Emissions-weighted CO$_2$ Price, by world sector"

    for i, value in enumerate(selec_list):
        df_selec = df[df[field] == value].sort_values("year")
        x = df_selec['year']
        y = df_selec[variable]

        if len(x) > 3:
            x_new = np.linspace(x.min(), x.max(), 300)
            spline = make_interp_spline(x, y, k=3)
            y_smooth = spline(x_new)
            if label == "jurisdictions":
                ax.plot(x_new, y_smooth, label=value, linewidth=2.2, color=colors(i))
            else:
                ax.plot(x_new, y_smooth, label=sector_map[value], linewidth=2.2, color=colors(i))
        else:
            if label == "jurisdictions":
                ax.plot(x, y, label=value, linewidth=2.2, color=colors(i))
            else:
                ax.plot(x, y, label=sector_map[value], linewidth=2.2, color=colors(i))

    # Labels and title
    ax.set_title(chart_title, fontsize=18, weight='bold')
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("CO$_2$ Price (USD/tCO$_2$)", fontsize=14)

    # Ticks
    ax.tick_params(axis='both', which='major', labelsize=12)

    # Legend
    ax.legend(title=legend_title, fontsize=12, title_fontsize=13)

    # Grid styling
    ax.grid(True, which='both', linestyle='--', linewidth=0.6, alpha=0.8)

    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Tight layout for print
    fig.tight_layout()

    # Save as high-resolution PNG and PDF
    png_output = "/Users/gd/GitHub/ECP/_output/_figures/plots/ecp_co2_ts_"+label+".png"
    pdf_output = "/Users/gd/GitHub/ECP/_output/_figures/plots/ecp_co2_ts_"+label+".pdf"

    fig.savefig(png_output, dpi=600, bbox_inches='tight')
    fig.savefig(pdf_output, bbox_inches='tight')

    plt.show()


plot_cp_time_series(df, jurisdictions, "jurisdictions")
plot_cp_time_series(df_world_sec, sector_map.keys(), "world_sec")