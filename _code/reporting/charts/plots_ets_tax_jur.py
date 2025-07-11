import pandas as pd
import matplotlib.pyplot as plt

def get_selected_jurisdictions(data_dir, jurisdictions):
    coverage_df = pd.read_csv(f"{data_dir}/coverage/tot_coverage_jurisdiction_CO2.csv")
    price_df = pd.read_csv(f"{data_dir}/ecp/ipcc/ecp_economy/ecp_CO2.csv")
    price_covered_df = pd.read_csv(f"{data_dir}/ecp/ipcc/ecp_economy/ecp_CO2.csv")

    # Filter each one directly
    coverage_df = coverage_df[coverage_df.jurisdiction.isin(jurisdictions)].copy()
    price_df = price_df[price_df.jurisdiction.isin(jurisdictions)].copy()
    price_covered_df = price_covered_df[price_covered_df.jurisdiction.isin(jurisdictions)].copy()

    return coverage_df, price_df, price_covered_df


def plot_selected_jurisdictions(data_dir, jurisdictions):
    coverage_df, price_df, price_covered_df = get_selected_jurisdictions(data_dir, jurisdictions)

    gdp_def = 124.16 / 107.59

    jurisdiction_map = {
        "USA": "United States",
        "CAN": "Canada",
        "GBR": "United Kingdom",
        "DEU": "Germany",
        "FRA": "France",
        # Add more if needed
    }

    coverage_df_2024 = coverage_df[coverage_df["year"] == 2024].copy()
    price_df_2024 = price_df[price_df["year"] == 2024].copy()
    price_covered_df_2024 = price_covered_df[price_covered_df["year"] == 2024].copy()

    coverage_df_2024["jurisdiction_name"] = coverage_df_2024["jurisdiction"].map(jurisdiction_map).fillna(coverage_df_2024["jurisdiction"])
    price_df_2024["jurisdiction_name"] = price_df_2024["jurisdiction"].map(jurisdiction_map).fillna(price_df_2024["jurisdiction"])
    price_covered_df_2024["jurisdiction_name"] = price_covered_df_2024["jurisdiction"].map(jurisdiction_map).fillna(price_covered_df_2024["jurisdiction"])

    coverage_df_2024 = coverage_df_2024[["jurisdiction_name", "cov_ets_CO2_jurCO2", "cov_tax_CO2_jurCO2"]]
    coverage_df_2024.rename(columns={
        "cov_ets_CO2_jurCO2": "ETS",
        "cov_tax_CO2_jurCO2": "Carbon tax"
    }, inplace=True)

    price_df_2024["Average CO₂ price (USD/t)"] = price_df_2024["ecp_all_jurCO2_usd_k"]
    price_df_2024 = price_df_2024[["jurisdiction_name", "Average CO₂ price (USD/t)"]]

    price_covered_df_2024["Average CO₂ price (USD/t) - covered emissions"] = price_covered_df_2024["ecp_all_jurCO2_usd_k"]
    price_covered_df_2024 = price_covered_df_2024[["jurisdiction_name", "Average CO₂ price (USD/t) - covered emissions"]]

    combined_df = coverage_df_2024.merge(price_df_2024, on="jurisdiction_name", how="outer").dropna()
    combined_df = combined_df.merge(price_covered_df_2024, on="jurisdiction_name", how="outer").dropna()
    combined_df.set_index("jurisdiction_name", inplace=True)
    combined_df = combined_df.sort_values(by=["ETS", "Carbon tax"], ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))

    bars_ets = ax.barh(combined_df.index, combined_df["ETS"], color="navy", label="ETS")
    bars_tax = ax.barh(combined_df.index, combined_df["Carbon tax"], left=combined_df["ETS"], color="red", label="Carbon tax")

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

    # USD/tCO2 unit label above price dots
    ax.text(1, -0.75, "USD/tCO$_2$", va='center', ha='left',
            fontsize=10, fontweight='bold', color="black", clip_on=False)

    # === NEW: average price dots & shifted labels beyond axis, not clipped ===

    # All emissions dot at x=1, not clipped
    ax.scatter(
        [1] * len(combined_df), combined_df.index,
        s=80, c="black", zorder=5, marker='o',
        label="Average price (all emissions)",
        clip_on=False
    )

    for i, (index, row) in enumerate(combined_df.iterrows()):
        price = row["Average CO₂ price (USD/t)"] * gdp_def
        label = "<1 USD/tCO$_2$" if price < 1 else f"{price:.0f}"
        ax.text(
            1.02, i, label,
            va='center', ha='left',
            fontsize=9, fontweight='bold', color="black",
            clip_on=False
        )

    # Covered emissions dot at x=1.08, not clipped
    ax.scatter(
        [1.08] * len(combined_df), combined_df.index,
        s=80, c="black", zorder=5, marker='d',
        label="Average price (covered emissions)",
        clip_on=False
    )

    for i, (index, row) in enumerate(combined_df.iterrows()):
        price = row["Average CO₂ price (USD/t) - covered emissions"] * gdp_def
        label = "<1 USD/tCO$_2$" if price < 1 else f"{price:.0f}"
        ax.text(
            1.1, i, label,
            va='center', ha='left',
            fontsize=9, fontweight='bold', color="black",
            clip_on=False
        )

    # Keep axis limit at exactly 1
    ax.set_xlim(0, 1)
    ax.set_xlabel("Share of jurisdiction CO$_2$ emissions covered")
    ax.set_title("Selected jurisdictions: carbon pricing coverage and prices (2024)")
    ax.invert_yaxis()

    ax.xaxis.grid(True, linestyle=":", color="gray", alpha=0.6)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend(loc="lower left", bbox_to_anchor=(0.27, -0.3),
              frameon=False, ncol=2)

    # Add right margin so dots/labels aren't clipped by figure border
    plt.subplots_adjust(right=0.85)

    plt.tight_layout()
    plt.savefig(r"/Users/gd/GitHub/ECP/_output/_figures/plots/selected_jurisdictions_ecp.svg")
    plt.savefig(r"/Users/gd/GitHub/ECP/_output/_figures/plots/selected_jurisdictions_ecp.png")
    plt.show()
