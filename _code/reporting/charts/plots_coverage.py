
#------------------------------------ Bar chart: coverage ------------------------------------#
def coverage_plots(coverage, year):
    wldAvgCov = coverage.loc[(coverage.jurisdiction=="World") & (coverage.year==year)]["cov_all_CO2_jurCO2"].item()
    coverage = coverage.loc[coverage.jurisdiction.isin(countries_eur), :]

    y_pos = np.arange(len(coverage.jurisdiction.unique()))
    labels = list(coverage.jurisdiction.unique())

    plt.figure(figsize=(10, 16))

    ax1 = plt.barh(y_pos, coverage.cov_all_CO2_jurCO2*100,
                color=color_bars) #

    ax2 = plt.axvline(x=wldAvgCov*100, color="firebrick", linestyle='--', label="World average")

    #plt.title("CO$_2$ prices in Europe (2021)",
    #          size=22)
    plt.xticks(size=18, color="gray")
    plt.yticks(ticks=y_pos, labels=labels, size=18, color="gray") #na_jur

    plt.xlabel("Percent of total CO$_2$ emissions", size=18, color="gray")
    plt.legend(loc="upper right", fontsize=16)

    plt.tight_layout()

    plt.savefig(path_output+r"\coverage_"+year+".png")
    plt.close()
