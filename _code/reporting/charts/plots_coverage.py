import os

#------------------------------------ Bar chart: coverage ------------------------------------#
def coverage_plots(coverage, year):
    wldAvgCov = coverage.loc[(coverage.jurisdiction=="World") & (coverage.year==year)]["cov_all_CO2_jurCO2"].item()
    coverage_filtered = coverage.loc[coverage.jurisdiction.isin(countries_eur), :]

    # Sort for consistent y-axis order
    coverage_filtered = coverage_filtered.sort_values(by="jurisdiction")
    y_pos = np.arange(len(coverage_filtered.jurisdiction))
    labels = list(coverage_filtered.jurisdiction)

    # Plot
    plt.figure(figsize=(10, 16))
    ax1 = plt.barh(y_pos, coverage_filtered.cov_all_CO2_jurCO2 * 100, color=color_bars)
    ax2 = plt.axvline(x=wldAvgCov * 100, color="firebrick", linestyle='--', label="World average")

    plt.xticks(size=18, color="gray")
    plt.yticks(ticks=y_pos, labels=labels, size=18, color="gray")
    plt.xlabel("Percent of total CO$_2$ emissions", size=18, color="gray")
    plt.legend(loc="upper right", fontsize=16)
    plt.tight_layout()

    # Save figure
    plt.savefig(path_output + r"\coverage_" + year + ".png")
    plt.close()

    # Save plot data to CSV
    output_csv_path = f"/Users/gd/GitHub/ECP/_output/_figures/dataFig/coverage_{year}.csv"
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    
    coverage_csv = coverage_filtered[["jurisdiction", "cov_all_CO2_jurCO2"]].copy()
    coverage_csv["cov_all_CO2_jurCO2"] = coverage_csv["cov_all_CO2_jurCO2"] * 100  # convert to percent
    coverage_csv.rename(columns={"cov_all_CO2_jurCO2": "coverage_percent"}, inplace=True)
    coverage_csv.to_csv(output_csv_path, index=False)
