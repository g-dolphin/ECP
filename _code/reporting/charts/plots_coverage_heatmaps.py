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

# Keep only jurisdictions with any positive coverage
jurisdictions_positive_any = df[df["cov_all_CO2_jurCO2"] > 0]["jurisdiction"].unique()
df_any = df[df["jurisdiction"].isin(jurisdictions_positive_any)].copy()

# Groups
national_jurisdictions_any = [j for j in jurisdictions_positive_any
                              if j not in canadian_provinces + us_states + china_provinces]

# Improved plot function
def plot_heatmap(data, title, label):
    if data.empty:
        print(f"⚠️  No data for: {title}")
        return
    
    pivot = data.pivot(index="jurisdiction", columns="year", values="cov_all_CO2_jurCO2")

    plt.figure(figsize=(12, max(5, len(pivot) * 0.4)))

    ax = sns.heatmap(
        pivot,
        cmap="Blues",
        linewidths=0.8,
        linecolor='white',
        cbar_kws={'label': 'Share of CO₂ emissions covered'},
        vmin=0, vmax=1
    )

    # Style: gridlines only white between cells
    ax.set_title(title, fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Jurisdiction", fontsize=12)
    
    # Rotate x-axis ticks
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=9)

    plt.tight_layout()

    out_path = f"/Users/gd/GitHub/ECP/_output/_figures/plots/coverage_hm_{label}.png"
    plt.savefig(out_path, dpi=300)
    plt.show()

    print(f"✅ Saved: {out_path}")

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
