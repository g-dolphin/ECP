import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import pandas as pd

df = pd.read_csv("/Users/gd/GitHub/ECP/_output/_dataset/ecp/ipcc/ecp_economy/ecp_CO2.csv")

# Apply a clean, publication-ready style
plt.style.use('seaborn-whitegrid')

jurisdictions = ["China", "France", "Germany", "Italy", "United Kingdom", "United States", "World"]

# Set up figure
fig, ax = plt.subplots(figsize=(12, 6))

# Define a consistent color cycle
colors = plt.get_cmap("tab10")

for i, jurisdiction in enumerate(jurisdictions):
    df_jurisdiction = df[df['jurisdiction'] == jurisdiction].sort_values("year")
    x = df_jurisdiction['year']
    y = df_jurisdiction['ecp_all_jurCO2_usd_k']

    if len(x) > 3:
        x_new = np.linspace(x.min(), x.max(), 300)
        spline = make_interp_spline(x, y, k=3)
        y_smooth = spline(x_new)
        ax.plot(x_new, y_smooth, label=jurisdiction, linewidth=2.2, color=colors(i))
    else:
        ax.plot(x, y, label=jurisdiction, linewidth=2.2, color=colors(i))

# Labels and title
ax.set_title("Emissions-weighted CO$_2$ Price, by jurisdiction", fontsize=18, weight='bold')
ax.set_xlabel("Year", fontsize=14)
ax.set_ylabel("CO$_2$ Price (USD/tCO$_2$)", fontsize=14)

# Ticks
ax.tick_params(axis='both', which='major', labelsize=12)

# Legend
ax.legend(title="Region", fontsize=12, title_fontsize=13)

# Grid styling
ax.grid(True, which='both', linestyle='--', linewidth=0.6, alpha=0.8)

# Remove top and right spines for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Tight layout for print
fig.tight_layout()

# Save as high-resolution PNG and PDF
png_output = "/Users/gd/GitHub/ECP/_output/_figures/plots/ecp_co2_ts.png"
pdf_output = "/Users/gd/GitHub/ECP/_output/_figures/plots/ecp_co2_ts.pdf"

fig.savefig(png_output, dpi=600, bbox_inches='tight')
fig.savefig(pdf_output, bbox_inches='tight')

plt.show()

