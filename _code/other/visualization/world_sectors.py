import pandas as pd
import matplotlib.pyplot as plt

# Load data
coverage_df = pd.read_csv("/Users/gd/GitHub/ECP/_dataset/coverage/tot_coverage_world_sectors_CO2.csv")
price_df = pd.read_csv("/Users/gd/GitHub/ECP/_dataset/ecp/ipcc/ecp_world_sectors/world_sectoral_ecp_CO2.csv")

# Define sector mapping
sector_map = {
    "1A1A1": "Electricity Generation",
    "1A1C": "Other Energy Industries",
    "1A2A": "Iron and Steel",
    "1A2B": "Non-Ferrous Metals",
    "1A2C": "Chemicals",
    "1A2D": "Pulp, Paper, Print",
    "1A2E": "Food Processing",
    "1A2F": "Non-Metallic Minerals",
    "1A2G": "Transport Equipment",
    "1A2H": "Machinery",
    "1A2I": "Mining and Quarrying",
    "1A2J": "Wood and Wood Products",
    "1A2L": "Textile and Leather",
    "1A3A1": "International Aviation",
    "1A3B": "Road Transport",
    "1A4A": "Buildings - Commercial and Institutional",
    "1A4B": "Buildings - Residential",
    "1A4C": "Agriculture, Forestry, Fishing"
}

# Prepare 2024 data
coverage_df_2024 = coverage_df[coverage_df["year"] == 2024].copy()
price_df_2024 = price_df[price_df["year"] == 2024].copy()

# Map sector names
coverage_df_2024["sector_name"] = coverage_df_2024["ipcc_code"].map(sector_map)
price_df_2024["sector_name"] = price_df_2024["ipcc_code"].map(sector_map)

# Select and rename columns
coverage_df_2024 = coverage_df_2024[["sector_name", "cov_ets_CO2_WldSectCO2", "cov_tax_CO2_WldSectCO2"]]
coverage_df_2024.rename(columns={
    "cov_ets_CO2_WldSectCO2": "ETS",
    "cov_tax_CO2_WldSectCO2": "Carbon tax"
}, inplace=True)

price_df_2024["Average CO₂ price (USD/t)"] = price_df_2024["ecp_all_sectCO2_usd_k"]
price_df_2024 = price_df_2024[["sector_name", "Average CO₂ price (USD/t)"]]

# Merge and sort
combined_df = coverage_df_2024.merge(price_df_2024, on="sector_name", how="outer").dropna()
combined_df.set_index("sector_name", inplace=True)
combined_df = combined_df.sort_values(by=["ETS", "Carbon tax"], ascending=False)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

# Stacked bars
bars_ets = ax.barh(combined_df.index, combined_df["ETS"], color="navy", label="ETS")
bars_tax = ax.barh(combined_df.index, combined_df["Carbon tax"], left=combined_df["ETS"], color="red", label="Carbon tax")

# Bar labels
for bar in bars_ets:
    width = bar.get_width()
    if width > 0.03:
        ax.text(width / 2, bar.get_y() + bar.get_height() / 2,
                f"{width:.0%}", ha="center", va="center", color="white", fontsize=8)

for bar in bars_tax:
    width = bar.get_width()
    if width > 0.03:
        ax.text(bar.get_x() + width / 2, bar.get_y() + bar.get_height() / 2,
                f"{width:.0%}", ha="center", va="center", color="white", fontsize=8)

# CO₂ price dots
ax.scatter([1.05] * len(combined_df), combined_df.index, s=100, c="black", zorder=5, marker='o', label="Average price")

# CO₂ price labels
for i, (index, row) in enumerate(combined_df.iterrows()):
    price = row["Average CO₂ price (USD/t)"]
    label = "<1 USD/tCO$_2$" if price < 1 else f"{price:.0f} USD/tCO$_2$"
    ax.text(1.08, i, label,
            va='center', ha='left', fontsize=10, fontweight='bold', color="black")

# Axes style
ax.set_xlim(0, 1.25)
ax.set_xlabel("Share of sector GHG emissions covered")
ax.set_title("Share of sectors' global GHG emissions covered by an ETS or Carbon Tax (2024)")
ax.invert_yaxis()

# Dotted grid
ax.xaxis.grid(True, linestyle=":", color="gray", alpha=0.6)
ax.set_axisbelow(True)

# Remove top and right spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Legend inside figure, bottom left corner (avoids overlap)
ax.legend(loc="lower left", bbox_to_anchor=(0.08, 0.02), frameon=False)

plt.tight_layout()
plt.savefig(r"/Users/gd/GitHub/ECP/_figures/plots/world_sectors_ecp.svg")
plt.savefig(r"/Users/gd/GitHub/ECP/_figures/plots/world_sectors_ecp.png")
plt.show()
