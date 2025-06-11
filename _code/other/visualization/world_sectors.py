import pandas as pd
import matplotlib.pyplot as plt

# Load uploaded data
coverage_df = pd.read_csv("/mnt/data/tot_coverage_world_sectors_CO2.csv")
price_df = pd.read_csv("/mnt/data/world_sectoral_ecp_CO2.csv")

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
    "1A4A": "Commercial and Institutional",
    "1A4B": "Residential",
    "1A4C": "Agriculture, Forestry, Fishing"
}

# Filter data for 2024 and map sectors
coverage_df_2024 = coverage_df[coverage_df["year"] == 2024].copy()
price_df_2024 = price_df[price_df["year"] == 2024].copy()

coverage_df_2024["sector_name"] = coverage_df_2024["ipcc_code"].map(sector_map)
price_df_2024["sector_name"] = price_df_2024["ipcc_code"].map(sector_map)

# Aggregate by sector
coverage_sector = (
    coverage_df_2024.groupby(["sector_name", "instrument"])
    .agg({"coverage_share": "sum"})
    .unstack(fill_value=0)
)

price_sector = (
    price_df_2024.groupby("sector_name")
    .agg({"ecp_usd_tCO2": "mean"})
)

# Merge coverage and price data
combined_df = coverage_sector.join(price_sector, how="outer").fillna(0)
combined_df.columns = ["Carbon tax", "ETS", "Average CO₂ price (USD/t)"]
combined_df = combined_df[["ETS", "Carbon tax", "Average CO₂ price (USD/t)"]]
combined_df = combined_df.sort_values(by=["ETS", "Carbon tax"], ascending=False)


# Re-plot with the legend correctly positioned just above the x-axis (below title, above x-label)
fig, ax = plt.subplots(figsize=(10, 6))

# Bar segments
bars_ets = ax.barh(refined_df.index, refined_df["ETS"], color="navy", label="ETS")
bars_tax = ax.barh(refined_df.index, refined_df["Carbon tax"], left=refined_df["ETS"], color="red", label="Carbon tax")

# Add percentage labels inside bars
for bar in bars_ets:
    width = bar.get_width()
    if width > 0.03:
        ax.text(width / 2, bar.get_y() + bar.get_height() / 2, f"{width:.0%}", ha="center", va="center", color="white", fontsize=8)

for bar in bars_tax:
    width = bar.get_width()
    if width > 0.03:
        ax.text(bar.get_x() + width / 2, bar.get_y() + bar.get_height() / 2, f"{width:.0%}", ha="center", va="center", color="white", fontsize=8)

# Add dots for average CO2 prices
ax.scatter([1.05] * len(refined_df), refined_df.index, 
           s=100, c="black", zorder=5, marker='o', label="Average price")

# Annotate prices with larger, bold font
for i, (index, row) in enumerate(refined_df.iterrows()):
    ax.text(1.08, i, f'{row["Average CO₂ price (USD/t)"]:.0f} USD/tCO$_2$', 
            va='center', ha='left', fontsize=10, fontweight='bold', color="black")

# Style
ax.set_xlabel("Share of sector GHG emissions covered")
ax.set_title("Share of sectors' global GHG emissions covered by an ETS or Carbon Tax (2024)")
ax.set_xlim(0, 1.25)
ax.invert_yaxis()

# Legend correctly placed above x-axis (below title, above x-label)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=False)

plt.tight_layout()
plt.show()
