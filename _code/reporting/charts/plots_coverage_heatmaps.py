import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import seaborn as sns

# Path to JSON config
json_path = os.path.join("/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/_dependencies/", "jurisdictions.json")

with open(json_path, 'r', encoding='utf-8') as f:
    jurisdictions = json.load(f)

canadian_provinces = jurisdictions["subnationals"]["Canada"]
us_states = jurisdictions["subnationals"]["United States"]
china_provinces = jurisdictions["subnationals"]["China"]

# Load data
df = pd.read_csv("/Users/gd/GitHub/ECP/_output/_dataset/coverage/tot_coverage_jurisdiction_CO2.csv")
df_world_sec = pd.read_csv("/Users/gd/GitHub/ECP/_output/_dataset/coverage/tot_coverage_world_sectors_CO2.csv")

# Keep only jurisdictions with any positive coverage
jurisdictions_positive_any = df[df["cov_all_CO2_jurCO2"] > 0]["jurisdiction"].unique()
df_any = df[df["jurisdiction"].isin(jurisdictions_positive_any)].copy()

# Groups
national_jurisdictions_any = [j for j in jurisdictions_positive_any
                              if j not in canadian_provinces + us_states + china_provinces]

# Plot function
def plot_heatmap(data, title, label):
    if data.empty:
        print(f"⚠️  No data for: {title}")
        return

    # Set output directory and base path
    out_dir = "/Users/gd/GitHub/ECP/_output/_figures"
    os.makedirs(out_dir, exist_ok=True)

    if label == "world_sec":
        pivot = data.pivot(index="ipcc_code", columns="year", values="cov_all_CO2_WldSectCO2")
        ylabel = "World sector"
    else:
        pivot = data.pivot(index="jurisdiction", columns="year", values="cov_all_CO2_jurCO2")
        ylabel = "Jurisdiction"

    # Save the pivot data as CSV
    csv_out_path = os.path.join(out_dir, f"/dataFig", f"coverage_hm_{label}.csv")
    pivot.to_csv(csv_out_path)
    print(f"📄 Saved data to: {csv_out_path}")

    # Plot path
    plot_out_path = os.path.join(out_dir, f"/plots", f"coverage_hm_{label}.png")

    # Create heatmap
    plt.figure(figsize=(12, max(5, len(pivot) * 0.4)))

    ax = sns.heatmap(
        pivot,
        cmap="Blues",
        linewidths=0.8,
        linecolor='white',
        cbar_kws={'label': 'Share of CO₂ emissions covered'},
        vmin=0, vmax=1
    )

    # Style
    ax.set_title(title, fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=9)

    plt.tight_layout()
    plt.savefig(plot_out_path, dpi=300)
    plt.show()

    print(f"✅ Saved plot to: {plot_out_path}")

# National
plot_heatmap(
    df_any[df_any["jurisdiction"].isin(national_jurisdictions_any)],
    "CO₂ Coverage: National Jurisdictions (1990–2024)",
    "national"
)

# Canada
plot_heatmap(
    df_any[df_any["jurisdiction"].isin(canadian_provinces)],
    "CO₂ Coverage: Canadian Provinces (1990–2024)",
    "canada"
)

# US
plot_heatmap(
    df_any[df_any["jurisdiction"].isin(us_states)],
    "CO₂ Coverage: US States (1990–2024)",
    "us"
)

# China
plot_heatmap(
    df_any[df_any["jurisdiction"].isin(china_provinces)],
    "CO₂ Coverage: China Provinces (1990–2024)",
    "china"
)

# World sectors
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


plot_heatmap(
    df_world_sec[df_world_sec.ipcc_code.isin(sector_map.keys())],
    "CO₂ Coverage: World sectors (1990–2024)",
    "world_sec"
)