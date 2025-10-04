import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("/Users/gd/GitHub/ECP/_output/_dataset/carbonCost/carbonCostTot.csv")

# Filter and sort
df_filtered = df[df["ccost_int"] > 0].copy()
df_filtered.sort_values(by="ccost_int", ascending=True, inplace=True)
df_filtered["ccost_int"] = df_filtered["ccost_int"]*100 # express in percent

# Setup figure
fig, ax = plt.subplots(figsize=(12, 10))
bar_color = "#1f77b4"

# Plot bars
bars = ax.barh(df_filtered["regionName"], df_filtered["ccost_int"], color=bar_color)

# Compute safe x-axis limit
max_value = df_filtered["ccost_int"].max()
ax.set_xlim(0, max_value * 1.25)

# Add text labels
for i, (value, label) in enumerate(zip(df_filtered["ccost_int"], df_filtered["co2_int"])):
    ax.text(value + max_value * 0.02, i, f"{label:.2f} tCO₂/USD", va='center', ha='left', fontsize=9)

# Labels and styling
ax.set_xlabel("USD per GDP", fontsize=12)
ax.set_title("Carbon Cost and CO₂ Emissions per Unit of GDP (2021)", fontsize=14, weight='bold')
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.xaxis.grid(True, linestyle=":", alpha=0.6)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("/Users/gd/GitHub/ECP/_output/_figures/plots/carbon_cost.png", dpi=300)
plt.show()
