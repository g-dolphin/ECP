import pandas as pd
import matplotlib.pyplot as plt

# Load data again for safety
df_gdp = pd.read_csv("/Users/gd/GitHub/ECP/_output/_dataset/coverage/cpriceCoverageGDP.csv")

# Filter for latest year
latest_year = df_gdp["year"].max()
df_latest = df_gdp[df_gdp["year"] == latest_year].copy()

# Sort by coverage
df_latest = df_latest.sort_values("cpCoverage", ascending=True)

# Plot: consistent style
plt.style.use("default")  # Or 'seaborn-v0_8-whitegrid' for subtle grid

fig, ax = plt.subplots(figsize=(10, max(5, len(df_latest) * 0.3)))

bars = ax.barh(
    df_latest["regionName"],
    df_latest["cpCoverage"],
    color="navy"
)

# Add % labels
for bar in bars:
    width = bar.get_width()
    ax.text(
        width + 0.01,  # adjust offset
        bar.get_y() + bar.get_height() / 2,
        f"{width:.0%}",
        va="center",
        ha="left",
        fontsize=8,
        color="black"
    )

# Title and labels
ax.set_title(f"Share of GDP covered by carbon pricing ({latest_year})",
             fontsize=14, weight="bold", pad=10)
ax.set_xlabel("Share of GDP", fontsize=12)
ax.set_xlim(0, 1)

# Ticks
ax.tick_params(axis="y", labelsize=9)
ax.tick_params(axis="x", labelsize=9)

# Add subtle vertical grid
ax.xaxis.grid(True, linestyle=":", color="gray", alpha=0.5)
ax.set_axisbelow(True)

# Remove spines for clean look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

# Save if needed
plt.savefig("/Users/gd/GitHub/ECP/_output/_figures/plots/gdp_coverage_bar.png", dpi=300)

plt.show()
