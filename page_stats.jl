
Pkg.activate()

Pkg.add("UrlDownload")
Pkg.add("DataFrames")
Pkg.add("PyCall")

using DataFrames
using CSV
using PyPlot
using PyCall

#if you want to keep the Python True/False syntax
#const True = true
#const False = false

#raw_data = urldownload("https://raw.githubusercontent.com/gd1989/ECP/master/Total_economy/Coverage/Total_coverage.csv?token=AD3IRDAVNXIUQ6ER3UJU5WS7UQL5K")
path_of_cov = "/Users/GD/Documents/GitHub/ECP/Total_economy/Coverage/Total_coverage.csv"

coverage = CSV.read(path_of_cov, DataFrame)
select!(coverage, ["Jurisdiction", "Year", "cov_tax_ets_share_jurGHG"])

#mean coverage in every year
for yr in years:


#distribution of coverage in 2016

cov_2016 = coverage[coverage[:Year] .== 2016, :]
dropmissing!(cov_2016)


fig, (ax, ax2) = plt.subplots(2,1, sharex=true) # make the axes

ax.hist(cov_2016.cov_tax_ets_share_jurGHG, color="blue", edgecolor="white",
        bins=20,
        density=false, alpha=0.5)
ax2.hist(cov_2016.cov_tax_ets_share_jurGHG, color="blue", edgecolor="white",
         bins=20,
         density=false, alpha=0.5)

ax.set_ylim([150,170]) # numbers here are specific to this example
ax2.set_ylim([0,10]) # numbers here are specific to this example

ax.spines["bottom"].set_visible(false)
ax2.spines["top"].set_visible(false)

ax.xaxis.tick_bottom()
ax.tick_params(labeltop=false)
ax2.xaxis.tick_bottom()

#plt.axvline(mean_age, label = "Mean", color = "red")
#plt.axvline(median_age, label = "Median")

plt.legend()

plt.savefig("/Users/GD/Documents/GitHub/ECP/page/_assets/coverage_hist.png")
plt.close()
