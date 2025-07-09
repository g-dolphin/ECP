# ✅ Update: keep jurisdictions with strictly positive coverage at ANY point between 1990–2024
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import seaborn as sns

# Define path to the JSON file
#json_path = os.path.join(os.path.dirname(__file__), "jurisdictions.json")
json_path = os.path.join("/Users/gd/GitHub/WorldCarbonPricingDatabase/_code/_compilation/_dependencies/", "jurisdictions.json")

# Load jurisdictions dictionary from file
with open(json_path, 'r', encoding='utf-8') as f:
    jurisdictions = json.load(f)

canadian_provinces = jurisdictions["subnationals"]["Canada"]
us_states = jurisdictions["subnationals"]["United States"]
china_provinces = jurisdictions["subnationals"]["China"]

df = pd.read_csv("/Users/gd/GitHub/ECP/_output/_dataset/coverage/tot_coverage_jurisdiction_CO2.csv")

# Get jurisdictions with strictly positive coverage any time in 1990–2024
jurisdictions_positive_any = df[df["cov_all_CO2_jurCO2"] > 0]["jurisdiction"].unique()

# Keep only those jurisdictions
df_any = df[df["jurisdiction"].isin(jurisdictions_positive_any)].copy()

# Re-define groups
national_jurisdictions_any = [j for j in jurisdictions_positive_any
                              if j not in canadian_provinces + us_states + china_provinces]

# Use the safer plot function
def plot_heatmap(data, title, label):
    if data.empty:
        print(f"⚠️  No data for: {title}")
        return
    pivot = data.pivot(index="jurisdiction", columns="year", values="cov_all_CO2_jurCO2")
    plt.figure(figsize=(12, max(6, len(pivot) * 0.4)))
    sns.heatmap(pivot, cmap="YlOrRd", linewidths=0.5, linecolor='gray', cbar_kws={'label': 'Coverage'})
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Jurisdiction")
    plt.tight_layout()
    plt.savefig("/Users/gd/GitHub/ECP/_output/_figures/plots/coverage_hm_"+label+".png")
    plt.show()

# Plot updated heatmaps
plot_heatmap(df_any[df_any["jurisdiction"].isin(national_jurisdictions_any)],
             "CO₂ Coverage: National Jurisdictions (1990–2024)", "national")

plot_heatmap(df_any[df_any["jurisdiction"].isin(canadian_provinces)],
             "CO₂ Coverage: Canadian Provinces (1990–2024)", "canada")

plot_heatmap(df_any[df_any["jurisdiction"].isin(us_states)],
             "CO₂ Coverage: US States (1990–2024)", "us")

plot_heatmap(df_any[df_any["jurisdiction"].isin(china_provinces)],
             "CO₂ Coverage: China Provinces (1990–2024)", "china")
